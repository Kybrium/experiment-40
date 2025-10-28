import sys
import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run makemessages but skip everything except selected folders (default: accounts, core, minecraft)."

    def add_arguments(self, parser):
        parser.add_argument("-l", "--locale", default="uk", help="Language code (default: uk)")
        parser.add_argument("--folders", nargs="+", default=["accounts", "core", "minecraft"], help="List of folders to include in extraction")

    def handle(self, *args, **options):
        lang = options["locale"]
        include_folders = options["folders"]

        from pathlib import Path
        base = Path.cwd()
        top_dirs = [p.name for p in base.iterdir() if p.is_dir()]

        ignore_patterns = [
            f"{d}/*" for d in top_dirs if d not in include_folders and d != "locale"
        ]

        self.stdout.write(self.style.NOTICE(f"Extracting translations for '{lang}' from: {', '.join(include_folders)}"))

        cmd = [sys.executable, "manage.py", "makemessages", "-l", lang]

        for pattern in ignore_patterns:
            cmd += ["--ignore", pattern]

        subprocess.run(cmd, check=True)

        self.stdout.write(self.style.SUCCESS("[INFO] makemessages completed successfully"))