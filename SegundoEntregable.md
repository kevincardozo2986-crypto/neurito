Neurito 2.0: experimentos de salto

Quería ver cómo cambia la decisión de saltar según el entrenamiento, el número de neuronas ocultas, la tasa de aprendizaje y la ventana de etiquetas. La red aprende de forma supervisada con datos sintéticos. No aprende por recompensa al esquivar obstáculos.

Cómo hice las pruebas

Armé un programa auxiliar que usa RedSalto y la física de JuegoSalto sin abrir Pygame. Cada medición son 1800 actualizaciones, que equivalen a 60 segundos de juego a 30 FPS (en tiempo real el cálculo termina mucho antes). El orden de decisión, salto y actualización es el mismo de saltar.py, y se mantienen las colisiones y la pausa de 30 fotogramas después de chocar.

Usé 5000 ejemplos de entrenamiento y 1500 de prueba, con semilla 42 para los modelos y 19 para la pista. Para comparar tamaños y tasas reutilicé exactamente los mismos datos. Para cada ventana generé datos nuevos con sus etiquetas, pero con la misma semilla y tamaño. Cada medición arranca con una instancia nueva del juego y los contadores en cero, y el entrenamiento queda detenido durante la evaluación.

La configuración base es de 12 neuronas ocultas, tasa 0.8 y ventana de 7–13 fotogramas. Las comparaciones de tamaño, tasa y ventana usan 400 épocas. Elegí estos criterios para que los experimentos fueran comparables entre sí, porque la guía no fija una duración ni una cantidad final de épocas.

Las tablas muestran la última pérdida del historial, la misma que aparece en pantalla. Se calcula antes de actualizar los pesos de esa época, mientras que la precisión y el juego se evalúan con los pesos ya actualizados. También verifiqué la pérdida recalculada con esos pesos.

1. Juego sin entrenar
Épocas	Precisión de prueba	Esquivados en 60 s	Choques en 60 s
0	44.93 %	0	12

Sin entrenar, la red no esquivó ni un obstáculo. Como todavía no hay historial, calculé la pérdida inicial directamente: 0.7099. Con los pesos iniciales, las decisiones no sirven para pasar la pista.

2. Entrenamiento de cien en cien épocas
Épocas	Pérdida mostrada	Precisión de prueba	Esquivados en 60 s	Choques en 60 s
100	0.2601	91.20 %	14	0
200	0.2306	91.87 %	14	0
300	0.2066	92.33 %	14	0
400	0.1753	92.60 %	14	0
500	0.1368	94.13 %	14	0

La pérdida baja y la precisión sube a medida que entrena, como era de esperar. Lo curioso es que desde las 100 épocas ya esquiva los 14 obstáculos de la medición sin chocar, así que las mejoras de clasificación posteriores no se notan en los contadores. Esta pista de 60 segundos ya se supera con el entrenamiento inicial. Eso no significa que todas las redes den igual en cualquier situación.

Los valores de 400 épocas coinciden, al redondear, con la grabación que compartí: pérdida 0.1753 y precisión 92.6 %. Los contadores de esa grabación eran acumulados; los de esta tabla empiezan en cero.

3. Número de neuronas ocultas

Dejé fijos tasa 0.8, ventana 7–13 y 400 épocas.

Neuronas ocultas	Pérdida mostrada	Precisión de prueba	Esquivados en 60 s	Choques en 60 s
3	0.2167	92.80 %	14	0
12	0.1753	92.60 %	14	0
24	0.1161	95.27 %	14	0

Con 24 neuronas la pérdida fue menor y la precisión más alta sobre ejemplos que no se usaron para entrenar. Aun así, las tres configuraciones dieron lo mismo en la pista. Me llamó la atención que la red de 3 neuronas tuvo una precisión un poco mayor que la de 12, aunque su pérdida fue peor. Tiene sentido: son métricas distintas y no miden lo mismo. En resumen, subir a 24 neuronas mejoró la clasificación, pero no hizo que esquivara más obstáculos.

