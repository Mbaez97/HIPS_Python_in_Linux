from modulos import *

def acces_logCMP():
	archivo = open('/var/log/httpd/access_log')
	ip_login = []
	ip_404 = []
	ip_tmp = []
	#Realizamos el recorrido por el archivo
	for columna in archivo[:-2]:
		columna_split = columna.split(' ')
		metodo_http = columna_split[5]
		#Extraemos el metodo HTTP
		if metodo_http == 'POST':  #Si tenemos el metodo http igual a POST, y analizamos los logins
			if 'login' in columna_split[6]:
				fecha = (columna_split[3].split(':'))[0]
				ip_login.append((fecha,columna_split[0]))
		else:#Al no ser un metodo POST, verificamos los intentos de GET
			if '404' in columna_split[8]:
				fecha = (columna_split[3].split(':'))[0]
				ip_404.append((fecha, columna_split[0]))
				#Verificamos si trato de realizar alguna accion en /tmp
				columna_tmp = columna.split('"',1)[1]
				if '/tmp/' in columna_tmp:
					ip_tmp.append((fecha, columna_split[0]))
					#si se intento modificar algo preparamos los mensajes para avisar las acciones que se realizaron ante el intruso
					fecha = time.strftime("%d/%m/%Y")
					hora = time.strftime("%H:%M:%S")
					entrada_tmp = fecha + '-->' + hora + '\n' + 'Ip bloqueada por intentar modificar algo en tmp' + '\n * ' + columna_split[0]
					hips_log = open('/var/log/hips/acces_hips.log', 'r+')
					if not entrada_tmp in hips_log.read().split(os.linesep):
						hips_log.write(entrada_tmp + '\n')
						#Recuparmos la contraseña del servidor de correos de gmail para enviar un correo al administrador del sistema en este caso
						#utilizamos mi correo
						os.system("openssl enc -aes-256-cbc -d -in /home/marcelojulianbaezferreira/contrasenhas_cifradas/contrasenha_correo.txt.enc -out contrasenha_correo.txt")
						contrasenha_correo = open("contrasenha_correo.txt")#Obtenemos nuestra contraseña cifrada del servidor de correos gmail
						imput = contrasenha_correo.read().replace('\n','')#La guardamos en la variable imput para su uso
						msg['Subject'] = "HIPS_alarma"
						msg.attach(MIMEText(entrada_tmp, 'plain')) #cargamos es el mensaje de aviso 
						alerta = smtplib.SMTP('smtpl.gmail.com: 587')#Iniciamos el servirdor SMTP en el puerto 587
						alerta.starttls()
						alerta.login(msg['From'], imput)
						alerta.sendmail(msg['From'], msg['To'], msg.as_string())
						alerta.quit()
						#Cerramos el archivo que contiene la contraseña del correo y eliminamos el archivo que contiene la contraseña cifrada
						contrasenha_correo.close()
						os.system("rm -rf contrasenha_correo.txt")
						#Enviamos un aviso a traves de la terminal
						os.system('echo "\nUna ip intento modificar algo en /tmp/ \n Revise el Correo del administrador"')

					hips_log.close()
					#bloqueamos a la ip sospechosa
					os.system('iptables -A -INPUT -s ' + columna_split[0] + ' -j DROP')
					ip_bloqueadas.append(columna_split[0])	
					#debemos bloquear nuestra ip desde la maquina remota

					#ver como hacer esta parte


					#
	contador_ip_404 = [[x, ip_404.count(x)] for x in set(ip_404)]
	contador_ip_login = [[x, ip_login.count(x)] for x in set(ip_login)]

	for temp in contador_ip_login:
		if temp[1] > N:#N es el numero maximo de login que establecimos en ell modulo modulos.py
			fecha = time.strftime("%d/%m/%Y")
			hora = time.strftime("%H:%M:%S")
			entrada_acceslog_http = fecha + '-->' + hora + '\n' + 'Ip bloqueada por superar el maximo numero de intentos de login' + '\n * ' + columna_split[0]
			hips_log = open('/var/log/hips/acces_hips.log', 'r+')	
			if not entrada_acceslog_http in hips_log.read().split(os.linesep):
				hips_log.write(entrada_acceslog_http + '\n')#guardamos en el archivo para enviar el informe
				#Recuparmos la contraseña del servidor de correos de gmail para enviar un correo al administrador del sistema en este caso
				#utilizamos mi correo
				os.system("openssl enc -aes-256-cbc -d -in /home/marcelojulianbaezferreira/contrasenhas_cifradas/contrasenha_correo.txt.enc -out contrasenha_correo.txt")
				contrasenha_correo = open("contrasenha_correo.txt")#Obtenemos nuestra contraseña cifrada del servidor de correos gmail
				imput = contrasenha_correo.read().replace('\n','')#La guardamos en la variable imput para su uso
				msg['Subject'] = "HIPS_alarma"
				msg.attach(MIMEText(entrada_acceslog_http, 'plain')) #cargamos es el mensaje de aviso 
				alerta = smtplib.SMTP('smtpl.gmail.com: 587')#Iniciamos el servirdor SMTP en el puerto 587
				alerta.starttls()
				alerta.login(msg['From'], imput)
				alerta.sendmail(msg['From'], msg['To'], msg.as_string())
				alerta.quit()
				#Cerramos el archivo que contiene la contraseña del correo y eliminamos el archivo que contiene la contraseña cifrada
				contrasenha_correo.close()
				os.system("rm -rf contrasenha_correo.txt")
				#Enviamos un aviso a traves de la terminal
				os.system('echo "\nUna ip supero el numero maximo de login \n Revise el Correo del administrador"')
			hips_log.close()
			#Bloqueamos el trafico de entrada de la ip
			os.system('iptables -A -INPUT -s' + temp[0][1] + ' -j DROP')
			ip_bloqueadas.append(temp[0][1])
			#debemos bloquear nuestra ip desde la maquina remota

			#ver como hacer esta parte
			#
	for temp in contador_ip_404:
		if temp[1] > N:
			fecha = time.strftime("%d/%m/%Y")
			hora = time.strftime("%H:%M:%S")
			entrada_acceslog_404 = fecha + '-->' + hora + '\n' + 'Ip bloqueada por superar el maximo numero de intentos de ingreso a paginas inexistentes' + '\n * ' + columna_split[0]
			hips_log = open('/var/log/hips/acces_hips.log', 'r+')	
			if not entrada_acceslog_404 in hips_log.read().split(os.linesep):
				hips_log.write(entrada_acceslog_404+ '\n')#guardamos en el archivo para enviar el informe
				#Recuparmos la contraseña del servidor de correos de gmail para enviar un correo al administrador del sistema en este caso
				#utilizamos mi correo
				os.system("openssl enc -aes-256-cbc -d -in /home/marcelojulianbaezferreira/contrasenhas_cifradas/contrasenha_correo.txt.enc -out contrasenha_correo.txt")
				contrasenha_correo = open("contrasenha_correo.txt")#Obtenemos nuestra contraseña cifrada del servidor de correos gmail
				imput = contrasenha_correo.read().replace('\n','')#La guardamos en la variable imput para su uso
				msg['Subject'] = "HIPS_alarma"
				msg.attach(MIMEText(entrada_acceslog_404, 'plain')) #cargamos es el mensaje de aviso 
				alerta = smtplib.SMTP('smtpl.gmail.com: 587')#Iniciamos el servirdor SMTP en el puerto 587
				alerta.starttls()
				alerta.login(msg['From'], imput)
				alerta.sendmail(msg['From'], msg['To'], msg.as_string())
				alerta.quit()
				#Cerramos el archivo que contiene la contraseña del correo y eliminamos el archivo que contiene la contraseña cifrada
				contrasenha_correo.close()
				os.system("rm -rf contrasenha_correo.txt")
				#Enviamos un aviso a traves de la terminal
				os.system('echo "\nUna ip supero el numero maximo de de intentos de ingreso a paginas inexistentes  \n Revise el Correo del administrador"')
			hips_log.close()
			#Bloqueamos el trafico de entrada de la ip
			os.system('iptables -A -INPUT -s' + temp[0][1] + ' -j DROP')
			ip_bloqueadas.append(temp[0][1])
			#debemos bloquear nuestra ip desde la maquina remota

			#ver como hacer esta parte
			#			



		pass
