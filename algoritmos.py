"""
Módulo de Algoritmos de Búsqueda No Informada: BFS, DFS, IDDFS y UCS
Maestría en Inteligencia Artificial - Universidad Sergio Arboleda
Autor: Bryan Orozco - Promoción XI / XII
"""

import time
import tracemalloc
from collections import deque
import heapq
from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple, Set


@dataclass
class ResultadoBusqueda:
    algoritmo: str
    exito: bool
    camino: List[Any] = field(default_factory=list)
    acciones: List[Any] = field(default_factory=list)
    costo_total: float = 0.0
    tiempo_ms: float = 0.0
    memoria_kb: float = 0.0
    nodos_expandidos: int = 0
    nodos_generados: int = 0
    profundidad: int = 0

    def resumen(self) -> str:
        estado_str = "EXITO" if self.exito else "FALLO"
        return (
            f"[{self.algoritmo}] {estado_str} | "
            f"Pasos: {len(self.acciones)} | "
            f"Costo: {self.costo_total:.2f} | "
            f"Nodos Exp.: {self.nodos_expandidos} | "
            f"Nodos Gen.: {self.nodos_generados} | "
            f"Tiempo: {self.tiempo_ms:.3f} ms | "
            f"Memoria: {self.memoria_kb:.2f} KB"
        )


class ProblemaBusqueda:
    """Clase base abstracta para formular un problema de búsqueda formal."""

    def __init__(self, estado_inicial: Any):
        self.estado_inicial = estado_inicial

    def es_objetivo(self, estado: Any) -> bool:
        raise NotImplementedError

    def acciones(self, estado: Any) -> List[Any]:
        raise NotImplementedError

    def resultado(self, estado: Any, accion: Any) -> Any:
        raise NotImplementedError

    def costo(self, estado: Any, accion: Any, estado_siguiente: Any) -> float:
        return 1.0


# ==============================================================================
# 1. BFS (Breadth-First Search / Búsqueda en Anchura - Cola FIFO)
# ==============================================================================
def bfs(problema: ProblemaBusqueda) -> ResultadoBusqueda:
    tracemalloc.start()
    t_inicio = time.perf_counter()

    inicio = problema.estado_inicial
    nodos_expandidos = 0
    nodos_generados = 1

    if problema.es_objetivo(inicio):
        t_fin = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return ResultadoBusqueda(
            algoritmo="BFS",
            exito=True,
            camino=[inicio],
            acciones=[],
            costo_total=0.0,
            tiempo_ms=(t_fin - t_inicio) * 1000.0,
            memoria_kb=peak / 1024.0,
            nodos_expandidos=0,
            nodos_generados=1,
            profundidad=0
        )

    # Cola FIFO guarda tuplas: (estado_actual, [camino_estados], [acciones_realizadas], costo_acumulado)
    frontera = deque([(inicio, [inicio], [], 0.0)])
    visitados = {inicio}

    while frontera:
        actual, camino, accs, costo_acum = frontera.popleft()
        nodos_expandidos += 1

        for accion in problema.acciones(actual):
            hijo = problema.resultado(actual, accion)
            nodos_generados += 1

            if hijo not in visitados:
                paso_costo = problema.costo(actual, accion, hijo)
                nuevo_costo = costo_acum + paso_costo
                nuevo_camino = camino + [hijo]
                nuevas_accs = accs + [accion]

                # Prueba de objetivo en generación (Regla BFS óptimo en saltos)
                if problema.es_objetivo(hijo):
                    t_fin = time.perf_counter()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    return ResultadoBusqueda(
                        algoritmo="BFS",
                        exito=True,
                        camino=nuevo_camino,
                        acciones=nuevas_accs,
                        costo_total=nuevo_costo,
                        tiempo_ms=(t_fin - t_inicio) * 1000.0,
                        memoria_kb=peak / 1024.0,
                        nodos_expandidos=nodos_expandidos,
                        nodos_generados=nodos_generados,
                        profundidad=len(nuevas_accs)
                    )

                visitados.add(hijo)
                frontera.append((hijo, nuevo_camino, nuevas_accs, nuevo_costo))

    t_fin = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return ResultadoBusqueda(
        algoritmo="BFS",
        exito=False,
        tiempo_ms=(t_fin - t_inicio) * 1000.0,
        memoria_kb=peak / 1024.0,
        nodos_expandidos=nodos_expandidos,
        nodos_generados=nodos_generados
    )


# ==============================================================================
# 2. DFS (Depth-First Search / Búsqueda en Profundidad - Pila LIFO)
# ==============================================================================
def dfs(problema: ProblemaBusqueda, max_iteraciones: int = 150000) -> ResultadoBusqueda:
    tracemalloc.start()
    t_inicio = time.perf_counter()

    inicio = problema.estado_inicial
    nodos_expandidos = 0
    nodos_generados = 1

    # Pila LIFO guarda: (estado_actual, [camino], [acciones], costo)
    pila = [(inicio, [inicio], [], 0.0)]
    visitados = set()

    while pila and nodos_expandidos < max_iteraciones:
        actual, camino, accs, costo_acum = pila.pop()

        if problema.es_objetivo(actual):
            t_fin = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return ResultadoBusqueda(
                algoritmo="DFS",
                exito=True,
                camino=camino,
                acciones=accs,
                costo_total=costo_acum,
                tiempo_ms=(t_fin - t_inicio) * 1000.0,
                memoria_kb=peak / 1024.0,
                nodos_expandidos=nodos_expandidos,
                nodos_generados=nodos_generados,
                profundidad=len(accs)
            )

        if actual in visitados:
            continue
        visitados.add(actual)
        nodos_expandidos += 1

        # reversed() para explorar de izquierda a derecha en LIFO
        acciones_disponibles = problema.acciones(actual)
        for accion in reversed(acciones_disponibles):
            hijo = problema.resultado(actual, accion)
            nodos_generados += 1
            if hijo not in visitados:
                paso_costo = problema.costo(actual, accion, hijo)
                pila.append((hijo, camino + [hijo], accs + [accion], costo_acum + paso_costo))

    t_fin = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return ResultadoBusqueda(
        algoritmo="DFS",
        exito=False,
        tiempo_ms=(t_fin - t_inicio) * 1000.0,
        memoria_kb=peak / 1024.0,
        nodos_expandidos=nodos_expandidos,
        nodos_generados=nodos_generados
    )


