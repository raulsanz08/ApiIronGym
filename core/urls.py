from django.urls import path
from .views import (
    register_user, login_user, obtener_rutinas, obtener_dietas,
    obtener_dias_entrenamiento, obtener_dias_dieta, obtener_ejercicios_por_dia, obtener_comidas_por_dia,
    obtener_perfil_usuario, actualizar_perfil_usuario,
    obtener_notificaciones,
    obtener_desafios, obtener_estadisticas, actualizar_notificacion, actualizar_desafio, actualizar_configuracion,
    guardar_mensaje, obtener_mis_mensajes, borrar_mis_mensajes,
)

urlpatterns = [

    path("api/register/", register_user, name="register"),
    path("api/login/", login_user, name="login"),
    path("api/perfil/", obtener_perfil_usuario, name="obtener_perfil"),
    path("api/perfil/update/", actualizar_perfil_usuario, name="actualizar_perfil"),


    path('api/rutinas/', obtener_rutinas, name="obtener_rutinas"),
    path('api/dietas/', obtener_dietas, name="obtener_dietas"),
    path('api/rutinas/<int:rutina_id>/dias/', obtener_dias_entrenamiento, name="dias_rutina"),
    path('api/dietas/<int:dieta_id>/dias/', obtener_dias_dieta, name="dias_dieta"),
    path('api/ejercicios-dia/<int:dia_id>/', obtener_ejercicios_por_dia, name="obtener_ejercicios_por_dia"),
    path('api/comidas-dia/<int:dia_id>/', obtener_comidas_por_dia, name="obtener_comidas_por_dia"),


    path('api/estadisticas/', obtener_estadisticas, name='obtener_estadisticas_usuario'),


    path('api/notificaciones/', obtener_notificaciones, name='obtener_notificaciones'),  # GET
    path('api/notificaciones/<int:pk>/update/', actualizar_notificacion, name='actualizar_notificacion'),  # PUT



    path('api/desafios/', obtener_desafios, name='obtener_desafios'),
    path('api/desafios/<int:pk>/', actualizar_desafio, name='actualizar_desafio'),


    path('api/configuracion/', actualizar_configuracion, name='actualizar_configuracion'),



    path('api/mensajes/guardar/', guardar_mensaje, name='guardar_mensaje'),
    path('api/mensajes/obtener/', obtener_mis_mensajes, name='obtener_mis_mensajes'),
    path('api/mensajes/borrar/', borrar_mis_mensajes, name='borrar_mis_mensajes'),

]
