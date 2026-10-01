from django.contrib import admin

from app_movil_escolar_api.models import (
    Administradores,
    Alumnos,
    Maestros,
    Materias,
    EventosAcademicos
)


# =========================================================
# PERFILES DE USUARIO
# =========================================================

@admin.register(
    Administradores,
    Alumnos,
    Maestros
)
class ProfilesAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "creation",
        "update"
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name"
    )

    ordering = (
        "id",
    )


# =========================================================
# MATERIAS
# =========================================================

@admin.register(Materias)
class MateriasAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "clave_materia",
        "nombre_materia",
        "semestre",
        "creditos",
        "estado",
        "creado_por",
        "creation",
        "update"
    )

    search_fields = (
        "clave_materia",
        "nombre_materia",
        "descripcion",
        "creado_por__username",
        "creado_por__email",
        "creado_por__first_name",
        "creado_por__last_name"
    )

    list_filter = (
        "estado",
        "semestre",
        "creation"
    )

    ordering = (
        "nombre_materia",
    )

    readonly_fields = (
        "creation",
        "update"
    )


# =========================================================
# EVENTOS ACADÉMICOS
# =========================================================

@admin.register(EventosAcademicos)
class EventosAcademicosAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre_evento",
        "tipo_evento",
        "fecha_inicio",
        "fecha_fin",
        "modalidad",
        "lugar",
        "creado_por",
        "creation"
    )

    search_fields = (
        "nombre_evento",
        "descripcion",
        "lugar",
        "creado_por__username",
        "creado_por__email",
        "creado_por__first_name",
        "creado_por__last_name"
    )

    list_filter = (
        "tipo_evento",
        "modalidad",
        "fecha_inicio",
        "creation"
    )

    ordering = (
        "fecha_inicio",
    )

    readonly_fields = (
        "creation",
        "update"
    )

    date_hierarchy = "fecha_inicio"