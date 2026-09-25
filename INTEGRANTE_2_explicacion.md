# Explicación de mi parte — Integrante 2
### Módulo: `grafo_transporte.py` — Construcción del grafo del sistema de transporte

**[Reemplazar por: Nombre completo del integrante 2]**

## ¿Qué problema resuelve mi módulo?

El módulo 1 (base de conocimiento) entrega conocimiento en forma de
**hechos lógicos** (por ejemplo, `conecta(A, B, linea, peso)`). Pero para
que un algoritmo de búsqueda pueda recorrer ese conocimiento de forma
eficiente, conviene traducirlo a una estructura de datos clásica: un
**grafo ponderado**. De eso se encarga este módulo: es el puente entre la
lógica (módulo 1) y la búsqueda (módulo 3).

## Cómo se construye el grafo

- Cada **estación** es un nodo del grafo.
- Cada **conexión directa** (hecho derivado en el módulo 1) se convierte
  en una **arista** dirigida, guardada en una lista de adyacencia:
  `{ estacion: [Arista(destino, linea, peso), ...] }`.
- La clase `Arista` guarda: la estación destino, la línea que se usa para
  llegar allí, y el peso del tramo en minutos.

## La regla del transbordo

Esta es la parte más importante de mi módulo: el método `costo_tramo`.
Cuando el sistema va a moverse de una estación a otra, este método revisa
si la línea que se necesita usar es **distinta** a la línea con la que se
venía viajando. Si es así, se suma la `PENALIZACION_TRANSBORDO` (definida
en el módulo 1) al costo del tramo. Esto simula el tiempo real que toma
bajarse de una ruta y subirse a otra, y es lo que hace que el sistema
prefiera rutas con menos transbordos cuando el tiempo total es similar.

## Cómo lo pueden probar ustedes

```bash
python3 grafo_transporte.py
```

Esto construye el grafo completo y muestra un resumen (número de
estaciones, conexiones, líneas y estaciones de transbordo), además de
listar los vecinos directos de la estación `Calle_100`, que es una
estación de transbordo entre dos líneas.

## Lo que voy a mostrar en el video

1. Explicar la diferencia entre "hecho lógico" (módulo 1) y "arista de
   grafo" (mi módulo): son la misma información, pero en una forma que
   un algoritmo de búsqueda puede recorrer directamente.
2. Explicar en voz alta la lógica de `costo_tramo`: por qué cambiar de
   línea cuesta más minutos.
3. Ejecutar `python3 grafo_transporte.py` en vivo y mostrar los vecinos
   de una estación de transbordo real.
