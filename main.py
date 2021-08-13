from logging import log
from os import close
from slixmpp import jid
from getpass import getpass
from client import *
from muc import *
from ssl import OP_NO_RENEGOTIATION

def online_user(event):
    xmpp.start()
    print("Bienvenido al chat! :", xmpp.boundjid.bare)

    while True:
        print(" ----------------- Menu ------------------------- ")
        print(" 1. Ver usuarios ")
        print(" 2. Agregar usuario a contactos ")
        print(" 3. Mostrar detalles de un contacto ")
        print(" 4. Mandar mensaje privado ")
        print(" 5. Madar mensaje grupal")
        print(" 6. Definir mensaje de presencia " )
        print(" 7. Enviar/recibir archivos " )
        print(" 8. Cerrar Sesion " )
        print(" 9. Eliminiar cuenta")

        opt = input("Ingrese la opcion deseada: ")

        if opt == "1":
            get_my_roster = GetRoster(xmpp.jid, xmpp.password)
            get_my_roster.connect()
            get_my_roster.process(forever=False)

        elif opt == "2":
            print(' Aniadir nuevo contacto ')
            contact_jid = input('Enter JID:')
            if '@' in contact_jid:
                xmpp.add_friend(contact_jid)
                print("You have a new friend")
            else:
                print('Bad input')
        
        

        elif opt == "3":
            uname = input("Enter username u want to find")
            if '@' in uname:
                get_my_roster = GetRoster(xmpp.jid, xmpp.password,uname)
                get_my_roster.connect()
                get_my_roster.process(forever=False)
            else:
                print("Bad Input")




        elif opt == "4":
            uname = input('Enter JID from the user:')
            if '@alumchat.xyz' in uname:
                to_send = input('Message you want to send:')
                if to_send:
                    my_priv = PrivMsg(xmpp.jid, xmpp.password, uname, to_send)
                    my_priv.connect()
                    my_priv.process(forever=False)
                else:
                    print('Any message')
            else:
                print('Bad input')
        
    
        
        
        elif option == '5':
            print(" Grupos")
            print(" 1. Crear Grupo")
            print(" 2. Unirse a grupo ")
            print(" 3. Mensaje General")
            print(" 4. Salir del grupo")
            print(" 5. Regresar")
            option_message = input('Ingrese su opcion: ')

       
            if option_message == '1':
                print("Creando Grupo")
                name = input('Group URL: ')
                nick = input('Nickname: ')
                if nick and name and '@conference.' in name:
                    group_create = create_group(xmpp.jid, xmpp.password, name, nick)
                    group_create.connect()
                    group_create.process(forever=False)
                else:
                    ('Input invalido')
                    continue
            
       
            elif option_message == '2':
                print(" Unirse a grupo ")
                name = input('Room URL: ')
                nick = input('Nick: ')
                if nick and name and '@conference.' in name:
                    group_join = join_group(xmpp.jid, xmpp.password, name, nick)
                    group_join.connect()
                    group_join.process(forever=False)
                else:
                    print('Input invalido')
                    continue
            
           
            elif option_message == '3':
                print(" Mandar mensaje a un grupo ")
                name = input('Room URL: ')
                msg = input('Mensaje: ')
                if msg and name and '@conference.' in name:
                    group_send = SendMsg_group(xmpp.jid, xmpp.password, name, msg)
                    group_send.connect()
                    group_send.process(forever=False)
                else:
                    print('Input invalido')
                    continue
            
        
            elif option_message == '4':
                print(" Salir del grupo ")
                name = input('Room URL: ')
                nick = input('Nick: ')
                if nick and name and '@conference.' in name:
                    group_exit = leave_group(xmpp.jid, xmpp.password, name, nick)
                    group_exit.connect()
                    group_exit.process(forever=False)
                else:
                    print("Input invalido")
                    continue
            elif option_message == '5':
                pass
            else:
                print('Input invalido')



# --------------------------------------------------------------

        elif opt == "6":
            estados = ["En linea", "AFK", "Ocupado", "Restringido"]
            print("Choose the state u want")
            i = 1
            for opt in estados:
                print(str(i)+'. '+opt)
                i += 1
            show_input = input('Show option: ')
            status = input('New Status ')
            try:
                show = estados[int(show_input)-1]
            except:
                print('Bad input')
                show = 'available'
            xmpp.set_presence(show, status)
            print("Estado Cambiado")


        elif opt == "7":
            uname = input('To: ')
            file = input('File Name: ')
            if file and uname and '@' in uname:
                send_file = SendFile(xmpp.jid, xmpp.password, uname, file, xmpp.boundjid.domain)
                send_file.connect()
                send_file.process(forever=False)

        
        elif opt == "8":
            xmpp.disconnect()
            print(" Se ha cerrado sesion de -->" , xmpp.boundjid.bare)
            break

        elif opt == "9":
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
        xmpp = Client( jid= username, password = user_password )
        xmpp.add_event_handler('session_start', online_user)
        xmpp.connect()
        xmpp.process(forever=False)
        
    elif option == '2':
        print(" -------------------------------------------------- ")
        print(" ----------------- Nuevo Usuario  ----------------- ")
        print(" -------------------------------------------------- ")

        username = input("Ingrese su nombre  de usuario: ")
        user_password = getpass(" Ingrese su contrasenia: ")

        xmpp = register_to_server(jid=username, password=user_password)
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