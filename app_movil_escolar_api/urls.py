from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app_movil_escolar_api.views import users
from app_movil_escolar_api.views import alumnos
from app_movil_escolar_api.views import maestros
from app_movil_escolar_api.views import auth
from app_movil_escolar_api.views import materias
from app_movil_escolar_api.views import eventos_academicos


urlpatterns = [

    # =====================================================
    # DJANGO ADMIN
    # =====================================================

    # Usamos /django-admin/ porque /admin/ ya pertenece
    # al endpoint de administradores de nuestra API.
    path(
        'django-admin/',
        admin.site.urls
    ),


    # =====================================================
    # ADMINISTRADORES
    # =====================================================

    path(
        'admin/',
        users.AdminView.as_view()
    ),

    path(
        'lista-admins/',
        users.AdminAll.as_view()
    ),


    # =====================================================
    # ALUMNOS
    # =====================================================

    path(
        'alumnos/',
        alumnos.AlumnosView.as_view()
    ),

    path(
        'lista-alumnos/',
        alumnos.AlumnosAll.as_view()
    ),


    # =====================================================
    # MAESTROS
    # =====================================================

    path(
        'maestros/',
        maestros.MaestrosView.as_view()
    ),

    path(
        'lista-maestros/',
        maestros.MaestrosAll.as_view()
    ),


    # =====================================================
    # MATERIAS
    # =====================================================

    path(
        'materias/',
        materias.MateriasView.as_view()
    ),

    path(
        'lista-materias/',
        materias.MateriasAll.as_view()
    ),


    # =====================================================
    # EVENTOS ACADÉMICOS
    # =====================================================

    path(
        'eventos-academicos/',
        eventos_academicos.EventosAcademicosView.as_view()
    ),

    path(
        'lista-eventos-academicos/',
        eventos_academicos.EventosAcademicosAll.as_view()
    ),


    # =====================================================
    # ESTADÍSTICAS
    # =====================================================

    path(
        'total-usuarios/',
        users.TotalUsers.as_view()
    ),


    # =====================================================
    # AUTENTICACIÓN
    # =====================================================

    path(
        'login/',
        auth.CustomAuthToken.as_view()
    ),

    path(
        'logout/',
        auth.Logout.as_view()
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )