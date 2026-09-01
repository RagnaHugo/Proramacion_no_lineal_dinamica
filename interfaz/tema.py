"""Paleta de colores compartida por toda la interfaz.

Barra lateral oscura + contenido claro, con tarjetas de resultado con un
tinte de color (morado, ámbar, verde) según el tipo de paso.

Cambiar el look de la app implica tocar solo este archivo, no cada vista.
"""

# --- Barra lateral (oscura, como en la referencia) ---
SIDEBAR = "#0B1020"
SIDEBAR_TARJETA = "#131A30"
SIDEBAR_BORDE = "#232C48"
SIDEBAR_TEXTO = "#FFFFFF"
SIDEBAR_TEXTO_SUAVE = "#94A3B8"

# --- Contenido principal (claro, como en la referencia) ---
FONDO = "#F1F5F9"
TARJETA = "#FFFFFF"
BORDE = "#E2E8F0"
BORDE_SUAVE = "#E2E8F0"

TEXTO = "#0F172A"
TEXTO_SUAVE = "#64748B"
TEXTO_INVERSO = "#FFFFFF"  # texto sobre superficies de color sólido (botones, tiles activos)

PRIMARIO = "#2563EB"
ACENTO = "#2563EB"
ERROR = "#DC2626"
VERDE = "#16A34A"
AMBAR = "#D97706"
EJES = "#94A3B8"

# Variantes de tarjeta con un leve tinte de color, para diferenciar
# tipos de resultado (función/derivadas vs. clasificación/resultado).
TARJETA_MORADA = "#EEF2FF"
TARJETA_AMBAR = "#FFFBEB"
TARJETA_VERDE = "#F0FDF4"

# --- Tipografía y medidas ---
# Fuente descargada en recursos/fuentes/ y registrada en main.py.
FUENTE = "Inter"
ALTURA_CONTROL = 52  # alto de botones/campos principales (ej. "Resolver función")
