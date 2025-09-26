from flask import Blueprint, jsonify
from .utils import get_classroom_service
from .courses import get_teacher_courses_with_metrics # <-- Importar la nueva función

api_bp = Blueprint('api', __name__)

@api_bp.route("/teacher/dashboard")
def get_teacher_dashboard():
    """Endpoint para obtener los cursos y métricas del profesor."""
    data = get_teacher_courses_with_metrics()
    if isinstance(data, tuple): # Manejar el caso de error
        error_msg, status_code = data
        return jsonify(error_msg), status_code
    return jsonify(data)

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
