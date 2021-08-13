import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser




#All the MUC fUnctions are based in the Multi User
#Chat Bot from the Chapter 3 in Slixmpp Documentation
#https://slixmpp.readthedocs.io/_/downloads/en/slix-1.6.0/pdf/

'''
---------------- CHAPTERS  --------------------

        3.4 Manage Presence Subscriptions
        3.5 Multi-User Chat (MUC) Bot
https://slixmpp.readthedocs.io/_/downloads/en/slix-1.6.0/pdf/

-----------------------------------------------
'''
class create_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('session_start', self.start)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        
        self.room = room
        self.alias = alias

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        
        #A group has to be open, and it will be assigned 
        status = 'open'
        self.plugin['xep_0045'].join_muc(
            self.room,
            self.alias,
            pstatus=status,
            pfrom=self.boundjid.full)

        await self.plugin['xep_0045'].set_affiliation(self.room, jid = self.boundjid.full,
            affiliation = 'owner')

        print("The group was created succesfully")
        self.disconnect()
        quit()

'''
-----------------------------------------------
                CHAPTER 3.5.1
            3.5.1 Joining The Room
https://slixmpp.readthedocs.io/_/downloads/en/slix-1.6.0/pdf/
-----------------------------------------------
'''
class join_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('session_start', self.start)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        self.room = room
        self.alias = alias
# -----------------------------------------------------------------
    async def start(self, event):
        await self.get_roster()
        self.send_presence()
# -----------------------------------------------------------------        
        status = 'open'
        self.plugin['xep_0045'].join_muc(
            self.room,
            self.alias,
            pstatus=status,
            pfrom=self.boundjid.full)
# -----------------------------------------------------------------        
        self.disconnect()
        quit()


'''
-----------------------------------------------
                CHAPTER 3.5.2
            3.5.2 Adding Functionality
https://slixmpp.readthedocs.io/_/downloads/en/slix-1.6.0/pdf/
-----------------------------------------------
'''
class leave_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)
# -----------------------------------------------------------------
        self.add_event_handler('session_start', self.start)
# -----------------------------------------------------------------
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        # -----------------------------------------------------------------
        self.room = room
        self.alias = alias
# -----------------------------------------------------------------
    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        print('AQUI')
        await self.plugin['xep_0045'].leave_muc(self.room, self.alias)
        print('AQUI')
# -----------------------------------------------------------------
        self.disconnect()
        quit()

'''
-----------------------------------------------
                CHAPTER 3.2
    Sign in, Send a Message, and Disconnect
https://slixmpp.readthedocs.io/_/downloads/en/slix-1.6.0/pdf/

-----------------------------------------------

'''

class SendMsg_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, msg):
        slixmpp.ClientXMPP.__init__(self, jid, password)
# -----------------------------------------------------------------
        self.add_event_handler('session_start', self.start)
# -----------------------------------------------------------------
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        self.room = room
        self.msg = msg
# -----------------------------------------------------------------
    async def start(self, event):
        await self.get_roster()
        self.send_presence()

        self.send_message(
            mto=self.room,
            mbody=self.msg,
            mtype='groupchat',
            mfrom=self.boundjid.full
        )
        print('Mensaje mandado correctamente')
        # -----------------------------------------------------------------
    

