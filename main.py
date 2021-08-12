from logging import log
from os import close
from slixmpp import jid
from getpass import getpass
from client import *
from ssl import OP_NO_RENEGOTIATION

def online_user(event):
    xmpp.start()
    print("Bienvenido al chat! :", xmpp.boundjid.bare)

    while True:
        print(" ----------------- Menu ------------------------- ")
        print(" 1. Ver usuario y su estado ")
        print(" 2. Agregar usuario a contactos ")
        print(" 3. Mostrar detalles de un contacto ")
        print(" 4. Mandar mensaje privado ")
        print(" 5. Madar mensaje general")
        print(" 6. Definir mensaje de presencia " )
        print(" 7. Enviar/recibir notificaciones " )
        print(" 8. Enviar/recibir archivos " )
        print(" 9. Cerrar Sesion " )
        print(" 10. Eliminiar cuenta")

        opt = input("Ingrese la opcion deseada: ")

        if opt == "1":
            pass

        elif opt == "4":
            pass
        
        elif opt == "9":
            xmpp.disconnect()
            print(" Se ha cerrado sesion de -->" , xmpp.boundjid.bare)
            break

        elif opt == "10":
            xmpp.delete()
            xmpp.disconnect()
            print(" Se ha eliminado la cuenta de -->  " , xmpp.boundjid.bare)
            break

        else:
            print("Opcion invalida")


while(True):
    print(" ------------------------------------------------ ")
    print(" ----------------- Menu ------------------------- ")
    print(" ------------------------------------------------ ")

    print("1. Iniciar Sesion")
    print("2. Registrar nueva cuenta")
    print("3. Salir")
    option = input("Ingrese la opcion deseada: ")

    if option == '1':

        print(" --------------------------------------------------- ")
        print("----------------- Inicio de Sesion ----------------- ")
        print(" --------------------------------------------------- ")


        username = input("Ingrese su nombre  de usuario: ")
        user_password = getpass(" Ingrese su contrasenia: ")
        xmpp = login_manager( jid= username, password = user_password )
        xmpp.add_event_handler('session_start', online_user)
        xmpp.connect()
        xmpp.process(forever=False)
        
    elif option == '2':
        print(" -------------------------------------------------- ")
        print(" ----------------- Nuevo Usuario  ----------------- ")
        print(" -------------------------------------------------- ")

        username = input("Ingrese su nombre  de usuario: ")
        user_password = getpass(" Ingrese su contrasenia: ")

        xmpp = Register(jid=username, password=user_password)
        xmpp.register_plugin('xep_0030')  # Service Discovery
        xmpp.register_plugin('xep_0004')  # Data forms
        xmpp.register_plugin('xep_0066')  # Out-of-band Data
        xmpp.register_plugin('xep_0077')  # In-band Registration
        xmpp.register_plugin('xep_0045')  # Groupchat
        xmpp.register_plugin('xep_0199')  # XMPP Ping
        xmpp['xep_0077'].force_registration = True
        xmpp.connect()
        xmpp.process(forever=False)

    elif option == '3':
        print ("Gracias por usar el sistema! ")
        break

    else:
        print('Opcion no valida')