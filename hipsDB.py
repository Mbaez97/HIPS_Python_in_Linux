#!/usr/bin/python
import delegator
#import hashlib
import psycopg2
import os
from os import listdir
import string
import getpass





dir_binarios = ['/etc/passwd','/etc/shadow','/bin','/usr/bin','/usr/sbin']	
#Falta encriptacion(RESUELTO CON OPENSSL)
#Encriptacion con open ssl
#Recuperamos el archivo donde se encuentran las contraseñas cifradas en el servidor, en este caso la contraseña de la base de datos
os.system("sudo openssl enc -aes-256-cbc -d -in /home/marcelojulianbaezferreira/contrasenhas_cifradas/contrasenha_BD.txt.enc -out contrasenha_BD.txt")
	
#Al desencriptar la contraseña debemos ir a la terminal donde estamos corriendo el script en python para poder colocar la contraseña de desencriptacion
contrasenha_BD = open("contrasenha_BD.txt")
connpass_BD = contrasenha_BD.read().replace('\n','')#copiamos el contenido del archivo que abrimos exceptuando los saltos y los espacios vacios
contrasenha_BD.close()#cerramos el archivo
os.system("rm -rf contrasenha_BD.txt")#Eliminamos la contraseña desencriptada
	
conn_data = {'database':'HIPS', 'user':'postgres'};
conn = psycopg2.connect(host="localhost", dbname=conn_data['database'], user=conn_data['user'], password=connpass_BD)
cursor=conn.cursor()
cursor.execute("SELECT version();")
record=cursor.fetchone()
print("Te has conectado a - ",record," ")

def carga_binarios(dir_binarios):
	try:
		cursor = conn.cursor()	
		#Eliminamos y volvemos a crear la tabla en la base de datos, mas facil que identificar con ids o otras cosas
		cursor.execute("DROP TABLE IF EXISTS binarios_sistema")
		cursor.execute("CREATE TABLE binarios_sistema(id SERIAL, directorio VARCHAR, md5sum VARCHAR)")
		print("Se creo la tabla en la base de datos")
	except:
		print("Error al conectarse con la base de datos")
		return
	
	lista_directorios = [] #Esta lista utilizaremos para extraer las firmas md5 de cada archivo
	for ruta in dir_binarios:
		if os.path.isdir(ruta):#Establecemos un analisis del directorio para saber si es un archivo o una carpeta
			list_aux = os.listdir(ruta)#Al ser una carpeta preparamos un vector con la direccion del archivo que vamos a analizar
			for elm_lista in list_aux:
				lista_directorios.append(ruta + '/' + elm_lista)
		else:
			lista_directorios = [ruta]#al ser un archivo preparamos la lista de direcciones como un elemento y es la direccion completa del archivo
		
		for direccion in lista_directorios:
			cmd= "sudo md5sum "+str(direccion)
			#cadena=open(direccion).read()
			#print("la cadena es ", cadena)
			#archivo_temp = hashlib.md5((cadena.decode().encode('utf-32')))
			#Obtenemos el md5 cambiando a formato str
			#sum_md5 = str(archivo_temp.hexdigest())
			sum_md5=delegator.run(cmd).out.split()[0]
			try:
				cursor.execute("INSERT INTO binarios_sistema(directorio, md5sum) VALUES (%s,%s)",(direccion, sum_md5))
			except psycopg2.Error as error:
				print("Error: {}".format(error))
			conn.commit()
	pass

def carga_sniffers():
	try:
		cursor = conn.cursor()
		cursor.execute("DROP TABLE IF EXISTS lista_sniffers")#Si existe la tabla la eliminamos, misma logica que utilizamos en la carga de binarios
		cursor.execute("CREATE TABLE lista_sniffers(id SERIAL, sniffer VARCHAR)")#Creamos la tabla
		print("Se creo la tabla en la base de datos")
	except:
		print("Error al conectarse con la base de datos")
		return
	
	lista_sniffers = open('lista_sniffers.txt', 'r')#En esta lista guardamos los nombres de los sniffers conocidos.
	
	for fila in lista_sniffers:
		sniffers = len(fila) - 1
		sniff = fila[:sniffers]
		#Insertamos en la base de datos donde tenemos el id y el nombre del sniff

		try:
			print(sniff)
			cursor.execute("INSERT INTO lista_sniffers (sniffer) VALUES (%s) ", (sniff, ))
		except psycopg2.Error as error:
			print("Error: {}".format(error))
		conn.commit()
	lista_sniffers.close()



def carga_lista_blanca():
	try:
		cursor = conn.cursor()
		cursor.execute("DROP TABLE IF EXISTS lista_blanca")
		cursor.execute("CREATE TABLE lista_blanca(id SERIAL, nombre_programa VARCHAR)")
		print("Se creo la tabla lista_blanca")
	except:
		print("Error al conectarse con la base de datos")
		return
	lista_blanca = open('lista_blanca.txt', 'r')
	for fila in lista_blanca:
		programa = len(fila) - 1
		nombre_programa = fila[:programa]

		try:
			print(programa)
			cursor.execute("INSERT INTO lista_blanca (nombre_programa) VALUES (%s)", (nombre_programa, ))
		except psycopg2.Error as error:
			print("Error: {}".format(error))
		conn.commit()
	lista_blanca.close()


def carga_usuarios():
	try:
		cursor = conn.cursor()   				   # conectamos a la base de datos
		cursor.execute("DROP TABLE IF EXISTS users") 	   # borramos tabla si existe
		# creamos la tabla users donde se guardamos usuarios, ips, email, pass 
		cursor.execute("CREATE TABLE users(id SERIAL, usr VARCHAR, addr VARCHAR, email VARCHAR, pass VARCHAR)") 
	except:
		print("No se pudo acceder a la base de datos")
		return

	delegator.run("sudo openssl enc -aes-256-cbc -d -in /home/marcelojulianbaezferreira/contrasenhas_cifradas/lista_usuarios.txt.enc -out lista_usuarios.txt")
	archivo=open('lista_usuarios.txt','r') #Abre el archivo que contiene la lista de usuarios permitidos	

	lineas = archivo.read().split(os.linesep)

	for aux in lineas[:-1]:
		if(aux != ''):
			vec = aux.split(' ') #Parseamos los datos en un vector de 4 campos los cuales identifican cada uno de los datos a ser insertado
			try:        #Insertamos los datos en la base de datos users
				cursor.execute("INSERT INTO users ( usr, addr, email, pass) VALUES (%s,%s,%s,%s)",(vec[0],vec[1],vec[2],vec[3][:len(vec[3])]) )
			except psycopg2 as error:
				print("Error: {}".format(error))
			conn.commit()
	archivo.close()
	# Borramos el archivo txt despues de utilizarlo, SIEMPRE.
	os.system("rm -rf lista_usuarios.txt")		

carga_sniffers()
carga_binarios(dir_binarios)
carga_usuarios()

conn.close()

