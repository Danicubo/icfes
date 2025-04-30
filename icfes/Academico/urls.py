from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro-estudiante/', views.registrarEstudiante),
    path('edicion-estudiante/', views.edicionEstudiante),
    path('eliminar-estudiante/', views.eliminarEstudiante),
    path('Academico/registro/', views.registro, name='login'),
    path('Academico/grados/', views.grados),
    path('Academico/materias-noveno-decimo/', views.materiasNovenoDecimo),
    path('Academico/simulacro/', views.simulacro1),
]
