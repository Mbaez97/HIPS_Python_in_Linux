from modulos_necesarios import *
from enviar_mail import enviar_correo
def binariosCMP(dir_binarios):
	#Creamos una lista donde almacenaremos las rutas de los archivos binarios
	list_dir = []

	for direccion in dir_binarios:
		#Se analiza si la ruta puesta es un archivo o una carpeta
		if os.path.isdir(direccion):
			list_temp = os.listdir(direccion)
			for elemento in list_temp:
				list_dir.append(direccion + '/' + elemento)
		else:#si no, prepara un a lista donde guardamos la direccion absoluta del unico archivo
				list_dir = [direccion]
		#Se recorre el vector y se obtiene ela firma md5 de cada archivo y comparamos con la base de datos
		for ruta in list_dir:
				cmd = 'sudo md5sum ' + str(ruta)
				sum_md5=delegator.run(cmd).out.split()[0]
				#temp = hashlib.md5((open(ruta)).read())
				#md5sum = str(temp.hexdigest())
				cursor.execute("SELECT directorio FROM binarios_sistema WHERE directorio = %s", (sum_md5))
				#Comprobamos si el archivo existe en la base de datos
				existe = cursor.fetchclone()
				if isinstance(existe, tuple):
					cursor.execute("SELECT md5sum FROM binarios_sistema WHERE directorio = %s", (ruta))
					check_md5 = cursor.fetchclone()[0]
					#A continuacion verificamos si el archivo de la base de datos y el archivo que estamos analizando tengan la misma firma md5
					if check_md5 != md5sum:
						fecha = time.strftime("%d/%m/%Y")
						hora = time.strftime("%H:%M:%S")
						entrada_binarios = fecha + '-->' + hora + '\n\n' + 'Archivo modificado: ' + '\n * ' + ruta
						hips_log = open('/var/log/hips/acces_hips.log', 'r+')
						if not entrada_binarios in hips_log.read().split(os.linesep):
							hips_log.write(entrada_binarios + '\n')
							enviar_correo(entrada_binarios, 'Alarma HIPS')
							mensaje_md5 = 'echo "\n El archivo ' + ruta + ' fue modificado, Revisar el correo del administrador"'
							os.system(mensaje_md5)
						hips_log.close()
				else:#Si el archivo no existe en la base de datos, generamos la alarma
					fecha = time.strftime("%d/%m/%Y")
					hora = time.strftime("%H:%M:%S")
					entrada_binarios = fecha + '-->' + hora + '\n\n' + 'El archivo no se encuentra en la  base de datos ' + '\n * ' + ruta
					hips_log = open('/var/log/hips/acces_hips.log', 'r+')
					if not entrada_binarios in hips_log.read().split(os.linesep):
						enviar_correo(entrada_binarios, 'Alarma HIPS')
						mensaje_md5 = 'echo "\n El archivo ' + ruta + ' no existe en la base de datos, Revisar el correo del administrador"'
						os.system(mensaje_md5)
					hips_log.close()
	pass

#binariosCMP()