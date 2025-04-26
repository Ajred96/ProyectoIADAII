# ProyectoIADAII
Desarrollo del proyecto 1 de ADA II

versiones:
Angular CLI: 11.2.4
Node: 14.17.3
OS: win32 x64

Angular:
...
Ivy Workspace:
Package                      Version
------------------------------------------------------
@angular-devkit/architect    0.1102.4 (cli-only)
@angular-devkit/core         11.2.4 (cli-only)
@angular-devkit/schematics   11.2.4 (cli-only)
@schematics/angular          11.2.4 (cli-only)
@schematics/update           0.1102.4 (cli-only)


Versión de Python: 3.13.1 (Compilado el 3 de diciembre de 2024)
Arquitectura: 64-bit (AMD64)
Compilador: MSC v.1942
Ubicación de pip: C:\Python313\Lib\site-packages\pip
Versión de pip: 24.3.1

📦 Paquetes Instalados
blinker 1.9.0
click 8.1.8
colorama 0.4.6
Flask 3.1.0
flask-cors 5.0.1
itsdangerous 2.2.0
Jinja2 3.1.6
MarkupSafe 3.0.2
Werkzeug 3.1.3
pip 24.3.1

## Estructura de Archivos

```bash

├── BateriaPruebas                ## Archivos de la Batería de Pruebas
├── Informe                       ## Código Fuente Latex y PDF del Informe 
├── README.md                     ## Este Archivo
├── backend                       ## CODIGO FUENTE DEL BACKEND
│   ├── Dockerfile                ## Dockerfile para despliegue del backend
│   ├── app.py                    ## Archivo principal de la api
│   ├── modciFB.py                ## FUNCIONES PARA PROCESAR FUERZA BRUTA
│   ├── modciPD.py                ## FUNCIONES PARA PROCESAR PROGRAMACIÓN DINÁMICA
│   ├── modciPV.py                ## FUNCIONES PARA PROCESAR PROGRAMACIÓN VORAZ
│   ├── requirements.txt          ## Librerias necesarias para instalar
│   ├── static                    ## Carpeta que guarda los archivos de resultados
│   └── utils.py                  ## FUNCIONES AUXILIARES PARA LOS ALGORITMOS 
├── docker-compose.yml            ## docker-compose para el despliegue del proyecto
└── frontend                      ##CÓDIGO FUENTE DEL FRONTEND
    ├── Dockerfile                ## Dockerfile para despliegue del frontend
    ├── README.md                 ## readme del front-end 
    ├── angular.json              ## archivo de angular
    ├── e2e                       ## archivo de angular
    ├── karma.conf.js             ## archivo de angular
    ├── package-lock.json         ## dependencias necesarias
    ├── package.json              ## dependencias necesarias
    ├── src                       ## APLICACIÓN DEL FRONTEND
    ├── tsconfig.app.json         ## archivo de angular
    ├── tsconfig.json             ## archivo de angular
    ├── tsconfig.spec.json        ## archivo de angular
    └── tslint.json               ## archivo de angular

```


## Ejecución del proyecto

La ejecución de este proyecto se apoya en contenedores Docker para garantizar un entorno aislado y reproducible. A continuación, se detallan los pasos necesarios para clonar, construir y lanzar la aplicación, tanto en sistemas Windows como Linux/macOS.

### 1. Clonar el repositorio

Abra una terminal o consola de comandos y ejecute:

```bash
git clone https://github.com/Ajred96/ProyectoIADAII.git
cd ProyectoIADAII
```

### 2. Instalar Docker y Docker Compose

Antes de continuar, asegúrese de tener instalado Docker en su sistema.

- **Windows**: Instalar desde [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux/macOS**: Seguir instrucciones en [instalación de Docker](https://docs.docker.com/get-docker/)

Una vez instalado, puede verificar la instalación ejecutando:

```bash
docker --version
docker compose version
```

### 3. Construir y ejecutar el proyecto

Desde la raíz del proyecto, ejecute el siguiente comando para construir e iniciar los contenedores:

```bash
docker compose up --build
```

Este comando descargará las imágenes necesarias y levantará automáticamente los servicios de la aplicación.

### 4. Acceder a la aplicación

Una vez que todos los servicios estén corriendo, la interfaz estará disponible en su navegador en:

```bash
http://localhost:4200
```

La aplicación quedará lista para ser utilizada sin necesidad de configuración adicional.
