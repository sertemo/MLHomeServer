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

# Determinar el comando de Python disponible
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Python no está instalado."
    exit 3
fi

# Ejecutar el script de Python pasando el desafío como argumento
# echo "Ejecutando el entrenamiento para el desafío: $DESAFIO"
$PYTHON_CMD $SCRIPT_PATH $DESAFIO

