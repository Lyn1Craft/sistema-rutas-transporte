"""
=====================================================================
 MÓDULO 1 · base_conocimiento.py
 Responsable: Integrante 1
=====================================================================
Este módulo define la BASE DE CONOCIMIENTO del sistema experto,
representada en forma de HECHOS y REGLAS LÓGICAS (estilo cláusulas
de Horn: "SI antecedente ENTONCES consecuente"), tal como lo pide
la actividad (capítulo 2: lógica y representación del conocimiento;
capítulo 3: sistemas basados en reglas, Benítez 2014).

No se usan librerías externas: se implementa un pequeño MOTOR DE
INFERENCIA HACIA ADELANTE (forward chaining) que parte de los hechos
base (líneas y estaciones) y aplica reglas hasta derivar todo el
conocimiento que necesita el sistema para razonar sobre el transporte
masivo (conexiones directas, estaciones de transbordo, etc).

-----------------------------------------------------------------
1. HECHOS BASE (representan el "mundo": líneas troncales y las
   estaciones que las componen, en orden).
-----------------------------------------------------------------
Cada hecho equivale, en lógica de predicados, a:
        linea(NombreLinea, [estacion_1, estacion_2, ..., estacion_n])

Nota: la red usada es una versión simplificada/didáctica de un
sistema de transporte masivo tipo BRT (buses troncales + estaciones
de transbordo), pensada para que el algoritmo sea claro de explicar
en el video. Pueden reemplazar estos datos por los de su ciudad real.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple


# =====================================================================
# HECHOS BASE: linea(L, [estaciones...])
# =====================================================================
LINEAS: Dict[str, List[str]] = {
    "Troncal_Caracas": [
        "Portal_Norte", "Calle_100", "Calle_72", "Calle_26",
        "Ricaurte", "Portal_Sur",
    ],
    "Troncal_NQS": [
        "Portal_80", "Minuto_de_Dios", "Salitre",
        "Ricaurte", "Restrepo", "Portal_Usme",
    ],
    "Troncal_Suba": [
        "Portal_Suba", "Suba_Calle_116", "Calle_100",
        "Polo", "Heroes",
    ],
    "Troncal_Autonorte": [
        "Portal_Norte", "Calle_106", "Calle_72", "Heroes",
    ],
}

# Tiempo (en minutos) estimado entre dos estaciones consecutivas
# de una misma línea. Se modela como hecho adicional:
#       tiempo_tramo(minutos)
TIEMPO_ENTRE_ESTACIONES_CONSECUTIVAS = 3  # minutos

# Penalización (en minutos) por cada transbordo entre líneas:
#       penalizacion_transbordo(minutos)
PENALIZACION_TRANSBORDO = 5  # minutos


# =====================================================================
# REPRESENTACIÓN DE HECHOS DERIVADOS
# =====================================================================
@dataclass
class Conexion:
    """Hecho derivado:  conecta(origen, destino, linea, peso)"""
    origen: str
    destino: str
    linea: str
    peso: float  # minutos


@dataclass
class BaseDeConocimiento:
    """
    Contenedor de todos los hechos (base y derivados) que el sistema
    experto usará para construir el grafo y razonar sobre rutas.
    """
    estaciones: Set[str] = field(default_factory=set)
    lineas_por_estacion: Dict[str, Set[str]] = field(default_factory=dict)
    conexiones: List[Conexion] = field(default_factory=list)
    estaciones_transbordo: Set[str] = field(default_factory=set)


# =====================================================================
# MOTOR DE INFERENCIA (forward chaining)
# =====================================================================
class MotorInferencia:
    """
    Aplica las reglas lógicas del sistema sobre los hechos base
    (LINEAS) y produce una BaseDeConocimiento con todos los hechos
    derivados que necesita el resto del programa.

    Reglas implementadas (en notación de cláusula de Horn):

    R1  estacion(X)             :- linea(L, Lista), X in Lista.
    R2  conecta(X, Y, L, peso)  :- linea(L, Lista), adyacentes(X, Y, Lista).
                                    (relación simétrica: también conecta(Y,X,L,peso))
    R3  pertenece(X, L)         :- linea(L, Lista), X in Lista.
    R4  es_transbordo(X)        :- pertenece(X, L1), pertenece(X, L2), L1 != L2.
    """

    def __init__(self, lineas: Dict[str, List[str]]):
        self.lineas = lineas

    def inferir(self) -> BaseDeConocimiento:
        kb = BaseDeConocimiento()

        # --- Regla R1 y R3: estaciones y su(s) línea(s) ---
        for linea, estaciones in self.lineas.items():
            for estacion in estaciones:
                kb.estaciones.add(estacion)
                kb.lineas_por_estacion.setdefault(estacion, set()).add(linea)

        # --- Regla R2: conexiones directas (adyacencia dentro de una línea) ---
        for linea, estaciones in self.lineas.items():
            for i in range(len(estaciones) - 1):
                a, b = estaciones[i], estaciones[i + 1]
                kb.conexiones.append(
                    Conexion(a, b, linea, TIEMPO_ENTRE_ESTACIONES_CONSECUTIVAS)
                )
                kb.conexiones.append(
                    Conexion(b, a, linea, TIEMPO_ENTRE_ESTACIONES_CONSECUTIVAS)
                )

        # --- Regla R4: estaciones de transbordo ---
        for estacion, lineas_asociadas in kb.lineas_por_estacion.items():
            if len(lineas_asociadas) > 1:
                kb.estaciones_transbordo.add(estacion)

        return kb


def construir_base_de_conocimiento() -> BaseDeConocimiento:
    """Punto de entrada usado por los demás módulos."""
    motor = MotorInferencia(LINEAS)
    return motor.inferir()


# --- Prueba rápida del módulo de forma aislada -----------------------
if __name__ == "__main__":
    kb = construir_base_de_conocimiento()
    print(f"Estaciones totales derivadas: {len(kb.estaciones)}")
    print(f"Conexiones directas derivadas: {len(kb.conexiones)}")
    print(f"Estaciones de transbordo detectadas: {sorted(kb.estaciones_transbordo)}")
