# Changelog

## [0.1.4] - 2026-03-23

### Added

- **Microservices Architecture**:
    - Containerized all application modules using **Docker** and **Docker Compose**.
    - Introduced **PostgreSQL 15** as the primary database for structured data storage.
    - Added a **Flask-based Web Dashboard** for real-time results and visualization access.
- **Docker Orchestration**:
    - Implemented `compose.yaml` to manage service dependencies, health checks, and networks.
    - Added **Docker Volumes** (`reports_data`, `plots_data`) for persistent data exchange between containers.
- **Advanced Docker CI Pipeline**:
    - Implemented dynamic container ID detection for robust artifact extraction in GitHub Actions.
    - Added automated `.env` generation for secure and isolated testing environments.

### Changed

- **Database Migration**: Successfully migrated the data layer from local SQLite to a production-ready **PostgreSQL** container.
- **Artifact Management**: Switched from direct path uploads to a "Container-to-Host" extraction strategy using `docker cp`.
- **Project Structure**: Reorganized the codebase into a `src/` modular directory layout for better container context.

### Fixed

- **Container Path Mismatch**: Resolved "File not found" errors by aligning host data mounting with internal container paths.
- **Service Race Conditions**: Implemented `depends_on` with `service_healthy` conditions to ensure DB readiness before data loading.
- **Data Ingestion**: Fixed raw data path resolution in the CI environment using automated file relocation scripts.

### Changed

- **Database Migration**: Successfully migrated the data layer from local SQLite to a production-ready **PostgreSQL** container.
- **Artifact Management**: Switched from direct path uploads to a "Container-to-Host" extraction strategy using `docker cp`.
- **Project Structure**: Reorganized the codebase into a `src/` modular directory layout for better container context.

### Fixed

- **Container Path Mismatch**: Resolved "File not found" errors by aligning host data mounting with internal container paths.
- **Service Race Conditions**: Implemented `depends\_

## [0.1.3] - 2026-03-01

### Added

- **Hybrid CI/CD Infrastructure**:
    - Added support for **Self-hosted Windows Runners** to leverage local hardware power.
    - Implemented **Matrix Strategy** with `max-parallel: 1` to ensure sequential execution on local machines.
- **Environment Stability**:
    - Added `PYTHONIOENCODING="utf-8"` to handle Unicode/Emoji logging in Windows terminals.
    - Switched to a robust local Git-fetch method to bypass `actions/checkout` EBUSY locks.

### Fixed

- **EBUSY Resource Lock**: Resolved "File busy" errors on Windows by disabling aggressive workspace cleaning.
- **UnicodeEncodeError**: Fixed pipeline crashes caused by emoji logging in non-UTF-8 environments.
- **Artifact Path Mismatch**: Aligned Python save paths with GitHub Action upload paths.

## [0.1.2] - 2026-02-23

### Added

- Comprehensive data quality audit script (nulls, duplicates, and uniqueness checks).
- Hypothesis-driven EDA:
    - Age vs. Wear percentage correlation.
    - Asset structure analysis by service subgroups.
    - Top manufacturers inventory distribution.
- Predictive modeling: Random Forest Regressor for estimating asset book value.
- Automated data cleaning pipeline (handling missing values as "Unknown").

### Fixed

- `TypeError` in financial columns by implementing a regex-based numeric conversion (stripping non-numeric characters and fixing decimal commas).
- `AttributeError` in date processing by enforcing `datetime` type casting before accessing `.dt` properties.
- Column mapping issues: aligned script logic with actual dataset schema (`primaryAmountValue`, `amortizationAmountValue`).

## [0.1.1] - 2026-02-17

### Added

- GitHub Actions for syntax check.
- Pytest stub in `tests/`.
- Data download script with retry logic.

### Fixed

- Encoding issues in `.gitignore`.

## [0.1.0] - 2026-02-16

### Added

- Initial project structure.
- EDA template for medical equipment data.
