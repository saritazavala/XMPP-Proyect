from re import X
import threading
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
#Usando ejemplo de xmpp obtenido de https://docplayer.net/60687805-Slixmpp-documentation.html


class register_to_server(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('register', self.register)
        self.add_event_handler('disconnected', self.got_diss)
    
    def got_diss(self, event):
        print('Got disconnected')

        
    def register(self, event):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
    
        try:
            resp.send()
            print("Cuenta creada con exito")

        except IqError:
            print("No se ha podido crear la cuenta")


        except IqTimeout:
            print("Sin respuesta del servidor")

        self.disconnect()

class my_client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('disconnected', self.got_diss)
        self.add_event_handler('failed_auth', self.failed)
        self.add_event_handler('error', self.handle_error)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0050')
        self.register_plugin('xep_0047')
        self.register_plugin('xep_0231')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0095')
        self.register_plugin('xep_0096')
        self.register_plugin('xep_0047')

        self['xep_0077'].force_registration = True

        self.received = set()
        self.presences_received = threading.Event()

    def handle_error(self):
        print("ERROR DETECTADO")
        self.disconnect()



    def failed(self):
        print("LAS CREDENCIALES INGRESADAS SON INCORRECTAS")
        self.disconnect()

    def start(self):
        self.send_presence()
        self.get_roster()

        self.send_message(mto=self.recipient, mbody=self.msg)
        self.disconnect()
    
    def delete(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.full
        resp['register']['remove'] = True

        try:
            resp.send()
            print("Cuenta "+self.boundjid+" eliminada con exito")

        except IqError as err:
            print("No se ha podido eliminar la cuenta", self.boundjid)
            self.disconnect()

        except IqTimeout:
            print("No se recibio respuesta del servidor")
            self.disconnect()

    def got_diss(self, event):
        print('Got disconnected')