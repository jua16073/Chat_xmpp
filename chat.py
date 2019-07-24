import asyncio
import logging
import getpass
import sys
from optparse import OptionParser


import slixmpp 


class EchoBot(slixmpp.ClientXMPP):

  def __init__(self, jid, password, recipient, msg):
    super().__init__(jid, password)

    self.recipient = recipient
    self.msg = msg

    self.add_event_handler('session_start', self.start)
    self.add_event_handler('message', self.message)


  def start(self, event):
    self.send_presence()
    self.get_roster()
    self.send_message(mto = self.recipient, mbody = self.msg, mtype = 'chat')
    self.disconnect( wait = True)

  def message(self, msg):
    if msg['type'] in ('normal', 'chat'):
      msg.reply("Thanks for sending:\n%s" %msg['body']).send()




if __name__ == "__main__":
  optp = OptionParser()
  opts, args = optp.parse_args()

  # Fields for user info
  if opts.jid is None:
    opts.jid = input("Username: ")
  if opts.password is None:
    opts.password = getpass.getpass("Password: ")

  #Instantiating bot
  xmpp = EchoBot(opts.jid, opts.password)
  xmpp.register_plugin('xep_0030')
  xmpp.register_plugin('xemp_0199')

  if xmpp.connect():
    xmpp.process(block=True)
  else:
    print('Unable to connect')
  
  pass