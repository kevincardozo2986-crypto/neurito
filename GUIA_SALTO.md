Neurito 2.0: mis respuestas a los experimentos

Todos los números salen de mis mediciones: 60 segundos de juego a 30 FPS (1800 actualizaciones), semilla 42 para los modelos y 19 para la pista. Salvo que diga otra cosa, usé 12 neuronas ocultas, tasa 0.8, ventana 7–13 y 400 épocas.

1. Juego sin entrenar

Probé el juego sin entrenar y la red no esquivó ni un obstáculo: en los 60 segundos tuvo 12 choques y 0 esquivados. Tiene sentido, porque con los pesos iniciales las decisiones no sirven. La precisión de prueba era de 44.93 %, ni siquiera llegaba a la mitad.

2. Entrenamiento de cien en cien épocas

Entrené de cien en cien hasta las 500 épocas. La pérdida fue bajando (0.2601 a las 100 y 0.1368 a las 500) y la precisión subió de 91.20 % a 94.13 %.

Lo curioso es que desde las 100 épocas ya esquivaba los 14 obstáculos sin chocar, así que en el juego no vi ninguna diferencia entre 100 y 500. Mi lectura es que la pista de 60 segundos era fácil y se pasaba con poco entrenamiento, pero eso no quiere decir que todas las redes den igual en cualquier situación.

3. Neuronas ocultas

Probé con 3, 12 y 24 neuronas.

Neuronas	Pérdida	Precisión de prueba	Esquivados	Choques
3	0.2167	92.80 %	14	0
12	0.1753	92.60 %	14	0
24	0.1161	95.27 %	14	0

La de 24 generaliza mejor, porque su precisión es la más alta sobre ejemplos que no usó para entrenar. Me sorprendió que la de 3 quedara un poquito por encima de la de 12 en precisión aunque tuviera más pérdida, pero son métricas distintas y no miden lo mismo.

En la pista las tres hicieron igual, o sea que más neuronas mejoró la clasificación pero no el juego.

4. Tasa de aprendizaje
Tasa	Pérdida	Precisión de prueba	Esquivados	Choques
0.01	0.5376	85.73 %	0	11
0.8	0.1753	92.60 %	14	0
1.2	0.1206	93.20 %	14	0

Con 0.01 el aprendizaje fue muy lento: la pérdida pasó de 0.6449 a las 100 épocas a 0.5376 a las 400, y la red no esquivó nada. Con 0.8 la pérdida bajó sin ninguna subida entre épocas. Con 1.2 terminó mejor, pero con oscilaciones: hubo 193 subidas de pérdida entre épocas seguidas de las 400.

Entonces una tasa más alta aprende más rápido, pero es menos estable. Tampoco es que las tasas altas siempre fallen, porque 1.2 sí pasó la pista.

5. Ventana de entrenamiento

Cambié la ventana en etiqueta() y en la generación de positivos al mismo tiempo.

Ventana	Positivos	Pérdida	Precisión de prueba	Esquivados	Choques
7–13	7.5–12.5	0.1753	92.60 %	14	0
4–10	4.5–9.5	0.1649	95.80 %	14	0
10–16	10.5–15.5	0.1155	95.40 %	13	1

La 4–10 enseña a saltar cuando el obstáculo está más cerca y la 10–16, a saltar antes. La original y la 4–10 fueron compatibles con la física en esta prueba, y la 10–16 no del todo.

Mi hipótesis es que al saltar tan temprano la mascota baja antes de terminar de pasar el obstáculo, pero no lo pude confirmar porque no registré la trayectoria. Además, las precisiones de ventanas distintas no se pueden comparar directo, porque cada una usa etiquetas diferentes.

Pregunta central

¿Por qué una red puede clasificar ejemplos con buena precisión y aun así chocar?

Porque la precisión solo mide qué tanto coincide la red con la regla de etiquetas, no si logra evitar colisiones. El resultado en el juego también depende de la altura y la duración del salto, la velocidad del obstáculo y el momento exacto de la decisión.

Además, mientras la mascota está en el aire la red puede decir «salta», pero el juego solo deja empezar otro salto cuando está en el suelo, y un ejemplo aislado no evalúa esa secuencia. Unos pocos errores cerca del momento crítico casi no se notan en la precisión, pero alcanzan para chocar.

Mi ejemplo es la ventana 10–16: llegó a 95.40 % de precisión y chocó una vez, mientras que la original llegó a 92.60 % y no chocó.

Alcance

Estos resultados son de una sola inicialización por configuración y una pista determinista, así que describen estas ejecuciones y nada más. Con otras semillas, pistas o duraciones podrían cambiar.