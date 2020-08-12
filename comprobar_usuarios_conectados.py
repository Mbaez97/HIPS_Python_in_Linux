from modulos_necesarios import *
from enviar_mail import enviar_correo
def comprobar_usuarios_conectados():

        #Extrae la lista de usuarios conectados actuales con su origen/direccion
        file=listar_usuario_conectado() # [[usuario1,dirrecion1],[usuario2,dirrecion2],.....]
         #Cantidad de filas de la tabla users
        cursor.execute("SELECT COUNT(*) FROM users")
        check = cursor.fetchone()
        nrows = check[0]
        #Se recorre linea por linea el archivo y se vuelve a quitar usuario y direccion
        for line in file:
                #extrae usuario y direccion de 1 elemento de la lista
               user = line[0]
               address=line[1]
                #Se recorre tabla users, revisando si coinciden los datos de los usuarios con los almacenados
                for y in range(0, nrows):
                        aviso = 1
                        c = y + 1
                        cursor.execute("SELECT * FROM users where id = %d " % c )
                        check= cursor.fetchone()
                        if(user == check[1] and address == check[2]): #check[2] es la ip permitida
                                aviso = 0
                #Si no coinciden los datos, se notifica
                if(aviso == 1):
                        mensaje = 'Usuario e IP no existen en la base de datos:\n' + user + '  [' + address + ']'
                        fecha = time.strftime("%d/%m/%Y")
                        hora = time.strftime("%H:%M:%S")
                        entrada = fecha + ' ---> ' + hora + '\n\n* ' + mensaje + '\n'
                        enviar_correo(entrada, 'Alarma HIPS')
                        #os.system("openssl enc -aes-256-cbc -d -in /home/marcelojulianbaezferreira/contrasenhas_cifradas/contrasenha_correo.txt.enc -out contrasenha_correo.txt")
                        #pass_file = open("contrasenha_correo.txt")
                        #input_pass_file = pass_file.read().replace('\n','')
                        #pass_file.close()
                        #os.system("rm -rf contrasenha_correo.txt")
                        #msg['Subject'] = "Alarma HIPS"
                        #msg.attach(MIMEText(entrada, 'plain'))
                        #server = smtplib.SMTP('smtp.gmail.com: 587')
                        #server.starttls()
                        #server.login(msg['From'], input_pass_file)
                        #server.sendmail(msg['From'], msg['To'], msg.as_string())
                        #server.quit()
                        archivo_cola = open('/var/spool/mqueue/mail_recibidos.txt','a')
                        archivo_cola.write(fecha + ' | ' + hora + ' | ' + 'From:' + msg['From'] + '\n')
                        archivo_cola.close()
                        archivo = open('/var/log/hids/alarmas_hids.log', 'a')
                        archivo.write(entrada)
                        archivo.close()

        file.close()

comprobar_ultimos_usuarios ()
def listar_usuario_conectado():
    cmd = "sudo who | awk '{print($1,$5)}' | sort | uniq | sed 's/(//g' | sed 's/)//g' | sed 's/:0//g'"
    c = delegator.run(cmd)
    lista = c.out.split('\n')
    lista_usuario_conectado=[]
    for elemento in lista:
        usuario_conectado = elemento.split()
        if len(usuario_conectado) == 1: # Trae solamente usuario, sin ubicacion, esta conectado desde local
            usuario_conectado.append('localhost')
        if len(usuario_conectado) != 0:
            lista_usuario_conectado.append(usuario_conectado)
    return lista_usuario_conectado   
