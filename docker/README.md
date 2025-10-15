# Docker Quick Docs

Welcome to the Docker docs for **Experiment 40**.

This folder contains:

- **[dev/](./dev/)** — containers & Compose for local development
- **[prod/](./prod/)** — (placeholder) production/deployment configs
- **.gitignore**
- **README.md** — you’re here

---

## Quick Navigation

- 🚀 **Dev setup & commands:** [dev/README.md](./dev/README.md)
- 🚢 **Prod notes (coming soon):** [prod/](./prod/)

---

## Notes

- MySQL is internal to the Docker network (no host port published).
- phpMyAdmin is available locally at `http://127.0.0.1:8080` (see dev docs).
- Environment variables are managed via `.env` files in each subfolder.
