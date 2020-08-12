import random
import string
import delegator
from enviar_mail import enviar_correo

#Funciones en caso de violacion al bitacora del sistema

# Obtener el nombre del usuario teniendo su uid
def obtener_nombre_uid(uid):
    cmd = "getent passwd "+str(uid)+" | cut -d : -f 1"
    c = delegator.run(cmd)
    return c.out

# Bloquear un usuario por usermod
def bloquear_usuario(usuario_a_bloquear):
    if usuario_a_bloquear != "root": # No se permite bloquear al usuario root              
        cmd="sudo usermod -L " + str(usuario_a_bloquear)
        delegator.run(cmd)

# Generar cadena aleatoria    
def palabra_aleatoria(stringLength=20):
    """Genera un cadena aleatoria dado una longitud """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# Cambiar contrasena de usuario por una aleatoria y enviar por correo
def cambiar_contrasena(nombre_usuario):
    contrasena_aleatoria = palabra_aleatoria()
    cmd = 'sudo usermod -p `perl -e "print crypt("'+contrasena_aleatoria+'","Q4")"` '+nombre_usuario
    delegator.run(cmd)
    mensaje = 'Usuario= ' + nombre_usuario + ' Contrasena= ' + contrasena_aleatoria
    enviar_correo(mensaje, 'Alarma HIPS . Cambio de contrasena aleatoria a usuario')

# Cierra la sesion de un usuario
def cerrar_sesion(nombre_usuario):
    cmd = "pkill -KILL -u " + str(nombre_usuario)
    delegator.run(cmd)