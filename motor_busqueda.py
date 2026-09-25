"""
=====================================================================
 MÓDULO 3 · motor_busqueda.py
 Responsable: Integrante 3
=====================================================================
Este módulo implementa la ESTRATEGIA DE BÚSQUEDA HEURÍSTICA (capítulo
9: técnicas basadas en búsquedas heurísticas, Benítez 2014) que el
sistema experto usa para encontrar la MEJOR RUTA entre una estación
de origen (A) y una de destino (B).

Algoritmo usado: A* (A-estrella).

Por qué A* y no solo Dijkstra o BFS:
  - Dijkstra (búsqueda de costo uniforme) SIEMPRE encuentra la ruta
    óptima, pero explora el grafo "a ciegas", sin usar ninguna
    información adicional sobre qué tan cerca está del destino.
  - A* usa además una FUNCIÓN HEURÍSTICA h(n) que estima cuánto falta
    para llegar al destino, lo que le permite priorizar los caminos
    más prometedores y explorar menos nodos.
  - Aquí h(n) = número mínimo de "saltos" (conexiones) entre la
    estación actual y el destino, calculado con un BFS previo sobre
    el grafo sin pesos. Esta heurística es ADMISIBLE (nunca
    sobreestima el costo real) porque cada salto cuesta como mínimo
    TIEMPO_ENTRE_ESTACIONES_CONSECUTIVAS minutos, así que
    h(n) * TIEMPO_ENTRE_ESTACIONES_CONSECUTIVAS es siempre <= al
    costo real restante. Esto garantiza que A* encuentre la ruta
    óptima (mínimo tiempo total, incluyendo transbordos).

f(n) = g(n) + h(n)
  g(n): costo real acumulado desde el origen hasta el nodo n
        (minutos de viaje + penalizaciones de transbordo ya pagadas)
  h(n): estimación heurística del costo restante hasta el destino
"""

import heapq
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from base_conocimiento import TIEMPO_ENTRE_ESTACIONES_CONSECUTIVAS
from grafo_transporte import GrafoTransporte


@dataclass
class PasoRuta:
    """Un tramo de la ruta final: de qué estación a cuál, en qué línea."""
    origen: str
    destino: str
    linea: str
    es_transbordo: bool


@dataclass
class ResultadoBusqueda:
    encontrada: bool
    pasos: List[PasoRuta] = field(default_factory=list)
    tiempo_total: float = 0.0
    numero_transbordos: int = 0
    nodos_explorados: int = 0
    mensaje: str = ""


