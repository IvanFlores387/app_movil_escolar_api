from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from app_movil_escolar_api.models import EventosAcademicos
from app_movil_escolar_api.serializers import EventoAcademicoSerializer


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
    Solamente administradores y maestros
    pueden acceder al módulo de eventos académicos.
    """
    return (
        usuario_es_admin(user)
        or usuario_es_maestro(user)
    )


def usuario_puede_modificar(user, evento):
    """
    Reglas de edición y eliminación:

    Administrador:
    - Puede modificar cualquier evento.

    Maestro:
    - Solamente puede modificar eventos creados por él.
    """

    if usuario_es_admin(user):
        return True

    if usuario_es_maestro(user):
        return evento.creado_por_id == user.id

    return False


# =========================================================
# LISTADO DE EVENTOS ACADÉMICOS
# =========================================================

class EventosAcademicosAll(generics.CreateAPIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )

    # -----------------------------------------------------
    # GET - Obtener todos los eventos
    # -----------------------------------------------------

    def get(self, request, *args, **kwargs):

        if not usuario_puede_acceder(request.user):
            return Response(
                {
                    "details":
                        "No tienes permisos para consultar eventos académicos."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        eventos = EventosAcademicos.objects.all().order_by(
            'fecha_inicio'
        )

        lista = EventoAcademicoSerializer(
            eventos,
            many=True
        ).data

        return Response(
            lista,
            status=status.HTTP_200_OK
        )


# =========================================================
# CRUD DE EVENTOS ACADÉMICOS
# =========================================================

class EventosAcademicosView(generics.CreateAPIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )

    # -----------------------------------------------------
    # GET - Obtener evento académico por ID
    # -----------------------------------------------------

    def get(self, request, *args, **kwargs):

        if not usuario_puede_acceder(request.user):
            return Response(
                {
                    "details":
                        "No tienes permisos para consultar eventos académicos."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        id_evento = request.GET.get('id')

        if not id_evento:
            return Response(
                {
                    "details":
                        "Es necesario proporcionar el ID del evento académico."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        evento = get_object_or_404(
            EventosAcademicos,
            id=id_evento
        )

        serializer = EventoAcademicoSerializer(
            evento,
            many=False
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # -----------------------------------------------------
    # POST - Registrar nuevo evento académico
    # -----------------------------------------------------

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        if not usuario_puede_acceder(request.user):
            return Response(
                {
                    "details":
                        "No tienes permisos para registrar eventos académicos."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EventoAcademicoSerializer(
            data=request.data
        )

        if serializer.is_valid():

            evento = serializer.save(
                creado_por=request.user
            )

            return Response(
                {
                    "message":
                        "Evento académico registrado correctamente.",

                    "evento":
                        EventoAcademicoSerializer(
                            evento
                        ).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # -----------------------------------------------------
    # PUT - Actualizar evento académico
    # -----------------------------------------------------

    @transaction.atomic
    def put(self, request, *args, **kwargs):

        if not usuario_puede_acceder(request.user):
            return Response(
                {
                    "details":
                        "No tienes permisos para actualizar eventos académicos."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        id_evento = request.data.get('id')

        if not id_evento:
            return Response(
                {
                    "details":
                        "Es necesario proporcionar el ID del evento académico."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        evento = get_object_or_404(
            EventosAcademicos,
            id=id_evento
        )

        # Validamos propiedad/permisos
        if not usuario_puede_modificar(
            request.user,
            evento
        ):
            return Response(
                {
                    "details":
                        "No tienes permisos para modificar este evento académico."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EventoAcademicoSerializer(
            evento,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            evento_actualizado = serializer.save()

            return Response(
                {
                    "message":
                        "Evento académico actualizado correctamente.",

                    "evento":
                        EventoAcademicoSerializer(
                            evento_actualizado
                        ).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # -----------------------------------------------------
    # DELETE - Eliminar evento académico
    # -----------------------------------------------------

    @transaction.atomic
    def delete(self, request, *args, **kwargs):

        if not usuario_puede_acceder(request.user):
            return Response(
                {
                    "details":
                        "No tienes permisos para eliminar eventos académicos."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        id_evento = request.GET.get('id')

        if not id_evento:
            return Response(
                {
                    "details":
                        "Es necesario proporcionar el ID del evento académico."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        evento = get_object_or_404(
            EventosAcademicos,
            id=id_evento
        )

        # Validamos propiedad/permisos
        if not usuario_puede_modificar(
            request.user,
            evento
        ):
            return Response(
                {
                    "details":
                        "No tienes permisos para eliminar este evento académico."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        nombre_evento = evento.nombre_evento

        evento.delete()

        return Response(
            {
                "message":
                    "Evento académico eliminado correctamente.",

                "evento":
                    nombre_evento
            },
            status=status.HTTP_200_OK
        )