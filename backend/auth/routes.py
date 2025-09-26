
import os
import json
from flask import Blueprint, redirect, request, session, url_for
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

auth_bp = Blueprint('auth', __name__)

# Configuración de OAuth
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, '..', '..', 'credentials.json') # Apunta a la raíz del proyecto
TOKEN_PATH = os.path.join(BASE_DIR, '..', '..', 'token.json') # Apunta a la raíz del proyecto

PORT = 5001 # Asegúrate que coincida con el puerto de app.py
REDIRECT_PATH = "/oauth/callback"
REDIRECT_URI = f"http://localhost:{PORT}{REDIRECT_PATH}"
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.rosters.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]

def load_client_config():
    """Carga la configuración del cliente desde credentials.json."""
    if not os.path.exists(CREDENTIALS_PATH):
        raise RuntimeError(
            "credentials.json no existe. Asegúrate de que el archivo esté en la raíz del proyecto."
        )
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "web" not in data:
        raise RuntimeError("credentials.json debe ser de tipo 'Web application'.")
    return data["web"]

@auth_bp.route("/login")
def login():
    """Inicia el flujo de autorización de Google OAuth."""
    client_config = load_client_config()
    
    flow = Flow.from_client_config(
        {"web": client_config},
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    session["state"] = state
    return redirect(auth_url)

@auth_bp.route(REDIRECT_PATH)
def oauth_callback():
    """Maneja el callback de Google OAuth."""
    state = session.get("state")
    if not state or state != request.args.get("state"):
        return "Error de estado de sesión. Intenta iniciar sesión de nuevo.", 400

    client_config = load_client_config()
    flow = Flow.from_client_config(
        {"web": client_config},
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI,
    )

    authorization_response = request.url
    try:
        flow.fetch_token(authorization_response=authorization_response)
        creds = flow.credentials

        # Guardar credenciales en la sesión del usuario
        session['credentials'] = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': list(creds.scopes) # Asegurarse de que sea una lista serializable
        }

        # Opcional: Guardar el token en un archivo para depuración o persistencia simple
        # Esto es útil para ver el token, pero en producción las credenciales
        # deberían manejarse de forma más segura y no en un archivo plano.
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

        # Redirigir al frontend
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173/')
        return redirect(frontend_url)
    except Exception as e:
        print(f"Error durante el callback de OAuth: {e}")
        return f"Error durante la autenticación: {e}", 500

@auth_bp.route("/logout")
def logout():
    """Limpia la sesión del usuario."""
    session.clear()
    return redirect("/")

@auth_bp.route("/check_auth")
def check_auth():
    """Verifica si el usuario está autenticado."""
    if 'credentials' in session:
        return {"isAuthenticated": True}
    return {"isAuthenticated": False}
