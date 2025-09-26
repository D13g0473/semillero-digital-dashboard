import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/classroom.courses.readonly"]

def main():
    creds = None
    # Force re-authentication
    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(os.path.dirname(__file__), '..', 'credentials.json'), SCOPES
    )
    creds = flow.run_local_server(port=8080)

    # Save the credentials for the next run
    with open(os.path.join(os.path.dirname(__file__), '..', 'token.json'), "w") as token:
        token.write(creds.to_json())
    
    print("¡Token guardado correctamente en token.json!")

    try:
        service = build("classroom", "v1", credentials=creds)

        # Call the Classroom API
        results = service.courses().list(pageSize=10).execute()
        courses = results.get("courses", [])

        if not courses:
            print("No se encontraron cursos.")
            return

        print("Cursos:")
        for course in courses:
            print(f"- {course['name']}")

    except HttpError as error:
        print(f"Ocurrió un error: {error}")

if __name__ == "__main__":
    main()