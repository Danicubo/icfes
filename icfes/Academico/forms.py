from django import forms

class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo")
    rol = forms.ChoiceField(
        choices=[('estudiante', 'Estudiante'), ('profesor', 'Profesor')],
        label="Rol"
    )