from django.shortcuts import render, redirect
from .models import Estudiante, Simulacro, Profesores, Resultados, Preguntas
from .utils.decorators import solo_profesores, solo_estudiantes
from django.contrib import messages
from .forms import SimulacroForm, PreguntaForm, LoginForm
from django.forms import modelformset_factory

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
    if request.method == 'POST':
        nombre = request.POST.get('txtNombreCompleto')
        correo = request.POST.get('txtCorreo')
        grado = request.POST.get('txtGrado')
        fecha = request.POST.get('txtFechaRegistro')

        try:
            Estudiante.objects.create(
                nombre_completo=nombre,
                correo=correo,
                grado=grado,
                fecha_registro=fecha
            )
            messages.success(request, 'Estudiante registrado correctamente.')
            return redirect('registro_estudiante')
        except Exception as e:
            messages.error(request, f'Error al registrar estudiante: {e}')
            # No hacemos redirect, así se muestra el error en la misma página

    estudiantes = Estudiante.objects.all().order_by('-id_Estudiantes')
    return render(request, 'Academico/registro-estudiante.html', {'estudiantes': estudiantes})
    
def edicionEstudiante(request, id_Estudiantes):
    """Muestra el formulario para editar un estudiante específico."""
    estudiante = get_object_or_404(Estudiante, id_Estudiantes=id_Estudiantes)
    return render(request, 'Academico/edicionEstudiante.html', {"estudiante": estudiante})

def editarEstudiante(request, id):
    try:
        estudiante = Estudiante.objects.get(pk=id)
    except Estudiante.DoesNotExist:
        messages.error(request, 'Estudiante no encontrado.')
        return redirect('registro_estudiante')

    if request.method == 'POST':
        estudiante.nombre_completo = request.POST.get('txtNombreCompleto')
        estudiante.correo = request.POST.get('txtCorreo')
        estudiante.grado = request.POST.get('txtGrado')
        estudiante.fecha_registro = request.POST.get('txtFechaRegistro')
        try:
            estudiante.save()
            messages.success(request, 'Estudiante actualizado correctamente.')
            return redirect('registro_estudiante')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {e}')

    return render(request, 'Academico/edicion-estudiante.html', {'estudiante': estudiante})

def eliminarEstudiante(request, id):
    try:
        estudiante = Estudiante.objects.get(pk=id)
        estudiante.delete()
        messages.success(request, 'Estudiante eliminado correctamente.')
    except Estudiante.DoesNotExist:
        messages.error(request, 'Estudiante no encontrado.')
    except Exception as e:
        messages.error(request, f'Error al eliminar: {e}')
    return redirect('registro_estudiante')

@solo_estudiantes
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
                    return redirect('/Academico/grados/')
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




""" def vista_para_estudiantes(request):
    if request.session.get('rol') != 'estudiante':
        return redirect('login')  # o mostrar error """

@solo_profesores
def index(request):
    return render(request, 'Academico/index.html')

@solo_estudiantes
def grados_9_10(request):
    return render(request, 'Academico/grados.html')


@solo_profesores
def crear_examen(request):
    PreguntasFormSet = modelformset_factory(Preguntas, form=PreguntaForm, extra=5)  # Aquí definimos 5 preguntas por defecto
    
    if request.method == 'POST':
        simulacro_form = SimulacroForm(request.POST)
        formset = PreguntasFormSet(request.POST, queryset=Preguntas.objects.none())  # Evita conflictos con instancias previas
        
        if simulacro_form.is_valid() and formset.is_valid():
            simulacro = simulacro_form.save()

            for form in formset:
                if form.cleaned_data:  # Evita guardar formularios vacíos
                    pregunta = form.save(commit=False)
                    pregunta.simulacro = simulacro
                    pregunta.save()

            return redirect('/')  # Redirige a una lista de exámenes (puedes ajustarlo a tu URL)

    else:
        simulacro_form = SimulacroForm()
        formset = PreguntasFormSet(queryset=Preguntas.objects.none())  # No se cargan preguntas existentes

    return render(request, 'Academico/crear_examen.html', {
        'simulacro_form': simulacro_form,
        'formset': formset
    })
    
    
def cuestionario(request):
    if request.method == 'POST':
        # Recibimos las respuestas del formulario
        respuestas_usuario = {
            'q1': request.POST.get('q1', ''),
            'q2': request.POST.get('q2', ''),
            'q3': request.POST.get('q3', ''),
            'q4': request.POST.get('q4', ''),
        }

        # Definimos las respuestas correctas
        respuestas_correctas = {
            'q1': 'correcto',
            'q2': 'correcto',
            'q3': 'correcto',
            'q4': 'correcto',
        }

        # Calculamos el puntaje
        puntaje = sum(1 for key in respuestas_correctas if respuestas_usuario.get(key) == respuestas_correctas[key])

        # Retornamos el resultado al template
        return render(request, 'Academico/ciencias_naturales.html', {'puntaje': puntaje})

    # En caso de GET simplemente mostramos el formulario vacío
    return render(request, 'Academico/ciencias_naturales.html')







def cuestionarioLenguaje(request):
    if request.method == 'POST':
        # Recibimos las respuestas del formulario
        respuestas_usuario = {
            'q1': request.POST.get('q1', ''),
            'q2': request.POST.get('q2', ''),
            'q3': request.POST.get('q3', ''),
            'q4': request.POST.get('q4', ''),
        }

        # Definimos las respuestas correctas
        respuestas_correctas = {
            'q1': 'correcto',
            'q2': 'correcto',
            'q3': 'correcto',
            'q4': 'correcto',
        }

        # Calculamos el puntaje
        puntaje = sum(1 for key in respuestas_correctas if respuestas_usuario.get(key) == respuestas_correctas[key])

        # Retornamos el resultado al template
        return render(request, 'Academico/lenguaje.html', {'puntaje': puntaje})

    # En caso de GET simplemente mostramos el formulario vacío
    return render(request, 'Academico/lenguaje.html')













