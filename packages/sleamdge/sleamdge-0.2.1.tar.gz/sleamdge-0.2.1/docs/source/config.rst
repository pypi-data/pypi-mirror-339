Configuration
=============

Minimal setup
-------------

For a minimal ``prosody <https://prosody.im>`` based setup, add these lines at the bottom of
``/etc/prosody/prosody.cfg.lua``:

.. code-block:: lua

  Component "sleamdge.example.org"
      component_secret = "secret"

And start sleamdge with:

.. code-block:: bash

  sleamdge \
    --jid sleamdge.example.org \
    --secret secret \
    --home-dir /somewhere/writable

Advanced usage
--------------

Refer to the `slidge admin docs <https://slidge.im/docs/slidge/main/admin>`_ for more
advanced setups and examples of configuration for other XMPP servers.

You will probably want to add support for `attachments <https://slidge.im/docs/slidge/main/admin/attachments.html>`_
received from Steam, and setup sleamdge as a `privileged component <https://slidge.im/docs/slidge/main/admin/privilege.html>`_
for better UX.

sleamdge-specific config
------------------------

All `generic slidge configuration options <https://slidge.im/docs/slidge/main/admin/config/#common-config>`_
apply.
sleamdge provides these additional component-wide options:

.. config-obj:: sleamdge.config
