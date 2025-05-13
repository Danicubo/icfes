from django import forms
from django.forms import modelformset_factory
from .models import Simulacro, Preguntas

from django import forms

class LoginForm(forms.Form):
    correo = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={'class': 'p-2 border-1 rounded-pill ' }),
    )
    rol = forms.ChoiceField(
        choices=[('estudiante', 'Estudiante'), ('profesor', 'Profesor')],
        label="Rol",
        widget=forms.Select(attrs={'class': 'p-2 border-1 rounded-pill'}),
    )
    
    
class SimulacroForm(forms.ModelForm):
    class Meta:
        model = Simulacro
        fields = ['area', 'fecha_registro', 'tiempo_limite']

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Preguntas
        fields = ['contenido', 'respuesta_correcta']