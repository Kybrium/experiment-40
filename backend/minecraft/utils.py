import requests
from django.utils.text import slugify
from .models import MinecraftAccount

def generate_unique_nickname(max_attempts: int, gender: str | None, nationality: str | None) -> str:
    """
    Ask randomuser.me for candidate names and return the first nickname that
    doesn't already exist in MinecraftAccount.nickname.

    Will try up to `max_attempts` unique names total.
    After that, returns None to signal "just suffix it yourself".
    """

    attempts_left = max_attempts

    # We'll pull in small batches so we don't spam the API.
    # randomuser.me supports ?results=#
    while attempts_left > 0:
        batch_size = min(5, attempts_left)

        params = {"results": batch_size}
        if gender:
            params["gender"] = gender
        if nationality:
            params["nat"] = nationality

        try:
            ru_resp = requests.get("https://randomuser.me/api/", params=params, timeout=5)
        except requests.RequestException:
            raise

        if ru_resp.status_code != 200:
            raise RuntimeError("identity_provider_error")

        payload = ru_resp.json()
        people = payload.get("results", []) or []

        for p in people:
            first_name = p.get("name", {}).get("first") or ""
            last_name = p.get("name", {}).get("last") or ""

            # fallback if API gave us weird blanks
            if not first_name and not last_name:
                continue

            base = f"{first_name}_{last_name}".strip()

            # normalize:
            # - lower
            # - replace spaces with _
            # - keep only safe chars via slugify + tweak
            #   slugify("Ålex Stone") -> "alex-stone"
            #   then replace "-" with "_"
            normalized = slugify(base).replace("-", "_")

            if not normalized:
                continue

            if not MinecraftAccount.objects.filter(nickname=normalized).exists():
                return normalized

        attempts_left -= batch_size

    # no unique candidate found within cap
    return None