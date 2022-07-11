import os
import tekore as tk
import csv
from utils import *
from tekore import RefreshingToken, Spotify

def generar_user_token() -> RefreshingToken:
    """Genera un token de usuario para la api de spotify

    Returns:
        RefreshingToken: Token de usuario para la api de spotify
    """

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
    """Llama a la api de spotify y retorna un objeto de tipo Spotify

    Returns:
        Spotify: Objeto de tipo Spotify
    """

    return tk.Spotify(generar_user_token())


def buscar_playlist_spotify(spotify: Spotify) -> str:
    """ Pide un nombre de playlist para buscarla entre sus playlists seguidas y la retorna.
    Args:
        spotify (Spotify): Usuario actual.
    Returns:
        list: Playlist encontrada
    """
    mostrar_playlists_spotify(spotify)
    playlists = spotify.followed_playlists(limit=50).items
    print("Seleccione una playlist")
    opcion: str = validar_opcion([str(i) for i in range(1, len(playlists) + 1)])
    return playlists[int(opcion) - 1].id
        
    return id_playlist_buscada
    

def mostrar_playlists_spotify(spotify: Spotify) -> None:

    # Nota : 'Spotify.followed_playlists' obtiene una lista de las listas de reproducción que posee o sigue el usuario actual.
    #         Los parametros que recibe son 'limit' y 'offset'(este ultimo no es obligatorio). Limit se corresponde al número
    #         de artículos a devolver (como maximo se puede ingresar el numero 50).
    recursos_playlists = spotify.followed_playlists(limit=50).items
    cant_playlists = recursos_playlists.__len__()

    print("------------------Lista de PLAYLISTS------------------")
    for i in range(cant_playlists):
        recurso_playlist = recursos_playlists[i]
        nombre_playlist = recurso_playlist.name
        print(f"{i+1} - '{nombre_playlist}'") 


def obtener_id_usuario_actual(spotify: Spotify) -> str:
    
    # Nota : 'spotify.current_user()' obtiene recursos del perfil del usuario actual. No requiere argumentos obligatorios.
    usuario_actual = spotify.current_user()
    id_usuario_actual = usuario_actual.id

    return id_usuario_actual


def crear_playlist_spotify(id_usuario_actual: str, spotify: Spotify) -> None:

    # Nota : ' spotify.playlist_create ' crea una lista de reproducción. Recibe como argumentos a 'user_id (str)', 'nombre_playlist (str)', 'public (bool)'
    #        y 'descripcion_playlist (str)'.
    try:
        nombre_playlist: str = input("Ingrese el nombre que le desea poner a la playlist: ")
        spotify.playlist_create(id_usuario_actual, nombre_playlist, public=True)
        print("Playlist creada con exito")
        input("Presione enter para continuar")
        
    except Exception as e:
        print(f"No se pudo crear la playlist: {e}")
        input("Presione enter para continuar.")


def exportar_playlist_spotify(spotify: Spotify) -> None:
    # exporta los 10 atributos de la playlist a un archivo csv
    id_playlist_buscada: str = buscar_playlist_spotify(spotify)
    
    try:
        playlist = spotify.playlist(id_playlist_buscada)
        
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
        
        with open(csv_playlist_path, "w", encoding="utf-8") as f:
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

        input("Playlist exportada correctamente.\nPresione enter para continuar.")

    except Exception as e:
        print(f"No se pudo exportar la playlist: {e}")
        input("Presione enter para continuar.")


def agregar_canciones_a_la_playlist(id_playlist_a_modificar: str, uri_de_cancion: list, spotify: Spotify):
    agregar_cancion = spotify.playlist_add(id_playlist_a_modificar, uri_de_cancion)
    input("Canción agregada.\nPresione enter para continuar.")
    return agregar_cancion


def buscar_nuevos_elementos(spotify: Spotify):

    id_playlist_buscada: str = buscar_playlist_spotify(spotify)
    nombre_elemento: str = input("Ingrese el nombre del elemento que quiere agregar a la playlist: ")
    busqueda: tuple = spotify.search(query=nombre_elemento, limit=3)
    opciones_de_cancion: list = []
    #busqueda[0].items
    for i in range(len(busqueda[0].items)):
        opciones_de_cancion.append(busqueda[0].items[i])
    for i in range(3):
        print(i + 1, opciones_de_cancion[i].name, " - ", opciones_de_cancion[i].artists[0].name)
    seleccion: str = validar_opcion(["1", "2", "3"])
    
    print(opciones_de_cancion[0].name, "-", opciones_de_cancion[0].artists[0].name)
    uri_cancion_a_agregar: str = opciones_de_cancion[int(seleccion) - 1].uri
    uris: list = [uri_cancion_a_agregar]
    agregar_canciones_a_la_playlist(id_playlist_buscada, uris, spotify)
