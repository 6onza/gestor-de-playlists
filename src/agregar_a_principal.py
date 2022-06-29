import os
import tekore as tk
from utils import *
from tekore import RefreshingToken, Spotify
import csv


def generar_user_token() -> RefreshingToken:

    if os.path.exists(FILE_TEKORE):

        configuracion = tk.config_from_file(FILE_TEKORE, return_refresh=True)
        user_token = tk.refresh_user_token(*configuracion[:2], configuracion[3])
        #  Esta linea es la reemplazante de la linea " user_token = tk.prompt_for_user_token(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=tk.scope.every) "
        #  o de la linea de abajo " user_token = tk.prompt_for_user_token(*conf, scope=tk.scope.every) ".
        # Ademas actualiza el archivo externo "FILE_TEKORE" con el nuevo TOKEN.
    else:
        conf = (CLIENT_ID_SPOTIFY, CLIENT_SECRET_SPOTIFY, REDIRECT_URI_SPOTIFY)
        user_token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
        tk.config_to_file(FILE_TEKORE, conf + (user_token.refresh_token,))
        #  Esto va a redireccionar a un formulario donde le pide al usuario la aceptacion de compartir los recursos de la cuenta spotify.
        #  Una vez que el usuario acepta, lo dirige al URL que indicamos arriba ( osea al REDIRECT_URI ) pero este URL tiene mas elementos
        #  agregados dentro de el (digamos que nos dirige a un URL mas extenso que al que indicamos). A su vez, si nos fijamos en la consola
        #  de pycharm, veremos que nos pide pegar a dicho URL extenso, asi que debemos copiar el URL extenso y pegarlo en la consola. Con
        #  esto se genera el token por primera vez y lo guarda en "user_token".
        #  Tambien se crea el archivo externo "FILE_TEKORE" con los siguientes datos : CLIENT_ID, CLIENT_SECRET, REDIRECT_URI y el TOKEN.

    return user_token


def llamar_api_spotify() -> Spotify:

    return tk.Spotify(generar_user_token())


def obtener_id_usuario_actual(spotify: Spotify) -> str:

    # Nota : 'spotify.current_user()' obtiene recursos del perfil del usuario actual. No requiere argumentos obligatorios.
    usuario_actual = spotify.current_user()
    id_usuario_actual = usuario_actual.id

    return id_usuario_actual

def crear_playlist_spotify(id_usuario_actual: str, spotify: Spotify) -> None:

    # Nota : ' spotify.playlist_create ' crea una lista de reproducción. Recibe como argumentos a 'user_id (str)', 'nombre_playlist (str)', 'public (bool)'
    #        y 'descripcion_playlist (str)'.
    nombre_playlist: str = input("Ingrese el nombre que le desea poner a la playlist: ")
    spotify.playlist_create(id_usuario_actual, nombre_playlist, public=True)

def mostrar_playlists_spotify(spotify: Spotify) -> None:

    # Nota : 'Spotify.followed_playlists' obtiene una lista de las listas de reproducción que posee o sigue el usuario actual.
    #         Los parametros que recibe son 'limit' y 'offset'(este ultimo no es obligatorio). Limit se corresponde al número
    #         de artículos a devolver (como maximo se puede ingresar el numero 50).
    recursos_playlists = spotify.followed_playlists(limit=50).items
    cant_playlists = recursos_playlists.__len__()

    print("------------------Lista de PLAYLISTS------------------")
    for i in range(cant_playlists):
        recurso_playlist = spotify.followed_playlists(limit=50).items[i]
        nombre_playlist = recurso_playlist.name
        print(f"{i+1} - '{nombre_playlist}'")