# ==============================================================================
# 3. IDDFS (Iterative Deepening Depth-First Search - Profundidad Iterativa)
# ==============================================================================
def _dls(problema: ProblemaBusqueda, estado: Any, limite: int, camino: List[Any], accs: List[Any], costo_acum: float, contadores: dict, visitados_rama: Set[Any]):
    contadores['expandidos'] += 1

    if problema.es_objetivo(estado):
        return (True, camino, accs, costo_acum, False)  # (exito, camino, accs, costo, cutoff)

    if limite <= 0:
        return (False, None, None, 0.0, True)  # Corte alcanzado

    hubo_corte = False
    for accion in problema.acciones(estado):
        hijo = problema.resultado(estado, accion)
        contadores['generados'] += 1

        # Evita ciclos en la rama viva actual
        if hijo in visitados_rama:
            continue

        paso_costo = problema.costo(estado, accion, hijo)
        visitados_rama.add(hijo)
        exito, res_camino, res_accs, res_costo, cutoff = _dls(
            problema, hijo, limite - 1,
            camino + [hijo], accs + [accion],
            costo_acum + paso_costo, contadores, visitados_rama
        )
        visitados_rama.remove(hijo)

        if exito:
            return (True, res_camino, res_accs, res_costo, False)
        if cutoff:
            hubo_corte = True

    return (False, None, None, 0.0, hubo_corte)


def iddfs(problema: ProblemaBusqueda, max_profundidad: int = 50) -> ResultadoBusqueda:
    tracemalloc.start()
    t_inicio = time.perf_counter()

    contadores = {'expandidos': 0, 'generados': 1}
    inicio = problema.estado_inicial

    for limite in range(max_profundidad + 1):
        visitados_rama = {inicio}
        exito, camino, accs, costo_total, hubo_corte = _dls(
            problema, inicio, limite, [inicio], [], 0.0, contadores, visitados_rama
        )
        if exito:
            t_fin = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return ResultadoBusqueda(
                algoritmo="IDDFS",
                exito=True,
                camino=camino,
                acciones=accs,
                costo_total=costo_total,
                tiempo_ms=(t_fin - t_inicio) * 1000.0,
                memoria_kb=peak / 1024.0,
                nodos_expandidos=contadores['expandidos'],
                nodos_generados=contadores['generados'],
                profundidad=len(accs)
            )
        if not hubo_corte:
            # Si en este nivel no hubo cortes, el espacio finito se agotó sin solución
            break

    t_fin = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return ResultadoBusqueda(
        algoritmo="IDDFS",
        exito=False,
        tiempo_ms=(t_fin - t_inicio) * 1000.0,
        memoria_kb=peak / 1024.0,
        nodos_expandidos=contadores['expandidos'],
        nodos_generados=contadores['generados']
    )


# ==============================================================================
# 4. UCS (Uniform-Cost Search / Costo Uniforme - Dijkstra con Min-Heap)
# ==============================================================================
def ucs(problema: ProblemaBusqueda) -> ResultadoBusqueda:
    tracemalloc.start()
    t_inicio = time.perf_counter()

    inicio = problema.estado_inicial
    nodos_expandidos = 0
    nodos_generados = 1

    # Elementos en heap: (costo_acumulado, id_unico, estado, camino, acciones)
    # id_unico desempatador para evitar comparar estados complejos en heap
    id_contador = 0
    frontera = [(0.0, id_contador, inicio, [inicio], [])]
    visitados = set()

    while frontera:
        costo_acum, _, actual, camino, accs = heapq.heappop(frontera)

        # REGLA CRÍTICA DE CLASE: Prueba de objetivo al EXTRAER de la cola de prioridad
        if problema.es_objetivo(actual):
            t_fin = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return ResultadoBusqueda(
                algoritmo="UCS",
                exito=True,
                camino=camino,
                acciones=accs,
                costo_total=costo_acum,
                tiempo_ms=(t_fin - t_inicio) * 1000.0,
                memoria_kb=peak / 1024.0,
                nodos_expandidos=nodos_expandidos,
                nodos_generados=nodos_generados,
                profundidad=len(accs)
            )

        if actual in visitados:
            continue
        visitados.add(actual)
        nodos_expandidos += 1

        for accion in problema.acciones(actual):
            hijo = problema.resultado(actual, accion)
            nodos_generados += 1
            if hijo not in visitados:
                paso_costo = problema.costo(actual, accion, hijo)
                nuevo_costo = costo_acum + paso_costo
                id_contador += 1
                heapq.heappush(
                    frontera,
                    (nuevo_costo, id_contador, hijo, camino + [hijo], accs + [accion])
                )

    t_fin = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return ResultadoBusqueda(
        algoritmo="UCS",
        exito=False,
        tiempo_ms=(t_fin - t_inicio) * 1000.0,
        memoria_kb=peak / 1024.0,
        nodos_expandidos=nodos_expandidos,
        nodos_generados=nodos_generados
    )
