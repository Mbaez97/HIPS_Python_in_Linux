from modulos_necesarios import *
from enviar_mail import enviar_correo

def log_secureCMP():
	#Extraemos las entradas con contraseñas fallidas
	failed_pass = os.popen('cat /var/log/secure | grep "Failed password"').read()
	failed_pass = failed_pass.split(os.linesep)
	contador_ip = []
	for fila_log in failed_pass[:-1]: #Recorremos el archivo
		if 'for invalid user' in fila_log: #si en algun sector de la fila encontramos la oracion "for invalid user" capturamos la ip 
			not_acces_ip = fila_log.split(' ')[12]#El valor 12 es el sector de la fila en el log donde se encuentra la ip en el caso que sea un usuario no valido
		else:
			not_acces_ip = fila_log.split(' ')[10]#Al no tener la caracteristica de "for invalid user" la ip se encuentra en el sector 10

		fecha = fila_log.split(' ')[0]	+ fila_log.split(' ')[1] #Guardamos el mes y el dia
		contador_ip.append((fecha, not_acces_ip))

	#Creamos una tupla de dos elementos que contendran la ip y el contador de accesos
	contador_ip_log = [[y, contador_ip.count(y)]] for y in set(contador_ip)
	for aux in contador_ip_log:
		if aux[1] > N: #El valor de N esta fijado en los modulos necesarios, establecimos como maximos intentos de login N = 5
			fecha = time.strftime("%d/%m/%Y")
			hora = time.strftime("%H:%M:%S")
			entrada_login_sys = fecha + '-->' + hora + '\n\n' + 'Ip bloqueada por superar el numero maximo de acceso a traves de ssh' + '\n *' + aux[0][1]
			hips_log = open('/var/log/hips/acces_hips.log', 'r+')
			if not entrada_login_sys in hips_log.read().split(os.linesep):
				hips_log.write(entrada_login_sys+'\n')
				enviar_correo(entrada_login_sys, 'Alarma HIPS')
				#Enviamos un aviso a traves de la terminal
				os.system('echo "\nUna ip supero los intentos de acceso \n Revise el Correo del administrador"') 
				bann_ip.append(aux[0][1])
				#Bloqueamos el trafico de la ip
				os.system('iptables -A INPUT -s ' + aux[0][1] + ' -j DROP')
				
			hips_log.close()

	#Proceso similar al anterios, explicado anteriormente
	cont_usr = []
	#Extraemos los accesos fallidos
	failed_login = os.popen('cat /var/log/secure | grep "FAILED LOGIN"').read()
	failed_login = failed_login.split(os.linesep)
	for fila_log in failed_login[:-1]:
		if not 'User not known to the underlying authentication module' in fila_log:
			#Identificamoe el usuario que no puede acceder
			usr_aux = fila_log.split(' ')[11]
			fecha = fila_log.split(' ')[0] + fila_log.split(' ')[1]
			cont_usr.append((fecha, usr_aux))

	contador_usr_log = [[y, cont_usr.count(y)]] for y in set(cont_usr)
	for aux in contador_usr_log:
		if aux[1] > N:
			#si no es root cambiamos la contraseña
			fecha = time.strftime("%d/%m/%Y")
			hora = time.strftime("%H:%M:%S")
			#Podemos implementar la funcion creada por SJ, 
			nuevo_passw = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
			os.system('echo "' + temp[0][1][:-1] +':'+ nuevo_passw + '" | chpasswd')
			entrada_notroot_log = fecha + ' ---> ' + hora + '\n\n' + 'Cambio de contrasenha por superar limite de intentos de acceso al sistema!' + '\n * ' + temp[0][1][:-1] + ' ---> ' + nuevo_passw + '\n\n'
			#Actualizamos la nueva contraseña generada en nuestra base de datos
			cursor.execute("UPDATE users set pass=%s where usr=%s;",(nuevo_passw,temp[0][1][:-1],))
			hips_log = open('/var/log/hips/acces_hips.log', 'r+')
			if not entrada_notroot_log in hips_log.read().split(os.linesep):
				hips_log.write(entrada_notroot_log+'\n')
				enviar_correo(entrada_notroot_log, 'Alarma HIPS')
				os.system('echo "\nUn usuario supero los intentos de acceso \n Revise el Correo del administrador\n" ')
				hips_log.close()
			else:
				#Si es root notificamos de igual manera al administrador 
				fecha = time.strftime("%d/%m/%Y")
				hora = time.strftime("%H:%M:%S")
				entrada_root_log = fecha + ' ---> ' + hora + '\n\n' + 'El usuario root supero los limites de intento de acceso al sistema' + '\n * ' + temp[0][1][:-1]
				hips_log = open('/var/log/hips/acces_hips.log', 'r+')
				if not entrada_root_log in hips_log.read().split(os.linesep):
					hips_log.write(entrada_root_log+'\n')
					enviar_correo(entrada_root_log, 'Alarma HIPS')
				hips_log.close()
				
log_secureCMP()			