def buscar_playlist_spotify(spotify: Spotify) -> list:
    """ Pide un nombre de playlist para buscarla entre sus playlists seguidas y la retorna.
    Args:
        spotify (Spotify): Usuario actual.

    Returns:
        list: Playlist encontrada
    """
    nombre_playlist: str = input("Ingrese el nombre de la playlist que desea exportar: ")

    # obtengo una lista de las playlists que sigue el usuario actual
    playlists = spotify.followed_playlists(limit=50).items
    playlist_buscada: list = []

    intentar_nuevamente: bool = True

    while (intentar_nuevamente):
        total_playlists: int = playlists.__len__()
        encontrada: bool =  False

        while (not encontrada and total_playlists > 0):
            

            if (playlists[total_playlists -1].name.lower() == nombre_playlist.lower()):
                playlist_buscada = playlists[total_playlists]
                encontrada = True              
            
            else:
                total_playlists -= 1

        if (not encontrada):
            print("No se encontro la playlist.")
            continuar: str = input("Desea intentar nuevamente? (s/n) ")
            
            if (continuar.lower() == "s"):
                nombre_playlist = input("Ingrese el nombre de la playlist que desea exportar: ")
            
            else:
                intentar_nuevamente = False
                input("Se cancelo la busqueda.\nPresione enter para continuar.")
       
        else:
            intentar_nuevamente = False
            
        
        
    return playlist_buscada


def exportar_playlist_spotify(playlist_buscada: str, spotify: Spotify) -> None:
    # exporta los 10 atributos de la playlist a un archivo csv
    try:
        playlist = spotify.playlist(playlist_buscada.id)
        
        nombre_playlist: str = playlist.name
        owner: str = playlist.owner.display_name
        playlist_id: str = playlist.id
        cant_tracks: str = playlist.tracks.total
        public: str = playlist.public
        collaborative: str = playlist.collaborative
        description: str = playlist.description
        images: str = playlist.images[0].url
        followers: str = playlist.followers.total
        playlist_url: str = playlist.external_urls['spotify']

        if (not os.path.exists(PLAYLISTS_DIR)):
            os.makedirs(PLAYLISTS_DIR)

        csv_playlist_nombre: str = playlist.name.replace(" ", "_")    
        csv_playlist_path: str = os.path.join(BASE_DIR, "playlists", f"{csv_playlist_nombre}.csv")
        
        with open(csv_playlist_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow([   "Nombre", 
                                "Propietario", 
                                "ID", 
                                "Cantidad de Tracks", 
                                "Publica", 
                                "Colaborativa", 
                                "Descripcion", 
                                "Imagen", 
                                "Seguidores", 
                                "URL"])
            
            writer.writerow([   nombre_playlist, 
                                owner, 
                                playlist_id, 
                                cant_tracks, 
                                public, 
                                collaborative, 
                                description, 
                                images, 
                                followers, 
                                playlist_url])

    except Exception as e:
        print(f"No se pudo exportar la playlist: {e}")
        input("Presione enter para continuar.")
    
def sincronizar_spotify_youtube(spotify: Spotify) -> list:

    lista_canciones_playlist = list() # Aca se formara una lista de listas.

    cant_playlists = spotify.followed_playlists(limit=50).items.__len__()
    print("¿ CUAL DE TODAS SUS PLAYLISTS de SPOTIFY DESEA SINCRONIZAR CON YOUTUBE ?")
    mostrar_playlists_spotify(spotify)
    lista_de_opciones = [str(i) for i in range(1, cant_playlists + 1)]
    eleccion = validar_opcion(lista_de_opciones)
    recurso_playlist_elegida = spotify.followed_playlists(limit=50).items[eleccion - 1]
    id_playlist_elegida = recurso_playlist_elegida.id
    recursos_canciones_playlist = spotify.playlist(id_playlist_elegida, as_tracks=False).tracks
    cant_canciones_playlist_elegida = recursos_canciones_playlist.items.__len__()

    for i in range(cant_canciones_playlist_elegida):
        cancion_de_playlist = recursos_canciones_playlist.items[i].track.name
        lista_canciones_playlist.append([cancion_de_playlist])

    return lista_canciones_playlist

def main() -> None:
    """ Funcion principal. """
    spotify = llamar_api_spotify()
    id_usuario_actual = obtener_id_usuario_actual(spotify)
    # crear_playlist(id_usuario_actual, spotify)
    mostrar_playlists_spotify(spotify)
    id_playlist_buscada = buscar_playlist_spotify(spotify)
    exportar_playlist_spotify(id_playlist_buscada, spotify)
    lista_de_canciones_playlist = sincronizar_spotify_youtube(llamar_api_spotify())
    print(lista_de_canciones_playlist)
main()