import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


class login_manager(slixmpp.ClientXMPP):
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
        print("Credenciales Inorrectas")
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

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.recipient = recipient
        self.msg = message

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.send_message(mto=self.recipient,mbody=self.msg,mtype='chat')

    def message(self, msg):
        if msg['type'] in ('chat'):
            recipient = msg['to']
            body = msg['body']
            print(str(recipient) +  ": " + str(body))
            message = input("Write the message: ")
            self.send_message(mto=self.recipient,mbody=message)

class Register(slixmpp.ClientXMPP):
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

class chat_group(slixmpp.ClientXMPP):
    
    def __init__(self, jid, password, jid_room, ak_room):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room, self.muc_online)
        # self.register_plugin('xep_0030')
        # self.register_plugin('xep_0199')
        # self.register_plugin('xep_0045')
        # self.register_plugin('xep_0096')
        self.room = jid_room
        self.ak = ak_room

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        
        try:
            self.plugin['xep_0045'].join_muc(self.room, self.ak)
            print("Bienvenido a tu nuevo grupo!")
        except IqError:
            print("Error encontrado")
        except IqTimeout:
            print("Timeout del server")
        self.disconnect()           

class subscribe(slixmpp.ClientXMPP):
    
    def __init__(self, jid, password, to):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.to = to

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        try:
            self.send_presence_subscription(pto=self.to)        
        except IqTimeout:
            print("Timeout") 
        self.disconnect()

class Users(slixmpp.ClientXMPP):

    def __init__(self, jid, password, user=None, show=True, message=""):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.presences = threading.Event()
        self.users = []
        self.user = user
        self.show = show
        self.message = message

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        all_users = []
        try:
            self.get_roster()
        except IqError as e:
            print("Error encontrado")
        except IqTimeout:
            print("Timeout del server")
        self.presences.wait(3)

        my_roster = self.client_roster.groups()
        for group in my_roster:
            for user in my_roster[group]:
                status = show = answer = priority = ''
                self.users.append(user)
                subs = self.client_roster[user]['subscription']                         
                conexions = self.client_roster.presence(user)                           
                username = self.client_roster[user]['name']                            
                for answer, pres in conexions.items():
                    if pres['show']:
                        show = pres['show']                                             
                    if pres['status']:
                        status = pres['status']                                         
                    if pres['priority']:
                        priority = pres['priority']                                    
                all_users.append([user,subs,status,username,priority])
                self.users = all_users

        
        if(self.show):
            if(not self.user):
                if len(all_users)==0:
                    print("No hay nadie agregado")
                else:
                    print("--- Agregados ---")
                for contact in all_users:
                    print('\tJID:' + contact[0] + 
                    '\t\tSUBSCRIPTION:' + 
                    contact[1] + 
                    '\t\tSTATUS:' +
                     contact[2])
            else:
                for contact in all_users:
                    if(contact[0]==self .user):
                        print('\tJID:' + contact[0] + 
                        '\n\tSUBSCRIPTION:' + 
                        contact[1] + 
                        '\n\tSTATUS:' + 
                        contact[2] + 
                        '\n\tUSERNAME:' + 
                        contact[3] + 
                        '\n\tPRIORITY:' + 
                        contact[4])
        else:
            for JID in self.users:
                self.notification_(JID, self.message, 'active')

        self.disconnect()

