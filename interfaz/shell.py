"""Armazón de la app: barra lateral persistente + área de contenido.

Cada navegación reconstruye el shell completo (page.clean + page.add) en
vez de mutar controles ya montados: es el mismo patrón simple usado en
toda la app y evita mantener estado de widgets vivos entre vistas.
"""

import libreria_grafica_hugo as ft

from .componentes import envoltura_contenido
from .informacion_view import build_informacion_view
from .inicio_view import build_inicio_view
from .pnl_view import build_pnl_view
from .sidebar import build_sidebar


def build_shell(page: ft.Page, activo="inicio"):
    def navegar_a(nombre):
        def manejador(e=None):
            page.clean()
            page.add(build_shell(page, activo=nombre))
        return manejador

    barra = build_sidebar(
        activo,
        on_inicio=navegar_a("inicio"),
        on_pnl=navegar_a("pnl"),
        on_informacion=navegar_a("informacion"),
    )

    if activo == "pnl":
        controles = build_pnl_view(page)
    elif activo == "informacion":
        controles = build_informacion_view()
    else:
        controles = build_inicio_view(navegar_a("pnl"))

    return ft.Row(
        controls=[barra, envoltura_contenido(controles)],
        spacing=0,
        expand=True,
    )
