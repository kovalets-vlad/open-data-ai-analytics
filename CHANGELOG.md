# Changelog

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
