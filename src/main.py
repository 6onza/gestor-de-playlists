import os
import tekore as tk
from utils import *
from tekore import RefreshingToken, Spotify
import csv
from spotify_api import *
from youtube_api import *
from generar_wordcloud import generar_wc


def sincronizar_spotify_youtube(spotify, youtube) -> None:

    lista_playlists_spotify: list = list()
    lista_playlists_youtube: list = list()

    cant_playlists_spotify:int = spotify.followed_playlists(limit=50).items.__len__()

    for i in range(cant_playlists_spotify):
        recurso_playlist = spotify.followed_playlists(limit=50).items[i]
        lista_playlists_spotify.append([recurso_playlist.name, recurso_playlist.id])

    playlists_youtube: list = obtener_playlists_youtube(youtube)

    for j in range(len(playlists_youtube)):
        playlist_youtube = playlists_youtube[j]
        lista_playlists_youtube.append([playlist_youtube["snippet"]["title"], playlist_youtube["id"]])

    lista_playlists_spotify_posible_sincronizacion: list = list()
    lista_playlists_youtube_posible_sincronizacion: list = list()

    for elemento_spotify in lista_playlists_spotify:
        for elemento_youtube in lista_playlists_youtube:
            if elemento_youtube[0] == elemento_spotify[0]:
                lista_playlists_youtube_posible_sincronizacion.append(elemento_youtube)
                lista_playlists_spotify_posible_sincronizacion.append(elemento_spotify)

    if lista_playlists_youtube_posible_sincronizacion != []:    #  Es indiferente si ponia "lista_playlist_spotify_posible_sincronizacion" por como armamos el
                                                                #  codigo arriba (cuando llenabamos "lista_playlist_youtube_posible_sincronizacion" a la vez se
                                                                #  llenaba "lista_playlist_spotify_posible_sincronizacion").

        for k in range(len(lista_playlists_youtube_posible_sincronizacion)):      #   Es indiferente si ponia "lista_playlist_spotify_posible_sincronizacion" por
                                                                                  #   como armamos el codigo arriba (cuando llenabamos
                                                                                  #   "lista_playlist_youtube_posible_sincronizacion" a la vez se llenaba
                                                                                  #   "lista_playlist_spotify_posible_sincronizacion").

            print(f"{k + 1} - {lista_playlists_youtube_posible_sincronizacion[k][0]}")

        lista_de_opciones: list = [str(i) for i in range(1, len(lista_playlists_youtube_posible_sincronizacion) + 1)]
        eleccion: int = int(validar_opcion(lista_de_opciones))

        datos_playlist_youtube_a_sincronizar: list = lista_playlists_youtube_posible_sincronizacion[eleccion - 1]
        datos_playlist_spotify_a_sincronizar: list = lista_playlists_spotify_posible_sincronizacion[eleccion - 1]

        lista_de_canciones_playlist_spotify_a_sincronizar: list = list()
        lista_de_canciones_playlist_youtube_a_sincronizar: list = list()

        # Comenzamos llenando "lista_de_canciones_playlist_spotify_a_sincronizar"
        id_playlist_spotify_a_sincronizar: str = datos_playlist_spotify_a_sincronizar[1]
        recursos_canciones_playlist_spotify_a_sincronizar = spotify.playlist(id_playlist_spotify_a_sincronizar, as_tracks=False).tracks
        cant_canciones_playlist_spotify_a_sincronizar: int = recursos_canciones_playlist_spotify_a_sincronizar.items.__len__()

        for a in range(cant_canciones_playlist_spotify_a_sincronizar):
            cancion_de_playlist_spotify_a_sincronizar = recursos_canciones_playlist_spotify_a_sincronizar.items[a].track
            nombre_cancion_de_playlist_spotify_a_sincronizar: str = cancion_de_playlist_spotify_a_sincronizar.name
            artista_cancion_de_playlist_spotify_a_sincronizar: str = cancion_de_playlist_spotify_a_sincronizar.artists[0].name
            lista_de_canciones_playlist_spotify_a_sincronizar.append([nombre_cancion_de_playlist_spotify_a_sincronizar.lower(), artista_cancion_de_playlist_spotify_a_sincronizar])

        # Seguimos llenando "lista_de_canciones_playlist_youtube_a_sincronizar"
        id_playlist_youtube_a_sincronizar: str = datos_playlist_youtube_a_sincronizar[1]
        canciones_playlist_youtube_a_sincronizar: list = obtener_canciones_de_una_playlist_youtube(id_playlist_youtube_a_sincronizar, youtube)

        for b in range(len(canciones_playlist_youtube_a_sincronizar)):
            cancion_de_playlist_youtube_a_sincronizar = canciones_playlist_youtube_a_sincronizar[b]
            nombre_cancion_de_playlist_youtube_a_sincronizar: str = cancion_de_playlist_youtube_a_sincronizar["snippet"]["title"]

            #  PUEDE SER que necesitemos buscar este "nombre_cancion_de_playlist_youtube_a_sincronizar" en Spotify, asi que vamos a tener que eliminar el
            #  "(Video Oficial)" o "(Official Video)" o "(Official Music Video)" que aparecen en los nombres de las canciones de Youtube porque en spotify
            #  no hay resultados de "(Video Oficial)" o "(Official Video)" o "(Official Music Video)".
            nombre_cancion_de_playlist_youtube_a_sincronizar = nombre_cancion_de_playlist_youtube_a_sincronizar.replace("(Official Video)", "")
            nombre_cancion_de_playlist_youtube_a_sincronizar = nombre_cancion_de_playlist_youtube_a_sincronizar.replace("(Video Oficial)", "")
            nombre_cancion_de_playlist_youtube_a_sincronizar = nombre_cancion_de_playlist_youtube_a_sincronizar.replace("(Official Music Video)", "")

            #  En el "nombre_cancion_de_playlist_youtube_a_sincronizar", Youtube trae el nombre de la cancion junto con todos los artistas de la cancion.
            #  NORMALMENTE el nombre de la cancion y el nombre del artista vienen separados por el simbolo "-" (donde a la izquierda de este simbolo se ubica
            #  el nombre del artista y a la derecha de ese simbolo se ubica el nombre de la cancion). Entonces trabajare con "nombre_cancion_de_playlist_youtube_a_sincronizar"
            #  para obtener al nombre de la cancion (pero unicamente al nombre) y el nombre del artista.
            posicion_caracter_especial: int = nombre_cancion_de_playlist_youtube_a_sincronizar.find("-")
            artista_cancion_de_playlist_youtube_a_sincronizar: str = nombre_cancion_de_playlist_youtube_a_sincronizar[0:posicion_caracter_especial:1]
            unicamente_nombre_cancion_de_playlist_youtube_a_sincronizar: str = nombre_cancion_de_playlist_youtube_a_sincronizar[posicion_caracter_especial + 1::1]

            lista_de_canciones_playlist_youtube_a_sincronizar.append([unicamente_nombre_cancion_de_playlist_youtube_a_sincronizar.lower(), artista_cancion_de_playlist_youtube_a_sincronizar])

        canciones_a_exportar_a_csv: list = list()
        # Primero vamos a ver cancion por cancion de la playlist de youtube si se encuentra en algunas de las canciones de spotify.
        for cancion_youtube in lista_de_canciones_playlist_youtube_a_sincronizar:
            coincidencias: int = 0
            for cancion_spotify in lista_de_canciones_playlist_spotify_a_sincronizar:
                if (cancion_spotify[0] in cancion_youtube[0]):
                    coincidencias += 1
            if coincidencias == 0:
                nombre_cancion_de_youtube_a_agregar_a_spotify: str = cancion_youtube[0] + " " + cancion_youtube[1]
                busqueda_de_cancion_en_spotify = spotify.search(nombre_cancion_de_youtube_a_agregar_a_spotify, types=('track',), limit=1)[0]
                cancion_encontrada_en_spotify = busqueda_de_cancion_en_spotify.items[0]
                uri_cancion_encontrada_en_spotify = cancion_encontrada_en_spotify.uri
                spotify.playlist_add(datos_playlist_spotify_a_sincronizar[1], uris=[uri_cancion_encontrada_en_spotify])
                canciones_a_exportar_a_csv.append(cancion_youtube)


        with open("canciones_a_sincronizar.csv", 'w', newline='', encoding="UTF-8") as archivo_csv:

            csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

            csv_writer.writerow(["Titulo de cancion", "Artistas"])

            csv_writer.writerows(canciones_a_exportar_a_csv)


    else:
        print("Lo siento, no hay playlists a sincronizar") 