4. Tasa de aprendizaje

Dejé fijos 12 neuronas, ventana 7–13 y 400 épocas.

Tasa	Pérdida mostrada	Precisión de prueba	Esquivados en 60 s	Choques en 60 s
0.01	0.5376	85.73 %	0	11
0.8	0.1753	92.60 %	14	0
1.2	0.1206	93.20 %	14	0

Con 0.01 el aprendizaje es muy lento: la pérdida pasó de 0.6449 a las 100 épocas a 0.5376 a las 400, y la red seguía sin esquivar nada. Con 0.8 la pérdida bajó sin subidas entre épocas en el tramo medido. Con 1.2 terminó con menos pérdida y más precisión que con 0.8, pero oscilando: hubo 193 aumentos de pérdida entre épocas consecutivas de las 400. O sea, una tasa más alta acelera el aprendizaje, pero lo vuelve menos estable. Tampoco es que las tasas altas siempre fallen, porque aquí 1.2 sí pasó la pista.

5. Ventana de entrenamiento

Para este experimento usé una variante, RedVentana, dentro del programa de pruebas. Cambia al mismo tiempo etiqueta() y la generación de positivos, sin tocar los valores originales del juego. Conservé 12 neuronas, tasa 0.8 y 400 épocas.

Ventana de etiquetas	Intervalo de positivos	Pérdida mostrada	Precisión de prueba	Esquivados en 60 s	Choques en 60 s
7–13 fotogramas	7.5–12.5	0.1753	92.60 %	14	0
4–10 fotogramas	4.5–9.5	0.1649	95.80 %	14	0
10–16 fotogramas	10.5–15.5	0.1155	95.40 %	13	1

La ventana 4–10 le enseña a saltar cuando el obstáculo ya está más cerca, y la 10–16 le enseña a saltar antes. La original y la 4–10 encajaron bien con la física en esta evaluación y no chocaron. La 10–16 tuvo muy buena precisión, pero chocó una vez. Mi hipótesis es que al adelantar el salto la mascota baja antes de terminar de pasar el obstáculo. Para confirmarlo tendría que registrar la trayectoria del choque, y eso no lo hice.

Ojo con comparar precisiones entre ventanas: cada una se calcula sobre etiquetas distintas, así que no dicen por sí solas cuál ventana es mejor para el juego.

Pregunta central

¿Por qué una red puede clasificar bien y aun así chocar?

Porque la precisión mide cuánto coincide la red con una regla de etiquetas, no si logra evitar colisiones. La regla dice cuándo conviene saltar según el tiempo estimado hasta el obstáculo, pero el resultado real también depende de la altura y duración del salto, la velocidad del obstáculo y el momento exacto de la decisión. Los errores cerca del instante crítico pueden ser pocos en el conjunto de prueba y aun así bastar para chocar.

Hay otro detalle: mientras la mascota está en el aire, la red puede “decir” que hay que saltar, pero el juego solo deja iniciar otro salto cuando está en el suelo. Clasificar un ejemplo aislado no evalúa toda esa secuencia física. Los resultados lo muestran directo: la ventana 10–16 llegó a 95.40 % de precisión y tuvo un choque, mientras que la original llegó a 92.60 % y no chocó. Mayor precisión no garantiza mejor desempeño en el juego.

Alcance de los resultados

Todo son mediciones hechas con el código del proyecto, en simulación sin interfaz gráfica. Usé una sola inicialización por configuración y una pista determinista por medición. Además, las configuraciones que chocan reinician la pista y pueden terminar enfrentando secuencias de obstáculos distintas a las de las que siguen esquivando. Por eso estos resultados describen estas ejecuciones y nada más: con otras semillas, pistas o duraciones podrían cambiar. Para sacar conclusiones más generales habría que repetir las pruebas con varias semillas y reportar cuánto varían.