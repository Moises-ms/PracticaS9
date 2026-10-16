# Respuestas de reflexión

**¿Por qué deshacer usa una pila y atender una cola?**
Atender debe respetar el orden de llegada: el que lleva más tiempo esperando sale primero (FIFO → cola).
Deshacer debe revertir la acción *más reciente* antes que las anteriores (LIFO → pila). Por eso al atender
A y luego B, el primer deshacer devuelve B y el segundo A; al reinsertarlos al inicio, se restaura el orden original.

**Costo de `pop(0)` e `insert(0, x)`**
Ambos son O(n): la lista es un arreglo contiguo y hay que desplazar todos los elementos restantes. Con miles de
solicitudes se nota. `append()` y `pop()` al final son O(1) amortizado.

**`collections.deque`**
Lista doblemente enlazada por bloques: `append`, `appendleft`, `pop` y `popleft` son O(1). Conviene cuando la cola
crece mucho o se atiende con alta frecuencia. Desventajas: el acceso por índice en el medio y `remove` siguen
siendo O(n), así que cancelar una solicitud intermedia no mejora. En esta práctica es una mejora posterior:
`pop(0)` → `popleft()`, `insert(0, x)` → `appendleft(x)`.

**¿Y si hay solicitudes urgentes?**
Una cola FIFO solo ordena por llegada; no tiene noción de prioridad, así que una urgente esperaría detrás de
todas las normales. Opciones: (1) dos colas (urgentes y normales) y atender siempre primero la de urgentes;
(2) una cola de prioridad con `heapq`, usando tuplas `(prioridad, orden_de_llegada, solicitud)` para que, a igual
prioridad, siga FIFO. El deshacer también cambiaría: habría que reinsertar la solicitud en su lugar correcto
según prioridad y llegada, no simplemente al inicio.
