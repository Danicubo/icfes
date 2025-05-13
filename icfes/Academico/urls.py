from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro-estudiante/', views.registrarEstudiante, name='registro_estudiante'),
    path('editar-estudiante/<int:id>/', views.editarEstudiante, name='editar_estudiante'),
    path('eliminar-estudiante/<int:id>/', views.eliminarEstudiante, name='eliminar_estudiante'),
    path('Academico/registro/', views.registro, name='login'),
    path('Academico/grados/', views.grados_9_10),
    path('Academico/materias-noveno-decimo/', views.materiasNovenoDecimo),
    path('Academico/simulacro/', views.simulacro1),
    path('logout/', views.logout, name='logout'),
    path('Academico/ciencias_naturales/', views.cuestionario, name='ciencias_naturales'),
    path('Academico/lenguaje/', views.cuestionarioLenguaje, name='lenguaje'),
    
    path('crear_examen/', views.crear_examen, name='crear_examen'),
]
