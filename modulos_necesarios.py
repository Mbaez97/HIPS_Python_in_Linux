#!/usr/bin/python
#Modulo para conexion a la base de datos PostGreSQL
import psycopg2 as pgDB
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
import commands
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

#Establecemos algunos valores que usaremos a lo largo de los distintos modulos del hips
maxColaMail = 120 #Maxima cola de correos
mensj = MIMEMultipart()
mensj['From'] = "hips.baez.oh.2020@gmail.com"#Correo creado unicamente para este trabajo
mensj['To'] = "marcelobaezparaguay@gmail.com"#En este campo estaria el correo del administrador que utilice el HIPS

#Actualmente estamos buscando un metodo de encriptacion para los datos, mientras utilizamos los datos en crudo
#Valores para la conexion a la base de datos
conn_data = {'host':'localhost', 'database':'HIPS', 'user':'postgres'};
#Recuperamos la contrasenha encriptada
os.system("openssl enc -a-256-cbc -d -in /home/marcelojulianbaezferreira/contrasenhas_cifradas/contrasenhaBD.txt.enc -out contrasenhaBD.txt")
contrasenhaBD = open("contrasenhaBD.txt")
pass = contrasenhaBD.read().replace('\n', '')
contrasenhaBD.close()
os.system("rm -rf contrasenhaBD.txt)
conn = psycopg2.connect(host=conn_data['host'], database=conn_data['database'], user=conn_data['user'], password=pass)
cursor = conn.cursor()
#base de datos conectada          

          
#Logs generados durante la ejecucion de este sript, de tal forma de enviar un solo mail con toda la informacion
lista_log = [] 
#Bandera que representa si debe o no enviar por mail los logs generados
enviarLogName = False

dir_binarios = ['/etc/passwd','/etc/shadow','/bin','/usr/bin','/usr/sbin']



