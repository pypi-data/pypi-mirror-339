# matteridge

A
[feature-rich](https://slidge.im/docs/matteridge/main/features.html)
[Mattermost](https://mattermost.com) to
[XMPP](https://xmpp.org/) puppeteering
[gateway](https://xmpp.org/extensions/xep-0100.html), based on
[slidge](https://slidge.im) and
[mattermost-api-reference-client](https://git.sr.ht/~nicoco/mattermost-api-reference-client).

[![PyPI package version](https://badge.fury.io/py/matteridge.svg)](https://pypi.org/project/matteridge/)
[![CI pipeline status](https://ci.codeberg.org/api/badges/14070/status.svg)](https://ci.codeberg.org/repos/14070)
[![Chat](https://conference.nicoco.fr:5281/muc_badge/slidge@conference.nicoco.fr)](https://slidge.im/xmpp-web/#/guest?join=slidge@conference.nicoco.fr)


## Installation

Refer to the [slidge admin documentation](https://slidge.im/docs/slidge/main/admin/)
for general info on how to set up an XMPP server component.

### Containers

From [the codeberg package registry](https://codeberg.org/slidge/-/packages/container/matteridge/latest)

```sh
docker run codeberg.org/slidge/matteridge  # works with podman too
```

Use the `:latest` tag for the latest release, `:vX.X.X` for release X.X.X, and `:main`
for the bleeding edge.

### Python package

With [pipx](https://pypa.github.io/pipx/):

```sh

# for the latest stable release (if any)
pipx install matteridge

# for the bleeding edge
pipx install matteridge \
    --pip-args='--extra-index-url https://codeberg.org/api/packages/slidge/pypi/simple/'

matteridge --help
```

## Documentation

Hosted on [codeberg pages](https://slidge.im/docs/matteridge/main/).

## Dev

```sh
git clone https://codeberg.org/slidge/matteridge
cd matteridge
docker-compose up  # works with podman-compose too
```
