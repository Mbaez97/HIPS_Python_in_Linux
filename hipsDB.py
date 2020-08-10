#!/usr/bin/python
import hashlib
import psycopg2
import os
from os import listdir
import string
import getpass





def main():
	dir_binarios = ['/etc/passwd','/etc/shadow','/bin','/usr/bin','/usr/sbin']
	
	#Falta encriptacion(RESUELTO CON OPENSSL)
	
	





	#Encriptacion con open ssl
	#Recuperamos el archivo donde se encuentran las contraseñas cifradas en el servidor, en este caso la contraseña de la base de datos
	os.system("openssl enc -aes-256-cbc -d -in /home/marcelojulianbaezferreira/contrasenhas_cifradas/contrasenha_BD.txt.enc -out contrasenha_BD.txt")
	
	#Al desencriptar la contraseña debemos ir a la terminal donde estamos corriendo el script en python para poder colocar la contraseña de desencriptacion
	contrasenha_BD = open(contrasenha_BD.txt)
	connpass_BD = contrasenha_BD.read().replace('\n','')#copiamos el contenido del archivo que abrimos exceptuando los saltos y los espacios vacios
	contrasenha_BD.close()#cerramos el archivo
	os.system("rm -rf contrasenha_BD.txt")#Eliminamos la contraseña desencriptada
	conn_data = {'database':'HIPS', 'user':'postgres'};


	conn = psycopg2.connect(host="localhost", dbname=conn_data['database'], user=conn_data['user'], password=connpass_BD)
	cursor = conn.cursor()

	#Eliminamos y volvemos a crear la tabla en la base de datos, mas facil que identificar con ids o otras cosas
	cursor.execute("DROP TABLE IF EXISTS binarios_sistema")
	cursor.execute("CREATE TABLE binarios_sistema(id SERIAL, directorio VARCHAR, md5sum VARCHAR)")
	carga_binarios(dir_binarios)
	print("Los Binarios del sistema fueron guardados correctamente en la base de datos")
	conn.close()


def carga_binarios(dir_binarios):
	lista_directorios = [] #Esta lista utilizaremos para extraer las firmas md5 de cada archivo
	for ruta in dir_binarios:
		if os.path.isdir(ruta):#Establecemos un analisis del directorio para saber si es un archivo o una carpeta
			list_aux = os.listdir(ruta)#Al ser una carpeta preparamos un vector con la direccion del archivo que vamos a analizar
			for elm_lista in list_aux:
				lista_directorios.append(ruta + '/' + elm_lista)
		else:
			lista_directorios = [ruta]#al ser un archivo preparamos la lista de direcciones como un elemento y es la direccion completa del archivo
		
		for direccion in lista_directorios:
			archivo_temp = hashlib.md5((open(direccion)).read())
			#Obtenemos el md5 cambiando a formato str
			sum_md5 = str(archivo_temp.hexdigest())
			try:
				cursor.execute("INSERT INTO binarios_sistema(directorio, md5sum) VALUES (%s,%s)",(direccion, sum_md5))
			except pgDB.Error as error:
				print("Error: {}".format(error))
			conn.commit()
	pass





