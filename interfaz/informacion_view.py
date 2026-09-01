"""Vista: Información — datos del proyecto académico."""

import libreria_grafica_hugo as ft

from . import datos_proyecto, iconos, tema
from .componentes import icono


def _fila(etiqueta, valor):
    return ft.Row(
        controls=[
            ft.Text(etiqueta, size=13, weight=ft.FontWeight.BOLD, color=tema.TEXTO_SUAVE, width=110),
            ft.Text(valor, size=13, color=tema.TEXTO),
        ],
    )


def build_informacion_view():
    integrantes = ft.Column(
        controls=[
            ft.Row(
                [icono(iconos.PERSONA, size=16, color=tema.ACENTO), ft.Text(nombre, size=14, color=tema.TEXTO)],
                spacing=8,
            )
            for nombre in datos_proyecto.INTEGRANTES
        ],
        spacing=8,
    )

    tarjeta = ft.Container(
        bgcolor=tema.TARJETA,
        border=ft.Border.all(1, tema.BORDE),
        border_radius=14,
        padding=ft.Padding.all(24),
        content=ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Image(src=datos_proyecto.LOGO, width=64, height=64, fit=ft.BoxFit.CONTAIN),
                        ft.Column(
                            [
                                ft.Text(datos_proyecto.UNIVERSIDAD, size=15, weight=ft.FontWeight.BOLD, color=tema.TEXTO),
                                ft.Text(datos_proyecto.FACULTAD, size=12, color=tema.TEXTO_SUAVE),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=16,
                ),
                ft.Container(height=8),
                _fila("Curso:", datos_proyecto.CURSO),
                _fila("Docente:", datos_proyecto.DOCENTE),
                _fila("Año:", datos_proyecto.ANIO),
                ft.Container(height=12),
                ft.Text("INTEGRANTES", size=12, weight=ft.FontWeight.BOLD, color=tema.TEXTO_SUAVE),
                integrantes,
            ],
            spacing=10,
        ),
    )

    return [
        ft.Text("INFORMACIÓN DEL PROYECTO", size=18, weight=ft.FontWeight.BOLD, color=tema.TEXTO),
        tarjeta,
    ]
