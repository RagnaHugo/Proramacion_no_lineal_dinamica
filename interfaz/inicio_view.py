"""Vista: Inicio — bienvenida y acceso a los módulos."""

import libreria_grafica_hugo as ft

from . import tema
from .componentes import tarjeta_modulo


def build_inicio_view(on_pnl):
    titulo = ft.Text("Programación No Lineal y Dinámica", size=24, weight=ft.FontWeight.BOLD, color=tema.TEXTO)

    bienvenida = ft.Container(
        bgcolor=tema.TARJETA,
        border=ft.Border.all(1, tema.BORDE),
        border_radius=12,
        padding=ft.Padding.all(20),
        content=ft.Column(
            controls=[
                ft.Text("Bienvenido", size=16, weight=ft.FontWeight.BOLD, color=tema.ACENTO),
                ft.Text(
                    "Esta herramienta ha sido desarrollada como parte del curso de "
                    "Programación No Lineal y Dinámica.",
                    size=13,
                    color=tema.TEXTO_SUAVE,
                ),
            ],
            spacing=6,
        ),
    )

    pregunta = ft.Text("¿Qué desea explorar?", size=15, weight=ft.FontWeight.BOLD, color=tema.TEXTO)

    tarjetas = ft.Row(
        controls=[
            tarjeta_modulo("PNL", "Programación No Lineal", on_pnl, activa=True),
            tarjeta_modulo("Dinámica", "Modelos", None, deshabilitada=True, etiqueta="Próximamente"),
        ],
        spacing=20,
        wrap=True,
        run_spacing=20,
    )

    return [titulo, bienvenida, pregunta, tarjetas]
