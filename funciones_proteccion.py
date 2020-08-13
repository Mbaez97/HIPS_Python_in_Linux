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

# Mover a cuarenta un archivo
def mover_cuarentena(path_archivo):
    # Quita todos los permisos
    cmd = "sudo chmod a-wxr " + str(path_archivo)
    delegator.run(cmd)
    # Crea el directorio de cuarentena
    cmd = "sudo mkdir /tmp/.cuarentena"
    delegator.run(cmd)
    # Mueve al directorio de cuarentena
    cmd = "sudo mv "+str(path_archivo) +" /tmp/.cuarentena"
    delegator.run(cmd)

# Kill proceso por pid
def kill_command(pid):
    cmd="sudo kill -9 " + str(pid)
    delegator.run(cmd)
    
# Kill proceso por name
def kill_command_name(command):
    cmd = "sudo pidof " + command
    c = delegator.run(cmd)
    pid = c.out
    kill_command(pid)    
