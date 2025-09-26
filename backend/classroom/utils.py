from flask import session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_classroom_service():
    """Construye y devuelve un objeto de servicio de la API de Classroom.

    Utiliza las credenciales almacenadas en la sesión del usuario.
    Devuelve None si el usuario no está autenticado.
    """
    if 'credentials' not in session:
        return None

    creds = Credentials(**session['credentials'])

    try:
        service = build('classroom', 'v1', credentials=creds)
        return service
    except HttpError as error:
        # En un caso real, aquí podrías manejar errores de API de forma más robusta
        print(f'Ocurrió un error al construir el servicio: {error}')
        return None
