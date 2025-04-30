from django.shortcuts import render, redirect
from .forms import RegistroForm
from .models import Estudiante, Simulacro, Profesores, Resultados
from django.http import HttpResponseForbidden

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


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Aquí podrías guardar la data si deseas
            return redirect('grados')
    else:
        form = RegistroForm()
    return render(request, 'Academico/registro.html', {'form': form})

def grados(request):
    return render(request, 'Academico/grados.html')

def materiasNovenoDecimo(request):
    return render(request, 'Academico/materiasNoveno.html')

def simulacro1(request):
    return render(request, 'Academico/simulacro.html')


def login_view(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        dato = request.POST['dato']

        user = None
        tipo = None

        # Buscar en estudiantes
        try:
            user = estudiante.objects.get(correo=correo, grado=dato)
            tipo = 'estudiante'
        except estudiante.DoesNotExist:
            pass

        # Si no es estudiante, buscar en profesores
        if not user:
            try:
                user = profesores.objects.get(correo=correo, especialidad=dato)
                tipo = 'profesor'
            except profesores.DoesNotExist:
                pass

        if user:
            request.session['usuario_id'] = user.id_Estudiantes if tipo == 'estudiante' else user.id_profesores
            request.session['usuario_tipo'] = tipo
            return redirect('/')  # Cambia 'inicio' por la vista a la que quieras redirigir
        else:
            return render(request, 'Academico/login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'Academico/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def solo_estudiantes(vista_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('usuario_tipo') != 'estudiante':
            return HttpResponseForbidden("Acceso denegado.")
        return vista_func(request, *args, **kwargs)
    return wrapper

def solo_profesores(vista_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('usuario_tipo') != 'profesor':
            return HttpResponseForbidden("Acceso denegado.")
        return vista_func(request, *args, **kwargs)
    return wrapper

@solo_estudiantes
def vista_estudiante(request):
    # contenido
    pass

@solo_profesores
def vista_profesor(request):
    # contenido
    pass

