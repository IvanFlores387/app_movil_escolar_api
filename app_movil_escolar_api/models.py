from django.db import models
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication


# =========================================================
# AUTENTICACIÓN POR TOKEN
# =========================================================

class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


# =========================================================
# ADMINISTRADORES
# =========================================================

class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=None
    )

    clave_admin = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    telefono = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    rfc = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    edad = models.IntegerField(
        null=True,
        blank=True
    )

    ocupacion = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    creation = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    update = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            "Perfil del admin "
            + self.user.first_name
            + " "
            + self.user.last_name
        )


# =========================================================
# ALUMNOS
# =========================================================

class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=None
    )

    matricula = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    curp = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    rfc = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    fecha_nacimiento = models.DateTimeField(
        auto_now_add=False,
        null=True,
        blank=True
    )

    edad = models.IntegerField(
        null=True,
        blank=True
    )

    telefono = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    ocupacion = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    creation = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    update = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            "Perfil del alumno "
            + self.user.first_name
            + " "
            + self.user.last_name
        )


# =========================================================
# MAESTROS
# =========================================================

class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=None
    )

    id_trabajador = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    fecha_nacimiento = models.DateTimeField(
        auto_now_add=False,
        null=True,
        blank=True
    )

    telefono = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    rfc = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    cubiculo = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    edad = models.IntegerField(
        null=True,
        blank=True
    )

    area_investigacion = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    materias_json = models.TextField(
        null=True,
        blank=True
    )

    creation = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    update = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            "Perfil del maestro "
            + self.user.first_name
            + " "
            + self.user.last_name
        )


# =========================================================
# MATERIAS
# =========================================================

class Materias(models.Model):

    ESTADOS = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
    ]

    id = models.BigAutoField(
        primary_key=True
    )

    clave_materia = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False
    )

    nombre_materia = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    descripcion = models.TextField(
        null=True,
        blank=True
    )

    creditos = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    semestre = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='activa'
    )

    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='materias_creadas'
    )

    creation = models.DateTimeField(
        auto_now_add=True
    )

    update = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            self.clave_materia
            + " - "
            + self.nombre_materia
        )


# =========================================================
# EVENTOS ACADÉMICOS
# =========================================================

class EventosAcademicos(models.Model):

    TIPOS_EVENTO = [
        ('congreso', 'Congreso'),
        ('conferencia', 'Conferencia'),
        ('taller', 'Taller'),
        ('seminario', 'Seminario'),
        ('feria', 'Feria'),
        ('curso', 'Curso'),
        ('otro', 'Otro'),
    ]

    MODALIDADES = [
        ('presencial', 'Presencial'),
        ('virtual', 'Virtual'),
        ('hibrido', 'Híbrido'),
    ]

    id = models.BigAutoField(
        primary_key=True
    )

    nombre_evento = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    tipo_evento = models.CharField(
        max_length=30,
        choices=TIPOS_EVENTO,
        default='otro'
    )

    descripcion = models.TextField(
        null=True,
        blank=True
    )

    fecha_inicio = models.DateTimeField(
        null=False,
        blank=False
    )

    fecha_fin = models.DateTimeField(
        null=True,
        blank=True
    )

    modalidad = models.CharField(
        max_length=20,
        choices=MODALIDADES,
        default='presencial'
    )

    lugar = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    enlace = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )

    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos_academicos_creados'
    )

    creation = models.DateTimeField(
        auto_now_add=True
    )

    update = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.nombre_evento