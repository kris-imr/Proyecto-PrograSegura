#!/bin/bash

[[ $1 ]] || { echo “se esperaba como primer parametro un archivo env“; exit 1; }

for linea in $(cat "$1"); do
           export "$linea"
   done

docker-compose up -d