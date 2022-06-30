import os
import tekore as tk
from utils import *
from tekore import RefreshingToken, Spotify
import csv
from llamar_apis import *
from generar_wordcloud import generar_wc
import quickstart


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


def mostrar_una_playlist() -> None:
    plataforma: str = seleccionar_plataforma()
   
    if (plataforma == "spotify"):
        spotify = llamar_api_spotify()
        mostrar_playlists_spotify(spotify)
    else:
        quickstart.main()
        


def main() -> None:

    cls()
    
    continuar_ejecucion: bool = True
    
    while (continuar_ejecucion):
        print("""
        [1] Listar las playlists actuales para un determinado usuario y plataforma
        [2] Elegir una playlist y exportarla a CSV indicando los 10 atributos principales
        [3] Crear una nueva playlist
        [4] Buscar nuevos elementos para visualizar o agregarlos a una playlist
        [5] Sincronizar una playlist entre Youtube y Spotify, (se exportaran en un archivo
            CSV los elementos que no encuentren en la plataforma de destino)
        [6] Analizar una playlist y construir la nube de palabras y el ranking del top 10 de
            palabas más utilizadas en las letras de dicha playlist
        [7] Salir
        """)
        option: str = validar_opcion(["1", "2", "3", "4", "5", "6"])

        if (option == "1"):
            mostrar_una_playlist()

        elif (option == "2"):
            spotify: Spotify = llamar_api_spotify()
            exportar_playlist_spotify(spotify)
        
        elif (option == "3"):
            spotify: Spotify = llamar_api_spotify()
            crear_playlist_spotify(spotify.current_user().id, spotify)

        elif (option == "4"):   
            pass

        elif (option == "5"):
            pass

        elif (option == "6"):
            spotify: Spotify = llamar_api_spotify()
            generar_wc(spotify)

        elif (option == "7"):
            continuar_ejecucion = False

main()