class MotorBusqueda:
    def __init__(self, grafo: GrafoTransporte):
        self.grafo = grafo

    # -----------------------------------------------------------------
    # Heurística admisible: distancia mínima en NÚMERO DE SALTOS entre
    # cada estación y el destino, calculada una sola vez con BFS
    # (Breadth-First Search) sobre el grafo sin pesos.
    # -----------------------------------------------------------------
    def _calcular_heuristica(self, destino: str) -> Dict[str, float]:
        distancias: Dict[str, int] = {destino: 0}
        cola = deque([destino])
        while cola:
            actual = cola.popleft()
            for arista in self.grafo.vecinos(actual):
                if arista.destino not in distancias:
                    distancias[arista.destino] = distancias[actual] + 1
                    cola.append(arista.destino)

        # Se convierte de "número de saltos" a "minutos estimados",
        # usando el costo mínimo posible por salto (sin transbordos),
        # para que la heurística nunca sobreestime el costo real.
        return {
            estacion: saltos * TIEMPO_ENTRE_ESTACIONES_CONSECUTIVAS
            for estacion, saltos in distancias.items()
        }

    # -----------------------------------------------------------------
    # Búsqueda A*
    # -----------------------------------------------------------------
    def buscar_mejor_ruta(self, origen: str, destino: str) -> ResultadoBusqueda:
        if not self.grafo.existe_estacion(origen):
            return ResultadoBusqueda(False, mensaje=f"La estación de origen '{origen}' no existe.")
        if not self.grafo.existe_estacion(destino):
            return ResultadoBusqueda(False, mensaje=f"La estación de destino '{destino}' no existe.")
        if origen == destino:
            return ResultadoBusqueda(False, mensaje="El origen y el destino son la misma estación.")

        h = self._calcular_heuristica(destino)
        if destino not in h or origen not in h:
            return ResultadoBusqueda(False, mensaje="No existe una ruta posible entre esas estaciones.")

        # Estado del problema de búsqueda: (estacion, linea_con_la_que_se_llegó)
        # Se incluye la línea porque el costo de la SIGUIENTE arista depende
        # de si implica transbordo o no (el "estado" debe capturar eso).
        EstadoNodo = Tuple[str, Optional[str]]

        contador = 0  # desempate estable en el heap
        estado_inicial: EstadoNodo = (origen, None)
        frontera: List[Tuple[float, int, EstadoNodo]] = [(h[origen], contador, estado_inicial)]

        costo_g: Dict[EstadoNodo, float] = {estado_inicial: 0.0}
        padre: Dict[EstadoNodo, Optional[EstadoNodo]] = {estado_inicial: None}
        linea_usada_para_llegar: Dict[EstadoNodo, Optional[str]] = {estado_inicial: None}

        nodos_explorados = 0
        visitados = set()

        while frontera:
            _, _, estado_actual = heapq.heappop(frontera)
            if estado_actual in visitados:
                continue
            visitados.add(estado_actual)
            nodos_explorados += 1

            estacion_actual, linea_actual = estado_actual

            if estacion_actual == destino:
                return self._reconstruir_resultado(
                    padre, estado_actual, costo_g[estado_actual], nodos_explorados
                )

            for arista in self.grafo.vecinos(estacion_actual):
                costo_tramo = self.grafo.costo_tramo(linea_actual, arista)
                nuevo_estado: EstadoNodo = (arista.destino, arista.linea)
                nuevo_g = costo_g[estado_actual] + costo_tramo

                if nuevo_estado not in costo_g or nuevo_g < costo_g[nuevo_estado]:
                    costo_g[nuevo_estado] = nuevo_g
                    padre[nuevo_estado] = estado_actual
                    linea_usada_para_llegar[nuevo_estado] = arista.linea
                    f = nuevo_g + h.get(arista.destino, float("inf"))
                    contador += 1
                    heapq.heappush(frontera, (f, contador, nuevo_estado))

        return ResultadoBusqueda(
            False, mensaje="No se encontró una ruta posible.", nodos_explorados=nodos_explorados
        )

    def _reconstruir_resultado(self, padre, estado_final, costo_total, nodos_explorados) -> ResultadoBusqueda:
        secuencia = []
        estado = estado_final
        while estado is not None:
            secuencia.append(estado)
            estado = padre[estado]
        secuencia.reverse()  # ahora va de origen -> destino

        pasos: List[PasoRuta] = []
        transbordos = 0
        linea_previa = None
        for i in range(1, len(secuencia)):
            estacion_prev, _ = secuencia[i - 1]
            estacion_act, linea_act = secuencia[i]
            es_transbordo = linea_previa is not None and linea_previa != linea_act
            if es_transbordo:
                transbordos += 1
            pasos.append(PasoRuta(estacion_prev, estacion_act, linea_act, es_transbordo))
            linea_previa = linea_act

        return ResultadoBusqueda(
            encontrada=True,
            pasos=pasos,
            tiempo_total=costo_total,
            numero_transbordos=transbordos,
            nodos_explorados=nodos_explorados,
            mensaje="Ruta encontrada.",
        )


# --- Prueba rápida del módulo de forma aislada -----------------------
if __name__ == "__main__":
    from grafo_transporte import construir_grafo

    grafo = construir_grafo()
    motor = MotorBusqueda(grafo)
    resultado = motor.buscar_mejor_ruta("Portal_Suba", "Portal_Sur")

    if resultado.encontrada:
        print(f"Tiempo total: {resultado.tiempo_total} min | "
              f"Transbordos: {resultado.numero_transbordos} | "
              f"Nodos explorados: {resultado.nodos_explorados}")
        for paso in resultado.pasos:
            marca = " (TRANSBORDO)" if paso.es_transbordo else ""
            print(f"  {paso.origen} -> {paso.destino}  [{paso.linea}]{marca}")
    else:
        print(resultado.mensaje)
