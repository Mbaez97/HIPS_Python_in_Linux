from modulos_necesario import *
from enviar_mail import enviar_correo
def archivos_tmpCMP():
	for dir_path,_,nm_archivo in os.walk('/tmp'):
		#Si encontramos algun archivo ejecutable dentro del directorio generamos la alarma al administrador 
		#Y colocamos en cuarentena el ejecutable
		for aux in nm_archivo:
			if (('.py' in aux) or ('.exe' in aux) or ('sh' in aux) or ('.deb' in aux) or ('.rpm' in aux)):
				fecha = time.strftime("%d/%m/%Y")
				hora = time.strftime("%H:%M:%S")
				entrada_tmp = fecha + '-->' + hora + '\n' + 'Se a detectado un archivo ejecutable, se a puesto en cuarentena!' + '\n * ' + aux + '\n'
				hips_log = open('/var/log/hips/hips_tmp_log.log', 'r+')
				if not entrada_tmp in hips_log.read().split(os.linesep):
					#Cambiamos los permisos del archivo y lo colocamos en solo lectura
					os.system('chmod 400 ' + '/tmp/' + aux)
					print("Se a cambiado los permisos del archivo peligroso")
					#Enviamos a cuarentena a la carpeta oculta
					os.system('mv ' + '/tmp/' + aux + ' /home/.cuarentena')

					print("El archivo fue puesto en cuarentena")
					#guardamos el log y enviamos el correo correspondiente al administrador

					hips_log.write(entrada_tmp+'\n')
					enviar_correo(entrada_tmp, 'Alarma hips')

					#avisamos en la terminal que existe un ejecutable sospechoso en /tmp
					os.system('echo "Ejecutable detectado, Revisar el correo del administrador"')

					#establecer un mensaje a la segunda maquina
				hips_log.close()
	#Aplicamos el mismo proceso para el directorio /var/tmp
	for dir_path,_,nm_archivo in os.walk('/var/tmp'):
		#Si encontramos algun archivo ejecutable dentro del directorio generamos la alarma al administrador 
		#Y colocamos en cuarentena el ejecutable
		for aux in nm_archivo:
			if (('.py' in aux) or ('.exe' in aux) or ('sh' in aux) or ('.deb' in aux) or ('.rpm' in aux)):
				fecha = time.strftime("%d/%m/%Y")
				hora = time.strftime("%H:%M:%S")
				entrada_tmp = fecha + '-->' + hora + '\n' + 'Se a detectado un archivo ejecutable, se a puesto en cuarentena!' + '\n * ' + aux + '\n'
				hips_log = open('/var/log/hips/hips_tmp_log.log', 'r+')
				if not entrada_tmp in hips_log.read().split(os.linesep):
					#Cambiamos los permisos del archivo y lo colocamos en solo lectura
					os.system('chmod 400 ' + '/tmp/' + aux)
					print("Se a cambiado los permisos del archivo peligroso")
					#Enviamos a cuarentena a la carpeta oculta
					os.system('mv ' + '/tmp/' + aux + ' /home/.cuarentena')

					print("El archivo fue puesto en cuarentena")
					#guardamos el log y enviamos el correo correspondiente al administrador

					hips_log.write(entrada_tmp+'\n')
					enviar_correo(entrada_tmp, 'Alarma hips')

					#avisamos en la terminal que existe un ejecutable sospechoso en /tmp
					os.system('echo "Ejecutable detectado, Revisar el correo del administrador"')

					#establecer un mensaje a la segunda maquina
				hips_log.close()


