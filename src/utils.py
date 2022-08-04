import os
from tekore import Spotify

# direccion del path principal
BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))


# tekore .cfg path
FILE_TEKORE: str = os.path.join(BASE_DIR, "tekore.cfg")


# carpeta donde se exportan las playlists
PLAYLISTS_DIR: str = os.path.join(BASE_DIR, "playlists")

# credenciales de la api spotify
CLIENT_ID_SPOTIFY: str = os.environ.get("CLIENT_ID_SPOTIFY")
CLIENT_SECRET_SPOTIFY: str = os.environ.get("CLIENT_SECRET_SPOTIFY")
REDIRECT_URI_SPOTIFY: str = os.environ.get("REDIRECT_URI_SPOTIFY")

# credenciales de youtube
API_KEY_YOUTUBE: str = os.environ.get("API_KEY_YOUTUBE")

# credenciales de la api de genius
CLIENT_ID_GENIUS: str = os.environ.get("CLIENT_ID_GENIUS")
CLIENT_SECRET_GENIUS: str = os.environ.get("CLIEN_SECRET_GENIUS")


def cls() -> None:
    """Limpia la terminal segun el sistema operativo"""

    command: str = 'clear'

    if os.name in ('nt', 'dos'):
        command = 'cls'

    os.system(command)


def validar_opcion(options: list) -> str:
    """Valida si la opción esta en la lista de opciones
    Args:
        options (list): Lista con las opciones disponibles
    Returns:
        str: Opción elegida
    """

    option: str = input("-> ")

    while (option not in options):
        option = input("Opción invalida, intente nuevamente: ")

    return option

def seleccionar_plataforma()-> str:
    print("Elija una la plataforma: ")
    print("[1]- Spotify")
    print("[2] - Youtube")
    
    opcion: str = validar_opcion(["1", "2"])
    
    if (opcion == "1"):
        return "spotify"
    else:
        return "youtube"   
