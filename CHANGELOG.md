# Changelog

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
