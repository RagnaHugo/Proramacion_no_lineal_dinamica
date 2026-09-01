"""Tipografía matemática real (superíndices, fracciones, etc.) para la
interfaz, sin depender de una instalación de LaTeX.

matplotlib trae su propio motor de tipeo matemático ("mathtext"): entiende
un subconjunto de LaTeX (^, _, \\frac, \\sqrt, \\sin, ...) y lo dibuja con
glifos reales. Aquí lo usamos para renderizar una fórmula sola, recortada,
como imagen PNG con fondo transparente — no para graficar.
"""

import base64
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


_cache = {}


def renderizar_formula(latex, color="#0F172A", fontsize=20):
    """Convierte una expresión en formato LaTeX/mathtext a imagen PNG (base64).

    Cachea por (latex, color, fontsize): las etiquetas de esquina (d/dx,
    d²/dx²) son iguales en cada resolución, no hace falta re-dibujarlas.
    """
    clave = (latex, color, fontsize)
    if clave in _cache:
        return _cache[clave]

    fig = plt.figure(figsize=(0.1, 0.1))
    fig.patch.set_alpha(0.0)
    fig.text(0, 0, f"${latex}$", fontsize=fontsize, color=color)

    buf = io.BytesIO()
    fig.savefig(
        buf, format="png", transparent=True,
        bbox_inches="tight", pad_inches=0.04, dpi=200,
    )
    plt.close(fig)
    buf.seek(0)
    resultado = base64.b64encode(buf.read()).decode("utf-8")
    _cache[clave] = resultado
    return resultado
