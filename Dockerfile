# Definir la imagen base
FROM python:3.10-slim

# Configurar el entorno de trabajo
WORKDIR /app

# Instalar curl para descargar poetry y otras herramientas útiles
RUN apt-get update && apt-get install -y curl

ENV POETRY_VERSION=1.8.2

# Instalar Poetry utilizando pip
RUN pip install "poetry==$POETRY_VERSION"

# Asegurarse de que el binario de Poetry esté en el PATH
ENV PATH="/root/.poetry/bin:${PATH}"

# Configurar Poetry: no crear un entorno virtual y no preguntar en la instalación
RUN poetry config virtualenvs.create false && \
    poetry config installer.parallel false

# Copiar solo archivos necesarios para la instalación de dependencias
COPY pyproject.toml poetry.lock* /app/

# Instalar dependencias de proyecto utilizando Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Copiar el resto del código fuente al contenedor
COPY . /app

# Otorgar permisos de ejecución al script de inicio
RUN chmod +x ./start.sh

# Exponer el puerto en el que uvicorn estará escuchando
EXPOSE 5000

# Comando para ejecutar el servidor
CMD ["./start.sh"]