def mostrar_playlists() -> None:
    plataforma: str = seleccionar_plataforma()
   
    if (plataforma == "spotify"):
        spotify: Spotify = llamar_api_spotify()
        mostrar_playlists_spotify(spotify)
    else:
        youtube = autenticar_youtube()
        mostrar_playlists_youtube(youtube)      


def exportar_atributos_de_una_playlist()->None:
    plataforma: str = seleccionar_plataforma()
    
    if (plataforma == "spotify"):
        spotify: Spotify = llamar_api_spotify()
        exportar_playlist_spotify(spotify)
    else:
        youtube = autenticar_youtube()
        exportar_playlist_youtube(youtube)


def crear_una_playlist()->None:
    plataforma: str = seleccionar_plataforma()
    
    if (plataforma == "spotify"):
        spotify: Spotify = llamar_api_spotify()
        id_user = spotify.current_user().id
        crear_playlist_spotify(id_user, spotify)
    else:
        youtube = autenticar_youtube()
        crear_una_playlist_youtube(youtube)


def agregar_una_cancion_a_playlist() -> None:
    plataforma: str = seleccionar_plataforma()
    
    if (plataforma == "spotify"):
        spotify: Spotify = llamar_api_spotify()
        seguir_agregando: bool = True
        while seguir_agregando:
            buscar_nuevos_elementos(spotify)
            seguir_agregando: bool = input("¿ Desea agregar otra canción a la playlist? (s/n) ")
            
            if (seguir_agregando == "s"):
                seguir_agregando: bool = True
            
            elif (seguir_agregando == "n"):
                seguir_agregando: bool = False
    else:
        youtube = autenticar_youtube()
        agregar_un_item_a_la_playlist_youtube(youtube)
    

def main() -> None:

    cls()
    
    continuar_ejecucion: bool = True
    
    while (continuar_ejecucion):
        cls()
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
            mostrar_playlists()
            input("Pulse enter para volver al menú")

        elif (option == "2"):
            exportar_atributos_de_una_playlist()
        
        elif (option == "3"):
            crear_una_playlist()

        elif (option == "4"):   
            agregar_una_cancion_a_playlist()

        elif (option == "5"):
            print(sincronizar_spotify_youtube(llamar_api_spotify()))

        elif (option == "6"):
            generar_wc()

        elif (option == "7"):
            continuar_ejecucion = False

main()
