#!/usr/bin/python
#Modulo para conexion a la base de datos PostGreSQL
import psycopg2
#import sys
import re
import os
import string
import datetime
#Modulo que nos permite comunicarnos con los servidores de correo para enviar correos
import smtplib
#import socket
#Modulo con el que podemos crear las tuplas necesarias para procesar los datos o guardarlos
import collections
import hashlib
from os import listdir
import pwd
import random
import time
#import commands
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
N = 6 # MAximo intentos de login
#Establecemos algunos valores que usaremos a lo largo de los distintos modulos del hips
maxColaMail = 120 #Maxima cola de correos

#Valores globales para el uso de correo
mensj = MIMEMultipart()
mensj['From'] = "hips.baez.oh.2020@gmail.com"#Correo creado unicamente para este trabajo
mensj['To'] = "marcelobaezparaguay@gmail.com"#En este campo estaria el correo del administrador que utilice el HIPS




#Actualmente estamos buscando un metodo de encriptacion para los datos, mientras utilizamos los datos en crudo
#Valores para la conexion a la base de datos
os.system("openssl enc -aes-256-cbc -d -in /home/marcelojulianbaezferreira/contrasenhas_cifradas/contrasenha_BD.txt.enc -out contrasenha_BD.txt")
	
#Al desencriptar la contraseña debemos ir a la terminal donde estamos corriendo el script en python para poder colocar la contraseña de desencriptacion
contrasenha_BD = open("contrasenha_BD.txt")
connpass_BD = contrasenha_BD.read().replace('\n','')#copiamos el contenido del archivo que abrimos exceptuando los saltos y los espacios vacios
contrasenha_BD.close()#cerramos el archivo
os.system("rm -rf contrasenha_BD.txt")#Eliminamos la contraseña desencriptada
	
conn_data = {'database':'HIPS', 'user':'postgres'}
conn = psycopg2.connect(host="localhost", dbname=conn_data['database'], user=conn_data['user'], password=connpass_BD)
cursor=conn.cursor()
cursor.execute("SELECT version();")
record=cursor.fetchone()
print("Te has conectado a - ",record," ")
#base de datos conectada          

          
#Logs generados durante la ejecucion de este sript, de tal forma de enviar un solo mail con toda la informacion
lista_log = [] 
#Bandera que representa si debe o no enviar por mail los logs generados
enviarLogName = False

dir_binarios = ['/etc/passwd','/etc/shadow','/bin','/usr/bin','/usr/sbin']



