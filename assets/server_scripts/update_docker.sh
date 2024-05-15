#!/bin/bash
# Última actualización 15/05/2024
IMAGE_NAME="sertemo/mlhomeserver:latest"
CONTAINER_NAME="friendly_black"
VOLUME_NAME="model-data"
LOG_FILE="/home/sertemo/Python/MLHomeServer/logfile.log"

# Función para añadir registros con fecha y hora a la consola y al archivo de log
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

# Hacer pull de la última imagen
docker pull $IMAGE_NAME | tee -a $LOG_FILE 2>&1

# Comprobar si el contenedor está corriendo
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    # Obtener el ID de la imagen del contenedor en ejecución
    RUNNING_IMAGE=$(docker inspect --format='{{.Image}}' $CONTAINER_NAME)

    # Obtener el ID de la última imagen
    LATEST_IMAGE=$(docker inspect --format='{{.Id}}' $IMAGE_NAME)

    # Comparar los IDs de imagen
    if [ "$RUNNING_IMAGE" != "$LATEST_IMAGE" ]; then
        log "Nueva imagen detectada, actualizando el contenedor..."

        # Detener y eliminar el contenedor actual
        docker stop $CONTAINER_NAME | tee -a $LOG_FILE 2>&1
        docker rm $CONTAINER_NAME | tee -a $LOG_FILE 2>&1

        # Correr el nuevo contenedor con la nueva imagen
        docker run -d -p 5000:5000 --name $CONTAINER_NAME -v $VOLUME_NAME:/app/models $IMAGE_NAME | tee -a $LOG_FILE 2>&1

        log "Contenedor actualizado exitosamente."
    else
        log "No se detectaron actualizaciones de imagen."
    fi
else
    # Correr el nuevo contenedor por primera vez si no está corriendo
    docker run -d -p 5000:5000 --name $CONTAINER_NAME -v $VOLUME_NAME:/app/models $IMAGE_NAME | tee -a $LOG_FILE 2>&1
    log "Contenedor creado por primera vez."
fi

# Limpieza de imágenes no utilizadas independientemente de la actualización
docker image prune -f --filter "until=24h" | tee -a $LOG_FILE 2>&1
log "Limpieza de imágenes antiguas completada."
