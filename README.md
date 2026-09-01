# Programación No Lineal y Dinámica

Aplicación de escritorio (Flet/Python) para analizar funciones de una
variable: calcula derivadas, valores críticos, clasifica máximos y mínimos,
y grafica el resultado.

## Requisitos

- [Python 3.13](https://www.python.org/downloads/) (o una versión 3.10+ debería funcionar igual)
- Git

## Instalación

Cloná el repositorio y entrá a la carpeta:

```bash
git clone https://github.com/RagnaHugo/Proramacion_no_lineal_dinamica.git
cd Proramacion_no_lineal_dinamica
```

Creá un entorno virtual e instalá las dependencias:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> El `.venv` no se sube al repositorio (está en `.gitignore`) porque queda
> atado a la máquina donde se crea — cada quien debe generar el suyo con
> los pasos de arriba. Si alguna vez ves el error
> `Could not find platform independent libraries <prefix>`, es señal de que
> el `.venv` que estás usando fue creado en otra computadora: borralo y
> creá uno nuevo con estos mismos comandos.

## Ejecutar

Con el entorno virtual activado:

```bash
python main.py
```

La primera vez, Flet descarga una sola vez su runtime de escritorio — puede
tardar unos segundos en abrir la ventana.

## Estructura del proyecto

```
main.py                    # punto de entrada
logica/                    # matemática pura (sin nada de interfaz)
  parser.py                #   interpreta el texto de la función
  pnl.py                    #   deriva, resuelve, clasifica
  formula.py                 #   tipografía matemática (LaTeX -> imagen)
interfaz/                  # todo lo visual (Flet)
  tema.py                   #   colores, fuente, medidas
  iconos.py                  #   nombres de los íconos SVG
  componentes.py              #   piezas reutilizables (tarjetas, botones, etc.)
  sidebar.py, shell.py         #   armazón de la app (barra lateral + navegación)
  inicio_view.py, pnl_view.py,
  informacion_view.py           #   las tres pantallas
  datos_proyecto.py             #   universidad, curso, docente, integrantes — editar acá
recursos/                  # assets: escudo, fuente Inter, íconos SVG
```
