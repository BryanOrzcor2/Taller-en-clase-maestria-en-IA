"""
Módulo de Experimentación y Benchmarking:
Mide cuantitativamente Tiempo (ms) y Memoria Pico (KB) de BFS, DFS, IDDFS y UCS
sobre los 4 problemas del Taller 2.
"""

import sys
import json

# Soporte completo UTF-8 en terminal de Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from typing import Dict, List, Any
from algoritmos import bfs, dfs, iddfs, ucs, ResultadoBusqueda
from problemas import (
    ProblemaPuzzle3x3,
    ProblemaNReinas,
    ProblemaMochila,
    ProblemaAgenteViajero
)


def ejecutar_benchmark_problema(nombre_problema: str, instancia_problema) -> List[ResultadoBusqueda]:
    """Ejecuta los 4 algoritmos sobre una instancia de problema y retorna sus métricas."""
    algoritmos_funcs = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("IDDFS", iddfs),
        ("UCS", ucs)
    ]

    resultados = []
    print(f"\n" + "=" * 80)
    print(f">> EJECUTANDO BENCHMARK: {nombre_problema}")
    print("=" * 80)

    for nombre_alg, func in algoritmos_funcs:
        print(f"   Corriendo {nombre_alg}...", end="", flush=True)
        res = func(instancia_problema)
        resultados.append(res)
        print(f" Listo! -> {res.resumen()}")

    return resultados


def imprimir_tabla_comparativa(nombre_problema: str, resultados: List[ResultadoBusqueda]):
    """Imprime una tabla formateada en consola con métricas de tiempo y memoria."""
    print(f"\n📊 TABLA COMPARATIVA: {nombre_problema}")
    header = f"{'Algoritmo':<10} | {'Éxito':<7} | {'Pasos':<7} | {'Costo':<10} | {'Nodos Exp.':<12} | {'Tiempo (ms)':<14} | {'Memoria (KB)':<14}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    for r in resultados:
        exito_str = "Sí" if r.exito else "No"
        pasos_str = str(len(r.acciones)) if r.exito else "-"
        costo_str = f"{r.costo_total:.1f}" if r.exito else "-"
        print(
            f"{r.algoritmo:<10} | {exito_str:<7} | {pasos_str:<7} | {costo_str:<10} | "
            f"{r.nodos_expandidos:<12} | {r.tiempo_ms:<14.3f} | {r.memoria_kb:<14.2f}"
        )
    print("-" * len(header))


def serializar_resultados(bateria_resultados: Dict[str, List[ResultadoBusqueda]]) -> str:
    """Convierte los resultados a JSON para alimentar la interfaz web o reportes."""
    data = {}
    for prob_nombre, lista_res in bateria_resultados.items():
        data[prob_nombre] = []
        for r in lista_res:
            data[prob_nombre].append({
                "algoritmo": r.algoritmo,
                "exito": r.exito,
                "num_pasos": len(r.acciones),
                "costo_total": r.costo_total,
                "tiempo_ms": round(r.tiempo_ms, 3),
                "memoria_kb": round(r.memoria_kb, 2),
                "nodos_expandidos": r.nodos_expandidos,
                "nodos_generados": r.nodos_generados,
                "acciones": [str(a) for a in r.acciones]
            })
    return json.dumps(data, indent=2, ensure_ascii=False)


def correr_suite_completa():
    problemas = [
        ("1. Puzzle 3x3 (8-Puzzle)", ProblemaPuzzle3x3()),
        ("2. N-Reinas (N=4)", ProblemaNReinas(n=4)),
        ("3. Mochila 0/1 (Listas de Objetos)", ProblemaMochila(pesos=[2, 3, 4, 5], valores=[3, 4, 8, 8], capacidad=7)),
        ("4. Agente Viajero (TSP - Bogotá hasta La Patagonia)", ProblemaAgenteViajero())
    ]

    todo = {}
    for nombre, inst in problemas:
        res = ejecutar_benchmark_problema(nombre, inst)
        todo[nombre] = res
        imprimir_tabla_comparativa(nombre, res)

    # Guardar dump en JSON para el frontend web
    json_path = "benchmark_resultados.json"
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(serializar_resultados(todo))
    print(f"\n[OK] Resultados guardados para el Frontend en: {json_path}")

    return todo


if __name__ == "__main__":
    correr_suite_completa()
