from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (Rutina, Dieta, DiaEntrenamiento, DiaDieta, EjercicioDia, ComidaDia,
                     PerfilUsuario, EstadisticasUsuario, Notificacion, Desafio, Configuracion, Mensaje)

import json


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"success": False, "message": "Faltan datos"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"success": False, "message": "El usuario ya existe"}, status=400)

            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()

            predeterminadas = [
                "¡No olvides hidratarte bien durante el día!",
                "Recuerda estirar antes y después de entrenar.",
                "Te queda por consumir la cena",
                "Entrenamiento del día: Piernas y glúteos.",
                "Configura tu perfil para un plan personalizado",
                "Tip: Evita entrenar con el estómago vacío.",
                "Mantente hidratado!",
                "Desafío de la semana: 10.000 pasos diarios.",
                "Revisa tu progreso en la sección de estadísticas.",
                "Nueva receta saludable disponible.",
                "Recuerda registrar tu alimentación de hoy.",
                "¡Sigue así, estás haciendo un gran trabajo!",
                "¿Te has pesado esta semana? No olvides hacerlo.",
                "Mantén la postura correcta durante tus ejercicios.",
                "Nuevo artículo en nuestro blog: Cómo evitar lesiones.",
                "¿Probaste la rutina de yoga que recomendamos?",
                "Tiempo estimado de recuperación: 24 horas.",
                "No te saltes el calentamiento.",
                "¡Comparte tu progreso con tus amigos!",
                "Descubre los beneficios de la proteína vegetal.",
                "Recordatorio: Toma al menos 2 litros de agua.",
                "Recuerda estirar antes y después de entrenar.",
                "Tiempo estimado de recuperación: 24 horas.",
                "Recuerda registrar tu alimentación de hoy."


            ]
            Notificacion.objects.bulk_create([
                Notificacion(usuario=user, descripcion=mensaje, activo=True)
                for mensaje in predeterminadas
            ])

            EstadisticasUsuario.objects.create(
                usuario=user,
                ritmoCardiaco=70,
                fuerza=10,
                peso=70,
                logros=0,
                disciplina=10,
                altura=170,
                resistencia=15
            )

            return JsonResponse({"success": True, "message": "Registro exitoso"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)



@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            user = authenticate(username=email, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)

                from .models import Notificacion

                if not Notificacion.objects.filter(usuario=user).exists():
                    Notificacion.objects.create(usuario=user, descripcion="¡Bienvenido a IronGym!", activo=True)
                    Notificacion.objects.create(usuario=user, descripcion="Recuerda mantenerte hidratado ", activo=True)
                    Notificacion.objects.create(usuario=user, descripcion="Hoy es un gran día para superarte ", activo=True)

                return JsonResponse({
                    "success": True,
                    "message": "Inicio de sesión exitoso",
                    "token": token.key
                })
            else:
                return JsonResponse({"success": False, "message": "Credenciales incorrectas"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)


@api_view(['GET'])
def obtener_rutinas(request):
    rutinas = list(Rutina.objects.values())
    return JsonResponse({"success": True, "rutinas": rutinas}, safe=False)


@api_view(['GET'])
def obtener_dietas(request):
    dietas = list(Dieta.objects.values())
    return JsonResponse({"success": True, "dietas": dietas}, safe=False)


@api_view(['GET'])
def obtener_dias_entrenamiento(request, rutina_id):
    try:
        dias = list(DiaEntrenamiento.objects.filter(rutina_id=rutina_id).values())
        return JsonResponse({"success": True, "dias": dias}, safe=False)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@api_view(['GET'])
def obtener_dias_dieta(request, dieta_id):
    try:
        dias = list(DiaDieta.objects.filter(dieta_id=dieta_id).values())
        return JsonResponse({"success": True, "dias": dias}, safe=False)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@api_view(['GET'])
def obtener_ejercicios_por_dia(request, dia_id):
    try:
        ejercicios = list(EjercicioDia.objects.filter(dia_entrenamiento_id=dia_id).values())
        return JsonResponse({"success": True, "ejercicios": ejercicios}, safe=False)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@api_view(['GET'])
def obtener_comidas_por_dia(request, dia_id):
    try:
        comidas = list(ComidaDia.objects.filter(dia_dieta_id=dia_id).values('id', 'nombre', 'descripcion'))
        return JsonResponse({"success": True, "comidas": comidas}, safe=False)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_perfil_usuario(request):
    try:
        perfil = PerfilUsuario.objects.get(usuario_id=request.user.id)
        return JsonResponse({
            "success": True,
            "nombre": perfil.nombre,
            "peso": perfil.peso,
            "altura": perfil.altura,
            "avatar_url": perfil.avatar_url
        })
    except PerfilUsuario.DoesNotExist:
        return JsonResponse({"success": False, "message": "Perfil no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def actualizar_perfil_usuario(request):
    try:
        data = json.loads(request.body)
        perfil, created = PerfilUsuario.objects.update_or_create(
            usuario_id=request.user.id,
            defaults={
                "nombre": data.get('nombre'),
                "peso": data.get('peso'),
                "altura": data.get('altura'),
                "avatar_url": data.get('avatar_url', "")
            }
        )
        return JsonResponse({"success": True, "message": "Perfil actualizado correctamente", "creado": created})
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_estadisticas(request):
    try:
        estadisticas = EstadisticasUsuario.objects.get(usuario=request.user)
        return Response({
            "ritmoCardiaco": estadisticas.ritmoCardiaco,
            "fuerza": estadisticas.fuerza,
            "peso": estadisticas.peso,
            "logros": estadisticas.logros,
            "disciplina": estadisticas.disciplina,
            "altura": estadisticas.altura,
            "resistencia": estadisticas.resistencia,
        })
    except EstadisticasUsuario.DoesNotExist:
        return Response({"error": "No se encontraron estadísticas para este usuario."}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_notificaciones(request):
    try:
        print(f"Usuario autenticado: {request.user}")

        notificaciones = Notificacion.objects.filter(usuario=request.user)

        notificaciones_data = [
            {
                "id": n.id,
                "descripcion": n.descripcion,
                "activo": n.activo,
                "fecha_creacion": n.fecha_creacion.isoformat(),
                "usuario_id": n.usuario.id
            }
            for n in notificaciones
        ]

        return JsonResponse({'success': True, "notificaciones": notificaciones_data}, safe=False)

    except Exception as e:
        return JsonResponse({'success': False, "message": f'Error: {str(e)}'}, status=500)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_notificacion(request, pk):
    try:
        data = json.loads(request.body)
        notificacion = Notificacion.objects.get(id=pk)

        if notificacion.usuario.id != request.user.id:
            return JsonResponse({"success": False, "message": "No tienes permiso para modificar esta notificación"}, status=403)

        if "descripcion" in data:
            notificacion.descripcion = data["descripcion"]
        if "activo" in data:
            notificacion.activo = data["activo"]

        notificacion.save()

        return JsonResponse({"success": True, "message": "Notificación actualizada correctamente"})

    except Notificacion.DoesNotExist:
        return JsonResponse({"success": False, "message": "Notificación no encontrada"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_desafios(request):
    try:
        desafios = Desafio.objects.all()

        desafios_list = [
            {
                'id': d.id,
                'titulo': d.titulo,
                'descripcion': d.descripcion,
                'imagenUrl': d.imagen_url,
                'activo': d.completado
            }
            for d in desafios
        ]

        return JsonResponse({'success': True, 'desafios': desafios_list}, safe=False)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_desafio(request, pk):
    try:
        data = json.loads(request.body)
        desafio = Desafio.objects.get(id=pk)


        if "completado" in data:
            desafio.completado = data["completado"]

        desafio.save()

        return JsonResponse({"success": True, "message": "Desafío actualizado correctamente"})

    except Desafio.DoesNotExist:
        return JsonResponse({"success": False, "message": "Desafío no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def actualizar_configuracion(request):
    try:
        data = json.loads(request.body)

        user = request.user
        configuracion, created = Configuracion.objects.get_or_create(user=user)


        nuevo_email = data.get('email')
        if nuevo_email:
            user.username = nuevo_email
            user.email = nuevo_email
            user.save()
            configuracion.email = nuevo_email


        nueva_contrasena = data.get('contrasena')
        if nueva_contrasena:
            user.password = make_password(nueva_contrasena)
            user.save()
            configuracion.contrasena = nueva_contrasena


        notificaciones_activadas = data.get('notificaciones')
        if notificaciones_activadas is not None:
            configuracion.notificaciones = notificaciones_activadas
            Notificacion.objects.filter(usuario=user).update(activo=notificaciones_activadas)


        nuevo_idioma = data.get('idioma')
        if nuevo_idioma:
            configuracion.idioma = nuevo_idioma

        configuracion.save()

        return JsonResponse({'success': True, 'message': 'Configuración actualizada exitosamente'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def guardar_mensaje(request):
    try:
        data = json.loads(request.body)
        texto = data.get('texto')
        remitente = data.get('remitente')

        if not texto or not remitente:
            return JsonResponse({'success': False, 'message': 'Faltan campos'}, status=400)

        mensaje = Mensaje.objects.create(
            usuario=request.user,
            texto=texto,
            remitente=remitente
        )

        return JsonResponse({'success': True, 'message': 'Mensaje guardado correctamente', 'id': mensaje.id})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_mis_mensajes(request):
    try:
        mensajes = Mensaje.objects.filter(usuario=request.user).order_by('fecha')
        mensajes_data = [
            {
                'texto': m.texto,
                'remitente': m.remitente,
                'fecha': m.fecha.isoformat()
            }
            for m in mensajes
        ]

        return JsonResponse({'success': True, 'mensajes': mensajes_data}, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def borrar_mis_mensajes(request):
    try:
        mensajes_borrados, _ = Mensaje.objects.filter(usuario=request.user).delete()

        return JsonResponse({'success': True, 'mensajes_borrados': mensajes_borrados})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)



