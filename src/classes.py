#-------------ESTUDIANTES----------------
class Estudiante:
    def __init__(self, nombre, apellido, carrera, semestre):
        self.nombre = nombre
        self.apellido = apellido
        self.carrera = carrera
        self.semestre = semestre
        self._materias = []
        self._promedio_final = 0
    
    def add_materia(self, materia):
        self._materias.append(materia)

    @property
    def materias(self):
        return self._materias

    def calcular_promedio(self):
        suma_prom = 0
        suma_UC = 0
        for m in self._materias:
            if not m.evaluaciones:
                continue
            else: 
                if len(m.evaluaciones) == 1:
                    nota = m.evaluaciones[0].nota
                    base = m.evaluaciones[0].base
                    nota_prom = (nota * 20)/base
                    suma_prom += nota_prom * m.creditos
                else: 
                    suma_prom += (m.calcular_promedio() * m.creditos)
                suma_UC += m.creditos
        if suma_UC == 0:
            return 0
        else: return suma_prom/suma_UC

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "carrera": self.carrera,
            "semestre": self.semestre,
            "promedio": self.calcular_promedio(),
            "materias": [m.to_dict() for m in self._materias]
        }



#------------MATERIAS--------------------
class Materia:
    def __init__(self, materia, creditos):
        self.materia = materia
        self.creditos = int(creditos)
        self.evaluaciones = []
    
    def add_evaluacion(self, evaluacion):
        porcentaje_actual = 0
        for e in self.evaluaciones:
            porcentaje_actual += e.porcentaje
        if porcentaje_actual + evaluacion.porcentaje > 100:
            raise ValueError("El porcentaje se excede de 100%, verifique el valor")
        else:  self.evaluaciones.append(evaluacion)

    def calcular_promedio(self):
        suma_notas_ponderadas = 0.0
        suma_porcentajes = 0.0

        for ev in self.evaluaciones:
            nota = float(getattr(ev, 'nota', 0))
            porcentaje = float(getattr(ev, 'porcentaje', 0))
            base = int(getattr(ev, 'base', 20)) 
            
            if base == 0: base = 20 
            nota_normalizada = nota / base
            suma_notas_ponderadas += nota_normalizada * porcentaje
            suma_porcentajes += porcentaje
        if suma_porcentajes == 0:
            return 0.0
        self.promedio_final = (suma_notas_ponderadas / suma_porcentajes) * 20
        
        return self.promedio_final

    def to_dict(self):
        return {
            "materia": self.materia,
            "creditos": self.creditos,
            "evaluaciones": [ev.to_dict() for ev in self.evaluaciones]
        }

#------------EVALUACIONES----------------
class Evaluacion:
    def __init__(self, evaluacion, porcentaje, nota, base):
        self.evaluacion = evaluacion
        # normalize porcentaje to a 0-100 scale
        try:
            pct = float(porcentaje)
        except Exception:
            pct = 0.0
        if pct <= 1:
            pct = pct * 100
        self.porcentaje = pct
        self.nota = float(nota)
        self.base = int(base)

    def to_dict(self):
        return {
            "evaluacion": self.evaluacion,
            "porcentaje": self.porcentaje,
            "nota": self.nota,
            "base": self.base
        }
