"""Motor de interfaz gráfica del proyecto, bajo un nombre propio.

Uso: `import libreria_grafica_hugo as ft` en vez de `import flet as ft`.
Es un alias directo (mismo objeto de módulo): todo lo que existe en la
librería original queda disponible igual, sin mantenimiento extra.
"""

import sys as _sys

import flet as _flet

_sys.modules[__name__] = _flet
