Mastodon Bridge
===============

.. image:: https://img.shields.io/pypi/v/simplebot_mastodon.svg
   :target: https://pypi.org/project/simplebot_mastodon

.. image:: https://img.shields.io/pypi/pyversions/simplebot_mastodon.svg
   :target: https://pypi.org/project/simplebot_mastodon

.. image:: https://pepy.tech/badge/simplebot_mastodon
   :target: https://pepy.tech/project/simplebot_mastodon

.. image:: https://img.shields.io/pypi/l/simplebot_mastodon.svg
   :target: https://pypi.org/project/simplebot_mastodon

.. image:: https://github.com/simplebot-org/simplebot_mastodon/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/simplebot-org/simplebot_mastodon/actions/workflows/python-ci.yml

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

A Mastodon <-> DeltaChat bridge plugin for `SimpleBot`_.

If this plugin has collisions with commands from other plugins in your bot, you can set a command prefix like ``/masto_`` for all commands::

  simplebot -a bot@example.com db -s simplebot_mastodon/cmd_prefix masto_

Install
-------

To install run::

  pip install simplebot-mastodon

User Guide
----------

To log in with OAuth, send a message to the bot::

  /login mastodon.social

replace "mastodon.social" with your instance, the bot will reply with an URL that you should open to grant access to your account, copy the code you will receive and send it to the bot.

To log in with your user and password directly(not recommended)::

  /login mastodon.social me@example.com myPassw0rd

Once you log in, A "Home" and "Notifications" chats will appear, in the Home chat you will receive your Home timeline and any message you send there will be published on Mastodon. In the Notifications chat you will receive all the notifications for your account.

If someone sends you a direct message in a private 1:1 conversation, it will be shown as a new chat where you can chat in private with that person, to start a private chat with some Mastodon user, send::

  /dm friend@example.com

and the chat with "friend@example.com" will pop up.

To logout from your account::

  /logout

For more info and all the available commands(follow, block, mute, etc), send this message to the bot::

  /help


.. _SimpleBot: https://github.com/simplebot-org/simplebot
