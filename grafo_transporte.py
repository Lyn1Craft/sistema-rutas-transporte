"""
=====================================================================
 MÓDULO 2 · grafo_transporte.py
 Responsable: Integrante 2
=====================================================================
Este módulo TRADUCE los hechos lógicos derivados por el motor de
inferencia (base_conocimiento.py) en una estructura de GRAFO PONDERADO,
que es la representación que el motor de búsqueda (módulo 3) necesita
para calcular la mejor ruta.

Cada nodo del grafo es una estación. Cada arista representa una
conexión directa entre dos estaciones consecutivas de una misma línea
(hecho conecta(X, Y, L, peso) inferido en el módulo 1).

Además, este módulo aplica la penalización por TRANSBORDO: si para ir
de una estación a otra el sistema debe cambiar de línea, se le suma un
costo adicional (PENALIZACION_TRANSBORDO) al "peso" final del tramo,
simulando el tiempo que toma bajarse de un bus/tren y subirse a otro.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

from base_conocimiento import (
    BaseDeConocimiento,
    construir_base_de_conocimiento,
    PENALIZACION_TRANSBORDO,
)


@dataclass
class Arista:
    """Una arista del grafo: destino, línea usada y peso (minutos)."""
    destino: str
    linea: str
    peso: float


class GrafoTransporte:
    """
    Grafo dirigido y ponderado construido a partir de la base de
    conocimiento. Estructura interna: diccionario de listas de
    adyacencia -> { estacion: [Arista, Arista, ...] }
    """

    def __init__(self, kb: BaseDeConocimiento):
        self.kb = kb
        self.adyacencia: Dict[str, List[Arista]] = {e: [] for e in kb.estaciones}
        self._construir()

    def _construir(self) -> None:
        for conexion in self.kb.conexiones:
            self.adyacencia[conexion.origen].append(
                Arista(destino=conexion.destino, linea=conexion.linea, peso=conexion.peso)
            )

    def vecinos(self, estacion: str) -> List[Arista]:
        return self.adyacencia.get(estacion, [])

    def existe_estacion(self, estacion: str) -> bool:
        return estacion in self.kb.estaciones

    def es_transbordo(self, estacion: str) -> bool:
        return estacion in self.kb.estaciones_transbordo

    def costo_tramo(self, linea_actual: str, arista: Arista) -> float:
        """
        Calcula el costo real de tomar 'arista' viniendo de 'linea_actual'.
        Si la línea cambia (y no es el primer tramo del viaje), se suma
        la penalización de transbordo definida en la base de conocimiento.
        """
        costo = arista.peso
        if linea_actual is not None and linea_actual != arista.linea:
            costo += PENALIZACION_TRANSBORDO
        return costo

    def resumen(self) -> str:
        lineas_totales = len(
            {a.linea for aristas in self.adyacencia.values() for a in aristas}
        )
        return (
            f"Grafo construido: {len(self.kb.estaciones)} estaciones, "
            f"{len(self.kb.conexiones)} conexiones dirigidas, "
            f"{lineas_totales} líneas, "
            f"{len(self.kb.estaciones_transbordo)} estaciones de transbordo."
        )


def construir_grafo() -> GrafoTransporte:
    kb = construir_base_de_conocimiento()
    return GrafoTransporte(kb)


# --- Prueba rápida del módulo de forma aislada -----------------------
if __name__ == "__main__":
    grafo = construir_grafo()
    print(grafo.resumen())
    print("\nVecinos directos de 'Calle_100' (estación de transbordo):")
    for arista in grafo.vecinos("Calle_100"):
        print(f"  -> {arista.destino}  (línea {arista.linea}, {arista.peso} min)")
