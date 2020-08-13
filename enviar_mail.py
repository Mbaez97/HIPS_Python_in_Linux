# import necessary packages
from modulos_necesarios import *
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
#import smtplip
# Enviar un correo
def enviar_correo(msg_a_enviar,subject):
    try:
        # create message object instance
        #msg = MIMEMultipart()
        message = msg_a_enviar
        # setup the parameters of the message
        #msg['From'] = "hips.baez.oh.2020@gmail.com"#Correo creado unicamente para este trabajo
        #msg['To'] = "marcelobaezparaguay@gmail.com"#En este campo estaria el correo del administrador que utilice el HIPS
        #Recuparmos la contraseña del servidor de correos de gmail para enviar un correo al administrador del sistema en este caso
        #utilizamos mi correo
        os.system("openssl enc -aes-256-cbc -d -in /home/marcelojulianbaezferreira/contrasenhas_cifradas/contrasenha_correo.txt.enc -out contrasenha_correo.txt")
        contrasenha_correo = open("contrasenha_correo.txt")#Obtenemos nuestra contraseña cifrada del servidor de correos gmail
        imput = contrasenha_correo.read().replace('\n','')#La guardamos en la variable imput para su uso
                        
        mensj['Subject'] = subject
        mensj.attach(MIMEText(message, 'plain')) #cargamos es el mensaje de aviso 
        alerta = smtplib.SMTP('smtpl.gmail.com: 587')#Iniciamos el servirdor SMTP en el puerto 587
        alerta.starttls()
        alerta.login(msg['From'], imput)
        alerta.sendmail(msg['From'], msg['To'], msg.as_string())
        alerta.quit()
        #Cerramos el archivo que contiene la contraseña del correo y eliminamos el archivo que contiene la contraseña cifrada
        contrasenha_correo.close()
        os.system("rm -rf contrasenha_correo.txt")
    except:
        pass
