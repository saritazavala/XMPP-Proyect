import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser

'''
---------------------------------------------------------------------------

                CHAPTER 3.1
        Slixmpp Quickstart - Echo Bot
https://slixmpp.readthedocs.io/_/downloads/en/slix-1.6.0/pdf/

            Also it was based in this example
https://lab.louiz.org/poezio/slixmpp/-/blob/master/examples/register_account.py

-------------------------------------------------------------------------

'''
#This class helos to register new users
#All the bases are in the previous link

class register_to_server(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('register', self.register)
        self.add_event_handler('disconnected', self.got_diss)
        self.register_plugin('xep_0030')  #Service Discovery
        self.register_plugin('xep_0004')  #Data forms
        self.register_plugin('xep_0066')  #Out-of-band Data
        self.register_plugin('xep_0077')  #In-band Registration
        self.register_plugin('xep_0045')  #Multi user chat
        self.register_plugin('xep_0199')  #XMPP Ping
        self['xep_0077'].force_registration = True
    
    #Function for disconection
    def got_diss(self, event):
        print('Got disconnected')
    
    #Function for register new user & password
    def register(self, event):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
    
        try:
            resp.send()
            print("Account was succesfuly")
        except IqError:
            print("There was an error creating the account")
        except IqTimeout:
            print("Server Timeout")

        self.disconnect()

'''
            # This module provides XMPP functionality that
            # is specific to client connections.
            # Part of Slixmpp: The Slick XMPP Library
            # :copyright: (c) 2011 Nathanael C. Fritz
            # :license: MIT, see LICENSE for more details

https://lab.louiz.org/poezio/slixmpp/-/blob/master/slixmpp/clientxmpp.py


'''
class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.password = password
        self.add_event_handler('disconnected', self.got_diss)
        self.add_event_handler('failed_auth', self.failed)
        self.add_event_handler('error', self.handle_error)
        self.add_event_handler('presence_subscribed', self.new_subscribed)
        self.add_event_handler('message', self.message)
        self.add_event_handler('got_offline', self.handle_offline)
        self.add_event_handler('got_online', self.handle_online)
        self.register_plugin('xep_0004') #Data Forms
        self.register_plugin('xep_0030') #Service Discovery
        self.register_plugin('xep_0045') #Multi user chat
        self.register_plugin('xep_0047') #In-band Bytestreams
        self.register_plugin('xep_0050') #Ad-Hoc Commands
        self.register_plugin('xep_0066') #Out of Band Data
        self.register_plugin('xep_0077') #In-band Registration
        self.register_plugin('xep_0085') #Chat State Notifications
        self.register_plugin('xep_0092') #Software version
        self.register_plugin('xep_0199') #Xmpp ping
        self.register_plugin('xep_0231') #Bits of Binary
        self['xep_0077'].force_registration = True
# -------------------------------------------------------------------------
#This function has the ability of sending a mesasge to an user
#This is basen in the privMesasge function of the main link
    def message(self, msg):
        sender = str(msg['from'])
        jid = sender.split('/')[0]
        username = jid.split('@')[0]

        if msg['type'] in ('chat', 'normal'): print('Nuevo mensaje de: '+username+' dice: '+msg['body'])

        elif msg['type'] in ('groupchat', 'normal'):
            nick  = sender.split('/')[1]
            if jid != self.jid:
                print('Nuevo mensaje del grupo: '+nick+' de: '+jid+' dice: '+msg['body'])

#Handle Errors
    def handle_error(self, event):
        print("An error was detected")
        self.disconnect()

#Handle when an user gets offline
    def handle_offline(self, presence):
        print(str(presence['from']).split('/')[0] + ' got disconected')

#Handle when an user gets online
    def handle_online(self, presence):
        print(str(presence['from']).split('/')[0] + ' got conected')

# When the credentials are incorrect
    def failed(self, event):
        print("Username or password is incorrect")
    

    def start(self):
        self.send_presence()
        self.get_roster()    

    def got_diss(self, event):
        print('Got disconnected')

# Message to user to know that there is new friend
# -------------------------------------------------------------
    def new_subscribed(self, presence):
        print(presence.get_from()+' has added you as a friend!')

# ---------------------------------------------------------
# https://lab.louiz.org/poezio/slixmpp/-/blob/master/slixmpp/plugins/xep_0016/stanza.py
# -------------------------------------------------------------------------------
    def set_presence(self, show, status):
        self.send_presence(show, status)
        self.get_roster()
        time.sleep(3)
    
# ----------------------------------------------------------------------------
# https://lab.louiz.org/poezio/slixmpp/-/blob/master/examples/pubsub_events.py
# ----------------------------------------------------------------------------

    def delete(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.full
        resp['register']['remove'] = True

        try:
            print("The account of", self.boundjid.bare, "has been deleted")
            resp.send()
        except IqError as err:
            print("There was an error deleting the account")
            self.disconnect()
        except IqTimeout:
            print("Server TimeOut")
            self.disconnect()
    
# Add User as a friend
    def add_friend(self, JID):
        self.send_presence_subscription(pto=JID, ptype='subscribe', pfrom = self.boundjid.bare)
        self.get_roster()
        time.sleep(3)



'''
        4.2.6 Example 14-7. (Page 225)
https://slixmpp.readthedocs.io/_/downloads/en/slix-1.6.0/pdf/

'''
class PrivMsg(slixmpp.ClientXMPP):
    def __init__(self, jid, password, uname, msg):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.uname = uname
        self.msg = msg

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('presence_subscribed', self.new_subscribed)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.send_message(mto=self.uname,
                          mbody=self.msg,
                          mtype='chat')
        
        print("Your message was sent correctly")
    
    #Menejo de nuevas subscripciones
    def new_subscribed(self, presence):
        print(presence.get_from()+' added you as a friend')

'''
---------------------------------------------------------------------------

                CHAPTER 3.1
        Slixmpp Quickstart - Echo Bot
https://slixmpp.readthedocs.io/_/downloads/en/slix-1.6.0/pdf/

            Also it was based in this example
https://lab.louiz.org/poezio/slixmpp/-/blob/master/examples/register_account.py

-------------------------------------------------------------------------
'''

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





'''
                    #Class for getting Roster
https://lab.louiz.org/poezio/slixmpp/-/blob/master/slixmpp/roster/single.py

'''
class GetRoster(slixmpp.ClientXMPP):
    #Class for getting Roster
    def __init__(self, jid, password, u_search = None):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.roster = {}
        self.u_search = u_search

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('changed_status', self.wait_for_presences)
        self.add_event_handler('disconnected', self.got_diss)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')

        self.received = set()
        self.presences_received = asyncio.Event()

 
    def got_diss(self, event):
        print('Got disconnected')
        quit()

    async def start(self, event):
        try:
            await self.get_roster()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Timeout del server')
        self.send_presence()

        print('Esperando actualizaciones...')
        await asyncio.sleep(5)

        print('El roster de %s es:' % self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            for jid in groups[group]:
                status = ''
                show = ''
                sub = ''
                name = ''
                sub = self.client_roster[jid]['subscription']
                conexion = self.client_roster.presence(jid)
                name = self.client_roster[jid]['name']
                for answer, pres in conexion.items():
                    if pres['show']:
                        show = pres['show']
                    if pres['status']:
                        status = pres['status']
                self.roster[jid] = User(jid, show, status, sub, name)


        # ----------------------------------------------------------------------------------
        #https://lab.louiz.org/poezio/slixmpp/-/blob/master/slixmpp/roster/multi.py
        # ----------------------------------------------------------------------------------

        if(not self.u_search):
            if len(self.roster) == 0:
                print('No hay usuarios agregados')
            else:
                for key in self.roster.keys():
                    friend = self.roster[key]
                    print('- Jid: '+friend.jid+' Username:'+friend.username+' Show:'+friend.show+' Status:'+friend.status+' Subscription:'+friend.subscription)

 
        else:
            if self.u_search in self.roster.keys():
                user = self.roster[self.u_search]
                print('- Jid: '+user.jid+' Username:'+user.username+' Show:'+user.show+' Status:'+user.status+' Subscription:'+user.subscription)
            else:
                print('Usuario no encontrado')
        

        await asyncio.sleep(5)
        self.disconnect()

    def wait_for_presences(self, pres):
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()
# ----------------------------------------------------------------------------------
#https://lab.louiz.org/poezio/slixmpp/-/blob/master/slixmpp/roster/multi.py
# ----------------------------------------------------------------------------------

#This is just for comodidad :v
# ------------------------
class User():
    def __init__(self, jid, show, status, subscription, username):
        self.jid = jid
        self.show = show
        self.status = status
        self.subscription = subscription
        self.username = username

'''
                CHAPTER 3.6
        Enable HTTP Proxy Support
https://slixmpp.readthedocs.io/_/downloads/en/slix-1.6.0/pdf/


'''

class SendFile(slixmpp.ClientXMPP):
    
    def __init__(self, jid, password, receiver, filename):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.receiver = receiver    
        self.file = open(filename, 'rb')
        self.domain = domain
        
    
        self.add_event_handler("session_start", self.start)
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0071')
        self.register_plugin('xep_0128')
        self.register_plugin('xep_0363')

    
    
    async def start(self, event):
        try:
    
            proxy = await self['xep_0363'].handshake(self.receiver)
            while True:
                data = self.file.read(1048576)
                if not data:
                    break
                await proxy.write(data)
            proxy.transport.write_eof()
    
        except (IqError, IqTimeout) as e:
            print("Error detected")
        else:
            print("File transfered correctly")
        finally:
    
    
            self.file.close()
    
            self.disconnect()


