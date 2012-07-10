jabberbiff
==========

Description
===========

jabberbiff is a biff(1) using modern technology. It monitors local
Mailbox folders (thanks to inotify) and on new message, it sends
you a message through a Jabber/XMPP notification.

Configuration
=============

 1. Copy ```jabberbiffrc.sample``` in ```$HOME/.jabberbiffrc```.
 2. Adapt it :)
 3. Run ```jabberbiff.py```

Requirements
============

 - pyxmpp
 - pyinotify

By the way, to compile these extensions, you will need libxml2-dev
and python-dev.


