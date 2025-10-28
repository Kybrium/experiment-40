# 🧩 Infrastructure App Overview

The **Infrastructure** app provides internal developer tools and maintenance utilities for the backend.

---

## 🚀 Available Commands

| Command                                   | Description                                                                                                                              |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `python manage.py makemessages_custom`    | Extracts translation strings **only** from selected folders (e.g. `accounts`, `core`) for i18n updates while skipping unnecessary files. |
| `python manage.py compilemessages_custom` | Compiles `.po` translation files in the specified folders into `.mo` files used by Django at runtime.                                    |

---

## 🧭 Usage

### 📝 Extract new or updated translatable strings

Run the following to update translation catalogs for Ukrainian (`uk`):

```bash
python manage.py makemessages_custom -l uk
```

To extract English (or any other language):

```bash
python manage.py makemessages_custom -l en
```

This command:

* Scans only the specified folders (`accounts`, `core` by default)
* Skips irrelevant directories like `venv/`, `frontend/`, etc.
* Creates or updates `.po` files inside each app’s `locale/<lang>/LC_MESSAGES/`

---

### ⚙️ Compile translations for runtime use

After editing `.po` files, compile them into `.mo` files so Django can load them:

```bash
python manage.py compilemessages_custom
```

Optional: target specific apps

```bash
python manage.py compilemessages_custom --folders accounts core
```

This will process only the translation catalogs found under each app’s `locale/` directory.

---

### ✅ Typical i18n workflow

```bash
# 1. Extract new strings
python manage.py makemessages_custom -l uk

# 2. Translate in:
#    accounts/locale/uk/LC_MESSAGES/django.po
#    core/locale/uk/LC_MESSAGES/django.po

# 3. Compile translations
python manage.py compilemessages_custom
```