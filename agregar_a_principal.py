
import os
import tekore as tk
from tekore import RefreshingToken, Spotify


CLIENT_ID = 'a86e89bf14a140028a500924baa6e1aa'
CLIENT_SECRET = '556d02cf69434829938abda6cf5d10a4'
REDIRECT_URI = 'https://example.com/callback'
FILE_TEKORE = 'tekore.cfg'             #ARCHIVO TEKORE



def generar_user_token() -> RefreshingToken:

    if os.path.exists(FILE_TEKORE):

        configuracion = tk.config_from_file(FILE_TEKORE, return_refresh=True)
        user_token = tk.refresh_user_token(*configuracion[:2], configuracion[3])
        #  Esta linea es la reemplazante de la linea " user_token = tk.prompt_for_user_token(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=tk.scope.every) "
        #  o de la linea de abajo " user_token = tk.prompt_for_user_token(*conf, scope=tk.scope.every) ".
        # Ademas actualiza el archivo externo "FILE_TEKORE" con el nuevo TOKEN.
    else:
        conf = (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
        user_token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
        tk.config_to_file(FILE_TEKORE, conf + (user_token.refresh_token,))
        #  Esto va a redireccionar a un formulario donde le pide al usuario la aceptacion de compartir los recursos de la cuenta spotify.
        #  Una vez que el usuario acepta, lo dirige al URL que indicamos arriba ( osea al REDIRECT_URI ) pero este URL tiene mas elementos
        #  agregados dentro de el (digamos que nos dirige a un URL mas extenso que al que indicamos). A su vez, si nos fijamos en la consola
        #  de pycharm, veremos que nos pide pegar a dicho URL extenso, asi que debemos copiar el URL extenso y pegarlo en la consola. Con
        #  esto se genera el token por primera vez y lo guarda en "user_token".
        #  Tambien se crea el archivo externo "FILE_TEKORE" con los siguientes datos : CLIENT_ID, CLIENT_SECRET, REDIRECT_URI y el TOKEN.

    return user_token
