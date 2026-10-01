from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from app_movil_escolar_api.models import Materias
from app_movil_escolar_api.serializers import MateriaSerializer


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def usuario_es_admin(user):
    """
    Verifica si el usuario autenticado pertenece
    al grupo 'administrador'.
    """
    return user.groups.filter(
        name='administrador'
    ).exists()


def usuario_es_maestro(user):
    """
    Verifica si el usuario autenticado pertenece
    al grupo 'maestro'.
    """
    return user.groups.filter(
        name='maestro'
    ).exists()


def usuario_puede_acceder(user):
    """
    Únicamente administradores y maestros
    pueden acceder al módulo de materias.
    """
    return (
        usuario_es_admin(user)
        or usuario_es_maestro(user)
    )


def usuario_puede_modificar(user, materia):
    """
    Reglas para editar/eliminar:

    - Administrador:
      Puede modificar cualquier materia.

    - Maestro:
      Únicamente puede modificar materias creadas por él.
    """

    if usuario_es_admin(user):
        return True

    if usuario_es_maestro(user):
        return materia.creado_por_id == user.id

    return False


# =========================================================
# LISTADO DE MATERIAS
# =========================================================

class MateriasAll(generics.CreateAPIView):

    # El usuario debe haber iniciado sesión.
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # -----------------------------------------------------
    # GET - Obtener todas las materias
    # -----------------------------------------------------

    def get(self, request, *args, **kwargs):

        # Solamente administrador y maestro pueden consultar.
        if not usuario_puede_acceder(request.user):
            return Response(
                {
                    "details":
                        "No tienes permisos para consultar materias."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        materias = Materias.objects.all().order_by(
            'nombre_materia'
        )

        lista = MateriaSerializer(
            materias,
            many=True
        ).data

        return Response(
            lista,
            status=status.HTTP_200_OK
        )


# =========================================================
# CRUD DE MATERIAS
# =========================================================

class MateriasView(generics.CreateAPIView):

    # Todas las operaciones requieren autenticación.
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # -----------------------------------------------------
    # GET - Obtener materia por ID
    # -----------------------------------------------------

    def get(self, request, *args, **kwargs):

        if not usuario_puede_acceder(request.user):
            return Response(
                {
                    "details":
                        "No tienes permisos para consultar materias."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        id_materia = request.GET.get('id')

        if not id_materia:
            return Response(
                {
                    "details":
                        "Es necesario proporcionar el ID de la materia."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        materia = get_object_or_404(
            Materias,
            id=id_materia
        )

        serializer = MateriaSerializer(
            materia,
            many=False
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # -----------------------------------------------------
    # POST - Registrar nueva materia
    # -----------------------------------------------------

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        if not usuario_puede_acceder(request.user):
            return Response(
                {
                    "details":
                        "No tienes permisos para registrar materias."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MateriaSerializer(
            data=request.data
        )

        if serializer.is_valid():

            materia = serializer.save(
                creado_por=request.user
            )

            return Response(
                {
                    "message":
                        "Materia registrada correctamente.",
                    "materia":
                        MateriaSerializer(materia).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # -----------------------------------------------------
    # PUT - Actualizar materia
    # -----------------------------------------------------

    @transaction.atomic
    def put(self, request, *args, **kwargs):

        if not usuario_puede_acceder(request.user):
            return Response(
                {
                    "details":
                        "No tienes permisos para actualizar materias."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        id_materia = request.data.get('id')

        if not id_materia:
            return Response(
                {
                    "details":
                        "Es necesario proporcionar el ID de la materia."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        materia = get_object_or_404(
            Materias,
            id=id_materia
        )

        # Verificar propiedad/permisos
        if not usuario_puede_modificar(
            request.user,
            materia
        ):
            return Response(
                {
                    "details":
                        "No tienes permisos para modificar esta materia."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MateriaSerializer(
            materia,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            materia_actualizada = serializer.save()

            return Response(
                {
                    "message":
                        "Materia actualizada correctamente.",
                    "materia":
                        MateriaSerializer(
                            materia_actualizada
                        ).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # -----------------------------------------------------
    # DELETE - Eliminar materia
    # -----------------------------------------------------

    @transaction.atomic
    def delete(self, request, *args, **kwargs):

        if not usuario_puede_acceder(request.user):
            return Response(
                {
                    "details":
                        "No tienes permisos para eliminar materias."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        id_materia = request.GET.get('id')

        if not id_materia:
            return Response(
                {
                    "details":
                        "Es necesario proporcionar el ID de la materia."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        materia = get_object_or_404(
            Materias,
            id=id_materia
        )

        # Verificar propiedad/permisos
        if not usuario_puede_modificar(
            request.user,
            materia
        ):
            return Response(
                {
                    "details":
                        "No tienes permisos para eliminar esta materia."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        nombre_materia = materia.nombre_materia

        materia.delete()

        return Response(
            {
                "message":
                    "Materia eliminada correctamente.",
                "materia":
                    nombre_materia
            },
            status=status.HTTP_200_OK
        )