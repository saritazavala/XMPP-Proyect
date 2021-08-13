# XMPP-Proyect
## Objetivos 

1. Apegarse a los estándares de un protocolo conocidoy abierto
2. Comprender las bases de programacion asaincrona requeridas para apegarse a las necesidades de desarrollo.

## Desarrollo
### **Características y limitaciones**
El proyecto consiste en implementar un cliente que soporte el protocolo XMPP. A partir de ello debe de soportar como mínimo las siguientes características:

### *Administración de cuenta (25% del funcionamiento)*

1. Registrar una nueva cuenta en el servidor
2. Iniciar sesión con una cuenta
3. Cerrar sesión con una cuenta
4. Eliminar la cuenta del servidor

### *Comunicación (75% del funcionamiento)*
1. Mostrar todos los usuarios/contactos y su estado
2. Agregar un usuario a los contactos-Mostrar detalles de contacto de un usuario
3. Comunicación 1 a 1 con cualquier usuario/contacto
4. Participar en conversaciones grupales
5. Definir mensaje de presencia
6. Enviar/recibir notificaciones
7. Enviar/recibir archivos

# Funcionamiento
Si se desea crear una cuenta, se debe seguir la siguiente estructura:
```
user@alumchat.xyz
```
De esa manera es como se almacena un usuario
## -----------------------------------------------------------------

Para las opciones de:
- Buscar un usuario y sus detalles
- Enviar mensaje directo
- Envio de mensaje

Siempre se debe ingresar el usuario como
```
user@alumchat.xyz
```
Para los mensajes grupales, se debe crear una sala, la cual se crea de esta manera: 
```
name@conference.alumchat.xyz' 
```
