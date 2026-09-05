"""
================================================================================
TALLER 2: ALGORITMOS DE BÚSQUEDA NO INFORMADA (BFS, DFS, IDDFS Y UCS)
REPRESENTACIÓN COMPUTACIONAL DE 4 PROBLEMAS CLÁSICOS & BENCHMARKING
================================================================================
Estudiante: Bryan Orozco
Programa: Maestría en Inteligencia Artificial (Promoción XI / XII)
Institución: Universidad Sergio Arboleda
Docente: Prof. Joaquín F. Sánchez Cifuentes

Problemas Desarrollados:
1. Puzzle 3x3 (8-Puzzle)
2. N-Reinas (N-Queens)
3. Problema de la Mochila 0/1 (Knapsack con Listas de Pesos y Valores)
4. Problema del Agente Viajero (TSP con Matriz de Distancias de Colombia)

Métricas Evaluadas:
- Tiempo de ejecución (ms con time.perf_counter)
- Consumo de memoria RAM pico (KB con tracemalloc)
- Cantidad de nodos expandidos y generados
- Optimalidad y costo acumulado de la ruta
================================================================================
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from algoritmos import bfs, dfs, iddfs, ucs
from problemas import (
    ProblemaPuzzle3x3,
    ProblemaNReinas,
    ProblemaMochila,
    ProblemaAgenteViajero
)
from benchmark import correr_suite_completa, imprimir_tabla_comparativa


def menu_interactivo():
    while True:
        print("\n" + "=" * 70)
        print("🏛️ MAESTRÍA EN IA - TALLER 2: BÚSQUEDA NO INFORMADA")
        print("=" * 70)
        print("1. Ejecutar Benchmark Completo (Todos los algoritmos y problemas)")
        print("2. Demostración Paso a Paso: Puzzle 3x3 (8-Puzzle)")
        print("3. Demostración Paso a Paso: N-Reinas (N=4)")
        print("4. Demostración Paso a Paso: Problema de la Mochila 0/1")
        print("5. Demostración Paso a Paso: Agente Viajero (TSP Colombia)")
        print("6. Salir")
        print("=" * 70)

        opcion = input("Selecciona una opción [1-6]: ").strip()

        if opcion == "1":
            correr_suite_completa()

        elif opcion == "2":
            prob = ProblemaPuzzle3x3()
            print("\n--- RESOLVIENDO PUZZLE 3x3 CON UCS Y BFS ---")
            res_ucs = ucs(prob)
            print(res_ucs.resumen())
            print("\nCamino paso a paso:")
            for i, estado in enumerate(res_ucs.camino):
                print(f"\nPaso {i}:")
                print(ProblemaPuzzle3x3.formatear(estado))

        elif opcion == "3":
            n_in = input("Ingresa la cantidad de Reinas N (ej. 4, 5, 8, por defecto 4): ").strip()
            n = int(n_in) if n_in.isdigit() and int(n_in) >= 4 else 4
            prob = ProblemaNReinas(n=n)
            print(f"\n--- RESOLVIENDO {n}-REINAS CON DFS ---")
            res_dfs = dfs(prob)
            print(res_dfs.resumen())
            if res_dfs.exito and res_dfs.camino:
                sol = res_dfs.camino[-1]
                print(f"\nPosición de Reinas (Columna C_i -> Fila F_j):")
                for col_idx, fila_idx in enumerate(sol):
                    print(f"  • Reina {col_idx+1}: Columna {col_idx+1}, Fila {fila_idx+1}")
                print(f"\nMatriz del Tablero {n}×{n} con las Reinas Pintadas (Q):")
                print(ProblemaNReinas.formatear(sol, n))
            else:
                print(f"\n[!] No se encontró solución para N={n}")

        elif opcion == "4":
            prob = ProblemaMochila(pesos=[2, 3, 4, 5], valores=[3, 4, 8, 8], capacidad=7)
            print("\n--- RESOLVIENDO MOCHILA 0/1 CON UCS (OPTIMIZANDO VALOR) ---")
            res_ucs = ucs(prob)
            print(res_ucs.resumen())
            if res_ucs.exito:
                _, _, seleccion = res_ucs.camino[-1]
                peso_usado = sum(p for p, s in zip(prob.pesos, seleccion) if s == 1)
                valor_ganado = sum(v for v, s in zip(prob.valores, seleccion) if s == 1)
                print(f"\nDecisión por objeto: {seleccion}")
                print(f"Peso Utilizado: {peso_usado} / {prob.capacidad}")
                print(f"Valor Total Obtenido: {valor_ganado}")

        elif opcion == "5":
            print("\n========================================================")
            print("  SELECTOR DE RUTAS: BOGOTÁ HASTA LA PATAGONIA (TSP)   ")
            print("========================================================")
            print("1. Ruta Panamericana Clásica (6 Ciudades: Bogotá, Quito, Lima, Santiago, Buenos Aires, Ushuaia)")
            print("2. Ruta Andina Pacífico (5 Ciudades: Bogotá, Quito, Lima, Santiago, Ushuaia)")
            print("3. Ruta Directa Rápida (4 Ciudades: Bogotá, Lima, Buenos Aires, Ushuaia)")
            print("4. Gran Travesía Total (8 Ciudades con La Paz y Bariloche)")
            
            sub_opc = input("\nElige una ruta [1-4, por defecto 1]: ").strip() or "1"
            
            if sub_opc == "2":
                ciudades_sel = ["Bogotá", "Quito", "Lima", "Santiago", "Ushuaia (Patagonia Sur)"]
                nombre_ruta = "Ruta Andina Pacífico"
            elif sub_opc == "3":
                ciudades_sel = ["Bogotá", "Lima", "Buenos Aires", "Ushuaia (Patagonia Sur)"]
                nombre_ruta = "Ruta Directa Rápida"
            elif sub_opc == "4":
                ciudades_sel = list(ProblemaAgenteViajero.CIUDADES_DISPONIBLES)
                nombre_ruta = "Gran Travesía Total (8 Ciudades)"
            else:
                ciudades_sel = list(ProblemaAgenteViajero.CIUDADES_DEFAULT)
                nombre_ruta = "Ruta Panamericana Clásica (6 Ciudades)"

            prob = ProblemaAgenteViajero(ciudades=ciudades_sel)
            print(f"\n--- RESOLVIENDO {nombre_ruta.upper()} CON UCS (DIJKSTRA) ---")
            print(f"Ciudades seleccionadas ({len(ciudades_sel)}): {', '.join(ciudades_sel)}")
            
            res_ucs = ucs(prob)
            res_bfs = bfs(prob)
            print("\n" + res_ucs.resumen())
            
            if res_ucs.exito:
                ruta = res_ucs.camino[-1]
                print(f"\n🗺️ Ruta Óptima Calculada (UCS):")
                for idx in range(len(ruta) - 1):
                    c_act = ruta[idx]
                    c_sig = ruta[idx+1]
                    dist = prob.distancia_entre(c_act, c_sig)
                    print(f"  Tramo {idx+1}: {c_act:<28} ──({dist:>5.0f} km)──> {c_sig}")
                
                ahorro = res_bfs.costo_total - res_ucs.costo_total
                print(f"\nDistancia Total UCS: {res_ucs.costo_total:.0f} km")
                print(f"Distancia Total BFS: {res_bfs.costo_total:.0f} km")
                if ahorro > 0:
                    print(f"⚡ ¡Ahorro con UCS!: {ahorro:.0f} km menos de recorrido gracias a optimización de costo.")

        elif opcion == "6":
            print("\n¡Hasta pronto!")
            break
        else:
            print("[!] Opción inválida. Digita un número del 1 al 6.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        correr_suite_completa()
    else:
        # Por defecto corre la suite completa para demostrar su funcionamiento
        correr_suite_completa()
