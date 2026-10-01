# Fork-Specific Changes

[![Docker pulls](https://badgen.net/docker/pulls/sandipb/mailrise)](https://hub.docker.com/r/sandipb/mailrise)
[![Last commit](https://badgen.net/github/last-commit/sandipb/mailrise/main)](https://github.com/sandipb/mailrise)
[![Checks status](https://badgen.net/github/checks/sandipb/mailrise)](https://github.com/sandipb/mailrise/actions)

This document describes all changes made in this fork of mailrise.

## Installation

### From PyPI

You can find the original Mailrise [on PyPI](https://pypi.org/project/mailrise/).
This fork is not published to PyPI. Install from source instead (see below).

The minimum Python version is 3.10. Docker images and the default tox target use Python 3.13.
Run `tox -e py310,py311,py312,py313` to test all supported Python versions.

Once installed, you should write a configuration file and then configure Mailrise
to run as a service. Here is the suggested systemd unit file::

    [Unit]
    Description=Mailrise SMTP notification relay

    [Service]
    ExecStart=/usr/local/bin/mailrise /etc/mailrise.conf

    [Install]
    WantedBy=multi-user.target

### From source

This repository is structured like any other Python package. To install it in
editable mode for development or debugging purposes, use::

    pip install -e ".[testing]"

To build a wheel, use::

    tox -e build

If you are using Visual Studio Code, a
[development container](https://code.visualstudio.com/docs/remote/containers)
is included with all the Python tooling necessary for working with Mailrise.

## Fork Versioning

This fork uses a simple versioning scheme that maintains a clear relationship to the upstream
project while distinguishing fork-specific releases:

* **Format**: `<upstream-version>-<N>`
* **Example**: `1.4.0-1`, `1.4.0-2`
* **Rationale**:

  * `1.4.0` matches the last upstream release version
  * `-N` identifies the fork iteration (increments with each fork release)
  * Keeps upstream updates separate from fork release numbering
  * The fork is identified by the repository owner (sandipb) in the container registry path

**Current version**: `1.4.0-5`

## Changes in this fork

* Synced with upstream commit `60d485e` (2025-11-08).
* Requires Apprise 2.0 or later; dependency versions are no longer pinned.
* Supports Python 3.10–3.13; Python 3.13 is the container and default test version.
* Publishes fork images to Docker Hub and GitHub Container Registry.
* Uses fork-specific release tags and container tags.
