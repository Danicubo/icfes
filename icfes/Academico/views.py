from django.shortcuts import render, redirect
from .models import Estudiante, Simulacro, Profesores, Resultados
from .forms import LoginForm
from .utils.decorators import solo_profesores

def index(request):
    listadoEstudiantes = Estudiante.objects.all()
    listadoSimulacro = Simulacro.objects.all()
    listadoProfesores = Profesores.objects.all()
    listadoResultados = Resultados.objects.all()

    contexto = {
        "estudiantes": listadoEstudiantes,
        "simulacros": listadoSimulacro,
        "profesores": listadoProfesores,
        "resultados": listadoResultados,
    }

    return render(request, 'Academico/index.html', contexto)

def registrarEstudiante(request):
    """Registra un nuevo estudiante."""
    if request.method == 'POST':
        nombre_completo = request.POST['txtNombreCompleto']
        correo = request.POST['txtCorreo']
        grado = request.POST['txtGrado']
        fecha_registro = request.POST['txtFechaRegistro']  # Asegúrate de tener este campo en tu formulario

        estudiante = Estudiante.objects.create(
            nombre_completo=nombre_completo,
            correo=correo,
            grado=grado,
            fecha_registro=fecha_registro
        )
        messages.success(request, '¡Estudiante registrado!')
        return redirect('/')  # Redirige a la página principal o a la lista de estudiantes
    else:
        # Si la solicitud no es POST, podrías mostrar un formulario vacío para registrar un estudiante
        return render(request, 'Academico/registroEstudiante.html')
    
def edicionEstudiante(request, id_Estudiantes):
    """Muestra el formulario para editar un estudiante específico."""
    estudiante = get_object_or_404(Estudiante, id_Estudiantes=id_Estudiantes)
    return render(request, 'Academico/edicionEstudiante.html', {"estudiante": estudiante})

def editarEstudiante(request):
    """Guarda los cambios realizados en la información de un estudiante."""
    if request.method == 'POST':
        id_Estudiantes = request.POST['txtIdEstudiantes']  # Asegúrate de que tu formulario tenga este campo oculto
        nombre_completo = request.POST['txtNombreCompleto']
        correo = request.POST['txtCorreo']
        grado = request.POST['txtGrado']

        try:
            estudiante = Estudiante.objects.get(id_Estudiantes=id_Estudiantes)
            estudiante.nombre_completo = nombre_completo
            estudiante.correo = correo
            estudiante.grado = grado
            estudiante.save()
            messages.success(request, '¡Estudiante actualizado!')
            return redirect('/')  # Redirige a la página principal o a la lista de estudiantes
        except Estudiante.DoesNotExist:
            messages.error(request, 'El estudiante no existe.')
            return redirect('/') # Redirige a una página de error o a la lista de estudiantes
    else:
        messages.error(request, 'Método no válido.')
        return redirect('/')

def eliminarEstudiante(request, id_Estudiantes):
    """Elimina un estudiante específico."""
    estudiante =get_object_or_404(Estudiante, id_Estudiantes=id_Estudiantes)
    estudiante.delete()
    messages.success(request, '¡Estudiante eliminado!')
    return redirect('/')  # Redirige a la página principal o a la lista de estudiantes


def grados(request):
    return render(request, 'Academico/grados.html')

def materiasNovenoDecimo(request):
    return render(request, 'Academico/materiasNoveno.html')

def simulacro1(request):
    return render(request, 'Academico/simulacro.html')


def registro(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            rol = form.cleaned_data['rol']

            if rol == 'estudiante':
                if Estudiante.objects.filter(correo=correo).exists():
                    estudiante = Estudiante.objects.get(correo=correo)
                    request.session['usuario_id'] = estudiante.id_Estudiantes
                    request.session['rol'] = 'estudiante'
                    return redirect('/Academico/materias-noveno-decimo/')
                else:
                    form.add_error(None, 'Estudiante no encontrado')
            elif rol == 'profesor':
                if Profesores.objects.filter(correo=correo).exists():
                    profesor = Profesores.objects.get(correo=correo)
                    request.session['usuario_id'] = profesor.id_profesores
                    request.session['rol'] = 'profesor'
                    return redirect('/')
                else:
                    form.add_error(None, 'Profesor no encontrado')
    else:
        form = LoginForm()

    return render(request, 'Academico/registro.html', {'form': form})


def logout(request):
    request.session.flush()
    return redirect('/Academico/registro')




def vista_para_estudiantes(request):
    if request.session.get('rol') != 'estudiante':
        return redirect('login')  # o mostrar error

@solo_profesores
def index(request):
    return render(request, 'Academico/index.html')