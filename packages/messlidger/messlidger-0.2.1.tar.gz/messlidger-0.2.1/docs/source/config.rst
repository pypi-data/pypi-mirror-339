Configuration
=============

Minimal setup
-------------

For a minimal ``prosody <https://prosody.im>`` based setup, add these lines at the bottom of
``/etc/prosody/prosody.cfg.lua``:

.. code-block:: lua

  Component "messlidger.example.org"
      component_secret = "secret"

And start messlidger with:

.. code-block:: bash

  messlidger \
    --jid messlidger.example.org \
    --secret secret \
    --home-dir /somewhere/writable

Advanced usage
--------------

Refer to the `slidge admin docs <https://slidge.im/docs/slidge/main/admin>`_ for more
advanced setups and examples of configuration for other XMPP servers.

You will probably want to add support for `attachments <https://slidge.im/docs/slidge/main/admin/attachments.html>`_
received from Facebook Messenger, and setup messlidger as a `privileged component <https://slidge.im/docs/slidge/main/admin/privilege.html>`_
for better UX.

messlidger-specific config
--------------------------

All `generic slidge configuration options <https://slidge.im/docs/slidge/main/admin/config/#common-config>`_
apply.
messlidger provides these additional component-wide options:

.. config-obj:: messlidger.config
