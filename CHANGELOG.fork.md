# Fork Changelog

All notable changes to this fork will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to the versioning scheme `<upstream-version>-<N>`.

## [Unreleased]

## [1.4.0-4] - 2025-01-07

### Added
- Python 3.12 and 3.13 support ([#2](https://github.com/sandipb/mailrise/issues/2))
- Comprehensive tox testing for Python 3.10, 3.11, 3.12, and 3.13

### Changed
- Updated tox configuration to test against multiple Python versions
- Enhanced CI/CD testing matrix for better compatibility verification
- Raised minimum Python version requirement from 3.9 to 3.10

## [1.4.0-3] - 2025-10-07

### Changed
- Reorganized branching strategy: `main` for development, `upstream` for upstream sync
- Updated GitHub Actions workflows to use `main` branch
- Updated Docker build actions to latest versions (setup-qemu v2→v3, setup-buildx v2→v3, metadata v4→v5, build-push v3→v6)
- Added comprehensive Docker image tagging strategy (major, major.minor, version, sha, latest, stable)
- Enabled Docker Hub publishing workflow
- Separated fork-specific documentation into README.fork.md and CHANGELOG.fork.md

## [1.4.0-2] - 2025-10-07

### Fixed
- Replaced Python 3.10+ union syntax for Python 3.9 compatibility ([#1](https://github.com/sandipb/mailrise/issues/1))

## [1.4.0-1] - (Initial Fork)

### Changed
- Updated Apprise from 1.7.1 to 1.9.5
- Updated aiosmtpd from 1.4.4.post2 to 1.4.6
- Updated PyYAML from 6.0.1 to 6.0.3
- Bumped minimum Python version to 3.9+ (from 3.8+) due to Apprise 1.9.5 requirement
- All tests passing with updated dependencies

[Unreleased]: https://github.com/sandipb/mailrise/compare/v1.4.0-4...HEAD
[1.4.0-4]: https://github.com/sandipb/mailrise/compare/v1.4.0-3...v1.4.0-4
[1.4.0-3]: https://github.com/sandipb/mailrise/compare/v1.4.0-2...v1.4.0-3
[1.4.0-2]: https://github.com/sandipb/mailrise/compare/v1.4.0-1...v1.4.0-2
[1.4.0-1]: https://github.com/sandipb/mailrise/releases/tag/v1.4.0-1
