import jsonpickle

_page = None

def inicializar(page):
    global _page
    _page = page

def cargar_datos_estudiantes(ruta=None): 
    if _page:
        datos_json = _page.client_storage.get("mis_notas_app_v1")
        if datos_json:
            try:
                return jsonpickle.decode(datos_json)
            except Exception as e:
                print(f"Error al decodificar datos: {e}")
                return []
    return []

def guardar_datos_estudiantes(datos):
    if _page:
        try:
            datos_json = jsonpickle.encode(datos)
            _page.client_storage.set("mis_notas_app_v1", datos_json)
        except Exception as e:
            print(f"Error al guardar en storage: {e}")

def registrar_estudiante(datos, nombre, apellido, carrera, semestre):
    from classes import Estudiante 
    estudiante = Estudiante(nombre, apellido, carrera, semestre)
    datos.append(estudiante)
    guardar_datos_estudiantes(datos)

def registrar_materia(datos, estudiante, materia, creditos):
    from classes import Materia
    nueva_materia = Materia(materia, int(creditos))
    estudiante.add_materia(nueva_materia)
    guardar_datos_estudiantes(datos)

def add_evaluacion(datos, materia, evaluacion, porcentaje, nota, base):
    from classes import Evaluacion
    nueva_evaluacion = Evaluacion(evaluacion, float(porcentaje), float(nota), int(base))
    materia.add_evaluacion(nueva_evaluacion)
    guardar_datos_estudiantes(datos)

def buscar_estudiante_por_nombre(datos, nombre_completo):
    if not nombre_completo: 
        return None
    
    for i, est in enumerate(datos):
        if hasattr(est, 'nombre'):
            nombre_actual = f"{est.nombre} {est.apellido}"
        else:
            nombre_actual = f"{est.get('nombre','')} {est.get('apellido','')}"

        if nombre_actual == nombre_completo:
            return est
            
    return None

def eliminar_estudiante(datos, estudiante_obj):
    if estudiante_obj in datos:
        datos.remove(estudiante_obj)
        guardar_datos_estudiantes(datos)
        return True
    return False

def eliminar_materia(datos, estudiante_obj, nombre_materia):
    if hasattr(estudiante_obj, 'materias'):
        for i, materia in enumerate(estudiante_obj.materias):
            m_nombre = getattr(materia, 'materia', '')
            if m_nombre == nombre_materia:
                estudiante_obj.materias.pop(i)
                guardar_datos_estudiantes(datos) 
                return True
    return False

def eliminar_evaluacion(datos, estudiante_obj, nombre_materia, nombre_evaluacion):
    if hasattr(estudiante_obj, 'materias'):
        for materia in estudiante_obj.materias:
            m_nombre = getattr(materia, 'materia', '')
            if m_nombre == nombre_materia:
                evaluaciones = getattr(materia, 'evaluaciones', [])
                for i, ev in enumerate(evaluaciones):
                    ev_nombre = getattr(ev, 'evaluacion', '') or getattr(ev, 'nombre', '')
                    if ev_nombre == nombre_evaluacion:
                        evaluaciones.pop(i)
                        guardar_datos_estudiantes(datos) 
                        return True
    return False