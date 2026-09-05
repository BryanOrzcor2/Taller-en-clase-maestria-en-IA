# 🧠 Taller 2: Algoritmos de Búsqueda No Informada & Evaluación Empírica
### Maestría en Inteligencia Artificial (MIA 2026-01) &bull; Universidad Sergio Arboleda
**Módulo 1:** Introducción a la Inteligencia Artificial  
**Docente:** Prof. Joaquín F. Sánchez Cifuentes  
**Estudiante:** Bryan Orozco  
**Repositorio GitHub:** [https://github.com/BryanOrzcor2/Taller-en-clase-maestria-en-IA](https://github.com/BryanOrzcor2/Taller-en-clase-maestria-en-IA)  

---

## 📌 Descripción General

Este proyecto implementa y evalúa formal y empíricamente los **4 algoritmos fundamentales de búsqueda no informada en inteligencia artificial**:

1. **BFS (Breadth-First Search):** Búsqueda en Anchura basada en cola FIFO (`collections.deque`).
2. **DFS (Depth-First Search):** Búsqueda en Profundidad basada en pila LIFO con poda en ramas de exploración.
3. **IDDFS (Iterative Deepening DFS):** Búsqueda en Profundidad Iterativa con cotas progresivas $L = 0, 1, 2, \dots$ combinando la optimalidad de BFS con la eficiencia de memoria de DFS.
4. **UCS (Uniform Cost Search):** Búsqueda de Costo Uniforme (Dijkstra) con cola de prioridad (`heapq`) y verificación de objetivo diferida al momento de extraer el nodo.

Para contrastar su comportamiento bajo diferentes estructuras de grafos y espacios de estados, se formularon computacionalmente **4 problemas clásicos**:
* 🧩 **Puzzle 3×3 (8-Puzzle):** Espacio cíclico con grafos de transposición ortogonal.
* 👑 **N-Reinas ($N=4$ hasta $N=12$):** Árbol de profundidad acotada con restricciones de no-ataque en filas y diagonales.
* 🎒 **Mochila 0/1 (Knapsack):** Árbol binario de inclusión/exclusión de objetos con función de costo por penalización para maximización de valor bajo capacidad $W$.
* 🗺️ **Agente Viajero (TSP Continental Bogotá ➔ La Patagonia):** Grafo conexo con matriz de distancias viales reales sudamericanas y selector interactivo de rutas.

Cada algoritmo mide de forma estricta:
* **Tiempo de CPU:** Milisegundos con resolución de nanosegundos mediante `time.perf_counter()`.
* **Consumo de Memoria RAM Pico:** Kilobytes (KB) mediante instrumentación de bajo nivel con `tracemalloc`.
* **Esfuerzo de Búsqueda:** Conteo de nodos expandidos y generados.
* **Calidad de la Solución:** Cantidad de pasos y costo acumulado $g(n)$.

---

## 📁 Estructura del Proyecto

```text
Taller-en-clase-maestria-en-IA/
├── README.md                      # Documentación maestra técnica y académica
├── algoritmos.py                  # Implementación genérica de BFS, DFS, IDDFS y UCS
├── problemas.py                   # Modelado formal de los 4 problemas de búsqueda
├── benchmark.py                   # Suite de pruebas automatizadas (4x4) y exportador JSON
├── DFS.py                         # Interfaz de consola interactiva CLI con menú
├── benchmark_resultados.json      # Resultados experimentales exportados para el visualizador
└── web/                           # Simulador visual interactivo (HTML5/CSS3/Vanilla JS)
    ├── index.html                 # Dashboard de control y visualizador de estados
    ├── style.css                  # Diseño glassmorphism oscuro responsivo
    └── app.js                     # Motor dinámico de animación, N-Reinas y TSP
```

---

## 🔬 Fundamentos Teóricos de los Algoritmos

| Algoritmo | Estructura de Datos | Complejidad Temporal | Complejidad Espacial | ¿Completo? | ¿Óptimo? |
|:---|:---:|:---:|:---:|:---:|:---:|
| **BFS** | Cola FIFO | $O(b^d)$ | $O(b^d)$ (Crítico) | **Sí** (si $b < \infty$) | **Sí** (si costos de paso son uniformes) |
| **DFS** | Pila LIFO | $O(b^m)$ | $O(b \cdot m)$ (Excelente) | **No** (en espacios infinitos o cíclicos) | **No** (toma la primera rama que alcance) |
| **IDDFS** | Pila LIFO incremental | $O(b^d)$ | $O(b \cdot d)$ (Excelente) | **Sí** (si $b < \infty$) | **Sí** (si costos de paso son uniformes) |
| **UCS** | Cola de Prioridad (`heapq`) | $O(b^{1 + \lfloor C^*/\epsilon \rfloor})$ | $O(b^{1 + \lfloor C^*/\epsilon \rfloor})$ | **Sí** (si costos $\ge \epsilon > 0$) | **Sí** (Garantizado para cualquier costo positivo) |

*Donde $b$ = factor de ramificación, $d$ = profundidad de la solución óptima, $m$ = profundidad máxima del árbol, $C^*$ = costo óptimo, $\epsilon$ = costo mínimo de paso.*

### 💡 Demostración de IDDFS: ¿Por qué no es costoso repetir niveles?
En IDDFS, la cantidad total de nodos visitados hasta profundidad $d$ es:
$$N_{\text{IDDFS}} = (d)b^1 + (d-1)b^2 + (d-2)b^3 + \dots + 1 \cdot b^d$$

Para un factor típico de ramificación $b = 10$ y profundidad $d = 5$:
* $N_{\text{BFS}} = 10 + 100 + 1,000 + 10,000 + 100,000 = \mathbf{111,110}$ nodos.
* $N_{\text{IDDFS}} = 5(10) + 4(100) + 3(1,000) + 2(10,000) + 1(100,000) = \mathbf{123,450}$ nodos.
* **Sobrecarga:** $\frac{123,450 - 111,110}{111,110} \approx \mathbf{11.1\%}$.
IDDFS solo repite un **11% de trabajo adicional**, pero **reduce la memoria de $O(b^d)$ a $O(b \cdot d)$** (de gigabytes a kilobytes).

### ⚠️ Regla de Oro de UCS (Dijkstra)
La prueba de objetivo en UCS **debe realizarse cuando el nodo se extrae de la cola de prioridad**, NO cuando se genera:
* Si se probara al generar, se descartaría un camino que alcanzó el objetivo con alto costo, impidiendo que otro camino más largo en saltos pero con menor costo acumulado $g(n)$ pueda alcanzar la meta de forma óptima.

---

## 🎯 Modelado de los 4 Problemas

### 1. 🧩 Puzzle 3×3 (8-Puzzle)
* **Estado:** Tupla inmutable de 9 enteros `(p0, p1, ..., p8)` donde `0` representa el espacio vacío.
* **Estado Objetivo:** `(1, 2, 3, 4, 5, 6, 7, 8, 0)`.
* **Acciones:** `ARRIBA`, `ABAJO`, `IZQUIERDA`, `DERECHA` (desplazamientos válidos de `0` dentro del tablero 3×3).
* **Costo:** $c = 1.0$ por movimiento.

### 2. 👑 N-Reinas ($N=4$ hasta $N=12$)
* **Estado:** Tupla `(f_0, f_1, ..., f_{k-1})` donde el índice representa la columna y el valor la fila asignada a la reina.
* **Acciones:** Asignar la reina en la columna $k$ en una fila $r \in [0, N-1]$ tal que no ataque a las reinas previas:
  $$r \neq f_c \quad \text{y} \quad |r - f_c| \neq |k - c| \quad \forall c < k$$
* **Estado Objetivo:** Longitud de la tupla igual a $N$ (todas las reinas ubicadas sin conflictos).

### 3. 🎒 Mochila 0/1 (Knapsack con Listas)
* **Estado:** Tupla `(indice_objeto, peso_acumulado, tupla_seleccion_binaria)`.
* **Acciones:**
  * `0`: Omitir el objeto actual.
  * `1`: Incluir el objeto actual (si `peso_acumulado + peso_i <= W`).
* **Función de Costo UCS:** Para resolver maximización con minimización, se aplica costo por penalización:
  $$c(s, a=1, s') = 1.0, \quad c(s, a=0, s') = 1.0 + \text{valor}[i]$$

### 4. 🗺️ Agente Viajero (TSP Continental: Bogotá ➔ La Patagonia)
* **Red Vial Real Sudamericana:** Distancias terrestres por carretera (Km): Bogotá, Quito, Lima, La Paz, Santiago, Buenos Aires, Bariloche (Patagonia Norte) y Ushuaia (Patagonia Sur / Fin del Mundo).
* **Estado:** Tupla con las ciudades visitadas `('Bogotá', 'Quito', ...)`.
* **Acciones:** Ciudad destino aún no visitada, o retornar a Bogotá al completar el circuito.
* **Estado Objetivo:** Longitud $N+1$ con inicio y final en `Bogotá`.

---

## 📊 Resultados Experimentales y Tablas Comparativas

Resultados directos generados con `benchmark.py` bajo entorno Python 3.10:

### 1. 🧩 Puzzle 3×3
| Algoritmo | Éxito | Pasos | Costo $g(n)$ | Nodos Exp. | Tiempo (ms) | Memoria RAM (KB) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **BFS** | Sí | **3** | **3.0** | 8 | 0.139 ms | 7.55 KB |
| **DFS** | Sí | 833 | 833.0 | 852 | 12.610 ms | **4493.48 KB** (Explosión) |
| **IDDFS** | Sí | **3** | **3.0** | 30 | 0.131 ms | **4.28 KB** (Mínima) |
| **UCS** | Sí | **3** | **3.0** | 16 | 0.158 ms | 4.80 KB |

> **Análisis:** DFS cayó en un ciclo largo de 833 pasos consumiendo casi **4.5 MB** de RAM. **IDDFS** halló la solución óptima en 3 pasos con tan solo **4.28 KB**, superando a BFS en consumo de memoria.

---

### 2. 👑 N-Reinas ($N=4$)
| Algoritmo | Éxito | Pasos | Costo $g(n)$ | Nodos Exp. | Tiempo (ms) | Memoria RAM (KB) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **BFS** | Sí | 4 | 4.0 | 13 | 0.083 ms | 3.04 KB |
| **DFS** | Sí | 4 | 4.0 | 8 | **0.049 ms** | **1.12 KB** |
| **IDDFS** | Sí | 4 | 4.0 | 41 | 0.153 ms | 3.56 KB |
| **UCS** | Sí | 4 | 4.0 | 15 | 0.083 ms | 1.62 KB |

> **Análisis:** En árboles finitos sin ramas infinitas donde todas las soluciones están a la misma profundidad $N$, **DFS** es el más rápido (0.049 ms) y el de menor huella en RAM (1.12 KB).

---

### 3. 🎒 Mochila 0/1 (Listas de Objetos)
| Algoritmo | Éxito | Pasos | Costo Penalidad | Nodos Exp. | Tiempo (ms) | Memoria RAM (KB) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **BFS** | Sí | 4 | 27.0 (Subóptimo) | 8 | 0.058 ms | 2.50 KB |
| **DFS** | Sí | 4 | 27.0 (Subóptimo) | 4 | 0.023 ms | 0.70 KB |
| **IDDFS** | Sí | 4 | 27.0 (Subóptimo) | 30 | 0.071 ms | 3.69 KB |
| **UCS** | Sí | 4 | **15.0 (Óptimo)** | 13 | 0.051 ms | 2.95 KB |

> **Análisis:** Solo **UCS** optimiza el valor total de los objetos. Los algoritmos no ponderados (BFS/DFS/IDDFS) se detienen en la primera combinación válida de profundidad 4, ignorando el valor económico.

---

### 4. 🗺️ Agente Viajero (TSP: Bogotá ➔ La Patagonia)
| Algoritmo | Éxito | Pasos | Distancia Total | Nodos Exp. | Tiempo (ms) | Memoria RAM (KB) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **BFS** | Sí | 6 | 19,900 km | 207 | 1.235 ms | 80.11 KB |
| **DFS** | Sí | 6 | 19,900 km | 6 | **0.063 ms** | **2.35 KB** |
| **IDDFS** | Sí | 6 | 19,900 km | 658 | 2.057 ms | 5.25 KB |
| **UCS** | Sí | 6 | **18,550 km (Óptimo)** | 175 | 1.036 ms | 40.25 KB |

> **Análisis:** **UCS (Dijkstra)** encontró la ruta óptima bajando por los Andes del Pacífico y retornando por el Atlántico argentino (`Bogotá ➔ Quito ➔ Lima ➔ Santiago ➔ Ushuaia ➔ Buenos Aires ➔ Bogotá`), **ahorrando 1,350 km** frente a BFS y DFS.

---

## 🖥️ Simulador Web Interactivo (`web/`)

El visualizador web construido con estética moderna de glassmorphism incluye:
1. **Selector Dinámico de N-Reinas ($N=4$ a $N=12$):** Permite cambiar el tamaño del tablero en caliente, calcular la solución y animar las reinas con coronas doradas (`👑`) sin bloqueos.
2. **Selector de Ciudades para TSP (Bogotá ➔ La Patagonia):**
   * Presets rápidos: *Ruta Panamericana Clásica (6)*, *Ruta Andina Pacífico (5)*, *Ruta Directa Rápida (4)* y *Gran Travesía (8)*.
   * Chips interactivos para incluir/excluir ciudades individualmente.
   * Visualización de tramos con distancias reales en km y cálculo dinámico de ahorro de combustible/kilometraje.
3. **Control Paso a Paso:** Botones `Anterior` y `Siguiente` para seguir la frontera de exploración nodo a nodo.
4. **Modo "Ejecutar y Comparar los 4":** Ejecución secuencial animada de BFS, DFS, IDDFS y UCS con actualización de la tabla comparativa.

---

## 🚀 Guía de Uso e Instalación

### Requisitos
* Python 3.10 o superior.
* Sin dependencias de terceros obligatorias (utiliza librerías de la biblioteca estándar de Python: `heapq`, `collections`, `tracemalloc`, `time`, `json`).
* Cualquier navegador web moderno (Edge, Chrome, Firefox) para el dashboard visual.

### 1. Ejecutar el menú interactivo por consola
```powershell
cd "c:\Users\Bryan\Documents\Sergio Arboleda\Modulo_1\Introducion a Inteleginaci aritifical\Taller 2\Taller-en-clase-maestria-en-IA"
python DFS.py
```
*Opciones disponibles:*
* `1`: Demostración interactiva de Puzzle 3×3 con BFS, DFS, IDDFS y UCS.
* `2`: Demostración de N-Reinas ($N$ configurable por el usuario).
* `3`: Suite completa de benchmarking (4 problemas $\times$ 4 algoritmos).
* `4`: Mochila 0/1 con UCS.
* `5`: Selector de rutas de Agente Viajero (Bogotá ➔ La Patagonia).
* `6`: Salir.

### 2. Ejecutar únicamente el benchmark automatizado
```powershell
python benchmark.py
```
*Genera las tablas comparativas en terminal y actualiza `benchmark_resultados.json`.*

### 3. Abrir el Simulador Web
Basta con abrir el archivo en el navegador:
```powershell
Start-Process "web/index.html"
```
O hacer doble clic en `web/index.html`.

---

## 📚 Conclusiones Académicas

1. **Trade-off Tiempo vs Memoria:** En problemas con ramificación profunda y grafos cíclicos (como 8-Puzzle), BFS y DFS fallan en extremos opuestos: BFS satura la memoria y DFS satura el tiempo. **IDDFS demostró ser la técnica superior** al garantizar optimalidad con memoria lineal $O(b \cdot d)$.
2. **Importancia del Costo de Paso:** En problemas con aristas de costo heterogéneo (TSP y Mochila), BFS y DFS son ciegos al costo y entregan soluciones subóptimas. **UCS es indispensable** cuando se busca minimizar distancia, tiempo o maximizar valor.
3. **Poda Temprana y Heurísticas:** El crecimiento exponencial $(N-1)!$ en TSP y $b^d$ en Puzzle evidencia la necesidad de algoritmos de búsqueda informada ($A^*$, Greedy Best-First) para problemas a escala industrial.
