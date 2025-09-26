from .utils import get_classroom_service
from collections import defaultdict

def get_teacher_courses_with_metrics():
    """
    Obtiene los cursos donde el usuario es profesor y calcula las métricas de progreso de los alumnos.
    """
    service = get_classroom_service()
    if not service:
        return {"error": "Usuario no autenticado"}, 401

    try:
        # 1. Obtener los cursos donde el usuario es profesor
        response = service.courses().list(teacherId="me", courseStates=['ACTIVE']).execute()
        courses = response.get('courses', [])
        
        if not courses:
            return []

        dashboard_data = []
        for course in courses:
            course_id = course['id']
            
            # 2. Obtener alumnos del curso
            students_response = service.courses().students().list(courseId=course_id).execute()
            students = students_response.get('students', [])
            
            # 3. Obtener trabajos/tareas del curso
            coursework_response = service.courses().courseWork().list(courseId=course_id).execute()
            courseworks = coursework_response.get('courseWork', [])
            
            # 4. Obtener todas las entregas de los alumnos para este curso
            submissions_response = service.courses().courseWork().studentSubmissions().list(
                courseId=course_id,
                courseWorkId='-' # El guion significa "todos los trabajos"
            ).execute()
            submissions = submissions_response.get('studentSubmissions', [])
            
            # 5. Procesar datos para generar métricas
            student_metrics = defaultdict(lambda: {
                'id': None,
                'fullName': 'Unknown',
                'email': 'Unknown',
                'metrics': defaultdict(int)
            })

            # Inicializar métricas para todos los alumnos inscritos
            for student in students:
                student_id = student['userId']
                student_metrics[student_id]['id'] = student_id
                student_metrics[student_id]['fullName'] = student['profile']['name']['fullName']
                student_metrics[student_id]['email'] = student['profile']['emailAddress']
                # Cada alumno tiene un total de tareas asignadas
                student_metrics[student_id]['metrics']['total_assignments'] = len(courseworks)


            # Contar estados de las entregas
            for sub in submissions:
                student_id = sub['userId']
                state = sub['state']
                
                if state == 'TURNED_IN':
                    # Verificar si fue entregada tarde
                    if sub.get('late', False):
                        student_metrics[student_id]['metrics']['late'] += 1
                    else:
                        student_metrics[student_id]['metrics']['on_time'] += 1
                elif state == 'RETURNED':
                     student_metrics[student_id]['metrics']['graded'] += 1
                elif state == 'CREATED' or state == 'NEW':
                    student_metrics[student_id]['metrics']['pending'] += 1
            
            # Calcular entregas faltantes
            for sid, data in student_metrics.items():
                submitted_count = (
                    data['metrics']['on_time'] + 
                    data['metrics']['late'] + 
                    data['metrics']['graded']
                )
                data['metrics']['missing'] = data['metrics']['total_assignments'] - submitted_count


            course_summary = {
                'id': course['id'],
                'name': course['name'],
                'description': course.get('description', ''),
                'students': list(student_metrics.values())
            }
            dashboard_data.append(course_summary)

        return dashboard_data

    except Exception as e:
        # Considera un logging más robusto en una app real
        print(f"Error al obtener datos de Classroom: {e}")
        return {"error": str(e)}, 500