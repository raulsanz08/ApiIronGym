from django.db import models
from django.contrib.auth.models import User

# Modelo de Rutinas
class Rutina(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagenUrl = models.URLField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'rutinas'
        managed = False # ← Esto le dice a Django que use esa tabla específica


# Modelo de Dietas
class Dieta(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagenUrl = models.URLField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'dietas'
        managed = False # ← Tabla manual en MySQL

class DiaEntrenamiento(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name="dias")
    dia = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagenUrl = models.URLField()

    def __str__(self):
        return f"{self.rutina.nombre} - {self.dia}"

    class Meta:
        db_table = 'dias_entrenamiento'
        managed = False  # 🔥 Esto le dice a Django que NO intente crear esta tabla

class DiaDieta(models.Model):
    dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE, related_name="dias")
    dia = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagenUrl = models.URLField()

    def __str__(self):
        return f"{self.dieta.nombre} - {self.dia}"

    class Meta:
        db_table = 'dias_dieta'   # Nombre exacto de la tabla en MySQL
        managed = False           # 🔥 Esto es lo que evita que Django intente crearla

class EjercicioDia(models.Model):
    dia_entrenamiento = models.ForeignKey(DiaEntrenamiento, on_delete=models.CASCADE, related_name="ejercicios")
    nombre = models.CharField(max_length=255)
    repeticiones = models.CharField(max_length=50)

    class Meta:
        managed = False  # 👈 Django no intentará crear/modificar la tabla
        db_table = 'ejercicios_dia'

    def __str__(self):
        return f"{self.dia_entrenamiento} - {self.nombre}"


class ComidaDia(models.Model):
    dia_dieta = models.ForeignKey(DiaDieta, on_delete=models.CASCADE, related_name="comidas")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        db_table = 'comidas_dia'
        managed = False  # 👈 Esto es importante

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.IntegerField()
    avatar_url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'perfil_usuario'
        managed = False  # No gestionamos la creación ni migración de esta tabla

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
        db_table = 'estadisticas'  # <-- aquí estaba el problema
        managed = False



class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notificaciones'
        managed = False

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
        managed = False  # Evita que Django intente crear la tabla

    def __str__(self):
        return self.titulo

class Configuracion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con el modelo de usuario
    email = models.EmailField(max_length=255)  # Nuevo email
    contrasena = models.CharField(max_length=255)  # Nueva contraseña (hashing recomendado)
    notificaciones = models.BooleanField(default=True)  # Activación de notificaciones
    idioma = models.CharField(max_length=50, default='es')  # Idioma (por defecto 'es' para español)

    # Marca de tiempo para saber cuándo se actualizó la configuración
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Configuración de {self.user.username}"

class Mensaje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensajes")
    texto = models.TextField()
    remitente = models.CharField(max_length=20)  # "Tú" o "IronBot"
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mensaje'
        managed = False  # Evita que Django intente crear la tabla

    def __str__(self):
        return f"{self.usuario.email} - {self.remitente}: {self.texto[:30]}..."







