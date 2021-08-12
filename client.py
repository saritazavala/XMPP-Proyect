import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

        self.recipient = recipient
        self.msg = message

    async def start(self, event):
        #Send presence
        self.send_presence()
        await self.get_roster()

        #Send message of type chat
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
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)
        self.user = jid

    def start(self, event):
        self.send_presence()
        self.get_roster()
        
    def got_diss(self, event):
        print('Got disconnected')

    def register(self, iq):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['register']['username'] = self.boundjid.user
        iq['register']['password'] = self.password

        try:
            iq.send()
            print("Nueva cuenta creadas", self.boundjid)
            self.disconnect()
        
        except IqError as e:
            print("No se ha podido crear la cuenta")
            self.disconnect()
        
        except IqTimeout:
            print("TimeOut del server")
            self.disconnect()
        
        except Exception as e:
            print(e)
            self.disconnect()

class Client_join_group(slixmpp.ClientXMPP):
    
    def __init__(self, jid, password, room_jid, room_ak):
        slixmpp.ClientXMPP.__init__(self, jid, password)
   
        self.add_event_handler("session_start", self.start)

        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room, self.muc_online)


        # self.register_plugin('xep_0030')
        # self.register_plugin('xep_0199')
        # self.register_plugin('xep_0045')
        # self.register_plugin('xep_0096')
        self.room = room_jid
        self.ak = room_ak

    async def start(self, event):
        #Send presence
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

class Client_subscribe(slixmpp.ClientXMPP):
    
    def __init__(self, jid, password, to):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.to = to

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        try:
            self.send_presence_subscription(pto=self.to)        #Subscribe to user
        except IqTimeout:
            print("Timeout") 
        self.disconnect()