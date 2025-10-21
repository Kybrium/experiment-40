# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### 🧭 How to update this file

- Add new entries under **[Unreleased]** when you make a PR or commit that changes behavior.
- Group entries under one of these headers:
  - `### Added` – new features, endpoints, or tools.
  - `### Changed` – updated or refactored behavior/configuration.
  - `### Fixed` – bug fixes or stability improvements.
  - `### Removed` – deprecated or deleted functionality.
- When you deploy or tag a version, move the content from `[Unreleased]` into a new dated or numbered section like:
  ```markdown
  ## [v1.0.0] – Initial Release
  ```

---

## [DEVELOPMENT] Merge No.11 - 21.10.2025
- Added registration endpoint on backend
- Added factory_boy
- Adjusted all tests for factory_boy and Faker
- Added tests for registration endpoint and serializer
- Updated docs

---

## [DEVELOPMENT] Merge No.10 - 17.10.2025
- Configured jest plugin for testings on frontend

---

## [DEVELOPMENT] Merge No.9 - 17.10.2025
- Added basic styling configurations for tailwind
- Updated documentation for frontend

---

## [DEVELOPMENT] Merge No.8 - 17.10.2025
- Added admin panel with 2FA on backend

---

## [DEVELOPMENT] Merge No.7 - 17.10.2025
- Configured Django Logger

---

## [DEVELOPMENT] Merge No.6 - 16.10.2025
- Implemented `MaintenanceModeMiddleware` (returns 503 when `MAINTENANCE_MODE=True`)
- Added `/ping/` healthcheck endpoint (JSON `{"status":"ok"}`)
- Wired routes in `core/urls.py` (includes `/ping/` and `/api/accounts/`)
- Added tests for maintenance middleware using `/ping/`
- Created `backend/core/README.md` documenting middleware, settings, and healthcheck


---

## [DEVELOPMENT] Merge No.5 - 16.10.2025
- Initialized User model
- Added `MeSerializer` for read-only user data representation  
- Implemented `/api/accounts/me/` endpoint for authenticated user info  
- Added unit tests for `User` model, `MeSerializer`, and `UserView`  
- Added integration tests for JWT authentication flow  
- Created documentation for backend and `accounts` app

---

## [DEVELOPMENT] Merge No.4 - 16.10.2025

- Fixed entrypoint.sh so venv sees it
- Fixed Dockerfile for backend to init venv correctly
- Removed from volume venv to not duplicate it
- In Makefile and dev.ps1 added commands to access shells of backend/frontend
- Updated README.md for dev docker

---

## [DEVELOPMENT] Merge No.3 - 15.10.2025

- Initialized the structure of docs in the repo

---

## [DEVELOPMENT] Merge No.2 - 15.10.2025

- Added phpMyAdmin browser interface on localhost:8080

---

## [DEVELOPMENT] Merge No.1 - 15.10.2025

- Added team-rosters.yml to rotate members of specific teams on tasks.
- Added CODEOWNERS file for automatic PRs assignment
- Added task.yaml for tasks assignment.
- Added issue-triage-by-team.yml and pr-team-mentions.yml for automatic assigning of issues and mentioning teams.
- Removed defaults in .github/ISSUE_TEMPLATE/config.yml since it is not supported anymore by GitHub.
- Updated Docker Compose configuration: removed host port mapping (`3306:3306`) for the database container to avoid port conflicts.
- The backend now connects to the database over the internal Docker network (`db:3306`), and the database is no longer exposed to the host system.

---
