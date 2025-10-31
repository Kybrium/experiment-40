from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management.commands.compilemessages import Command as CompileMessagesCommand


class Command(BaseCommand):
    help = "Compile translations only for selected folders (default: accounts, minecraft)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--folders",
            nargs="+",
            default=["accounts", "minecraft"],
            help="List of app folders to compile translations for",
        )

    def handle(self, *args, **options):
        base = Path.cwd()
        folders = options["folders"]

        self.stdout.write(self.style.NOTICE(
            f"Compiling translations for folders: {', '.join(folders)}"
        ))

        compiled = 0
        compile_cmd = CompileMessagesCommand()

        for folder in folders:
            app_path = base / folder
            locale_dir = app_path / "locale"

            if not locale_dir.exists():
                self.stdout.write(self.style.WARNING(f"[skip] no locale/ in {folder}/"))
                continue

            self.stdout.write(self.style.NOTICE(f"[run] compiling {folder}/locale"))

            compile_cmd.handle(
                locale=None,
                exclude=[],
                ignore_patterns=[],
                verbosity=1,
                settings=None,
                pythonpath=None,
                traceback=False,
                no_color=False,
                force_color=False,
                locale_paths=[str(locale_dir)],
                fuzzy=False,
            )

            compiled += 1

        if compiled == 0:
            self.stdout.write(self.style.WARNING("No locales compiled."))
        else:
            self.stdout.write(self.style.SUCCESS(f"[INFO] compiled {compiled} folder(s) successfully"))