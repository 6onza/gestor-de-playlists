import os

# direccion del path principal
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# tekore .cfg path
FILE_TEKORE = os.path.join(BASE_DIR, "tekore.cfg")


# carpeta donde se exportan las playlists
PLAYLISTS_DIR = os.path.join(BASE_DIR, "playlists")

# credenciales de la api spotify
CLIENT_ID_SPOTIFY = '1e0c8ce0ab5c4bb6a4bdf6735ab9e950'
CLIENT_SECRET_SPOTIFY = '9ecfcf4d27d94a4e908c644b45b68f84'
REDIRECT_URI_SPOTIFY = 'https://localhost:8000/callback'

# credenciales de la api de genius
CLIENT_ID_GENIUS = "fYI4WYtFKPrbhG40VGPhGd2rv7pLBmMCpjIG3mgrl1JmXxcESW6YozwTg7CjvZu_"
CLIENT_SECRET_GENIUS = "7oaL53G1sgCaATqX1bXcrtA7uj9taxe6KhCPXfnyV7Xof9BXSqCVWF5E_284OmXQVRAMV_WPyusMNyA5p0e6PA"


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

