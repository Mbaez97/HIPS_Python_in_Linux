# import necessary packages
from modulos_necesarios import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Enviar un correo
def enviar_correo(msg_a_enviar,subject):
    try:
        # create message object instance
        msg = MIMEMultipart()
        message = msg_a_enviar
        # setup the parameters of the message
        msg['From'] = "hips.baez.oh.2020@gmail.com"#Correo creado unicamente para este trabajo
        msg['To'] = "marcelobaezparaguay@gmail.com"#En este campo estaria el correo del administrador que utilice el HIPS
        msg['Subject'] = subject
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        # create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        os.system("openssl enc -a-256-cbc -d -in /home/marcelojulianbaezferreira/contrasenhas_cifradas/contrasenha_correo.txt.enc -out contrasenha_correo.txt")
        contrasenhaMail = open("contrasenhaMail.txt")
		pwd = contrasenhaMail.read().replace('\n', '')
		contrasenhaMail.close()
        server.login(msg['From'], pwd)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
    except:
        pass