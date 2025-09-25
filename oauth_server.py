import json
import os
from flask import Flask, redirect, request, session, url_for
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# Config
PORT = 5001
REDIRECT_PATH = "/oauth/callback"
REDIRECT_URI = f"http://localhost:{PORT}{REDIRECT_PATH}"
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
]

app = Flask(__name__)
# WARNING: For demo purposes only. Replace with a secure random secret in production.
app.secret_key = "dev-secret-change-me"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")


def load_client_config():
    if not os.path.exists(CREDENTIALS_PATH):
        raise RuntimeError(
            "credentials.json no existe. Crea este archivo con las credenciales OAuth de tipo 'Web application'."
        )
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "web" not in data:
        raise RuntimeError("credentials.json no tiene la clave 'web'. Asegúrate de usar credenciales de tipo 'Web application'.")
    return data["web"]


@app.route("/")
def index():
    return (
        "<h3>OAuth Google Classroom</h3>"
        "<p><a href='/login'>Iniciar autenticación</a></p>"
    )


@app.route("/login")
def login():
    web_config = load_client_config()

    flow = Flow.from_client_config(
        {"web": web_config},
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


@app.route(REDIRECT_PATH)
def oauth_callback():
    state = session.get("state")
    if not state:
        return "Falta 'state' en la sesión. Vuelve a /login", 400

    web_config = load_client_config()
    flow = Flow.from_client_config(
        {"web": web_config},
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI,
    )

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    creds = flow.credentials

    # Guardar en formato de usuario autorizado (compatible con Credentials.from_authorized_user_file)
    authorized_user = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": web_config.get("client_id"),
        "client_secret": web_config.get("client_secret"),
        "scopes": list(creds.scopes or SCOPES),
    }

    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        json.dump(authorized_user, f, indent=2)

    return (
        "<p>Autenticación completada. Se generó token.json.</p>"
        "<p>Ahora puedes cerrar este servidor y ejecutar: <code>python3 google-classroom-api.py</code></p>"
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=True)
