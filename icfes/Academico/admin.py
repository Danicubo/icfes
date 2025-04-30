from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Simulacro, Estudiante, Profesores, Preguntas, Resultados

admin.site.register(Simulacro)
admin.site.register(Estudiante)
admin.site.register(Profesores)
admin.site.register(Preguntas)
admin.site.register(Resultados)
