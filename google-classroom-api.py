import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Definir el alcance de la API (modificar según necesidades)
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']

def main():
    creds = None
    # El token se guarda en token.json después del primer login
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('classroom', 'v1', credentials=creds)
        # Ejemplo: obtener lista de cursos
        results = service.courses().list(pageSize=10).execute()
        courses = results.get('courses', [])
        if not courses:
            print('No se encontraron cursos.')
        else:
            print('Cursos:')
            for course in courses:
                print(course['name'])
    except HttpError as error:
        print(f'Ocurrió un error: {error}')

if __name__ == '__main__':
    main()
