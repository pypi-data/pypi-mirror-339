# matridge

A
[feature-rich](https://slidge.im/docs/matridge/main/features.html)
[Matrix](https://matrix.org) to
[XMPP](https://xmpp.org/) puppeteering
[gateway](https://xmpp.org/extensions/xep-0100.html), based on
[slidge](https://slidge.im) and
[nio](https://matrix-nio.readthedocs.io/).

[![PyPI package version](https://badge.fury.io/py/matridge.svg)](https://pypi.org/project/matridge/)
[![CI pipeline status](https://ci.codeberg.org/api/badges/14069/status.svg)](https://ci.codeberg.org/repos/14069)
[![Chat](https://conference.nicoco.fr:5281/muc_badge/slidge@conference.nicoco.fr)](https://slidge.im/xmpp-web/#/guest?join=slidge@conference.nicoco.fr)


## Installation

Refer to the [slidge admin documentation](https://slidge.im/docs/slidge/main/admin/)
for general info on how to set up an XMPP server component.

### Containers

From [the codeberg package registry](https://codeberg.org/slidge/-/packages/container/matridge/latest)

```sh
docker run codeberg.org/slidge/matridge  # works with podman too
```

Use the `:latest` tag for the latest release, `:vX.X.X` for release X.X.X, and `:main`
for the bleeding edge.

### Python package

With [pipx](https://pypa.github.io/pipx/):

```sh

# for the latest stable release (if any)
pipx install matridge

# for the bleeding edge
pipx install matridge \
    --pip-args='--extra-index-url https://codeberg.org/api/packages/slidge/pypi/simple/'

matridge --help
```

## Documentation

Hosted on [codeberg pages](https://slidge.im/docs/matridge/main/).

## Dev

```sh
git clone https://codeberg.org/slidge/matridge
cd matridge
docker-compose up  # works with podman-compose too
```
