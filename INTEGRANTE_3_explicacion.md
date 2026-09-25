# Explicación de mi parte — Integrante 3
### Módulo: `motor_busqueda.py` — Motor de búsqueda heurística A*

**[Reemplazar por: Nombre completo del integrante 3]**

## ¿Qué problema resuelve mi módulo?

Este es el módulo que realmente **encuentra la mejor ruta**. Recibe el
grafo ya construido (módulo 2) y, dadas una estación de origen (A) y una
de destino (B), aplica una **técnica de búsqueda heurística** (capítulo 9
del libro de Benítez) para encontrar el camino de menor tiempo total.

## ¿Por qué A* y no otro algoritmo?

- Una búsqueda "a ciegas" (por ejemplo BFS o Dijkstra puro) revisa el
  grafo sin ninguna intuición de hacia dónde queda el destino.
- **A\*** usa una función `f(n) = g(n) + h(n)`:
  - `g(n)`: lo que **realmente** ya costó llegar hasta el nodo `n`
    (minutos de viaje + transbordos ya pagados).
  - `h(n)`: una **estimación** de lo que falta para llegar al destino.
- Mi heurística `h(n)` es el número mínimo de "saltos" entre estaciones
  hasta el destino (calculado una sola vez con BFS sin pesos), convertido
  a minutos usando el costo mínimo posible por tramo.
- Esta heurística es **admisible** (nunca sobreestima el costo real),
  porque en la vida real ningún tramo puede costar menos de ese mínimo.
  Eso **garantiza matemáticamente** que A* encuentre la ruta óptima, y
  además explora menos nodos que una búsqueda ciega (lo pueden ver en el
  campo `nodos_explorados` que imprime cada resultado).

## Detalle importante: el "estado" incluye la línea actual

No basta con saber en qué estación está el viajero: también hace falta
saber **con qué línea llegó**, porque el costo del siguiente tramo
depende de si toca hacer transbordo o no. Por eso cada nodo de búsqueda es
en realidad la pareja `(estacion, linea_actual)`, no solo la estación.

## Cómo lo pueden probar ustedes

```bash
python3 motor_busqueda.py
```

Esto calcula la ruta óptima entre `Portal_Suba` y `Portal_Sur`, mostrando
cada tramo, cuáles son transbordo, el tiempo total y cuántos nodos exploró
el algoritmo.

## Lo que voy a mostrar en el video

1. Explicar con un dibujo/diagrama simple qué es `f(n) = g(n) + h(n)`.
2. Explicar por qué mi heurística es admisible y qué pasaría si no lo
   fuera (podría dar una ruta que "parece" buena pero no es la óptima).
3. Ejecutar `python3 motor_busqueda.py` en vivo y comentar la ruta y el
   número de nodos explorados.
