# ML Home Server

Pequeño proyecto para montar un servidor en el ordenador Samsung del 2011 con linux.

La idea es poder utilizarlo como API para hacer predicciones con modelos y devolver dichas predicciones

Los pasos que he tenido que seguir para conseguirlo se describen a continuación

## 1. API con FastAPI

Crear una pequeña API usando FastAPI para dar respuesta a las peticiones.

La API usa modelos entrenados y serializados con pickle para hacer predicciones en el endpoint **/predict/aidtec**.

La idea es realizar diferentes endpoints para diferentes tipos de desafíos. Todos colgarán de **/predict**.

## 2. Salir de CGNAT

Mi proveedor de internet **Pepehone** por lo visto usa el servicio [**CGNAT**](https://www.ysi.si/es/tendencias/4692/cgnat-que-es-y-como-funciona) que asigna la misma ip a varios usuarios. Este hecho imposibilita utilizar la ip y redireccionarla al ordenador servidor

## 3. Port Forwarding

Hay que configurar dentro de las opciones del router un redireccionamiento de ips y puertos.

Entramos en el router con **192.168.1.1**

En **Acces Control** > **Port Forwarding** se añaden 2 reglas manuales:
- Internal host con la IP privada de ethernet de mi ordenador Samsung y 5000 como external e internal port
- Internal host con la IP privada de wifi de mi ordenador Samsung y 5001 como external y 5000 internal port

## 4. Dominio

Con los pasos anterior ya se podría poner en marcha el servidor. Las solicitudes a la ip_publica:5000 deberían tener respuesta.

Para evitar usar la ip de mi proveedor que supuestamente es dinámica (veremos más adelante como solventar este problema) compro un dominio en [**porkbun.com**](https://porkbun.com)

Compro el dominio: http://www.trymlmodels.com

Hay que desplegar la pestaña **details** y habilitar **API ACCESS**.

También hay que crear la **secret_api_key** y la **api_key**. Estas dos keys hay que anotarlas porque se usarán más adelante.

## 5. Servicio de DNS

Para redirigir automáticamente el dominio a la IP correspondiente hay que poner en marcha un servicio que verifique periódicamente si la ip ha cambiado y la actualice en **porkbun**.

### 5.1 Descargar oink_ddns

Descargamos [**Oink**](https://github.com/RLado/Oink) para realizar dicha tarea.

Descargamos el paquete: https://github.com/RLado/Oink/releases/download/v1.1.0/oink_1.1-0_amd64.deb

Una vez descargamos se instala haciendo:

```sh
$ dpkg -i oink_1.1-0_amd64.deb
```

### 5.2 Configurar el archivo config.json

El archivo de configuración está en **etc/oink_ddns/config.json**

Como tiene permisos de administrador es aconsejable realizar primero un:

```sh
$ sudo su
```

Y después abrirlo con **nano** para configurarlo


```sh
$ nano config.json
```

Poner las apikeys y secretapikeys proporcionadas por **porkbun**. En el subdominio poner **www**.

### 5.3 Correr el servicio en el ordenador

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


## API

Para la API he usado FastAPI

Para hacer request de momento funcionan los siguientes endpoints:

- GET http://www.trymlmodels.com:5000
- GET http://www.trymlmodels.com:5000/about
- POST con un csv http://www.trymlmodels.com:5000/predict/aidtec

## Servidor
Para correr el servidor en el puerto 5000 hay que lanzar el siguiente comando:
```sh
$ uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

**OJO** : Usar solo la flag `--reload` en desarrollo.



