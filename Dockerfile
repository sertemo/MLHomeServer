# Definir la imagen base
FROM python:3.10-slim

# Configurar el entorno de trabajo
WORKDIR /app

# Instalar curl para descargar poetry y otras herramientas útiles
RUN apt-get update && apt-get install -y curl

ENV POETRY_VERSION=1.8.2

# Instalar Poetry utilizando pip
RUN pip install "poetry==$POETRY_VERSION"
ENV PYTHONPATH=/app/src:$PYTHONPATH


# Asegurarse de que el binario de Poetry esté en el PATH
ENV PATH="/root/.poetry/bin:${PATH}"

# Configurar Poetry: no crear un entorno virtual y no preguntar en la instalación
RUN poetry config virtualenvs.create false && \
    poetry config installer.parallel false

# Copiar solo archivos necesarios para la instalación de dependencias
COPY pyproject.toml poetry.lock* /app/

# Instalar dependencias de proyecto utilizando Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

RUN echo $PATH && poetry run which uvicorn

# Copiar el resto del código fuente al contenedor
COPY . /app

# Exponer el puerto en el que uvicorn estará escuchando
EXPOSE 5000

# Comando para ejecutar el servidor en modo producción
#CMD ["uvicorn", "src.mlhomeserver.main:app", "--host", "0.0.0.0", "--port", "5000"]
CMD ["uvicorn", "src.mlhomeserver.main:app", "--host", "localhost", "--port", "5000"]
