# messlidger

A
[feature-rich](https://slidge.im/docs/messlidger/main/features.html)
[Facebook Messenger](https://messenger.com) to
[XMPP](https://xmpp.org/) puppeteering
[gateway](https://xmpp.org/extensions/xep-0100.html), based on
[slidge](https://slidge.im) and
[mautrix-facebook](https://github.com/mautrix/facebook).

[![PyPI package version](https://badge.fury.io/py/messlidger.svg)](https://pypi.org/project/messlidger/)
[![CI pipeline status](https://ci.codeberg.org/api/badges/14071/status.svg)](https://ci.codeberg.org/repos/14071)
[![Chat](https://conference.nicoco.fr:5281/muc_badge/slidge@conference.nicoco.fr)](https://slidge.im/xmpp-web/#/guest?join=slidge@conference.nicoco.fr)

> ⚠️ **Warning**
>
> Messlidger cannot **send** messages from XMPP to Messenger anymore because the
> [library used to communicate with Facebook Messenger](https://github.com/mautrix/facebook)
> is not maintained anymore. It can still be used to **receive** messages though.

## Installation

Refer to the [slidge admin documentation](https://slidge.im/docs/slidge/main/admin/)
for general info on how to set up an XMPP server component.

### Containers

From [the codeberg package registry](https://codeberg.org/slidge/-/packages/container/messlidger/latest)

```sh
docker run codeberg.org/slidge/messlidger  # works with podman too
```

Use the `:latest` tag for the latest release, `:vX.X.X` for release X.X.X, and `:main`
for the bleeding edge.

### Python package

With [pipx](https://pypa.github.io/pipx/):

```sh

# for the latest stable release (if any)
pipx install messlidger

# for the bleeding edge
pipx install messlidger \
    --pip-args='--extra-index-url https://codeberg.org/api/packages/slidge/pypi/simple/'

messlidger --help
```

## Documentation

Hosted on [codeberg pages](https://slidge.im/docs/messlidger/main/).

## Dev

```sh
git clone https://codeberg.org/slidge/messlidger
cd messlidger
docker-compose up  # works with podman-compose too
```
