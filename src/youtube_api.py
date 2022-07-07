from __future__ import print_function
import os 
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import csv
from utils import ( cls,
                    validar_opcion,
                    PLAYLISTS_DIR,
                    BASE_DIR
                )

SCOPES: list = ["https://www.googleapis.com/auth/youtube.readonly",
                "https://www.googleapis.com/auth/youtube.force-ssl"]

YOUTUBE_API_SERVICE_NAME: str = "youtube"
YOUTUBE_API_VERSION: str = "v3"
client_secrets_file: str = "credentials.json"

def autenticar_youtube():
    creds = None

    if os.path.exists(f'{BASE_DIR}/credenciales_youtube/token.json'):
        creds = Credentials.from_authorized_user_file(f'{BASE_DIR}/credenciales_youtube/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f'{BASE_DIR}/credenciales_youtube/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(f'{BASE_DIR}/credenciales_youtube/token.json', 'w') as token:
            token.write(creds.to_json())
    
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    credentials=creds)
    
    return youtube


def obtener_channel_id(youtube)-> str:
    # consigo la id del usuario autenticado
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()
    channel_id: str = response["items"][0]["id"]
    
    return channel_id


def obtener_playlists_youtube(youtube)-> list:
    """ Obtiene las playlists de Youtube y las devuelve en una lista

    Returns:
        list: Lista de playlists de Youtube 
    """
    channel_id = obtener_channel_id(youtube)

    # consigo las playlists del usuario autenticado
    pl_request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        maxResults=25,
    )
    pl_response = pl_request.execute()

    return pl_response["items"]


def mostrar_playlists_youtube(youtube)-> None:
    cls()
    playlists: list = obtener_playlists_youtube(youtube)

    print(f"Playlists de Youtube: ")
    
    for i,playlist in enumerate(playlists):
        print(f"{i + 1} - {playlist['snippet']['title']}")

def exportar_playlist_youtube(youtube)-> None:
    """ exporta 10 caracteristicas de una playlist de Youtube elegida a un archivo csv

    Returns:
        None:
    """
    channel_id = obtener_channel_id(youtube)

    playlists: list = obtener_playlists_youtube(youtube)
    mostrar_playlists_youtube(youtube)
    
    opcion: int = validar_opcion([str(i) for i in range(len(playlists))] )
    playlist_id: str = playlists[int(opcion)-1]["id"]
    playlist_elegida = youtube.playlists().list(
        part="snippet,contentDetails",
        id=playlist_id,
        maxResults=20,
    ).execute()

    if (not os.path.exists(PLAYLISTS_DIR)):
            os.makedirs(PLAYLISTS_DIR)
    
    nombre: str = playlist_elegida['items'][0]['snippet']['title']
    propietario: str = playlist_elegida['items'][0]['snippet']['channelTitle']
    id_playlist: str = playlist_elegida['items'][0]['id']
    cantidad_tracks: str = playlist_elegida['items'][0]['contentDetails']['itemCount']
    descripcion: str = playlist_elegida['items'][0]['snippet']['description']
    fecha_publicacion: str = playlist_elegida['items'][0]['snippet']['publishedAt']
    url: str = playlist_elegida['items'][0]['snippet']['thumbnails']['default']['url']
    e_tag: str = playlist_elegida['etag']
    id_canal: str = playlist_elegida['items'][0]['snippet']['channelId']
    tipo: str = playlist_elegida['items'][0]['kind']

    try:
        with open(f"{PLAYLISTS_DIR}/{nombre}.csv", "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                    "nombre", 
                    "propietario", 
                    "id de playlist", 
                    "cantidad de tracks", 
                    "descripcion",  
                    "fecha de publicacion",  
                    "url", 
                    "e-tag", 
                    "id del canal",
                    "tipo"]
            )
            writer.writerow([
                    nombre, 
                    propietario, 
                    id_playlist, 
                    cantidad_tracks, 
                    descripcion, 
                    fecha_publicacion, 
                    url, 
                    e_tag, 
                    id_canal,
                    tipo]
                    )
        print(f"Playlist {nombre} exportada correctamente")
        input("Pulse enter para continuar...")

    except Exception as e:
        print(f"Error al exportar la playlist {nombre}: {e}")
        input("Pulse enter para continuar...")


def obtener_nombres_de_canciones_youtube(youtube)-> list:
    """ Obtiene los nombres de las canciones de una playlist de Youtube

    Returns:
        list: Lista de nombres de canciones de la playlist
    """
    playlists = obtener_playlists_youtube(youtube)

    nombres_de_canciones: list = []
    mostrar_playlists_youtube(youtube)
    opcion: str = validar_opcion([str(i) for i in range(1, len(playlists) + 1)])
    playlist_id: str = playlists[int(opcion)-1]["id"]

    
    playlist_elegida = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=20,
    ).execute()

    for cancion in playlist_elegida["items"]:
        nombres_de_canciones.append(cancion["snippet"]["title"])
    
    info_canciones: dict = {}
    #separo lo q esta entre guiones que suele ser lo que separa el nombre de la cancion de sus autores
    for cancion in nombres_de_canciones:
        cancion_aux = cancion.split("-")
        # verifico q se haya podido separar el autor del nombre de la cancion sino la omito
        if type(cancion_aux) == list and len(cancion_aux) == 2:
            info_canciones[cancion_aux[0]] = cancion_aux[1]

    return info_canciones


def crear_una_playlist_youtube(youtube):

    try:
        nombre: str = input("Nombre de la playlist: ")
        descripcion: str = input("Descripcion de la playlist: ")
       
        if descripcion == "":
            descripcion = None

        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": nombre,
                    "description": descripcion
                },
                "status": {
                    "privacyStatus": "public"
                }
            }
        )
        response = request.execute()
        print(f"Playlist creada: {response['snippet']['title']}")
        input("Pulse enter para continuar...")



    except Exception as e:
        print("Hubo un error al crear la playlist: ", e)
        input("Pulsa enter para continuar...") 


def buscar_cancion(youtube)-> list:
    """ Busca una cancion en Youtube

    Returns:
        id_cancion: str: Id de la cancion encontrada
    """
    #busco las canciones segun el nombre
    nombre_cancion: str = input("Nombre de la cancion: ")
    request = youtube.search().list(
        part="snippet",
        q=nombre_cancion,
        type="video",
        maxResults=3,
    )
    response = request.execute()

    for i, cancion in enumerate(response["items"]):
        print(f"{i + 1} - {cancion['snippet']['title']}")
    
    print("Elija entre una de las opciones")
    opcion = validar_opcion([str(i) for i in range(1, 4)])
    
    return response["items"][int(opcion) - 1]["id"]["videoId"]
    


def agregar_un_item_a_la_playlist_youtube(youtube):
    cls()
    playlists: list = obtener_playlists_youtube(youtube)

    mostrar_playlists_youtube(youtube)
    opcion: str = validar_opcion([str(i) for i in range(1, len(playlists) + 1)])
    playlist_id: str = playlists[int(opcion)-1]["id"]

    id_cancion: str = buscar_cancion(youtube)
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": id_cancion
                }
            }
        }
    )
    response = request.execute()
    print(f"Cancion agregada a la playlist: {response['snippet']['title']}")
    input("Pulse enter para continuar...")