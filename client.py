#Cliente.py
#Sara Zavala

import slixmpp
import aiodns
import asyncio 

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Client(slixmpp.ClientXMPP):
    def __init__(self):
        slixmpp.ClientXMPP.__init__(self, "zav18893@alumchat.xyz", "123")
        self.to = "echobot@alumchat.xyz"
        self.message = "Hola bot :v"
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    async def start(self, event):
        print("Inicio de sesion")
        self.send_presence()
        await self.get_roster()
        self.send_message(mto=self.to, mbody=self.message, mtype='chat')
        self.disconnect()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()

#xmpp is gonna be our client object
xmpp = Client()
xmpp.register_plugin('xep_0030')  # Service Discovery
xmpp.register_plugin('xep_0004')  # Data Forms
xmpp.register_plugin('xep_0060')  # PubSub
xmpp.register_plugin('xep_0199')  # XMPP Ping

# Connect to the XMPP server and start processing XMPP stanzas.
#Connection
xmpp.connect()
xmpp.process(forever=False)
print("1. Ver conectados")
print(" 2. Mandar mensaje privado")
print("3. Madar mensaje general")

