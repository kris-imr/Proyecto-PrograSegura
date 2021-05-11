#!/bin/bash

DIR=/home/erick/proyecto

[[ -f "$1" ]] || { echo "se espera un archivo como parametro"; exit 1; }

if [ ! -d $DIR ]
then
	echo "No estás sobre el directorio correcto"
else
	if [ -s "$1" ]
	then
		if [ -n "$2" ]
		then
			for linea in $(ccdecrypt -c "$1"); do
				export $linea
			done
			python manage.py $2
		else
			echo "No se recibió alguna instrucción"
		fi
	else
		echo "El archivo no contiene ningún dato a procesar"
	fi
fi
