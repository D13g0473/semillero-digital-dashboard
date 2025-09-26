import os
from flask import Flask, session
from flask_cors import CORS # Importar CORS
from auth.routes import auth_bp
from classroom.routes import api_bp

app = Flask(__name__)

# Clave secreta para manejar sesiones


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-me")

# Configurar CORS para permitir peticiones desde el frontend
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Registrar Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    if 'credentials' in session:
        return "Usuario autenticado. <a href='/auth/logout'>Cerrar sesión</a>. <a href='/api/courses'>Ver cursos (JSON)</a>"
    return "Backend de Semillero Digital funcionando. <a href='/auth/login'>Iniciar sesión</a>"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
