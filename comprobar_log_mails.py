import delegator
from enviar_mail import enviar_correo
from funciones_proteccion import cambiar_contrasena
from modulos_necesarios import maxColaMail, maxMailDia
# Verificar el registro de mail /var/log/maillog, trae los correos que superan el limite establecido por dia y toma medidas de prevencion
def verificar_registro_mail_x_correo():
    limite_mail_dia = maxMailDia
    cmd = """sudo grep -P ' from=<\K[^>]*' /var/log/maillog | grep "@" | awk '{print($1,$2,$7)}' | sort | uniq -c | awk '{if($1>"""+str(limite_mail_dia)+""") print($4)}' | grep -Po 'from=<\K[^>]*'"""
    c = delegator.run(cmd)
    lista_mail = c.out.split()
    # Por cada cuenta que supero el limite de envios de mails establecido por dia
    for mail in lista_mail:
        cuenta = mail.split('@')[0] #mail=juan@gmail.com, separa juan y gmail.com, y juan esta en la posicion 0
        if len(cuenta) != 0:
            # Se notifica la alarma que una cuenta supero el limite de emails por dia
            try:
                os.mkdir('/var/log/hids')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            tipo_alarma= 'Una cuenta ha superado la cantidad establecida de mails por dia ' + ' :: ' +str(cuenta)
            # Crear o continuar archivo
            f = open("/var/log/hids/alarmas_hids.log","a")
            # Fecha y hora
            fecha = time.strftime("%d/%m/%y %X")
            # Mensaje a agregar
            mensaje = str(fecha) + ' :: ' + str(tipo_alarma) + '\n'
            f.write(mensaje)
            f.close()
            #Envia el mail
            enviar_correo(mensaje,'Alarma HIPS')

            # Se activa el sistema de prevencion y lo registra
            # Crear directorio
            try:
                os.mkdir('/var/log/hids')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            tipo_prevencion=  'Se cambiara contraseña de usuario por haber superado el limite de mails por dia '+' :: ' +str(cuenta)
            # Crear o continuar archivo
            f = open("/var/log/hids/prevencion_hids.log","a")
            # Fecha y hora
            fecha = time.strftime("%d/%m/%y %X")
            # Mensaje a agregar
            mensaje = str(fecha) + ' :: ' + str(tipo_prevencion) + '\n'
            f.write(mensaje)
            f.close()
            # Enviar email
            enviar_correo(mensaje, 'PREVENCION HIPS')
            #Se cambia la contraseña del usuario del linux, y la nueva contraseña es enviada al correo electronico
            cambiar_contrasena(cuenta)
            
            # Se limpia la cola de mails de dicho usuario y se registra en el sistema de prevencion
            tipo_prevencion=  'Se elimino la cola de mails de usuario por superar la cantidad establecida de mails por dia '+' :: ' +str(cuenta)
            # Crear o continuar archivo
            f = open("/var/log/hids/prevencion_hids.log","a")
            # Fecha y hora
            fecha = time.strftime("%d/%m/%y %X")
            # Mensaje a agregar
            mensaje = str(fecha) + ' :: ' + str(tipo_prevencion) + '\n'
            f.write(mensaje)
            f.close()
            eliminar_mail_cola(cuenta)         

# Verificar la cola de mail
def verificiar_cola_de_mail_x_correo():
    limite_mail_cola = maxColaMail
    cmd = """sudo grep postqueue -p | awk '{print($7)}' | grep "@" | sort | uniq -c | awk '{if($1>"""+str(limite_mail_cola)+""") print($2)}'"""
    c = delegator.run(cmd)
    lista_mail = c.out.split('\n')
    # Por cada usuario que supera el limite de mails en cola de mail
    for mail in lista_mail:
        cuenta = mail.split('@')[0]
        if len(cuenta) != 0:
            # Se notifica la alarma que una cuenta supero el limite de emails en cola
            try:
                os.mkdir('/var/log/hids')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            tipo_alarma= 'Una cuenta ha superado la cantidad establecida de mails en cola '+ '::' + str(cuenta)
            # Crear o continuar archivo
            f = open("/var/log/hids/alarmas_hids.log","a")
            # Fecha y hora
            fecha = time.strftime("%d/%m/%y %X")
            # Mensaje a agregar
            mensaje = str(fecha) + ' :: ' + str(tipo_alarma) + '\n'
            f.write(mensaje)
            f.close()
            #Envia el mail
            enviar_correo(mensaje,'Alarma HIPS')

            #Se activa el sistema de prevencion y se registra
             # Crear directorio
            try:
                os.mkdir('/var/log/hids')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            tipo_prevencion=  'Se cambiara contrasena de usuario por haber superado el limite de mails en cola '+' :: ' +str(cuenta)
            # Crear o continuar archivo
            f = open("/var/log/hids/prevencion_hids.log","a")
            # Fecha y hora
            fecha = time.strftime("%d/%m/%y %X")
            # Mensaje a agregar
            mensaje = str(fecha) + ' :: ' + str(tipo_prevencion) + '\n'
            f.write(mensaje)
            f.close()
            # Enviar email
            enviar_correo(mensaje, 'PREVENCION HIPS')           
            # Se procede a cambiar la contrasena de la cuenta y enviarlo por correo
            cambiar_contrasena(cuenta)
            
            # Se limpia la cola de mails de dicho usuario
            tipo_prevencion=  'Se elimino la cola de mails de usuario por superar la cantidad establecida de mails en cola '+' :: ' +str(cuenta)
            # Crear o continuar archivo
            f = open("/var/log/hids/prevencion_hids.log","a")
            # Fecha y hora
            fecha = time.strftime("%d/%m/%y %X")
            # Mensaje a agregar
            mensaje = str(fecha) + ' :: ' + str(tipo_prevencion) + '\n'
            f.write(mensaje)
            f.close()           
            eliminar_mail_cola(cuenta)           
            
# Borrar todos los mails en cola de un correo emisor
def eliminar_mail_cola(cuenta_correo):
    cmd = """sudo postqueue -p |grep -v "^ " |grep """+cuenta_correo+""" | awk ' { print $1}' | tr -d '*!' | postsuper -d -"""
    delegator.run(cmd)
    
# Analisis general de envio de mails y toma de medidas
def analisis_envio_mail():
    verificar_registro_mail_x_correo()
    verificiar_cola_de_mail_x_correo()
    