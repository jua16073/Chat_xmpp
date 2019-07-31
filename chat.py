import asyncio
import logging
import sys
from getpass import getpass
from argparse import ArgumentParser
import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout

import misc

if sys.version_info < (3, 0):
  reload(sys)
  sys.setdefaultencoding('utf8')


#x@alumchat.xyz/6rbcf812cb

class client_xmpp(sleekxmpp.ClientXMPP):
  def __init__(self, jid, password):
    sleekxmpp.ClientXMPP.__init__(self,jid, password)

    self.add_event_handler("session_start", self.start)
    self.add_event_handler("register", self.register)
    self.add_event_handler("message", self.message)

  def start(self, event):
    self.send_presence()
    self.get_roster()

  def message(self, msg):
    print(msg['from'],": ")
    print(msg['body'])

  def salir(self):
    self.disconnect()

  def tosend(self, to, body):
    self.send_message(mto = to + '@alumchat.xyz',
                      mbody = body
                      )
  
  def lista(self):
    list_f = self.client_roster
    for key in list_f:
      print(key)

  def delete_account(self):
    resp = self.Iq()
    resp['type'] = 'set'
    resp['from'] = self.boundjid.user
    resp['register'] = ' '
    resp['register']['remove'] = ' '

    try:
      resp.send(now = True)
      logging.info("Erased account %s" % self.boundjid)
    except IqError as e:
      print("Something went wrong")
    except IqTimeout:
      print("No response from server")
  
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
    except IqTimeout:
      logging.error("No response from server")

#//////////////////////////////////////////////////////////////////////////////
def menu():
  print("\nChoose an option: ")
  print("1. Show friends")
  print("2. Add friend")
  print("3. Chat 1v1")
  print("4. Erase account")
  print("5. Log out\n")


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
  xmpp.register_plugin('xep_0060')
  xmpp.register_plugin('xep_0066') # Out-of-band Data
  xmpp.register_plugin('xep_0077') # In-band Registration
  xmpp.register_plugin('xep_0199') # XMPP Ping
  xmpp.register_plugin('xep_0045')

  xmpp['xep_0077'].force_registration = True

  #If connection succeds, displays de menu
  if (xmpp.connect()):
    xmpp.process(block = False)
    while True:
      menu()
      resp = input("-")
      if resp == '1':
        xmpp.lista()
      elif resp == '2':
        amigo = input('User: ') + '@alumchat.xyz'
        xmpp.send_presence_subscription(pto = amigo,
                                        ptype='subscribe'
                                        )
      elif resp == '3':
        to = input("To : ")
        body = input("Message: ")
        xmpp.tosend(to, body)
      elif resp == '4':
        xmpp.delete_account()
      elif resp == '5':
        xmpp.salir()
        break
  else:
    print("Can't connect")
  pass