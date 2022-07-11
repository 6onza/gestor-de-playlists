# Gestor de playlists
### Trabajo Práctico Grupal - Facultad de Ingenieria - Universidad de Buenos Aires

* Clonar el repositorio `git clone https://github.com/1murda/tp-2`

## Crear proyecto en la API de Google para el manejo de sus recursos
* Link para crearlo `https://console.cloud.google.com/projectcreate` 
* Luego de crearlo en la opcion credenciales `https://console.cloud.google.com/apis/credentials/` se debe crear unas credenciales 0auth2 de tipo App de escritorio y descargar el archivo de las credenciales en la carpeta `credenciales_youtube` con el nombre credentials.json.
* En la parte de Pantalla de consentimiento se deben agregar los emails de los usuarios en los que se van a realizar las prebas.
* Se les debe otorgar todos los permisos disponibles al proyecto.
* Habilitar la API de Youtube en el proyecto con el nombre  `YouTube Data API v3`.

## Crear aplicacion para el manejo de la API de Spotify
* Crear app en `https://developer.spotify.com/dashboard/applications`
* Colocar las credenciales de la app en el archivo `utils.py`

## Crear proyecto en LyricsGenius
* Crear proyecto en `https://genius.com/api-clients/new`
* Colocar las credenciales en el archivo `utils.py`

## Dependencias
* Instalar las dependencias `pip3 install -r requirements.txt`
* Instalar las dependencias de la api de google `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`


Ejecutar el script principal `python3 main.py`
