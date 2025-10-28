import sys
import subprocess
from pathlib import Path
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run compilemessages only for selected folders (default: accounts, core, minecraft)."

    def add_arguments(self, parser):
        parser.add_argument("--folders", nargs="+", default=["accounts", "core", "minecraft"], help="List of folders to compile translations for")

    def handle(self, *args, **options):
        folders = options["folders"]
        base = Path.cwd()

        self.stdout.write(self.style.NOTICE(f"Compiling translations for folders: {', '.join(folders)}"))

        for folder in folders:
            app_path = base / folder
            if not app_path.exists():
                self.stdout.write(self.style.WARNING(f"[skip] {folder} not found"))
                continue

            locale_dir = app_path / "locale"
            if not locale_dir.exists():
                self.stdout.write(self.style.WARNING(f"[skip] no locale/ in {folder}/"))
                continue

            self.stdout.write(self.style.NOTICE(f"[run] compilemessages in {folder}/locale"))

            cmd = [
                sys.executable,
                str(base / "manage.py"),
                "compilemessages",
            ]

            subprocess.run(cmd, check=True, cwd=locale_dir)

        self.stdout.write(self.style.SUCCESS("[INFO] compilemessages completed successfully"))