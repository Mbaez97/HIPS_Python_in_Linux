from modulos_necesarios import maxColaMail
from enviar_mail import enviar_correo

def comprueba_cola_correo():

        #ABRIMOS EL ARCHIVO DE CORREOS RECIBIDOS.
        archivo_cola = open('/var/spool/mqueue/mail_recibidos.txt','r')
        lineas = archivo_cola.readlines()
        cantidad = len(lineas)

        if((cantidad) > maxColaMail):
                cantidad = str(cantidad)
                mensaje ='La cola de correos supera la cantidad maxima establecida. Hay en cola ' + cantidad + ' mensajes!'
                fecha = time.strftime("%d/%m/%Y")
                hora = time.strftime("%H:%M:%S")
                entrada = fecha + ' ---> ' + hora + '\n * ' + mensaje + '\n\n'
                enviar_correo(entrada,'Alarma HIPS')
                archivo_cola = open('/var/spool/mqueue/mail_recibidos.txt','a')
                archivo_cola.write(fecha + ' | ' + hora + ' | ' + 'From:' + msg['From'] + '\n')
                archivo_cola.close()
                archivo = open('/var/log/hids/alarmas_hids.log', 'a')
                archivo.write(entrada)
                archivo.close()
                mensaje_pass = 'echo "\nCola de correo llena! Revisar correo para mas info.\n" '
                os.system(mensaje_pass)
