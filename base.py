# 1 Autenticarse con un perfil en las plataformas Youtube y Spotify
lista_de_perfiles: list = []

usuario_youtube: str = input("Ingrese su nombre de usuario de Youtube")
clave_youtube: str = input("Ingrese su contraseña de Youtube")
usuario_spotify: str = input("Ingrese su nombre de usuario de Spotify")
clave_spotify: str = input("Ingrese su contraseña de Spotify")

spotify = {
    "usuario": usuario_spotify,
    "clave": clave_spotify
}

youtube = {
    "usuario": usuario_youtube,
    "clave": clave_youtube
}
# autenticar perfiles e ingresar a cada plataforma

# 2 Listar las playlists actuales para un determinado usuario y plataforma
'''NECESITAMOS VER BIEN LO DE LAS APIS'''


 playlists_del_usuario_youtube: list = []
 playlists_del_usuario_spotify: list = []
 #SPOTIFY
 for item in spotify:
       if item == "playlist_spotify":
 for playlists in playlists_spotify:

 for playlists in range(len(playlists_del_usuario)):
       print(i," - ", playlists_del_usuario_spotify, " (SPOTIFY)"


# 3 Poder elegir una playlist y exportarla a CSV indicando los 10 atributos
# principales.

# 4 Crear una nueva playlist en una determinada plataforma
def crear_playlist(plataforma: str) -> list:
    if plataforma != "SPOTIFY" or plataforma != "YOUTUBE":
        print("plataforma incorrecta")
        plataforma = input("INGRESE SU PLATAFORMA: ")
    elif plataforma == "SPOTIFY":
        nueva_playlist: list = []
        nombre: str = input("INGRESE EL NOMBRE DE LA PLAYLIST NUEVA: ")
        cancion: str = input("Ingrese el nombre de la cancion que quiera agregar,\n"
                             "presione enter para finalizar.")
        while cancion != "":
            #  buscar la cancion en dicha plataforma.
            cancion: str = input("Ingrese el nombre de la cancion que quiera agregar,\n"
                                 "presione enter para finalizar.")
        if cancion == "":
            return nueva_playlist
    elif plataforma == "YOUTUBE":
        nueva_playlist: list = []
        cancion: str = input("Ingrese el nombre de la cancion que quiera agregar,\n"
                             "presione enter para finalizar.")
        while cancion != "":
            #  buscar la cancion en dicha plataforma.
            cancion: str = input("Ingrese el nombre de la cancion que quiera agregar,\n"
                                 "presione enter para finalizar.")
        if cancion == "":
            return nueva_playlist

# 5 Buscar nuevos elementos para visualizar o agregarlos a una playlist, en el caso
# de resultado múltiple traer las 3 opciones mas reproducidas y darle a elegir al
# usuario con cual desea quedarse. A su vez, y en el caso que corresponda poder
# mostrar su letra.
#
# printear las playlist de cada plataforma con un numero.

        seleccion_de_playlist: str = input("SELECCIONE SU PLAYLIST: ")
        if not seleccion_de_playlist.isnumeric():
                print("PLAYLIST INCORRECTA O INEXISTENTE")
                seleccion_de_playlist: str = input("SELECCIONE SU PLAYLIST: ")
        elif seleccion_de_playlist > len(playlists)
                print("PLAYLIST INCORRECTA O INEXISTENTE")
                seleccion_de_playlist: str = input("SELECCIONE SU PLAYLIST: ")
        elif seleccion_de_playlist == playlists[i]:

# 6 Sincronizar una determinada playlist entre ambas plataformas, exportando en
# CSV los elementos que no encuentren en la plataforma de destino.

# printear todas las playlists
# seleccionar una playlist de x plataforma
# clonar dicha playlist en la otra plataforma
if yt in lista[i]:
        crear_playlist(s)


1[a, yt]
2[]
3c
4d

# 7 Analizar una playlist y construir la nube de palabras y el ranking del top 10 de
# palabas más utilizadas en las letras de dicha playlist (debe analizarse el
# contenido de las letras y filtrar los comentarios). 
