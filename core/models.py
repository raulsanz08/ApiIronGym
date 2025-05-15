from django.db import models
from django.contrib.auth.models import User


class Rutina(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagenUrl = models.URLField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'rutinas'



class Dieta(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagenUrl = models.URLField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'dietas'

class DiaEntrenamiento(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name="dias")
    dia = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagenUrl = models.URLField()

    def __str__(self):
        return f"{self.rutina.nombre} - {self.dia}"

    class Meta:
        db_table = 'dias_entrenamiento'

class DiaDieta(models.Model):
    dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE, related_name="dias")
    dia = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagenUrl = models.URLField()

    def __str__(self):
        return f"{self.dieta.nombre} - {self.dia}"

    class Meta:
        db_table = 'dias_dieta'

class EjercicioDia(models.Model):
    dia_entrenamiento = models.ForeignKey(DiaEntrenamiento, on_delete=models.CASCADE, related_name="ejercicios")
    nombre = models.CharField(max_length=255)
    repeticiones = models.CharField(max_length=50)

    class Meta:
        db_table = 'ejercicios_dia'

    def __str__(self):
        return f"{self.dia_entrenamiento} - {self.nombre}"


class ComidaDia(models.Model):
    dia_dieta = models.ForeignKey(DiaDieta, on_delete=models.CASCADE, related_name="comidas")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        db_table = 'comidas_dia'

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.IntegerField()
    avatar_url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'perfil_usuario'

    def __str__(self):
        return f"{self.nombre} (Usuario ID: {self.usuario.id})"

class EstadisticasUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    ritmoCardiaco = models.IntegerField(db_column='ritmo_cardiaco')
    fuerza = models.IntegerField()
    peso = models.IntegerField()
    logros = models.IntegerField()
    disciplina = models.IntegerField()
    altura = models.IntegerField()
    resistencia = models.IntegerField()

    class Meta:
        db_table = 'estadisticas'



class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notificaciones'

    def __str__(self):
        return f'Notificación para {self.usuario.username}: {self.descripcion[:20]}...'


class Desafio(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen_url = models.URLField(max_length=255, blank=True, null=True)
    completado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'desafios'

    def __str__(self):
        return self.titulo

class Configuracion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    contrasena = models.CharField(max_length=255)
    notificaciones = models.BooleanField(default=True)
    idioma = models.CharField(max_length=50, default='es')


    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Configuración de {self.user.username}"

class Mensaje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensajes")
    texto = models.TextField()
    remitente = models.CharField(max_length=20)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mensaje'

    def __str__(self):
        return f"{self.usuario.email} - {self.remitente}: {self.texto[:30]}..."







