#!/bin/bash

# Este script toma un argumento y lo pasa al script train.py que realiza el entrenamiento.

# Salir si no se proporciona exactamente un argumento
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <nombre_desafio>"
    exit 1
fi

# El argumento que especifica el desafío
DESAFIO=$1

# Ruta completa al script train.py
SCRIPT_PATH="src/mlhomeserver/ml/training/train.py"

# Comprobando si el script existe
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "El script $SCRIPT_PATH no existe."
    exit 2
fi

# Ejecutar el script de Python pasando el desafío como argumento
# echo "Ejecutando el entrenamiento para el desafío: $DESAFIO"
# python para windows python3 para linux
python $SCRIPT_PATH $DESAFIO

