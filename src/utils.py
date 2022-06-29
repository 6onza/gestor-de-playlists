import os

# direccion del path principal
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# tekore .cfg path
FILE_TEKORE = os.path.join(BASE_DIR, "tekore.cfg")


# carpeta donde se exportan las playlists
PLAYLISTS_DIR = os.path.join(BASE_DIR, "playlists")

# credenciales de las apis
CLIENT_ID = '1e0c8ce0ab5c4bb6a4bdf6735ab9e950'
CLIENT_SECRET = '9ecfcf4d27d94a4e908c644b45b68f84'
REDIRECT_URI = 'https://localhost:8000/callback'


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

