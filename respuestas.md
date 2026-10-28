Experimentos y respuestas de Neurito

Cómo hice los experimentos

todos los experimentos se ejecutan en la consola con uv run .\main.py, antes de abrir la ventana de Pygame. Dejé los 3000 ejemplos de entrenamiento y la semilla 42 como estaban. Para comparar todo usé el mismo conjunto de 1000 ejemplos de prueba, generado con np.random.RandomState(123). Así los resultados son comparables aunque cambie el número de neuronas. Verifiqué la parte de consola sin abrir la ventana; los valores siguientes son los que imprime el programa. Cada experimento entrena una red independiente y la mascota conserva su modelo original de tres acciones.

1. Cambiar una necesidad y dejar las otras fijas

Con 6 neuronas, 1200 épocas y tasa 0.1, fui subiendo una variable de 0 a 1 en pasos de 0.001 mientras las otras dos se quedaban quietas. Con energía 0.6 y aburrimiento 0.2, la predicción pasó de dormir a comer al llegar a hambre 0.400. Con hambre 0.4 y aburrimiento 0.2, pasó de dormir a comer al llegar a energía 0.600. Con hambre 0.4 y energía 0.7, pasó de comer a jugar al llegar a aburrimiento 0.405. Son los primeros valores del recorrido donde se observó cada cambio. Ese 0.405 es un poco más que la frontera teórica de 0.4, y eso me dice que la red no copia la regla a la perfección, solo se acerca mucho.

2. Prioridades casi iguales

Con la entrada [0.500, 0.500, 0.500], las probabilidades fueron 35.21 % para comer, 33.45 % para dormir y 31.34 % para jugar. No fueron exactamente iguales porque la red aprendió una aproximación. Al subir el hambre a 0.501, comer subió a 35.65 %; al bajar la energía a 0.499, dormir subió a 33.87 %; al subir el aburrimiento a 0.501, jugar subió a 31.76 %. En cada caso cambié solo esa entrada. Bajar la energía aumenta la prioridad de dormir porque se usa 1 - energy. En las cuatro pruebas siguió ganando comer. Softmax cambia las probabilidades suavemente, pero la decisión con argmax solo cambia cuando otra salida pasa a la más alta.

3. Número de neuronas ocultas

Probé con 3, 6, 10 y 20 neuronas, manteniendo 1200 épocas y tasa 0.1. Con 3, las pérdidas de entrenamiento y prueba fueron 0.1618 y 0.1759, con precisión de 96.3 %. Con 6 fueron 0.1224 y 0.1380, con 99.4 %. Con 10 fueron 0.1261 y 0.1408, con 99.1 %. Con 20 fueron 0.1220 y 0.1378, con 99.0 %. La red de 6 tuvo la mejor precisión en esta ejecución; la de 20 tuvo una pérdida ligeramente menor, pero no mayor precisión. La regla es sencilla y aumentar el tamaño no dio una mejora clara. Aun así fue una sola corrida por tamaño, con inicializaciones distintas, así que no puedo asegurar que 6 siempre sea la mejor. Para eso habría que repetirlo con varias semillas.

4. Épocas y tasa de aprendizaje

Con 6 neuronas y tasa 0.1, la precisión pasó de 91.2 % con 200 épocas a 99.4 % con 1200 y a 99.7 % con 3000. Las pérdidas finales de entrenamiento fueron 0.4961, 0.1224 y 0.0710; las de prueba fueron 0.5116, 0.1380 y 0.0842. Más épocas ayudaron, aunque la mejora de precisión fue cada vez menor; no se observó un estancamiento total. Con 1200 épocas y tasa 0.01 aprendió lentamente: tuvo pérdida de entrenamiento 0.7372, de prueba 0.7515 y precisión 80.1 %. Con tasa 1.0 la pérdida de entrenamiento fue la más baja (0.0447), y la de prueba fue 0.0593, pero la precisión quedó en 98.4 %. Hubo oscilaciones: la pérdida subió de 0.0888 en la época 600 a 0.0970 en la 800. Con tasa 10.0 el entrenamiento fue inestable: terminó con pérdidas de entrenamiento y prueba de 3.0699 y 3.0821, y precisión de 33.3 %, cercana a la referencia de azar entre tres clases equilibradas. La consola muestra la evolución de la pérdida para comparar estos comportamientos.

5. Una cuarta acción

El quinto experimento ya entrena una red independiente con “neutral” como cuarta acción. Usa las mismas tres entradas y asigna la etiqueta 3 cuando hambre < 0.4, energía > 0.6 y aburrimiento < 0.4; en los demás casos conserva las etiquetas 0 para comer, 1 para dormir y 2 para jugar. La salida pasa a tener W2 de forma (n, 4) y b2 de forma (1, 4). Con 6 neuronas, 1200 épocas y tasa 0.1, obtuvo pérdida de entrenamiento 0.1422, pérdida de prueba 0.1628 y precisión global 98.0 %. Sin embargo, acertó el 86.59 % de los 82 ejemplos de prueba realmente neutrales, frente a 100 % para comer, 98.68 % para dormir y 98.38 % para jugar. Para [0.2, 0.9, 0.2], asignó 95.64 % a neutral. Esa región ocupa el 6.4 % del espacio de entradas bajo muestreo uniforme, aunque en esta prueba concreta hubo 82 de 1000 ejemplos, así que conviene revisar los resultados por clase y agregar datos cerca de sus límites. La ventana sigue usando el modelo original y su regla externa para mostrar neutral; la cuarta acción aprendida se prueba en consola.

Respuestas

¿En qué se diferencian los pesos de los sesgos? Los pesos multiplican las entradas y definen cuánto influye cada una. Los sesgos se suman al resultado y sirven para mover el umbral de la neurona, incluso si las entradas son cero. En z1 = X @ W1 + b1, W1 son los pesos y b1 los sesgos.

¿Por qué el cansancio es 1 - energy? Porque tener mucha energía es lo contrario de tener sueño. Si la energía es 1, el cansancio es 0, y si la energía es 0, el cansancio es 1. Así las tres prioridades van igual: mientras más alto el valor, más urgente la necesidad. Esto solo se usa para generar las etiquetas, la entrada de la red sigue siendo la energía normal.

¿Qué hacen ReLU y Softmax? ReLU está en la capa oculta y hace max(0, valor): lo negativo lo vuelve cero y lo positivo lo deja igual. Eso le da a la red la parte no lineal que necesita para aprender cosas más complejas. Softmax está en la salida y convierte los tres valores en probabilidades que suman 1, y con eso se calcula la pérdida y se elige la acción.

¿Por qué una precisión alta puede engañar? Porque solo mide qué tanto coincide la red con una regla inventada que ya conocemos, no si entiende algo real. Además, un 99 % puede esconder errores cerca de los empates o en zonas con pocos datos, y no dice si la red está muy segura o poco segura de sus respuestas. También pasa que la interfaz puede mostrar “neutral” por su propia regla aunque la red haya predicho otra cosa. Y si uno escoge la mejor configuración mirando siempre la misma prueba, el resultado queda un poco sesgado.
