# AGENTS

This file provides guidance to AI agents when working with code in this repository.

## Project Overview

Mailrise is an SMTP server that converts emails into Apprise notifications. It acts as an SMTP gateway, accepting standard email messages and routing them to 60+ notification services (Matrix, Nextcloud, Pushover, Discord, etc.) via the Apprise library.

**Note**: This is a fork of the original repository at https://github.com/YoRyan/mailrise

## Development Commands

### Testing
```bash
# Run all tests with coverage
tox

# Run tests directly with pytest
pytest

# Run specific test file
pytest tests/test_smtp.py
```

### Building
```bash
# Build distribution package
tox -e build

# Clean build artifacts
tox -e clean
```

### Installation
```bash
# Install in editable mode for development
pip install -e .

# Install with test dependencies
pip install -e ".[testing]"
```

### Running the SMTP Server
```bash
# Run with a configuration file
mailrise /path/to/mailrise.conf
```

## Architecture

### Core Components

**SMTP Handler** (`src/mailrise/smtp.py`):
- `AppriseHandler`: aiosmtpd handler that processes incoming SMTP messages
- `handle_RCPT`: Accepts recipient addresses
- `handle_DATA`: Parses email messages and dispatches to routers
- `_parsemessage()`: Extracts subject, body, and attachments from email
- `_apprise_notify()`: Sends notifications via Apprise

**Router System** (`src/mailrise/router.py`, `src/mailrise/simple_router.py`):
- `Router`: Abstract base class for routing logic
- `SimpleRouter`: YAML-based router matching recipient addresses to Apprise configs
- Recipient addresses encode routing information: `config_name@mailrise.xyz` or `config_name.info@mailrise.xyz`
- Notification types (.info/.success/.warning/.failure) extracted from email address
- Supports fnmatch patterns for flexible recipient matching

**Configuration** (`src/mailrise/config.py`):
- `load_config()`: Parses YAML configuration files
- `ConfigFileLoader`: Custom YAML loader with `!env_var` support for secrets
- Supports TLS modes: off, onconnect, starttls, starttlsrequire
- Can import custom routers/authenticators via `import_code` directive

**Authentication** (`src/mailrise/basic_authenticator.py`):
- `BasicAuthenticator`: SMTP AUTH with username/password from config

### Data Flow

1. Email arrives via SMTP → `AppriseHandler.handle_DATA()`
2. Email parsed into `EmailMessage` (subject, from, to, body, attachments)
3. Router converts `EmailMessage` → one or more `AppriseNotification` instances
4. Each notification sent via Apprise to configured services
5. Attachments written to temp files and passed through to Apprise

### Key Data Structures

- `EmailMessage`: Parsed email with subject, from, to, body, attachments
- `EmailAttachment`: Attachment data and filename
- `AppriseNotification`: Title, body, notify_type, config YAML, attachments
- `MailriseConfig`: Complete server configuration including router and authenticator

### Pluggability

Mailrise supports custom routers and authenticators via Python imports:
- Custom router: Implement `Router` interface, expose as module-level `router` variable
- Custom authenticator: Implement aiosmtpd authenticator callback, expose as `authenticator`
- Reference: `tests/noop_pluggable.py`

## Testing Notes

- Tests use pytest with pytest-asyncio for async testing
- `tests/conftest.py`: Shared fixtures
- Test files cover SMTP handling, routing, config parsing, imports
- Coverage reporting enabled by default

## Configuration Format

YAML-based configuration with structure:
- `configs.<name>`: Maps email addresses to Apprise configurations
- `listen.host`/`listen.port`: Network binding
- `tls.mode`/`certfile`/`keyfile`: TLS settings
- `smtp.auth.basic`: Static username/password auth
- `import_code`: Path to custom router/authenticator Python module

## Fork Conventions

### Branching Strategy
- `main`: Development branch for fork-specific work
- `upstream/main`: Remote-tracking branch for https://github.com/YoRyan/mailrise
- Feature branches created from `main`
- Pull requests target `main`

### Syncing Upstream
Branch from the current `main`; never rebase published fork commits, which
produces PR conflicts. Then:

1. Fetch `upstream` and merge the exact commit under review, pinned by SHA
   because `upstream/main` moves: `git merge <sha>`.
