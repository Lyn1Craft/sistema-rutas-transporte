# Sistema Experto de Rutas para Transporte Masivo

Sistema inteligente basado en conocimiento que, a partir de una **base de
conocimiento escrita en reglas lógicas** y una **estrategia de búsqueda
heurística (A\*)**, calcula la mejor ruta entre dos estaciones (punto A y
punto B) de un sistema de transporte masivo.

Proyecto desarrollado para la actividad 3 del curso, con base en:
> Benítez, R. (2014). *Inteligencia artificial avanzada*. Barcelona: Editorial UOC.
> Capítulo 2 (lógica y representación del conocimiento), Capítulo 3 (sistemas
> basados en reglas) y Capítulo 9 (técnicas basadas en búsquedas heurísticas).

## Equipo de trabajo

| Integrante | Módulo a cargo | Archivo |
|---|---|---|
| Integrante 1 | Base de conocimiento y motor de inferencia (reglas lógicas) | `base_conocimiento.py` |
| Integrante 2 | Construcción del grafo del sistema de transporte | `grafo_transporte.py` |
| Integrante 3 | Motor de búsqueda heurística A* | `motor_busqueda.py` |
| Integrante 4 | Interfaz, integración y pruebas | `main.py` |

Cada integrante tiene además su propio archivo `INTEGRANTE_N_explicacion.md`
con la explicación detallada de su parte, para usar como guion del video y
como evidencia de autoría en el commit de Git.

## Estructura del repositorio

```
.
├── base_conocimiento.py          # Módulo 1: hechos + reglas + motor de inferencia
├── grafo_transporte.py           # Módulo 2: grafo ponderado del sistema de transporte
├── motor_busqueda.py             # Módulo 3: búsqueda heurística A*
├── main.py                       # Módulo 4: CLI + batería de pruebas
├── generar_pdf_pruebas.py        # Script de apoyo: genera el PDF de pruebas
├── Pruebas_Sistema_Rutas.pdf     # Entregable: evidencia de pruebas
├── INTEGRANTE_1_explicacion.md
├── INTEGRANTE_2_explicacion.md
├── INTEGRANTE_3_explicacion.md
├── INTEGRANTE_4_explicacion.md
└── README.md
```

## Requisitos

- Python 3.8 o superior.
- No requiere librerías externas para ejecutar el sistema (solo la librería
  estándar de Python: `heapq`, `collections`, `dataclasses`).
- Para regenerar el PDF de pruebas: `pip install reportlab`.

## Cómo ejecutarlo

Clonar el repositorio y ubicarse en la carpeta del proyecto:

```bash
git clone <URL_DEL_REPOSITORIO>
cd <carpeta_del_repositorio>
```

**1. Modo interactivo** (el usuario escribe la estación de origen y destino):

```bash
python3 main.py
```

Ejemplo de uso dentro del menú:
```
Estación de ORIGEN (A): Portal_Suba
Estación de DESTINO (B): Portal_Sur
```

Escriba `lista` para ver todas las estaciones disponibles, y `salir` para
terminar.

**2. Modo pruebas automáticas** (corre 5 casos de prueba y muestra resultados):

```bash
python3 main.py --pruebas
```

**3. Regenerar el PDF de pruebas** (opcional, requiere reportlab):

```bash
pip install reportlab
python3 generar_pdf_pruebas.py
```

## Diseño del sistema (resumen)

1. **Base de conocimiento (reglas lógicas):** las líneas del sistema de
   transporte y sus estaciones se representan como hechos base. Un motor de
   inferencia hacia adelante (*forward chaining*) aplica reglas lógicas
   (estilo cláusulas de Horn) para derivar las conexiones entre estaciones y
   detectar automáticamente cuáles son estaciones de transbordo.
2. **Grafo ponderado:** los hechos derivados se traducen en un grafo donde
   cada arista tiene un peso en minutos, y se penaliza con minutos
   adicionales cualquier tramo que implique cambiar de línea (transbordo).
3. **Búsqueda heurística A\*:** se implementa el algoritmo A* con una
   heurística admisible (número mínimo de saltos hasta el destino,
   calculado con BFS) para garantizar que la ruta encontrada es la de
   **menor tiempo total**, considerando los transbordos.
4. **Interfaz y pruebas:** una CLI permite consultar rutas manualmente, y una
   batería de 5 casos de prueba (rutas directas, con 1 y 2 transbordos, y dos
   casos borde) valida el correcto funcionamiento del sistema.

## Nota sobre los datos usados

La red de estaciones y líneas usada en este proyecto es una versión
simplificada/didáctica (4 líneas, 16 estaciones) pensada para que el
funcionamiento del algoritmo sea fácil de explicar y verificar en el video.
Puede reemplazarse fácilmente por los datos reales del sistema de transporte
masivo de su ciudad, editando únicamente el diccionario `LINEAS` en
`base_conocimiento.py`; el resto del sistema (grafo, búsqueda, interfaz)
funciona sin cambios.
