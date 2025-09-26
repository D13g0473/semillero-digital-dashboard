from flask import Blueprint, jsonify
from .utils import get_classroom_service

api_bp = Blueprint('api', __name__)

@api_bp.route("/courses")
def get_courses():
    """Endpoint para obtener la lista de cursos del usuario autenticado."""
    service = get_classroom_service()
    if not service:
        return jsonify({"error": "Usuario no autenticado"}), 401

    try:
        results = service.courses().list(pageSize=20).execute()
        courses = results.get('courses', [])
        return jsonify(courses)
    except Exception as e:
        # Manejo básico de errores
        return jsonify({"error": str(e)}), 500
