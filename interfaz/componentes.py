"""Widgets reutilizables entre vistas (inicio, módulos, etc.)."""

import libreria_grafica_hugo as ft

from . import tema

BORDE_RECTO = ft.RoundedRectangleBorder(radius=0)


def icono(nombre, size=18, color=None):
    """Icono SVG (recursos/iconos/<nombre>.svg, ver interfaz/iconos.py).

    El archivo se pinta con `color` vía color_blend_mode (SRC_IN), así el
    mismo .svg sirve para cualquier color sin tener que duplicar archivos.
    """
    return ft.Image(
        src=f"iconos/{nombre}.svg",
        width=size,
        height=size,
        color=color or tema.TEXTO_SUAVE,
        color_blend_mode=ft.BlendMode.SRC_IN,
        fit=ft.BoxFit.CONTAIN,
    )


def tarjeta_modulo(titulo, subtitulo, on_click, activa=False, deshabilitada=False, etiqueta=None):
    """Tarjeta clicable (botón grande) usada en Inicio para entrar a un módulo.

    `activa=True` la resalta con el color principal.
    `deshabilitada=True` la atenúa y desactiva el click (ej. "Próximamente").
    `etiqueta` agrega un texto pequeño extra (ej. "Próximamente").
    Es un botón: esquinas rectas, sin border_radius.
    """
    color_titulo = tema.TEXTO_INVERSO if activa else tema.TEXTO
    color_subtitulo = tema.TEXTO_INVERSO if activa else tema.TEXTO_SUAVE

    controles_texto = [
        ft.Text(titulo, size=28, weight=ft.FontWeight.BOLD, color=color_titulo, text_align=ft.TextAlign.CENTER),
        ft.Text(subtitulo, size=12, color=color_subtitulo, text_align=ft.TextAlign.CENTER),
    ]
    if etiqueta:
        controles_texto.append(insignia(etiqueta, tema.TEXTO_SUAVE))

    contenido = ft.Column(
        controls=controles_texto,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
    )

    estilo = {}
    if activa:
        estilo["bgcolor"] = tema.PRIMARIO
    else:
        estilo["bgcolor"] = tema.TARJETA
        estilo["border"] = ft.Border.all(1, tema.BORDE)

    return ft.Container(
        content=contenido,
        width=200,
        height=140,
        border_radius=0,
        padding=ft.Padding.all(16),
        ink=not deshabilitada,
        opacity=0.55 if deshabilitada else 1.0,
        on_click=None if deshabilitada else on_click,
        **estilo,
    )


def insignia(texto, color):
    """Etiqueta pequeña tipo 'pill' (ej. estado, conteo, clasificación).

    No es un botón (no es clicable): conserva la forma redondeada.
    """
    return ft.Container(
        content=ft.Text(texto, size=11, weight=ft.FontWeight.BOLD, color=color),
        bgcolor=tema.TARJETA,
        border=ft.Border.all(1, color),
        border_radius=999,
        padding=ft.Padding.symmetric(vertical=4, horizontal=10),
    )


def tarjeta_resultado(titulo, contenido, bgcolor=None, col=None):
    """Tarjeta responsiva para un paso del análisis (función, derivada, etc.).

    Pensada para vivir dentro de un ft.ResponsiveRow: `col` define cuánto
    ancho ocupa por breakpoint, así las tarjetas se reacomodan solas en vez
    de solaparse cuando la ventana es angosta.
    """
    return ft.Container(
        col=col or {"xs": 12, "md": 6},
        bgcolor=bgcolor or tema.TARJETA,
        border=ft.Border.all(1, tema.BORDE),
        border_radius=12,
        padding=ft.Padding.all(16),
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=12, weight=ft.FontWeight.BOLD, color=tema.TEXTO_SUAVE),
                ft.Container(height=6),
                contenido,
            ],
            spacing=0,
            tight=True,
        ),
    )


def envoltura_contenido(controles):
    """Área de contenido del shell (junto a la barra lateral): con scroll
    propio para que nada se corte ni se solape si la ventana es chica.
    """
    return ft.Container(
        expand=True,
        bgcolor=tema.FONDO,
        padding=ft.Padding.all(32),
        content=ft.Column(
            controls=controles,
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
    )
