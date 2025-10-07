# Fork-Specific Changes

[![Docker pulls](https://badgen.net/docker/pulls/sandipb/mailrise)](https://hub.docker.com/r/sandipb/mailrise)
[![Last commit](https://badgen.net/github/last-commit/sandipb/mailrise/main)](https://github.com/sandipb/mailrise)
[![Checks status](https://badgen.net/github/checks/sandipb/mailrise)](https://github.com/sandipb/mailrise/actions)

This document describes all changes made in this fork of mailrise.

## Installation

### From PyPI

You can find the original Mailrise [on PyPI](https://pypi.org/project/mailrise/).
This fork is not published to PyPI. Install from source instead (see below).

The minimum Python version is 3.10+.

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

    pip install -e .

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
  * Makes it easy to merge upstream changes if the original project resumes activity
  * The fork is identified by the repository owner (sandipb) in the container registry path

**Current version**: `1.4.0-4`

## Changes in this fork

* Updated dependencies:

  * Apprise: 1.7.1 → 1.9.5
  * aiosmtpd: 1.4.4.post2 → 1.4.6
  * PyYAML: 6.0.1 → 6.0.3

* Python requirement: 3.10+ (was 3.8+, updated due to Apprise 1.9.5 requirement and modern Python support)
* All tests passing with updated dependencies
