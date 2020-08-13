from enviar_mail import enviar_correo
from modulos_necesarios import *
from funciones_proteccion import mover_cuarentena, kill_command_name

#Detectamos si se entro en modo promiscuo analizando el archivo var/log/messages
def detectar_promiscuo_messages():
	cmd = "sudo cat /var/log/messages | grep 'entered promiscuous mode' | awk '{print $7}' | sort | uniq"
	c = delegator.run(cmd)
	lista_device = c.out.split()
	#Se detecta dispositivo en modo promiscuo
    for device in lista_device:
		#Se registra el log de alarma y se envia al mail al detectar que se ha entrado en modo promiscuo
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
	    mensaje = str(fecha) + ' :: ' +'Se ha detectado dispositivo '+ str(device) + ' ha entrado en modo promiscuo ' +  '\n'
	    f.write(mensaje)
	    f.close()
	    # Enviar email
	    enviar_correo(mensaje, 'Alarma HIPS')
	detectar_promiscuo_messages()	    

#Comparamos con la lista de aplicaciones sniffers conocidas de la base de datos
def detectar_aplicacion_sniffers():
	cursor.execute("SELECT sniffer FROM lista_sniffers")
	lista_aplicacion=cursor.fetchall()
    for aplicacion in lista_aplicacion:	
        if len(aplicacion) != 0 :
            # Busco si existe un proceso en ejecucion con dicho nombre
            cmd = "sudo ls -l /proc/*/exe 2>/dev/null | awk '{print($11)}' | grep " + str(aplicacion[0])
            c = delegator.run(cmd)
            lista_proceso = c.out.split()
            for proceso in lista_proceso:
            	#Se registra el log de alarma y se envia al mail al detectar que se ha entrado en modo promiscuo
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
			    mensaje = str(fecha) + ' :: ' +'Se ha detectado aplicacion de captura de paquetes en ejecucion '+ str(proceso) +  '\n'
			    f.write(mensaje)
			    f.close()
			    # Enviar email
			    enviar_correo(mensaje, 'Alarma HIPS')  
			    #Procedemos a matar el proceso          	
                	    kill_command_name(proceso)
    			    #Registramos la eliminacion del proceso en el log de prevencion y enviamos al mail
			    f = open("/var/log/hids/prevencion_hids.log","a")
			    # Fecha y hora
			    fecha = time.strftime("%d/%m/%y %X")
			    # Mensaje a agregar
			    mensaje = str(fecha) + ' :: ' + 'Se ha emitido una orden para terminar aplicacion de captura de paquetes ' +str(proceso)  + '\n'
			    f.write(mensaje)
			    f.close()
			    # Enviar email
			    enviar_correo(mensaje, 'PREVENCION HIPS')   			   
			    # Movemos a cuarentena
			    mover_cuarentena(proceso)
			    #Registramos la cuarentena en el log de prevencion
			    f = open("/var/log/hids/prevencion_hids.log","a")
			    # Fecha y hora
			    fecha = time.strftime("%d/%m/%y %X")
			    # Mensaje a agregar
			    mensaje = str(fecha) + ' :: ' + 'Se ha puesto a cuarenta aplicacion de captura de paquetes ' +str(proceso)  + '\n'
			    f.write(mensaje)
			    f.close()
			    # Enviar email
			    enviar_correo(mensaje, 'PREVENCION HIPS')
detectar_aplicacion_sniffers()
 
#Detectamos si se entro en modo promiscuo viendo los registros de auditorias
def detectar_promiscuo_aud():
    cmd = "sudo aureport --anomaly --input-logs | grep ANOM_PROMISCUOUS | awk '{print $5}' | grep -v '?' | sort | uniq"
    c = delegator.run(cmd)
    lista_command = c.out.split()
    for command in lista_command: # Se detecta dispositivo en modo promiscuo y proceso causante
    	#Registramos la alarma en el log de alarma
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
	    mensaje = str(fecha) + ' :: ' +'Se ha detectado modo promiscuo causado por proceso' + str(command) +  '\n'
	    f.write(mensaje)
	    f.close()
	    # Enviar email
	    enviar_correo(mensaje, 'Alarma HIPS')
            # Se cierra el proceso causante
            kill_command_name(command)
	    #Registramos la eliminacion del proceso en el log de prevencion y enviamos al mail
	    f = open("/var/log/hids/prevencion_hids.log","a")
	    # Fecha y hora
	    fecha = time.strftime("%d/%m/%y %X")
	    # Mensaje a agregar
	    mensaje = str(fecha) + ' :: ' + 'Se ha emitido la orden para terminar proceso que origino modo promiscuo ' +str(command)  + '\n'
	    f.write(mensaje)
	    f.close()
	    # Enviar email
	    enviar_correo(mensaje, 'PREVENCION HIPS')
            # Se mueve a cuarentena proceso causante
            mover_cuarentena(command)
            #Registramos la cuarentena en el log de prevencion y enviamos al mail
	    f = open("/var/log/hids/prevencion_hids.log","a")
	    # Fecha y hora
	    fecha = time.strftime("%d/%m/%y %X")
	    # Mensaje a agregar
	    mensaje = str(fecha) + ' :: ' + 'Se ha puesto a cuarenta command que origino modo promiscuo ' +str(command)  + '\n'
	    f.write(mensaje)
	    f.close()	
detectar_promiscuo_aud()
