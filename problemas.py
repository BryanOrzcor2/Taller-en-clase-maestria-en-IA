"""
Módulo de Representación Computacional de Problemas Formales de IA:
1. Puzzle 3x3 (8-Puzzle)
2. N-Reinas (N-Queens)
3. Mochila 0/1 (0/1 Knapsack basado en listas)
4. Agente Viajero (TSP basado en Matriz de Adyacencia)

Maestría en Inteligencia Artificial - Universidad Sergio Arboleda
"""

from typing import List, Tuple, Any, Dict
from algoritmos import ProblemaBusqueda


# ==============================================================================
# 1. PROBLEMA: PUZZLE 3x3 (8-PUZZLE)
# ==============================================================================
class ProblemaPuzzle3x3(ProblemaBusqueda):
    """
    Representación del 8-Puzzle:
    - Estado: Tupla inmutable de 9 números de 0 a 8 (0 representa el espacio vacío).
      Ej: (1, 2, 3, 4, 0, 5, 6, 7, 8)
    - Acciones: 'ARRIBA', 'ABAJO', 'IZQUIERDA', 'DERECHA' (movimiento del hueco 0).
    """

    OBJETIVO_DEFAULT = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    # Movimientos ortogonales sobre matriz 3x3: (delta_fila, delta_columna)
    MOVIMIENTOS = {
        'ARRIBA': (-1, 0),
        'ABAJO': (1, 0),
        'IZQUIERDA': (0, -1),
        'DERECHA': (0, 1)
    }

    def __init__(self, estado_inicial: Tuple[int, ...] = None, estado_objetivo: Tuple[int, ...] = None, costos_acciones: Dict[str, float] = None):
        if estado_inicial is None:
            # Configuración limpia a 3 pasos de distancia de la meta (1 2 3 / 0 4 6 / 7 5 8)
            estado_inicial = (1, 2, 3, 0, 4, 6, 7, 5, 8)
        super().__init__(estado_inicial)
        self.estado_objetivo = estado_objetivo or self.OBJETIVO_DEFAULT
        self.costos_acciones = {
            'ARRIBA': 1.0,
            'ABAJO': 1.0,
            'IZQUIERDA': 1.0,
            'DERECHA': 1.0
        }
        if costos_acciones:
            self.costos_acciones.update(costos_acciones)

    def es_objetivo(self, estado: Tuple[int, ...]) -> bool:
        return estado == self.estado_objetivo

    def acciones(self, estado: Tuple[int, ...]) -> List[str]:
        idx_cero = estado.index(0)
        fila = idx_cero // 3
        col = idx_cero % 3
        validas = []

        for mov, (df, dc) in self.MOVIMIENTOS.items():
            nf, nc = fila + df, col + dc
            if 0 <= nf < 3 and 0 <= nc < 3:
                validas.append(mov)
        return validas

    def resultado(self, estado: Tuple[int, ...], accion: str) -> Tuple[int, ...]:
        idx_cero = estado.index(0)
        fila = idx_cero // 3
        col = idx_cero % 3
        df, dc = self.MOVIMIENTOS[accion]
        nf, nc = fila + df, col + dc
        nuevo_idx = nf * 3 + nc

        lista = list(estado)
        lista[idx_cero], lista[nuevo_idx] = lista[nuevo_idx], lista[idx_cero]
        return tuple(lista)

    def costo(self, estado: Any, accion: Any, estado_siguiente: Any) -> float:
        return float(self.costos_acciones.get(accion, 1.0))

    @staticmethod
    def formatear(estado: Tuple[int, ...]) -> str:
        s = ""
        for i in range(3):
            s += " ".join(str(estado[i * 3 + j]) if estado[i * 3 + j] != 0 else "_" for j in range(3)) + "\n"
        return s.strip()


