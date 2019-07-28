import asyncio
import logging
from getpass import getpass
from argparse import ArgumentParser
from slixmpp import  ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout

class client_xmpp(ClientXMPP):
  def __init__(self, jid, password):
    super().__init__(jid, password)

    self.add_event_handler("session_start", self.start)

    self.add_event_handler("register", self.register)

  def start(self, event):
    self.send_presence()
    self.get_roster()
    self.disconnect()

  async def register(self, iq):
    resp = self.Iq()
    resp['type'] = 'set'
    resp['register']['username'] = self.boundjid.user
    resp['register']['password'] = self.password

    try:
      await resp.send()
      logging.info("Account created for %s!" %self.boundjid)
    except IqError as e:
      logging.error("Could not register account: %s" % e.iq['error']['text'])
      self.disconnect()
    except IqTimeout:
      loging.error("No response from server")
      self.disconnect()

#//////////////////////////////////////////////////////////////////////////////

# Main Method
if __name__ == "__main__":
  parser = ArgumentParser()

  parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
  parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                      action="store_const", dest="loglevel",
                      const=logging.DEBUG, default=logging.INFO)

  parser.add_argument("-j", "--jid", dest = "jid", help = "JID to use")
  parser.add_argument("-p", "--password", dest = "password", help = "password to use")

  args = parser.parse_args()

  #logging.basicConfig(level = args.loglevel,  format = '%(levelname) - 8s %(message)s')
  logging.basicConfig(level=args.loglevel,format='%(levelname)-8s %(message)s')


  if args.jid is None:
    args.jid = input("Username: ") + "@alumchat.xyz"
  if args.password is None:
    args.password = getpass("Password: ")

  xmpp = client_xmpp(args.jid, args.password)

  xmpp.register_plugin('xep_0030') # Service Discovery
  xmpp.register_plugin('xep_0004') # Data forms
  xmpp.register_plugin('xep_0066') # Out-of-band Data
  xmpp.register_plugin('xep_0077') # In-band Registration


  xmpp.connect()
  xmpp.process()

  pass