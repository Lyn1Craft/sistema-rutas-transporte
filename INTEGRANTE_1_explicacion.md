# Explicación de mi parte — Integrante 1
### Módulo: `base_conocimiento.py` — Base de conocimiento y motor de inferencia

**[Reemplazar por: Nombre completo del integrante 1]**

## ¿Qué problema resuelve mi módulo?

Antes de poder buscar una ruta, el sistema necesita **saber** cómo está
organizado el transporte masivo: qué líneas existen, qué estaciones tiene
cada una, en qué orden, y cuáles estaciones permiten cambiarse de línea
(transbordo). Toda esa información se representa aquí como una **base de
conocimiento en reglas lógicas**, tal como lo pide la actividad.

## Representación del conocimiento usada

Sigo el enfoque de cláusulas de Horn (SI ... ENTONCES ...) visto en el
capítulo 2 y 3 del libro de Benítez (2014):

- **Hechos base:** `linea(NombreLinea, [estacion_1, estacion_2, ...])`.
  En el código esto es el diccionario `LINEAS`.
- **Regla 1:** `estacion(X) :- linea(L, Lista), X in Lista.`
  (una estación existe si aparece en alguna línea)
- **Regla 2:** `conecta(X, Y, L, peso) :- linea(L, Lista), adyacentes(X, Y, Lista).`
  (dos estaciones están conectadas directamente si son consecutivas en una
  misma línea; la relación es simétrica, se puede ir en ambos sentidos)
- **Regla 3:** `pertenece(X, L) :- linea(L, Lista), X in Lista.`
  (a qué línea(s) pertenece cada estación)
- **Regla 4:** `es_transbordo(X) :- pertenece(X, L1), pertenece(X, L2), L1 != L2.`
  (una estación es de transbordo si pertenece a más de una línea)

## Cómo funciona el motor de inferencia

La clase `MotorInferencia` implementa **encadenamiento hacia adelante**
(*forward chaining*): parte únicamente de los hechos base (`LINEAS`) y va
aplicando las reglas anteriores hasta derivar todo el conocimiento que el
resto del sistema necesita, que queda guardado en un objeto
`BaseDeConocimiento` con:

- `estaciones`: todas las estaciones del sistema.
- `lineas_por_estacion`: a qué línea(s) pertenece cada estación.
- `conexiones`: todas las conexiones directas ya derivadas (con su peso en
  minutos).
- `estaciones_transbordo`: las estaciones donde se puede cambiar de línea
  (calculadas automáticamente, no manualmente).

## Cómo lo pueden probar ustedes

```bash
python3 base_conocimiento.py
```

Esto imprime cuántas estaciones y conexiones se derivaron, y cuáles
estaciones fueron detectadas como transbordo, sin que nadie las haya
escrito explícitamente: son el resultado de aplicar la Regla 4.

## Lo que voy a mostrar en el video

1. Mostrar el diccionario `LINEAS` (los hechos base).
2. Explicar, con una de las reglas, cómo se pasa de hecho a hecho
   derivado (por ejemplo, cómo `Calle_100` termina siendo detectada como
   transbordo porque aparece en `Troncal_Caracas` y en `Troncal_Suba`).
3. Ejecutar `python3 base_conocimiento.py` en vivo y explicar la salida.
