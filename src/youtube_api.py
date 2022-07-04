import os
from utils import cls
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# ########### SCOPES PARA LA API DE YOUTUBE ################################
SCOPES_READ_ONLY: list = ["https://www.googleapis.com/auth/youtube.readonly"]
SCOPES_PARA_MODIFICAR: list = ["https://www.googleapis.com/auth/youtube.force-ssl"]
#######################################3####################################
api_service_name: str = "youtube"
api_version: str = "v3"
client_secrets_file: str = "credentials.json"

def autenticar_youtube(scopes: list) -> googleapiclient.discovery.Resource:
    """ Autentica al usuario en Youtube y devuelve un objeto Resource

    Returns:
        googleapiclient.discovery.Resource: Objeto Resource de Youtube
    """
    # obtengo las credenciales de la API Sy el API Client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
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
    youtube = autenticar_youtube(SCOPES_READ_ONLY)
    playlists: list = obtener_playlists_youtube(youtube)

    print(f"Playlists de Youtube: ")
    
    for i,playlist in enumerate(playlists):
        print(f"{i + 1} - {playlist['snippet']['title']}")

        
def crear_una_playlist_youtube():

    youtube = autenticar_youtube(SCOPES_PARA_MODIFICAR)

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
        print("Hubo un error al crear la playlist: ", e)")
        input("Pulsa enter para continuar...") 
