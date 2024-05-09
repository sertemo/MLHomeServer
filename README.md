# ML Home Server
### v0.1.0
![Tests](https://github.com/sertemo/MLHomeServer/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/sertemo/MLHomeServer/graph/badge.svg?token=6N7LBN76A2)](https://codecov.io/gh/sertemo/MLHomeServer)
![Dependabot](https://img.shields.io/badge/dependabot-enabled-blue.svg?logo=dependabot)
![GitHub](https://img.shields.io/github/license/sertemo/MLHomeServer)
----
![Pytest](https://img.shields.io/badge/testing-pytest-blue.svg)
![Black](https://img.shields.io/badge/code%20style-black-blue.svg)
![Flake8](https://img.shields.io/badge/linter-flake8-blue.svg)
![MyPy](https://img.shields.io/badge/type%20checker-mypy-blue.svg)
----
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=python&logoColor=white)

## Descripción
Pequeño proyecto para montar un servidor en el ordenador Samsung del 2011 con **Xubuntu**.

La idea es poder utilizarlo como API para hacer predicciones con modelos de ML y devolver dichas predicciones.

Este proyecto ofrece además la posibilidad de entrenar modelos.

## Entrenar un modelo localmente
### 1. Configurar el archivo de desafíos config.yml dentro de la raiz del proyecto
Antes de entrenar un modelo hay que definir el desafío y los parámetros necesarios para el entrenamiento.

Se presupone que ya se han hecho las pruebas pertinentes y el análisis exploratorio para el desafío en los notebooks.

El objetivo del entrenamiento manual es tener alojado en el contexto del proyecto el modelo para lanzar las predicciones.

Para que el entrenamiento se realice correctamente hay que añadir los parámetros del **dataset**, del **preprocesador** del dataset y del **modelo** al archivo `config.yml` en la raiz principal del proyecto.

El esquema del archivo es el siguiente:

```yml
nombre_desafio:  # El nombre del desafío en cuestión
  dataset:
    filename: "train.csv"  # Nombre del archivo de train dentro de data/nombre_desafio
    label_col_name: "target"  # Nombre de la columna de los targets
    params:  # Parámetros a pasar al 'read_csv' para abrir correctamente el dataframe
      index_col: 0  # El dataframe tiene su primera columna como índice
  preprocessor:
    class_name: "CustomTransformer"  # Dentro de data_processing/nombre_desafio_transformer.py en este caso
    params:  # Estos serán los parámetros a pasar al preprocesador
      parametro1:
        - "1"
        - "2"
        - "3"
      parametro2:
        - "objeto1"
        - "objeto2"
  model:
    type: "modulo.modelo"  # El módulo en el que se encuentra el modelo (tanto custom como de terceros)
    class_name: "Modelo"  # Debe ser un modelo 
    params:
      parametro1: 123
      parametro2: 321
  label_encoder: true
```

**Notas importantes**
- Será siempre necesario hacer un preprocesador personalizado y guardarlo en **ml/data_processing/nombre_desafio_transformer.py**
- El **preprocesador** debe tener un método `fit_transform`. o heredar de `TransformerMixin` del módulo `sklearn.base`.
- El archivo dataset par el entrenamiento debe estar guardado en la carpeta data dentro de una carpeta con el mismo nombre del desafío: **data/nombre_desafio/**.
- El modelo puede ser un modelo personalizado, en tal caso deberá guardarse en la carpeta **models** y especificar el módulo en el que se encuentra y su nombre en el archivo config.yml.
- Para que sea válido el modelo debe tener los métodos `fit` y `predict`.
- En caso de usar un modelo de una librería como por ejemplo `sklearn` es necesario también especificar el módulo desde el que hay que importarlo y su nombre.


Un ejemplo de archivo para el desafío **aidtec** es el siguiente:

```yml
aidtec:
  dataset:
    filename: "train.csv"
    label_col_name: "calidad"
    params:
      index_col: 0
  preprocessor:
    class_name: "WineDatasetTransformer"
    params:
      drop_columns:
        - "year"
        - "color"
        - "alcohol"
        - "densidad"
        - "dioxido de azufre libre"
  model:
    type: "sklearn.ensemble"
    class_name: "RandomForestClassifier"
    params:
      n_estimators: 900
      random_state: 42
  label_encoder: true
```

### 2. Ejecutar train.sh
```sh
$ ./train.sh <nombre_desafio>
```

Esto ejecutará el script `train.py` en la carpeta **ml/training** con el nombre del desafío como argumento.

Es importante que el nombre del desafío coincida con el establecido en el archivo `desafios_settings.py`. Todos los datos del entrenamiento serán extraido de ahi.


----

## Puesta en marcha del servidor
### 1. API con FastAPI
Crear una pequeña API usando FastAPI para dar respuesta a las peticiones.

La API usará modelos entrenados y serializados con pickle o joblib para hacer predicciones en los diferentes endpoints correspondientes a cada desafío.

La idea es realizar diferentes endpoints para diferentes tipos de desafíos.

Se realizarán routers distintos para cada desafío de ML.

### 2. Salir de CGNAT
Mi proveedor de internet **Pepehone** por lo visto usa el servicio [**CGNAT**](https://www.ysi.si/es/tendencias/4692/cgnat-que-es-y-como-funciona) que asigna la misma ip a varios usuarios. Este hecho imposibilita utilizar la ip y redireccionarla al ordenador servidor.

Para salir de CGNAT ha bastado con llamar al servicio técnico y pedirlo. En 24 horas estaba hecho.

### 3. Port Forwarding
Hay que configurar dentro de las opciones del router un redireccionamiento de ips y puertos.

Entramos en el router con **192.168.1.1**

En **Acces Control** > **Port Forwarding** se añaden 2 reglas manuales:
- Internal host con la IP privada de ethernet de mi ordenador Samsung y 5000 como external e internal port
- Internal host con la IP privada de wifi de mi ordenador Samsung y 5001 como external y 5000 internal port

### 4. Dominio
Con los pasos anterior ya se podría poner en marcha el servidor. Las solicitudes a la <ip_publica>:5000 deberían tener respuesta.

Para evitar usar la ip de mi proveedor que supuestamente es dinámica (veremos más adelante como solventar este problema) compro un dominio en [**porkbun.com**](https://porkbun.com).

El dominio comprado es el siguiente: **trymlmodels.com** con subdominio www.

Dentro de la plataforma de porkbun, hay que desplegar la pestaña **details** y habilitar **API ACCESS**.

También hay que crear la **secret_api_key** y la **api_key**. Estas dos keys hay que anotarlas porque se usarán más adelante.

### 5. Servicio DDNS
Para redirigir automáticamente el dominio a la IP correspondiente hay que poner en marcha un servicio que verifique periódicamente si la ip ha cambiado y la actualice en **porkbun**.

#### 5.1 Descargar oink_ddns
Descargamos [**Oink**](https://github.com/RLado/Oink) para realizar dicha tarea.

Descargamos el paquete: https://github.com/RLado/Oink/releases/download/v1.1.0/oink_1.1-0_amd64.deb

Una vez descargamos se instala haciendo:

```sh
$ dpkg -i oink_1.1-0_amd64.deb
```

#### 5.2 Configurar el archivo config.json
El archivo de configuración está en **etc/oink_ddns/config.json**

Como tiene permisos de administrador es aconsejable realizar primero un:

```sh
$ sudo su
```

Y después abrirlo con **nano** para configurarlo


```sh
$ nano config.json
```

Poner las apikey y secretapikey proporcionadas por **porkbun**. Hay que crear dos entradas dentro de **domains**, una con subdominio y otra sin subdominio para que ambos se actualicen en porkbun.

```sh
{
    "global": {
        "secretapikey": "sk1_xxxxxx",
        "apikey": "pk1_xxxxx",
        "interval": 900,
        "ttl": 600
    },
    "domains": [
        {
            "domain": "trymlmodels.com",
            "subdomain": "www"
        },
	{
	    "domain": "trymlmodels.com"
        }
    ]
}
```

#### 5.3 Correr el servicio en el ordenador
Para correr el servicio:
```sh
$ systemctl start oink_ddns
```
(o restart)

Para ver status:
```sh
$ systemctl status oink_ddns
```

Este servicio hace apuntar mi dominio a mi ip pública. Actualiza temporalmente la ip pública comprobándolo ya que será cambiante.


### 6. Servidor Uvicorn
Para correr la API en el servidor en el puerto 5000 hay que lanzar el siguiente comando:
```sh
$ uvicorn src.mlhomeserver.main:app --host 0.0.0.0 --port 5000 --reload
```

Por comodidad se prepara un scrip en bash: `start.sh` para ejecutar este comando:
Para ejecutar con `--reload`:
```sh
$ ./start.sh dev
```

Para ejecutar en modo producción:
```sh
$ ./start.sh
```

## Uso de la API
Para hacer request de momento funcionan los siguientes endpoints:

- GET http://www.trymlmodels.com:5000 > mensaje bienvenida
- GET http://www.trymlmodels.com:5000/about > Información del servidor
- POST con un csv http://www.trymlmodels.com:5000/desafio/predict > devuelve las predicciones
- GET http://www.trymlmodels.com:5000/desafio/model > devuelve info del modelo

## Agradecimientos
Special thanks to [**Miguel Zubiaga**](https://www.mzubiaga.net/) por ayudarme a montar este mini proyecto.

## Licencia
Copyright 2024 Sergio Tejedor Moreno

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.



