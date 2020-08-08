#!/usr/bin/python
import hashlib
#import md5
import psycopg2
import os
from os import listdir
import string
import getpass



#Falta encriptacion
conn_data = {'database':'HIPS', 'user':'postgres', 'password':'Majubafe29797'};
conn = psycopg2.connect(host="localhost", database=conn_data['database'], user=conn_data['user'], password=conn_data['password'])
cursor = conn.cursor()

#Eliminamos y volvemos a crear la tabla en la base de datos, mas facil que identificar con ids o otras cosas
cursor.execute("DROP TABLE IF EXISTS binarios_sistema")
cursor.execute("CREATE TABLE binarios_sistema(id SERIAL, directorio VARCHAR, md5sum VARCHAR)")


dir_binarios = ['/etc/passwd','/etc/shadow','/bin','/usr/bin','/usr/sbin']
#los directorios de los  ya las tenemos dentro de modulos_necesarios en la lista dir_binarios

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

carga_binarios(dir_binarios)
conn.close()


