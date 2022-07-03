import os
from utils import cls
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


SCOPES: list = ["https://www.googleapis.com/auth/youtube.readonly"]
api_service_name: str = "youtube"
api_version: str = "v3"
client_secrets_file: str = "credentials.json"

def autenticar_youtube() -> googleapiclient.discovery.Resource:
    """ Autentica al usuario en Youtube y devuelve un objeto Resource

    Returns:
        googleapiclient.discovery.Resource: Objeto Resource de Youtube
    """
    # obtengo las credenciales de la API Sy el API Client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    credentials = flow.run_console()

    # creo el objeto Resource de Youtube
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

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


def mostrar_playlists_youtube()-> None:
    cls()
    youtube = autenticar_youtube()
    playlists: list = obtener_playlists_youtube(youtube)
    print(f"Playlists de Youtube: ")
    
    for i,playlist in enumerate(playlists):
        print(f"{i + 1} - {playlist['snippet']['title']}")

        
def crear_una_playlist_youtube():
    id_request = id_request.execute()
    nombre = input("Ingrese el nombre de la nueva playlist: ")
    descr = input("ingrese la descripcion (opcional): ")
    if len(descr) == 0:
        descr = None
    else:
        descr= descr
    playlists_insert_response = youtube.playlists().insert(
    part="snippet,status",
    body=dict(
        snippet=dict(
            title=nombre,
            description= descr
            ),
            status=dict(
            privacyStatus="public"
            )
        )
    ).execute()

    print("id de la playlist: ", playlists_insert_response["id"])
    return None
        
