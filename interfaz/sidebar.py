"""Barra lateral persistente: logo, navegación y datos del proyecto."""

import flet as ft

from . import datos_proyecto, tema
from .componentes import insignia

ANCHO = 240


def _item_nav(icono, texto, on_click, activo=False, deshabilitado=False, etiqueta=None):
    controles = [
        ft.Icon(icono, size=18, color=tema.TEXTO if activo else tema.TEXTO_SUAVE),
        ft.Text(
            texto,
            size=14,
            weight=ft.FontWeight.BOLD if activo else ft.FontWeight.NORMAL,
            color=tema.TEXTO if activo else tema.TEXTO_SUAVE,
        ),
    ]
    if etiqueta:
        controles.append(ft.Container(expand=True))
        controles.append(
            ft.Text(etiqueta, size=10, color=tema.TEXTO_SUAVE, italic=True)
        )

    return ft.Container(
        content=ft.Row(controles, spacing=10),
        bgcolor=tema.PRIMARIO if activo else None,
        border_radius=10,
        padding=ft.Padding.symmetric(vertical=10, horizontal=12),
        ink=not deshabilitado,
        opacity=0.5 if deshabilitado else 1.0,
        on_click=None if deshabilitado else on_click,
    )


def _tarjeta_proyecto():
    integrantes = ft.Column(
        controls=[
            ft.Row(
                [ft.Icon(ft.Icons.PERSON, size=14, color=tema.ACENTO), ft.Text(nombre, size=13, color=tema.TEXTO)],
                spacing=6,
            )
            for nombre in datos_proyecto.INTEGRANTES
        ],
        spacing=6,
    )

    return ft.Container(
        bgcolor=tema.TARJETA,
        border=ft.Border.all(1, tema.BORDE),
        border_radius=14,
        padding=ft.Padding.all(16),
        content=ft.Column(
            controls=[
                ft.Text("PROYECTO ACADÉMICO", size=11, weight=ft.FontWeight.BOLD, color=tema.TEXTO_SUAVE),
                ft.Container(height=4),
                ft.Text(f"Curso: {datos_proyecto.CURSO}", size=12, color=tema.TEXTO_SUAVE),
                ft.Text(f"Docente: {datos_proyecto.DOCENTE}", size=12, color=tema.TEXTO_SUAVE),
                ft.Container(height=8),
                ft.Text("INTEGRANTES", size=11, weight=ft.FontWeight.BOLD, color=tema.TEXTO_SUAVE),
                integrantes,
                ft.Container(height=8),
                ft.Text(f"Año: {datos_proyecto.ANIO}", size=11, color=tema.TEXTO_SUAVE),
            ],
            spacing=4,
        ),
    )


def build_sidebar(activo, on_inicio, on_pnl, on_informacion):
    logo = ft.Row(
        controls=[
            ft.Icon(ft.Icons.SHOW_CHART_ROUNDED, size=28, color=tema.ACENTO),
            ft.Column(
                controls=[
                    ft.Text("PNL", size=18, weight=ft.FontWeight.BOLD, color=tema.TEXTO),
                    ft.Text("y Dinámica", size=11, color=tema.TEXTO_SUAVE),
                ],
                spacing=0,
            ),
        ],
        spacing=10,
    )

    navegacion = ft.Column(
        controls=[
            _item_nav(ft.Icons.HOME_ROUNDED, "Inicio", on_inicio, activo=activo == "inicio"),
            _item_nav(ft.Icons.FUNCTIONS_ROUNDED, "f(x)  PNL", on_pnl, activo=activo == "pnl"),
            _item_nav(ft.Icons.ACCOUNT_TREE_ROUNDED, "Dinámica", None, deshabilitado=True, etiqueta="Próximamente"),
            _item_nav(ft.Icons.INFO_ROUNDED, "Información", on_informacion, activo=activo == "informacion"),
        ],
        spacing=4,
    )

    return ft.Container(
        width=ANCHO,
        bgcolor=tema.SIDEBAR,
        border=ft.Border(right=ft.BorderSide(1, tema.BORDE_SUAVE)),
        padding=ft.Padding.all(20),
        content=ft.Column(
            controls=[
                logo,
                ft.Container(height=24),
                navegacion,
                ft.Container(height=32),
                _tarjeta_proyecto(),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
    )