2. Resolve conflicts by keeping fork-specific content. The usual conflicts are
   fork-customized files: the Docker workflows, packaging metadata
   (`pyproject.toml`, `setup.cfg`), and the dev container definition. The exact
   set follows what upstream touched, so fork documentation and the Docker build
   action may auto-merge.
3. Run the repository checks, push the branch, open a PR against `main`, and
   confirm GitHub reports it mergeable.
4. Land with a merge commit. Fork-only PRs share no ancestry to preserve and may
   be squashed.

A merge commit, or a fast-forward when the fork has not diverged, keeps the
upstream commits as ancestors of `main` with their original SHAs, authors, and
messages, and keeps `git blame` pointing at them. Squashing folds the whole sync
into one fork commit, losing per-commit granularity, author dates, and blame;
GitHub preserves those authors only as `Co-authored-by` trailers. Rebasing
preserves author name, email, and date, but rewrites the SHA and committer and
drops the original signature, so `upstream/main` is still not an ancestor and the
duplicates are re-resolved on every later sync.

Verify after landing:

```bash
git merge-base --is-ancestor upstream/main main   # passes once the synced tip is merged
git rev-list --count main..upstream/main          # 0 only when the synced commit is upstream's tip
git rev-list --parents -1 <merge> | wc -w         # 3 = the sync landed as a merge
```

All three also pass on a squashed sync, so spot-check blame on a file upstream
changed and confirm it credits the upstream commit rather than a fork commit.

Repair a squashed or rebased sync by merging `upstream/main` while keeping the
fork's tree: ancestry returns and the tree stays identical, but the sync's lines
still blame the squash. Only rewriting `main` restores blame.

`upstream/main` is the upstream repository's main branch; the fork also has a
branch named `upstream`, which fetches as `origin/upstream`.

### Versioning Scheme
- Format: `<upstream-version>-<N>`, for example `1.4.0-5`
- Release tags carry a `v` prefix (`v1.4.0-5`); the release and Docker workflows
  trigger only on `v*` tags, so an unprefixed tag publishes nothing
- Rationale:
  - First part matches upstream version (e.g., `1.4.0`)
  - Second part (`-N`) is fork iteration number
  - Keeps upstream updates separate from fork release numbering
  - Fork identity maintained via repository owner in container registry

### Documentation
- `README.rst`: Main README matching upstream with brief fork notice at top
- `README.fork.md`: All fork-specific changes, installation instructions, versioning
- `CHANGELOG.fork.md`: Detailed changelog following Keep a Changelog format
- `CLAUDE.md`: Agent-specific guidance

### Docker Images
- Published to both GitHub Container Registry (ghcr.io) and Docker Hub
- Tag strategy (source of truth: `.github/actions/docker-build/action.yml`):
  - `latest`: Latest build from `main` branch
  - `stable`: Latest tagged release (tags starting with `v`)
  - `<version>`: Full version (e.g., `1.4.0-5`)
  - `sha-<short-sha>`: Build from specific commit
- Fork releases are semver pre-release versions (`<upstream-version>-<N>`), and
  the metadata action expands `{{major}}` and `{{major}}.{{minor}}` to the full
  pre-release string, so those rules collapse onto `<version>`; no `<major>` or
  `<major>.<minor>` tags are published. This holds only while every release tag
  keeps its `-N` suffix. Use `stable` to follow the latest release

### GitHub Workflows
- `.github/workflows/github-packages.yml`: Builds and pushes to GitHub Container Registry
- `.github/workflows/docker-hub.yml`: Builds and pushes to Docker Hub
- Triggered on:
  - Push to `main` branch
  - Push of tags matching `v*` pattern
  - Manual workflow dispatch

For branch-only publication, use `git push --no-follow-tags`. Automatic tag
following can publish fetched upstream tags unintentionally. Push release tags
explicitly.

### Commit Message Convention
- Follow [Conventional Commits](https://www.conventionalcommits.org/) specification
- Format: `<type>: <description>`
- Common types:
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation changes
  - `refactor`: Code refactoring
  - `ci`: CI/CD changes
  - `chore`: Maintenance tasks
- Examples:
  - `fix: replace Python 3.10+ union syntax for Python 3.9 compatibility`
  - `docs: document Docker tagging strategy and workflow`
  - `ci: update Docker GitHub Actions to latest versions`
