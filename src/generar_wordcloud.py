from utils import *
from tekore import Spotify
from wordcloud import WordCloud
from spotify_api import *
from lyricsgenius import Genius
import re
import matplotlib.pyplot as plt


def obetener_info_de_tracks(spotify: Spotify)-> dict:
    """obtiene la informacion de las canciones de la playlist elegida del usuario actual
    Args:
        spotify (Spotify): Instancia de la api de spotify

    Returns:
        dict: Diccionario con la informacion de las canciones
    """
    playlist_tracks_info = {}

    id_playlist_buscada = buscar_playlist_spotify(spotify)
    playlist = spotify.playlist(id_playlist_buscada)

    # obtengo los objetos 'PlaylistTrack' de la playlist
    oj_playlist_tracks = playlist.tracks.items
    # guardo la el nombre de la cancion y el nombre del artista
    for oj_track in oj_playlist_tracks:
        playlist_tracks_info[oj_track.track.name] = oj_track.track.artists[0].name
    
    return playlist_tracks_info


def limpiar_letras(letras: tuple) -> str:
    """limpia las letras de las canciones de playlist elegida del usuario actual"""
    # creo un string con todas las letras de las canciones
    letras_canciones_string = ' '.join(letras)

    letras_canciones_string = letras_canciones_string.replace('\n', ' ')
    letras_canciones_string = letras_canciones_string.replace('\r', ' ')
    # elimino el "(Text Back)" de las letras
    letras_canciones_string = re.sub(r'\(Text Back\)', '', letras_canciones_string) 
    # elimino lo que esta entre [] en las letras
    letras_canciones_string = re.sub(r'\[.*?\]', '', letras_canciones_string)
    
    return letras_canciones_string
    

def generar_wc(spotify: Spotify):
    """genera un wordcloud con las letras de las canciones de playlist elegida del usuario actual"""
    genius = Genius(CLIENT_ID_GENIUS)
    playlist_tracks_info = obetener_info_de_tracks(spotify)

    # creo un diccionario con las letras de las canciones
    letras_canciones = {}

    for key, value in playlist_tracks_info.items():
        letras_canciones[key] = genius.search_song(value, key)
    
    for key, value in letras_canciones.items():
        
        if value is None:
            letras_canciones[key] = ''
        else:
            letras_canciones[key] = value.lyrics

    # limpio las letras
    letras_str: str = limpiar_letras(letras_canciones.values())
    # genero un wordcloud con las letras de las canciones
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_words=10).generate(letras_str)
    # muestro el wordcloud
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
