# Tercer entregable: Neurito aprende a recorrer laberintos

## 1. Sin entrenamiento

| Épocas | Pérdida inicial | Precisión | Éxitos red pura | Éxitos asistidos |
| --- | --- | --- | --- | --- |
| 0 | 1.3950 | 27.65 % | 22/716 (3.07 %) | 629/716 (87.85 %) |

Se atasca porque los pesos iniciales no representan ninguna ruta útil. Como toma el argmax y no tiene memoria, repite la misma acción: insiste contra una pared o va y vuelve entre dos casillas. La asistencia ya resuelve muchos retos, así que sus reglas aportan buena parte del comportamiento.

## 2. Entrenar 100, 200 y 400 épocas

| Épocas | Pérdida | Precisión | Éxitos puros | Éxitos asistidos | Intentos medios, pura¹ |
| --- | --- | --- | --- | --- | --- |
| 100 | 0.1352 | 84.92 % | 367/716 (51.26 %) | 716/716 (100.00 %) | 24.78 |
| 200 | 0.0376 | 90.08 % | 582/716 (81.28 %) | 716/716 (100.00 %) | 13.30 |
| 400 | 0.0107 | 91.48 % | 592/716 (82.68 %) | 716/716 (100.00 %) | 12.78 |

La pérdida baja, la precisión sube y la red pura resuelve más retos. La asistencia ya llega al 100 % desde las 100 épocas, así que no deja ver las mejoras posteriores.

## 3. Red pura frente a navegación asistida

| Modo, 400 épocas | Éxitos | Intentos medios de los éxitos | Intentos contra paredes |
| --- | --- | --- | --- |
| Red pura | 592/716 (82.68 %) | 6.04 | 135 |
| Asistido | 716/716 (100.00 %) | 6.62 | 0 |

La red aprende las probabilidades de las acciones. Lo de evitar paredes y visitas viene de las reglas, no de los pesos. La asistencia no consulta BFS, pero tampoco evalúa a la red sola.

## 4. Neuronas ocultas

| Ocultas | Pérdida | Precisión | Éxitos puros | Éxitos asistidos |
| --- | --- | --- | --- | --- |
| 16 | 0.0342 | 87.15 % | 532/716 (74.30 %) | 716/716 (100.00 %) |
| 32 | 0.0161 | 89.25 % | 561/716 (78.35 %) | 716/716 (100.00 %) |
| 96 | 0.0107 | 91.48 % | 592/716 (82.68 %) | 716/716 (100.00 %) |
| 128 | 0.0103 | 90.78 % | 611/716 (85.34 %) | 716/716 (100.00 %) |

Con 16 y 32 hubo menos precisión y menos éxitos que con 96. Con 128 hubo más éxitos aunque la precisión fue un poco menor: importa dónde están los errores, porque uno que arranca un ciclo arruina todo el recorrido.

## 5. Tasa de aprendizaje

| Tasa | Pérdida | Precisión | Éxitos puros | Éxitos asistidos | Aumentos de pérdida² |
| --- | --- | --- | --- | --- | --- |
| 0.01 | 0.6818 | 73.88 % | 146/716 (20.39 %) | 711/716 (99.30 %) | 0 |
| 0.45 | 0.0107 | 91.48 % | 592/716 (82.68 %) | 716/716 (100.00 %) | 85 |
| 1.2 | 0.0022 | 93.85 % | 617/716 (86.17 %) | 716/716 (100.00 %) | 62 |



Con 0.01 la pérdida bajó sin oscilar, pero aprendió muy lento. Con 0.45 y 1.2 hubo oscilaciones (normales con mini-lotes) y la pérdida terminó mucho menor. Aquí 1.2 fue la mejor y no vi divergencia.

## 6. Cambio de mapa

| Mapa | Retos | Éxitos puros | Éxitos asistidos | Intentos medios asistidos |
| --- | --- | --- | --- | --- |
| 1 | 210 | 180 (85.71 %) | 210 (100.00 %) | 6.85 |
| 2 | 251 | 197 (78.49 %) | 251 (100.00 %) | 6.12 |
| 3 | 255 | 215 (84.31 %) | 255 (100.00 %) | 6.93 |

La red pura rindió distinto según el mapa y la asistencia resolvió todos. Los tres mapas están en el entrenamiento y la red no recibe sus paredes, así que no puedo concluir que recorra un laberinto desconocido.

## 7. DFS, BFS y A*

Usé programas auxiliares para comparar los tres algoritmos y entrenar una red con las etiquetas de cada uno. Después retiré esos archivos; los resultados quedan en este informe y el juego conserva BFS. Para repetir la comparación habría que reconstruir los programas auxiliares.

**Búsqueda directa, sin red** (los mismos 716 retos):

| Algoritmo | Llegadas a meta | Pasos medios de la ruta | Nodos expandidos medios |
| --- | --- | --- | --- |
| DFS | 716/716 | 11.08 | 18.51 |
| BFS | 716/716 | 6.06 | 18.49 |
| A* | 716/716 | 6.06 | 10.17 |

BFS y A* dan la ruta mínima y A* expande menos nodos. DFS llega, pero con rutas más largas. Son conteos de trabajo, no tiempos.

**Imitar a cada experto con la red:**

| Experto | Pérdida | Precisión con su experto | Coincidencia con BFS | Éxitos puros | Éxitos asistidos |
| --- | --- | --- | --- | --- | --- |
| DFS | 0.0100 | 94.83 % | 51.82 % | 82/716 (11.45 %) | 421/716 (58.80 %) |
| BFS | 0.0107 | 91.48 % | 91.48 % | 592/716 (82.68 %) | 716/716 (100.00 %) |
| A* | 0.0107 | 92.60 % | 90.92 % | 619/716 (86.45 %) | 716/716 (100.00 %) |

La red que imita a DFS acierta mucho sus etiquetas pero navega mal. Una ruta DFS depende de la memoria de lo explorado, y la red solo ve mapa, posición y meta, así que copiar acciones sueltas no es ejecutar el procedimiento. BFS y A* dieron resultados parecidos; A* tuvo más éxitos puros, pero con una sola semilla no puedo decir que siempre sea mejor.

## Conclusión

Entrenar mejoró la navegación, pero la precisión de una acción no equivale al éxito de un recorrido: los errores se acumulan, generan ciclos o chocan contra paredes. La asistencia aporta reglas que hay que separar de lo aprendido. Con DFS se ve bien que imitar con precisión a un experto local no reproduce su procedimiento completo.

Usé una sola inicialización por configuración y miré los mismos datos de prueba varias veces, así que los resultados describen estas ejecuciones y no prueban generalización a mapas desconocidos.

## Pruebas y ejecución

Durante los experimentos verifiqué las rutas de los tres algoritmos y la longitud óptima de BFS y A*. Las cinco pruebas originales conservadas revisan conectividad y BFS, separación de datos y aprendizaje, probabilidades, asistencia y éxito.

```powershell
uv run python -m unittest -v test_laberinto.py
uv run laberinto.py
```
