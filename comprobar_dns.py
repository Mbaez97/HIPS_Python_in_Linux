from modulos_necesarios import *
from funciones_proteccion import bloquear_ip

# Retorna las ips que sobrepasan la cantidad limite de operaciones dns por minuto
def tcp_dump_dns():
	parametro_limite = 30
	cmd = """sudo cat /var/log/tcpdump_log |  awk '{print($1,$3)}' | sed 's/\:/ /g' | awk '{print($1,$2,$4)}' | sed 's/\./ /g' | awk '{print($1,$2,$3,$4,$5,$6)}' | sort | uniq -c | awk '{if($1>"""+str(parametro_limite)+""") print($4,$5,$6,$7)}' | sed 's/\ /./g'"""
	c = delegator.run(cmd)
	return c.out.split('\n')

# Bloquear ips atacantes a dns, sobrepasan el limite de operaciones dns por minuto
def analisis_ddos_dns():
	lista = tcp_dump_dns()
	cantidad_atacante = 0
	for elemento in lista:
		if len(elemento) != 0:
			cantidad_atacante = cantidad_atacante + 1
			#Registramos en el log de alarma
			try:
				os.mkdir('/var/log/hids')
			except OSError as e:
				if e.errno != errno.EEXIST:
					raise
			# Crear o continuar archivo
			f = open("/var/log/hids/prevencion_hids.log","a")
			# Fecha y hora
			fecha = time.strftime("%d/%m/%y %X")
			# Mensaje a agregar
			mensaje = str(fecha) + ' :: ' + 'Se ha detectado ip que ha sobrepasado limite de operaciones dns' + ' :: ' + elemento + '\n'
			f.write(mensaje)
			f.close()
			# Enviar email
			enviar_correo(mensaje, 'PREVENCION HIPS')
			# Se bloquea la ip del posible atacante
			bloquear_ip(elemento)
			#Se Registra en el log de prevencion
			# Crear o continuar archivo
			f = open("/var/log/hids/alarmas_hids.log","a")
			# Fecha y hora
			fecha = time.strftime("%d/%m/%y %X")
			# Mensaje a agregar
			mensaje = str(fecha) + ' :: ' + 'Se ha bloqueado ip por sobrepasar limite de operaciones dns' + ' :: ' + elemento + '\n'
			f.write(mensaje)
			f.close()
			# Enviar email
			enviar_correo(mensaje, 'Alarma HIPS')
	if cantidad_atacante > 1:
		# Crear o continuar archivo
		f = open("/var/log/hids/prevencion_hids.log","a")
		# Fecha y hora
		fecha = time.strftime("%d/%m/%y %X")
		# Mensaje a agregar
		mensaje = str(fecha) + ' :: ' + 'Posible ataque DDOS detectado al servicio de DNS'  + '\n'
		f.write(mensaje)
		f.close()
		# Enviar email
		enviar_correo(mensaje, 'PREVENCION HIPS')

analisis_ddos_dns()
