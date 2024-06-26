#!/bin/bash

# Inicializa el servidor #

# Comprobar si se pasa el argumento 'dev'
if [[ $1 == "dev" ]]; then
    # Ejecutar uvicorn con la opción --reload
    echo "Ejecutando en modo desarrollador"
    uvicorn src.mlhomeserver.main:app --host 0.0.0.0 --port 5000 --reload
else
    # Ejecutar uvicorn sin la opción --reload
    echo "Ejecutando en modo producción"
    uvicorn src.mlhomeserver.main:app --host 0.0.0.0 --port 5000
fi