from django.db import models


class Simulacro(models.Model):
    id_Simulacro = models.AutoField(primary_key=True)
    area = models.CharField(max_length=15)
    fecha_registro = models.DateField()
    tiempo_limite = models.CharField(max_length=10)

class Estudiante(models.Model):
    id_Estudiantes = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    grado = models.CharField(max_length=10)
    fecha_registro = models.DateField()

    def nombreCompleto(self):
        return self.nombre_completo

class Profesores(models.Model):
    id_profesores = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    grado = models.CharField(max_length=10)
    especialidad = models.CharField(max_length=50)

class Preguntas(models.Model):
    id_preguntas = models.AutoField(primary_key=True)
    contenido = models.CharField(max_length=50)
    respuesta_correcta = models.CharField(max_length=50)

class Resultados(models.Model):
    id = models.AutoField(primary_key=True)
    id_Estudiantes = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    id_Simulacro = models.ForeignKey(Simulacro, on_delete=models.CASCADE)
    Puntaje_decimal = models.CharField(max_length=45)
    Fecha_realizacion = models.DateField()
