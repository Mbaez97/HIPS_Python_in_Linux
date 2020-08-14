from modulos_necesarios import *
from enviar_mail import enviar_correo

def crontabCMP():
	#cargamos el archivo donde tenemos las tareas
	os.system("openssl enc -aes-256-cbc -d -in tareas.txt.enc -out tareas.txt")
	tareas = open('tareas.txt', 'r')
	lineas_tareas = tareas.readlines()

	#Llamamos al crontab con el parametro -l para ver la lista de cron y redireccionamos la salida a un archivo dentro de nuestro directorio
	os.system("crontab -l > tareas_cron.txt")
	tareas_cron = open('tareas_cron.txt', 'r')
	lineas_cron = tareas_cron.readlines()

	for aux1 in lineas_tareas:
		for aux2 in lineas_cron:
			if (aux1 != aux2):
				fecha = time.strftime("%d/%m/%Y")
				hora = time.strftime("%H:%M:%S")
				entrada_cron = fecha + '-->' + hora + '\n' + 'Se ha encontrado una tarea no programada de nombre' + aux2 + '\n'
				hips_log = open('/var/log/hips/hips_tmp_log.log', 'r+')
				if not entrada_cron in hips_log.read().split(os.linesep):
					hips_log.write(entrada_cron+'\n')
					enviar_correo(entrada_cron, 'Alarma HIPS')
					#Avisamos desde la terminal que se encontro algo sospechoso
					mensaje = 'echo "\n Se encontro una tarea no programada. Revisar el correo del administrador " '
					os.system(mensaje)
				hips_log.close()

	tareas.close()
	tareas_cron.close()
	os.system("rm -rf tareas.txt tareas_cron.txt")
		
	

crontabCMP()