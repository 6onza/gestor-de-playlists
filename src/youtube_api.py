import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors



def mostrar_playlists_youtube():
    ##############################################################################
    # consigo la id del usuario autenticado
    id_request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    id_response = id_request.execute()
    channel_id = id_response["items"][0]["id"]
   ###############################################################################
   
   ###############################################################################
   # consigo las playlists del usuario autenticado

    pl_request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        maxResults=25,
    )
    response = pl_request.execute()
   #################################################################################
    # muestro los nombres de las playlist
    print("Playlists de Youtube: ")
    
    for i,playlist in enumerate(response["items"]):
        print(f"{i + 1} {playlist['snippet']['title']}")
    

if __name__ == "__main__":
    SCOPES: list = ["https://www.googleapis.com/auth/youtube.readonly"]
    api_service_name: str = "youtube"
    api_version: str = "v3"
    client_secrets_file: str = "credentials.json"

    # obtengo las credenciales de la API Sy el API Client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    credentials = flow.run_console()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)