import sys
import logging
import getpass
from optparse import OptionParser

import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout

if sys.version_info < (3, 0):
  sys.setdefaultencoding('utf8')


class client(sleekxmpp.ClientXMPP):
  def __init__(self, jid, password):
    super(client, self).__init__(jid, password)

    self.add_event_handler('session_start', self.start)
    self.add_event_handler('message', self.message)

  def start(self, event):
    self.send_presence()
    self.get_roster()
    self.send_message(mto = 'p_x@alumchat.xyz',
                      mbody = 'cambio a sleek'
                      )
  
  def message(self, msg):
    print(msg['from'], ": ")
    print(msg['body'])

  def send_msg(self, msg):
    self.send_message(mto = 'p_x@alumchat.xyz',
                      mbody = 'cambio a sleek'
                      )
  
  def register(self, iq):
    resp = self.Iq()
    resp['type'] = 'set'
    resp['register']['username'] = self.boundjid.user
    resp['register']['password'] = self.password

    try: 
      resp.send(now = True)
      logging.info("Account created for %s" % self.boundjid)
    except IqError as e:
      logging.error("Could not register account")
    except IqTimeout:
      logging.error("No response from server")
  
  def log_out(self):
    self.disconnect()

def menu():
  print("Seleccione una opcion: \n")
  print("1. Mostrar todos los usuarios")
  print("2. Chat 1v1")
  print("3. Salir")


if __name__ == "__main__":
  print("Comenzando otra vez")
  optp = OptionParser()

  optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
  optp.add_option("-j", "--jid", dest="jid",
                  help="JID to use")
  optp.add_option("-p", "--password", dest="password",
                  help="password to use")
  
  opts, args = optp.parse_args()

  if opts.jid is None:
    opts.jid = input("Username: ") + '@alumchat.xyz'
  if opts.password is None:
    opts.password = getpass.getpass("Password: ")


  xmpp = client(opts.jid, opts.password)
  xmpp.register_plugin('xep_0030') # Service Discovery
  xmpp.register_plugin('xep_0004') # Data forms
  xmpp.register_plugin('xep_0060')
  xmpp.register_plugin('xep_0066') # Out-of-band Data
  xmpp.register_plugin('xep_0077') # In-band Registration
  xmpp.register_plugin('xep_0199') # XMPP Ping
  xmpp.register_plugin('xep_0045')
  xmpp['xep_0077'].force_registration = True

  xmpp.connect(('alumchat.xyz', 5222)):
    xmpp.process(block = True)
    while True:
      menu()
      option = input()
      if option == 10:
        break
    xmpp.log_out()
  else:
    print('Unable to connect')

  pass