# ==============================================================================
# 2. PROBLEMA: N-REINAS (N-QUEENS)
# ==============================================================================
class ProblemaNReinas(ProblemaBusqueda):
    """
    Representación de N-Reinas:
    - Estado: Tupla con las filas ocupadas por cada reina en columnas sucesivas (0 a k-1).
      Ej: (1, 3, 0) significa: Reina 0 en fila 1, Reina 1 en fila 3, Reina 2 en fila 0.
    - Acciones: Fila válida (0 a N-1) para colocar la siguiente reina en la columna k sin ataques.
    - Objetivo: Se han colocado exitosamente N reinas sin ataques mutuos.
    """

    def __init__(self, n: int = 4):
        self.n = n
        super().__init__(estado_inicial=())  # Tablero vacío al inicio

    def es_objetivo(self, estado: Tuple[int, ...]) -> bool:
        return len(estado) == self.n

    def acciones(self, estado: Tuple[int, ...]) -> List[int]:
        col_actual = len(estado)
        if col_actual >= self.n:
            return []

        filas_validas = []
        for fila_candidata in range(self.n):
            conflicto = False
            for col_anterior, fila_anterior in enumerate(estado):
                # Conflicto horizontal
                if fila_anterior == fila_candidata:
                    conflicto = True
                    break
                # Conflicto diagonal: |f1 - f2| == |c1 - c2|
                if abs(fila_anterior - fila_candidata) == abs(col_anterior - col_actual):
                    conflicto = True
                    break
            if not conflicto:
                filas_validas.append(fila_candidata)

        return filas_validas

    def resultado(self, estado: Tuple[int, ...], accion: int) -> Tuple[int, ...]:
        return estado + (accion,)

    def costo(self, estado: Any, accion: Any, estado_siguiente: Any) -> float:
        return 1.0

    @staticmethod
    def formatear(estado: Tuple[int, ...], n: int) -> str:
        header = "    " + "  ".join(f"C{c+1}" for c in range(n))
        separator = "   +" + "---+" * n
        lines = [header, separator]
        for f in range(n):
            fila_str = f"F{f+1} |"
            for c in range(n):
                if c < len(estado) and estado[c] == f:
                    fila_str += " Q |"
                else:
                    fila_str += " . |"
            lines.append(fila_str)
            lines.append(separator)
        return "\n".join(lines)


# ==============================================================================
# 3. PROBLEMA: MOCHILA 0/1 (KNAPSACK BASADO EN LISTAS)
# ==============================================================================
class ProblemaMochila(ProblemaBusqueda):
    """
    Representación computacional del Problema de la Mochila 0/1 con listas:
    - Estado: Tupla (indice_objeto, peso_acumulado, tupla_seleccion_binaria)
    - Acciones: 
        1 -> Incluir el objeto i en la mochila (si cabe)
        0 -> Omitir el objeto i
    - Objetivo: Se ha evaluado la decisión para todos los N objetos.
    - Para UCS (Minimización): El costo de paso penaliza el valor perdido respecto
      al valor máximo teórico posible (Costo = valor_maximo - valor_ganado).
    """

    def __init__(self, pesos: List[int] = None, valores: List[int] = None, capacidad: int = None):
        # Datos didácticos por defecto
        self.pesos = pesos or [2, 3, 4, 5, 9]
        self.valores = valores or [3, 4, 8, 8, 10]
        self.capacidad = capacidad or 10
        self.num_items = len(self.pesos)
        self.valor_total_posible = sum(self.valores)

        # Estado inicial: (item_idx, peso_acum, seleccion)
        super().__init__(estado_inicial=(0, 0, ()))

    def es_objetivo(self, estado: Tuple[int, int, Tuple[int, ...]]) -> bool:
        idx, _, _ = estado
        return idx == self.num_items

    def acciones(self, estado: Tuple[int, int, Tuple[int, ...]]) -> List[int]:
        idx, peso_acum, _ = estado
        if idx >= self.num_items:
            return []

        acciones_disp = [0]  # Siempre es válido no llevar el objeto
        peso_item = self.pesos[idx]

        if peso_acum + peso_item <= self.capacidad:
            acciones_disp.append(1)  # Se puede llevar

        return acciones_disp

    def resultado(self, estado: Tuple[int, int, Tuple[int, ...]], accion: int) -> Tuple[int, int, Tuple[int, ...]]:
        idx, peso_acum, seleccion = estado
        nuevo_peso = peso_acum + (self.pesos[idx] if accion == 1 else 0)
        return (idx + 1, nuevo_peso, seleccion + (accion,))

    def costo(self, estado: Tuple[int, int, Tuple[int, ...]], accion: int, estado_siguiente: Any) -> float:
        # En UCS minimizamos: no llevar un objeto cuesta su valor dejado sobre la mesa
        idx, _, _ = estado
        if accion == 1:
            return 1.0  # Costo base mínimo
        else:
            return 1.0 + float(self.valores[idx])  # Penalidad de costo por no tomar valor


