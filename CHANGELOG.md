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

## [DEVELOPMET] Merge No.3 - 15.09.2025

- Initialized the structure of docs in the repo

---

## [DEVELOPMENT] Merge No.2 - 15.09.2025

- Added phpMyAdmin browser interface on localhost:8080

---

## [DEVELOPMENT] Merge No.1 - 15.09.2025

- Added team-rosters.yml to rotate members of specific teams on tasks.
- Added CODEOWNERS file for automatic PRs assignment
- Added task.yaml for tasks assignment.
- Added issue-triage-by-team.yml and pr-team-mentions.yml for automatic assigning of issues and mentioning teams.
- Removed defaults in .github/ISSUE_TEMPLATE/config.yml since it is not supported anymore by GitHub.
- Updated Docker Compose configuration: removed host port mapping (`3306:3306`) for the database container to avoid port conflicts.
- The backend now connects to the database over the internal Docker network (`db:3306`), and the database is no longer exposed to the host system.

---
