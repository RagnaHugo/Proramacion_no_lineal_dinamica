"""Vista: Información — datos del proyecto académico."""

import flet as ft

from . import datos_proyecto, tema


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
                [ft.Icon(ft.Icons.PERSON, size=16, color=tema.ACENTO), ft.Text(nombre, size=14, color=tema.TEXTO)],
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
                _fila("Universidad:", datos_proyecto.UNIVERSIDAD),
                _fila("Facultad:", datos_proyecto.FACULTAD),
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
