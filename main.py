"""
=====================================================================
 MÓDULO 4 · main.py
 Responsable: Integrante 4
=====================================================================
Este módulo integra los tres módulos anteriores y ofrece:

  1. Una INTERFAZ DE CONSOLA (CLI) para que el usuario ingrese una
     estación de origen (A) y una de destino (B), y el sistema
     responda con la mejor ruta usando el motor de búsqueda A*.
  2. Una función de BATERÍA DE PRUEBAS (ejecutar_pruebas) que corre
     varios casos de prueba automáticamente y muestra los resultados
     de forma clara. Esta es la salida que se debe capturar
     (pantallazos o texto) para armar el "documento PDF con las
     pruebas realizadas" que pide la rúbrica de la actividad.

Ejecución:
    python3 main.py            -> abre el menú interactivo
    python3 main.py --pruebas  -> corre la batería de pruebas y termina
"""

import sys

from base_conocimiento import construir_base_de_conocimiento, LINEAS
from grafo_transporte import GrafoTransporte, construir_grafo
from motor_busqueda import MotorBusqueda, ResultadoBusqueda


# =====================================================================
# Presentación de resultados
# =====================================================================
def imprimir_resultado(origen: str, destino: str, resultado: ResultadoBusqueda) -> None:
    print("=" * 70)
    print(f"RUTA SOLICITADA: {origen}  ->  {destino}")
    print("=" * 70)
    if not resultado.encontrada:
        print(f"[SIN RUTA] {resultado.mensaje}")
        return

    for i, paso in enumerate(resultado.pasos, start=1):
        etiqueta = " *** TRANSBORDO ***" if paso.es_transbordo else ""
        print(f"  {i}. {paso.origen} -> {paso.destino}   (línea: {paso.linea}){etiqueta}")

    print("-" * 70)
    print(f"Tiempo total estimado : {resultado.tiempo_total} minutos")
    print(f"Número de transbordos : {resultado.numero_transbordos}")
    print(f"Nodos explorados (A*) : {resultado.nodos_explorados}")
    print("=" * 70)
    print()


# =====================================================================
# Menú interactivo
# =====================================================================
def menu_interactivo(motor: MotorBusqueda, estaciones_validas) -> None:
    print("\nSISTEMA EXPERTO DE RUTAS - TRANSPORTE MASIVO")
    print("Escriba 'lista' para ver todas las estaciones disponibles.")
    print("Escriba 'salir' para terminar.\n")

    while True:
        origen = input("Estación de ORIGEN (A): ").strip()
        if origen.lower() == "salir":
            break
        if origen.lower() == "lista":
            print(", ".join(sorted(estaciones_validas)))
            continue

        destino = input("Estación de DESTINO (B): ").strip()
        if destino.lower() == "salir":
            break

        resultado = motor.buscar_mejor_ruta(origen, destino)
        imprimir_resultado(origen, destino, resultado)


# =====================================================================
# Batería de pruebas (evidencia para el PDF de pruebas de la entrega)
# =====================================================================
CASOS_DE_PRUEBA = [
    # (origen, destino, descripción del caso)
    ("Portal_Norte", "Portal_Sur", "Ruta directa por la misma troncal (Caracas)"),
    ("Portal_Suba", "Portal_Sur", "Ruta que requiere transbordo (Suba -> Caracas)"),
    ("Portal_80", "Heroes", "Ruta que requiere dos transbordos (NQS -> Caracas -> Autonorte/Suba)"),
    ("Calle_100", "Calle_100", "Caso borde: origen igual a destino (debe fallar controladamente)"),
    ("Portal_Norte", "Marte", "Caso borde: estación de destino inexistente (debe fallar controladamente)"),
]


def ejecutar_pruebas() -> None:
    kb = construir_base_de_conocimiento()
    grafo = GrafoTransporte(kb)
    motor = MotorBusqueda(grafo)

    print(grafo.resumen())
    print(f"Líneas cargadas: {list(LINEAS.keys())}\n")

    for origen, destino, descripcion in CASOS_DE_PRUEBA:
        print(f"CASO DE PRUEBA: {descripcion}")
        resultado = motor.buscar_mejor_ruta(origen, destino)
        imprimir_resultado(origen, destino, resultado)


def main() -> None:
    if "--pruebas" in sys.argv:
        ejecutar_pruebas()
        return

    grafo = construir_grafo()
    motor = MotorBusqueda(grafo)
    print(grafo.resumen())
    menu_interactivo(motor, grafo.kb.estaciones)


if __name__ == "__main__":
    main()
