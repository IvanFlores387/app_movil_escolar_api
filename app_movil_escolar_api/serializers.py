from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Administradores,
    Alumnos,
    Maestros,
    Materias,
    EventosAcademicos
)


# =========================================================
# USUARIOS
# =========================================================

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email'
        )


# =========================================================
# ADMINISTRADORES
# =========================================================

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Administradores
        fields = '__all__'


# =========================================================
# ALUMNOS
# =========================================================

class AlumnoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Alumnos
        fields = '__all__'


# =========================================================
# MAESTROS
# =========================================================

class MaestroSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Maestros
        fields = '__all__'


# =========================================================
# MATERIAS
# =========================================================

class MateriaSerializer(serializers.ModelSerializer):

    # Mostramos los datos del usuario que creó la materia,
    # pero no permitimos que el frontend decida qué usuario es.
    creado_por = UserSerializer(read_only=True)

    class Meta:
        model = Materias
        fields = '__all__'

        read_only_fields = (
            'id',
            'creado_por',
            'creation',
            'update',
        )

    def validate_clave_materia(self, value):
        """
        Limpia la clave de la materia y la guarda en mayúsculas.

        Ejemplo:
        '  itis-401  ' -> 'ITIS-401'
        """

        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                'La clave de la materia es obligatoria.'
            )

        return value

    def validate_nombre_materia(self, value):
        """
        Evita nombres vacíos o formados únicamente por espacios.
        """

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'El nombre de la materia es obligatorio.'
            )

        return value


# =========================================================
# EVENTOS ACADÉMICOS
# =========================================================

class EventoAcademicoSerializer(serializers.ModelSerializer):

    # Al igual que en materias, el usuario creador será asignado
    # automáticamente desde el backend.
    creado_por = UserSerializer(read_only=True)

    class Meta:
        model = EventosAcademicos
        fields = '__all__'

        read_only_fields = (
            'id',
            'creado_por',
            'creation',
            'update',
        )

    def validate_nombre_evento(self, value):
        """
        Evita registrar eventos sin nombre.
        """

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'El nombre del evento es obligatorio.'
            )

        return value

    def validate(self, data):
        """
        Valida que la fecha de finalización no sea anterior
        a la fecha de inicio.
        """

        fecha_inicio = data.get(
            'fecha_inicio',
            getattr(self.instance, 'fecha_inicio', None)
        )

        fecha_fin = data.get(
            'fecha_fin',
            getattr(self.instance, 'fecha_fin', None)
        )

        if (
            fecha_inicio is not None
            and fecha_fin is not None
            and fecha_fin < fecha_inicio
        ):
            raise serializers.ValidationError({
                'fecha_fin':
                    'La fecha de finalización no puede ser anterior '
                    'a la fecha de inicio.'
            })

        return data