# ==============================================================================
# 4. PROBLEMA: AGENTE VIAJERO (TSP - TRAVELLING SALESPERSON BASADO EN MATRIZ)
# ==============================================================================
class ProblemaAgenteViajero(ProblemaBusqueda):
    """
    Representación computacional del TSP con Matriz de Adyacencia:
    - Ruta Continental: Bogotá hasta La Patagonia (Ushuaia, Argentina/Chile)
    - Ciudades: ['Bogotá', 'Quito', 'Lima', 'Santiago', 'Buenos Aires', 'Ushuaia (Patagonia)']
    - Matriz de Distancias en Km de la Red Vial Sudamericana / Panamericana.
    - Estado: Tupla con la ruta de ciudades visitadas ('Bogotá', 'Quito', ...)
    - Acciones: Nombre de la siguiente ciudad no visitada, o volver a Bogotá al completar el circuito.
    - Objetivo: Circuito cerrado que contiene todas las ciudades y regresa a Bogotá minimizando kilometraje.
    """

    CIUDADES_DISPONIBLES = [
        "Bogotá",
        "Quito",
        "Lima",
        "La Paz",
        "Santiago",
        "Buenos Aires",
        "Bariloche (Patagonia Norte)",
        "Ushuaia (Patagonia Sur)"
    ]

    # Matriz/Red de distancias viales reales aproximadas (Km) en Sudamérica
    DISTANCIAS_MAP = {
        ("Bogotá", "Bogotá"): 0,
        ("Bogotá", "Quito"): 1050,
        ("Bogotá", "Lima"): 2950,
        ("Bogotá", "La Paz"): 3900,
        ("Bogotá", "Santiago"): 5800,
        ("Bogotá", "Buenos Aires"): 6100,
        ("Bogotá", "Bariloche (Patagonia Norte)"): 7500,
        ("Bogotá", "Ushuaia (Patagonia Sur)"): 9200,

        ("Quito", "Quito"): 0,
        ("Quito", "Lima"): 1900,
        ("Quito", "La Paz"): 2900,
        ("Quito", "Santiago"): 4800,
        ("Quito", "Buenos Aires"): 5200,
        ("Quito", "Bariloche (Patagonia Norte)"): 6600,
        ("Quito", "Ushuaia (Patagonia Sur)"): 8300,

        ("Lima", "Lima"): 0,
        ("Lima", "La Paz"): 1500,
        ("Lima", "Santiago"): 3300,
        ("Lima", "Buenos Aires"): 3850,
        ("Lima", "Bariloche (Patagonia Norte)"): 4900,
        ("Lima", "Ushuaia (Patagonia Sur)"): 6450,

        ("La Paz", "La Paz"): 0,
        ("La Paz", "Santiago"): 2300,
        ("La Paz", "Buenos Aires"): 2650,
        ("La Paz", "Bariloche (Patagonia Norte)"): 3600,
        ("La Paz", "Ushuaia (Patagonia Sur)"): 5150,

        ("Santiago", "Santiago"): 0,
        ("Santiago", "Buenos Aires"): 1400,
        ("Santiago", "Bariloche (Patagonia Norte)"): 1100,
        ("Santiago", "Ushuaia (Patagonia Sur)"): 3150,

        ("Buenos Aires", "Buenos Aires"): 0,
        ("Buenos Aires", "Bariloche (Patagonia Norte)"): 1580,
        ("Buenos Aires", "Ushuaia (Patagonia Sur)"): 3050,

        ("Bariloche (Patagonia Norte)", "Bariloche (Patagonia Norte)"): 0,
        ("Bariloche (Patagonia Norte)", "Ushuaia (Patagonia Sur)"): 2150,

        ("Ushuaia (Patagonia Sur)", "Ushuaia (Patagonia Sur)"): 0,
    }

    # Ruta estándar de 6 ciudades para benchmarking
    CIUDADES_DEFAULT = [
        "Bogotá",
        "Quito",
        "Lima",
        "Santiago",
        "Buenos Aires",
        "Ushuaia (Patagonia Sur)"
    ]

    def __init__(self, ciudades: List[str] = None, ciudad_origen: str = "Bogotá"):
        self.ciudades = list(ciudades) if ciudades else list(self.CIUDADES_DEFAULT)
        self.ciudad_origen = ciudad_origen
        if self.ciudad_origen not in self.ciudades:
            self.ciudades.insert(0, self.ciudad_origen)
        self.n_ciudades = len(self.ciudades)

        super().__init__(estado_inicial=(self.ciudad_origen,))

    def distancia_entre(self, c1: str, c2: str) -> float:
        if (c1, c2) in self.DISTANCIAS_MAP:
            return float(self.DISTANCIAS_MAP[(c1, c2)])
        if (c2, c1) in self.DISTANCIAS_MAP:
            return float(self.DISTANCIAS_MAP[(c2, c1)])
        # Estimación por defecto si no está explícito
        return 2000.0

    def es_objetivo(self, estado: Tuple[str, ...]) -> bool:
        # Ha visitado todas las N ciudades seleccionadas y retornó al origen (longitud N + 1)
        return len(estado) == self.n_ciudades + 1 and estado[-1] == self.ciudad_origen

    def acciones(self, estado: Tuple[str, ...]) -> List[str]:
        if len(estado) == self.n_ciudades:
            # Ya visitó todas las seleccionadas: retornar al origen
            return [self.ciudad_origen]

        if len(estado) > self.n_ciudades:
            return []

        # Ciudades aún no visitadas en el conjunto elegido
        visitadas = set(estado)
        return [c for c in self.ciudades if c not in visitadas]

    def resultado(self, estado: Tuple[str, ...], accion: str) -> Tuple[str, ...]:
        return estado + (accion,)

    def costo(self, estado: Tuple[str, ...], accion: str, estado_siguiente: Any) -> float:
        ciudad_actual = estado[-1]
        ciudad_destino = accion
        return self.distancia_entre(ciudad_actual, ciudad_destino)
