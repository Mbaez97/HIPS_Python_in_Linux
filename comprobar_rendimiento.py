import delegator
import os
from modulos_necesarios import *
from funciones_proteccion import kill_command

#Procedemos a encontrar los procesos que superen el limite establecido de consumo ram y terminarlos
def analizar_proceso():
	porcentaje_limite = 80
	#Listamos los procesos que sobrepasen el limite de porcentaje de consumo ram
	cmd = """sudo ps aux | awk '{print $2, $4, $11}' | sort -k2r | awk '{if($2>"""+str(porcentaje_limite)+""") print($0)}'"""
	c = delegator.run(cmd)
	lista_proceso_ram = c.out.split('\n')
	#Traemos la lista de los procesos permitidos, teniendo en cuenta que pueden haber procesos normales que consuman mucha ram	
	cursor.execute("SELECT nombre_programa FROM lista_blanca")
	lista_proceso_permitido=cursor.fetchall()
	#Realizamos comparaciones para ver si es un proceso normal
	for command in lista_proceso_ram:
		if len(command) != 0:
			command_name = command.split()[2].split('/')[-1] #El nombre del proceso
			command_pid = command.split()[0]# pid
			blanca = 0
			for command_blanca in lista_proceso_permitido:
				if(command_name == command_blanca):
					blanca = 1 #Es un proceso seguro
					break
			if blanca == 0 : # No se encuentra en la lista blanca y consume alta ram
				#Registramos el log de alarma
				try:
					os.mkdir('/var/log/hids')
				except OSError as e:
					if e.errno != errno.EEXIST:
						raise
				# Crear o continuar archivo
				f = open("/var/log/hids/alarmas_hids.log","a")
				# Fecha y hora
				fecha = time.strftime("%d/%m/%y %X")
				# Mensaje a agregar
				mensaje = str(fecha) + ' :: ' + 'Detectado alto consumo de ram de proceso no registrado en lista blanca '+str(command_name)   + '\n'
				f.write(mensaje)
				f.close()
				# Enviar email
				enviar_correo(mensaje, 'Alarma HIPS')	
				#Matamos el proceso
				kill_command(command_pid)
				#Registramos el log de prevencion
				# Crear o continuar archivo
				f = open("/var/log/hids/prevencion_hids.log","a")
				# Fecha y hora
				fecha = time.strftime("%d/%m/%y %X")
				# Mensaje a agregar
				mensaje = str(fecha) + ' :: ' + 'Se ha matado proceso con alto consumo de cpu '+str(command_name)  + '\n'
				f.write(mensaje)
				f.close()
				# Enviar email
				enviar_correo(mensaje, 'PREVENCION HIPS')
analizar_proceso()  
																																																																													
