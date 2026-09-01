"""Vista: Inicio — bienvenida y acceso a los módulos."""

import flet as ft

from . import tema
from .componentes import tarjeta_modulo


def build_inicio_view(on_pnl):
    encabezado = ft.Column(
        controls=[
            ft.Text("PROGRAMACIÓN NO LINEAL Y DINÁMICA", size=22, weight=ft.FontWeight.BOLD, color=tema.TEXTO),
            ft.Text("Selecciona un módulo para continuar.", size=13, color=tema.TEXTO_SUAVE),
        ],
        spacing=4,
    )

    tarjetas = ft.Row(
        controls=[
            tarjeta_modulo("PNL", "Optimización", on_pnl, activa=True),
            tarjeta_modulo("Dinámica", "Modelos", None, deshabilitada=True, etiqueta="Próximamente"),
        ],
        spacing=20,
        wrap=True,
        run_spacing=20,
    )

    return [encabezado, tarjetas]
