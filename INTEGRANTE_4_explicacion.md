# Explicación de mi parte — Integrante 4
### Módulo: `main.py` — Interfaz, integración y pruebas

**[Reemplazar por: Nombre completo del integrante 4]**

## ¿Qué problema resuelve mi módulo?

Mi módulo es el que **une** los tres módulos anteriores en un programa
usable: carga la base de conocimiento (módulo 1), construye el grafo
(módulo 2), invoca el motor de búsqueda (módulo 3), y le muestra el
resultado al usuario de forma clara. También contiene la **batería de
pruebas** que sirve como evidencia del correcto funcionamiento del sistema
(el PDF de pruebas que pide la rúbrica sale de aquí).

## Las dos formas de ejecutar el sistema

1. **Modo interactivo** (`python3 main.py`): abre un menú de consola donde
   el usuario escribe la estación de origen y la de destino, y el sistema
   responde con la mejor ruta. Incluye el comando `lista` para ver todas
   las estaciones válidas, y `salir` para terminar.
2. **Modo pruebas** (`python3 main.py --pruebas`): corre automáticamente
   5 casos de prueba diseñados para cubrir distintos escenarios:
   - Caso 1: ruta directa, sin transbordos.
   - Caso 2: ruta con 1 transbordo.
   - Caso 3: ruta con 2 transbordos (el caso más exigente).
   - Caso 4: caso borde — origen igual a destino (debe rechazarse sin
     que el programa se caiga).
   - Caso 5: caso borde — estación de destino inexistente (debe
     rechazarse con un mensaje claro).

## Manejo de errores

La función `imprimir_resultado` revisa siempre el campo
`resultado.encontrada`: si es `False`, se muestra el mensaje de error
correspondiente en lugar de intentar imprimir una ruta que no existe. Esto
evita que el programa se caiga con estaciones mal escritas o inexistentes.

## Sobre el documento de pruebas (PDF)

El archivo `generar_pdf_pruebas.py` (script de apoyo, no es parte del
algoritmo) ejecuta `main.py --pruebas`, captura la salida real de la
consola, y arma con ella el PDF `Pruebas_Sistema_Rutas.pdf`, que es el
entregable de evidencia de pruebas que exige la actividad.

## Cómo lo pueden probar ustedes

```bash
python3 main.py --pruebas
```

## Lo que voy a mostrar en el video

1. Ejecutar el modo interactivo en vivo, pidiendo una ruta al sistema.
2. Ejecutar el modo `--pruebas` y repasar los 5 casos, explicando qué
   valida cada uno.
3. Mostrar brevemente el PDF de pruebas generado y cómo se relaciona con
   la salida de consola que se acaba de ver.
