from modulos_necesarios import maxColaMail

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
                os.system("openssl enc -aes-256-cbc -d -in pass_file.txt.enc -out pass_file.txt -k PASS")
                pass_file = open("pass_file.txt")
                input_pass_file = pass_file.read().replace('\n','')
                pass_file.close()
                os.system("rm -rf pass_file.txt")
                msg['Subject'] = "ALARMA EN HIDS!"
                msg.attach(MIMEText(mensaje, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com: 587')
                server.starttls()
                server.login(msg['From'], input_pass_file)
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.quit()
                archivo_cola = open('/var/spool/mqueue/mail_recibidos.txt','a')
                archivo_cola.write(fecha + ' | ' + hora + ' | ' + 'From:' + msg['From'] + '\n')
                archivo_cola.close()
                archivo = open('/var/log/hids/alarmas_hids.log', 'a')
                archivo.write(entrada)
                archivo.close()
                mensaje_pass = 'echo "\nCola de correo llena! Revisar correo para mas info.\n" '
                os.system(mensaje_pass)
