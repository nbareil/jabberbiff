#! /usr/bin/env python

#############################################################################
##                                                                         ##
## jabberbiff.py --- Mail notification over Jabber                         ##
##                                                                         ##
## Copyright (C) 2010-2012  Nicolas Bareil             <nico@chdir.org>    ##
##                                                                         ##
## This program is free software; you can redistribute it and/or modify it ##
## under the terms of the GNU General Public License version 2 as          ##
## published by the Free Software Foundation; version 2.                   ##
##                                                                         ##
## This program is distributed in the hope that it will be useful, but     ##
## WITHOUT ANY WARRANTY; without even the implied warranty of              ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU       ##
## General Public License for more details.                                ##
##                                                                         ##
#############################################################################

from pyxmpp.jabber.simple import send_message
from ConfigParser import SafeConfigParser
from pyxmpp.jid import JID
from pyinotify import *

import email
import re
import os

config = SafeConfigParser()
config.read(os.path.join(os.environ['HOME'], '.jabberbiffrc'))

IGNORE_REGEX_MAILBOXES = map(lambda x: x[1], config.items('ignoremailboxes'))
MAILBOXESDIR = config.get('mailboxes', 'src')
if config.get('mailboxes', 'dotprepended').lower() in ['1', 'true', 'yes']:
    # dovecot prepends a dot in front of folder name
    n=1
else:
    n=0
MAILBOXESTRIM= len(MAILBOXESDIR) + n

BOT_JID     = config.get('bot', 'jid')
BOT_PASSWD  = config.get('bot', 'passwd')
JABBER_RCPT = config.get('notify', 'rcpt')

ignores = map(lambda x: re.compile(x), IGNORE_REGEX_MAILBOXES)

class MaildirEvent(ProcessEvent):
    def process_IN_CREATE(self, event):
        if not event.path.endswith('/new'):
            return
        folder = event.path[MAILBOXESTRIM:-4] or 'INBOX'
	absolutepath = os.path.join(event.path, event.name)
	msg = email.message_from_file(open(absolutepath))
        #print 'New mail in %s: %s : %s' % (folder, msg['From'], msg['Subject'])
	for ignore in ignores:
	   if ignore.match(folder):
		return
        send_message(JID(BOT_JID), BOT_PASSWD, JABBER_RCPT, '%s: %s\n%s' % (folder, msg['From'] , msg['Subject']), message_type='chat')

event = MaildirEvent()

watcher = WatchManager()
watcher.add_watch(MAILBOXESDIR, IN_CREATE, rec=True, auto_add=True)

notifier = Notifier(watcher, event)
while True:
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    except KeyboardInterrupt:
        notifier.stop()
        break
