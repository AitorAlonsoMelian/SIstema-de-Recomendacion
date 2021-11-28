# Sistema de recomendación

## Uso

Para ejecutar el programa se ejecuta:

 ```$ python Recomendacion.py [Matriz de utilidad] [Métrica elegida] [Número de vecinos] [Tipo de predicción]```

Posibles valores de los argumentos:
- **Matriz de utilizad**: Cualquier fichero de texto que contenga una matriz con el formato adecuado.
- **Métrica**: [pearson/cosine_distance/euclidean_distance]
- **Número de vecinos**: Cualquier número mayor que 2.
- **Tipo de predicción**: [simple/mean_diff]

El programa mostrará por línea de comandos las iteraciones para los diferentes usuarios, especificando las posiciones de las que está haciendo la predicción, mostrando los índices de los vecinos mas parecidos junto con sus valores.
Como el formato de las matrices puede no verse de manera adecuada en la terminal, el resultado de la matriz de predicciones y la matriz de similitud entre usuarios los imprimo en el fichero 'out.txt'.

## Descripción del código desarrollado

El código está dividido en dos secciones, una sección para la declaración de funciones, y otra para el programa principal.

### Programa principal
Lo primero en ejecutarse es la funcion arg_handler, que gestiona la entrada por parámetros del programa, y devuelve los argumentos para guardarlo en la variable args. Se accede a la variable `file` de args para guardar la matriz, aunque esta no está en el formato adecuado para ser tratada.

Para tener la matriz en un formato adecuado hago uso del siguiente código:
```python
matrix = []
# Se va rellenando una matriz con el formato [[Fila1],[Fila2]...] para tener los datos mas accesibles
for i in fileMatrix:
    aux = []
    for j in i.split():
        if (j != '-'):
            aux.append(int(j))
        else:
            aux.append(j)
    matrix.append(aux)
```
Una vez la matriz de utilidad esté en un formato accesible, se crea la matriz de similitud entre usuarios:
```python
user_sim_matrix = []
for i in range(len(matrix)):
    user_sim_matrix.append([])
    for j in range(len(matrix)):
        user_sim_matrix[i].append(round(sim(i, j, matrix, args.metric),7))
```
Para introducir cada valor en la matriz se llama a la función de similitud `sim`, que calcula la similitud entre el usuario i y el usuario j basandose en la matriz de utilidad y la métrica seleccionada. 

Para llevar a cabo la predicción, se llama a la función prediction, pasandole todos los parámetros necesarios, que es la que rellena la matriz con los valores de las predicciones, y la devuelve a la variable `pred_matrix`.

Finalmente abro el fichero `out.txt` para escribir las matrices resultantes en este fichero, ya que, en caso de que la matriz sea muy grande, no se ve de manera correcta en la terminal.

```python
# Se escribe la matriz rellena con las predicciones en un fichero para poder visualizarla mejor.
f = open('out.txt','w')
f.write("Matriz de predicciones: \n")
for i in range(len(pred_matrix)):
    f.write("Usuario " + str(i) + ":\t")
    for j in pred_matrix[i]:
        f.write("{:.2f}".format(j))
        f.write("\t")
    f.write("\n")
f.write("\n")

# Se escribe la matriz de similitudes entre usuarios en un fichero para poder visualizarla mejor.
f.write("Matriz de similitud entre usuarios:\n")
for i in range(len(user_sim_matrix)):
    f.write("Usuario " + str(i) + ":\t")
    for j in user_sim_matrix[i]:
        f.write("{:.2f}".format(j))
        f.write("\t")
    f.write("\n")

f.close()
```

### Funciones

```python
def arg_handler(): # Gestiona los argumentos pasados por línea de comandos.

    parser = argparse.ArgumentParser(description="Programa de sistemas de recomendación")

    parser.add_argument('file', type=argparse.FileType('r'))
    parser.add_argument('metric')
    parser.add_argument('neighbors', type=int)
    parser.add_argument('pred')

    if (parser.parse_args().metric != 'pearson' and parser.parse_args().metric != 'cosine_distance' and parser.parse_args().metric != 'euclidean_distance'):
        print("Metrica no soportada. (pearson/cosine_distance/euclidean_distance)")
        sys.exit()
    if (parser.parse_args().neighbors < 2):
        print("Se deben seleccionar mínimo 2 vecinos")
        sys.exit()
    if (parser.parse_args().pred != 'simple' and parser.parse_args().pred != 'mean_diff'):
        print("Tipo de predicción no soportado. (simple/mean_diff)")
        sys.exit()

    return parser.parse_args()
```
No hay mucho que mencionar de arg_handler, ya que lo único que hace es gestionar los argumentos de la línea de comandos, y devolverlos parseados.

```python
def sim(user1, user2, matrix, metric): # Calcula la similitud entre el user1 y el user2 basado en la matriz proporcionada y la métrica seleccionada
    
    user1_vector = []
    user2_vector = []
    for i in range(len(matrix[user1])):
        if (matrix[user1][i] != '-' and matrix[user2][i] != '-'):
            user1_vector.append(matrix[user1][i])
            user2_vector.append(matrix[user2][i])

    if (metric == 'pearson'):
        return pearson(user1_vector, user2_vector)
    elif (metric == 'cosine_distance'):
        return cosine_distance(user1_vector, user2_vector)
    elif (metric == 'euclidean_distance'):
        return euclidean_distance(user1_vector, user2_vector)
```
La función sim devuelve la similitud entre dos usuarios dependiendo de las métricas y la matriz proporcionada. Primero el bucle inicial crea dos arrays con las puntuaciones de los productos que AMBOS usuarios han puntuado, ya que no tiene sentido tener en cuenta para calcular la correlación un producto que no haya votado uno de los dos. Una vez se tengan esos arrays, simplemente dependiendo de la métrica se llama al método correspondiente pasandole esos dos arrays.
```python
def pearson(u: list,v: list): # Devuelve la correlación de pearson entre 2 arrays (Cada array representa un usuario)
    u_mean = sum(u)/len(u)
    v_mean = sum(v)/len(v)
    x = 0
    y1 = 0
    y2 = 0
    for i in range(len(u)):
        x += (u[i]-u_mean)*(v[i]- v_mean)
        y1 += (u[i] - u_mean)**2
        y2 += (v[i] - v_mean)**2
    result = x/(sqrt(y1)*sqrt(y2))
    return result
```
Respecto al método de pearson no hay mucho que explicar tampoco, es la aplicación de la fórmula de la correlación de pearson, la cual dividí en varias partes para que se hiciera más sencillo de programar y de entender. Como la distancia coseno y la distancia euclidea son aplicaciones de fórmulas matemáticas también, las omitiré de la explicación, pero están disponibles en el código fuente.

```python
def prediction(user_sim_matrix, matrix, neighbors, pred, metric): # Función que itera sobre todas las filas de la matriz y la va rellenando con las predicciones realizadas
    pred_matrix = deepcopy(matrix)
    .
    .
    .
```
La función prediction es la más importante, ya que es la que hace todos los cálculos. Primero hacemos una copia de la matriz de utilidad original, para ello uso `deepcopy`, una función de la librería `copy`. Uso esta función ya que si hago una copia directamente sin esa función, al editar la matriz `pred_matrix` estaré editando también la matriz original.
Se hace una copia ya que, en caso de no hacerlo, estaríamos usando las predicciones que se hagan, por ejemplo, sobre el usuario 0, para formar las predicciones sobre el usuario 1, lo cual no es muy adecuado.
```python
    .
    .
    for i in range(len(pred_matrix)):
        print("ITERACION PARA EL USUARIO " + str(i) + ":")
        while (is_incomplete(pred_matrix[i])):
            index = incomplete_index(pred_matrix[i])
    .
    .
```
Se empezará iterando sobre la `pred_matrix`. Mientras la fila `i` de la matriz de predicciones siga incompleta, se seguirá ejecutando el código, hasta llenar la fila de ese usuario de predicciones. `is_incomplete` devuelve True si encuentra un '-' en alguna posición de la fila, o False en caso contrario. `incomplete_index` devuelve el índice del array que aun no está completado.
```python
            .
            .
            aux = deepcopy(user_sim_matrix[i])
            print("Predicción para la posición [" + str(i) + "][" + str(index) + "]")
            for j in range(len(aux)):
                if (matrix[j][index] == '-'):
                    aux.remove(user_sim_matrix[i][j])
            
            if (metric == 'pearson' or metric == 'cosine_distance'):
                aux.sort(reverse=True)
            else:
                aux.sort(reverse=False)
                
            best_neighbors_values = aux[0:neighbors]
            best_neighbors_indexs = []
            for x in range(len(best_neighbors_values)):
                best_neighbors_indexs.append(user_sim_matrix[i].index(best_neighbors_values[x]))
            
            print("Indices de los mejores vecinos: " + str(best_neighbors_indexs))
            print("Valores de los mejores vecinos: " + str(best_neighbors_values))
            .
            .
```
Esta parte del código lo que hace es seleccionar los k mejores vecinos, e imprimir por pantalla sus indices y sus valores. Como no queremos editar la matriz de similitudes original hacemos una copia del array de la matriz que vamos a utilizar. Primero, elimino de `aux` las similitudes de los usuarios que, al igual que el usuario del que estamos intentando predecir su puntuación, tampoco ha puntuado el producto a predecir, con lo cual no nos sirve de nada ese usuario. Luego se ordenan los valores de mayor a menor, o de menor a mayor, segun la métrica utilizada, y se seleccionan los `neighbors` mejores vecinos. Luego se busca en la matriz de similitudes a que indices(usuarios) corresponden esos valores.

```python
            .
            .
            if (pred == 'simple'):
                for j in best_neighbors_indexs:
                    x += user_sim_matrix[i][j] * matrix[j][index]
                    y += abs(user_sim_matrix[i][j])
                result = round(x/y, 2)
                if(result < 0):
                    result = 0
                elif(result > 5):
                    result = 5
                print("Predicción: " + str(result))
                pred_matrix[i][index] = result
            .
            .
```
Si la predicción seleccionada es simple, se ejecuta esta parte del código, en el que aplico la fórmula proporcionada en los apuntes de la asignatura, y guardo en la posición correspondiente de la matriz el resultado, para luego devolverlo.
```python   
            .
            .
            elif (pred == 'mean_diff'):
                u_mean = 0
                counter = 0
                for z in pred_matrix[i]:
                    if (z != '-'):
                        u_mean += z
                        counter += 1
                u_mean = u_mean/counter
                
                for j in best_neighbors_indexs:
                    v_mean = 0
                    counter = 0
                    for z in matrix[j]:
                        if (z != '-'):
                            v_mean += z
                            counter += 1
                    v_mean = v_mean/counter
                    x += user_sim_matrix[i][j] * (matrix[j][index] - v_mean)
                    y += abs(user_sim_matrix[i][j])

                result = round(u_mean + (x/y), 2)
                if(result < 0):
                    result = 0
                elif(result > 5):
                    result = 5
                print("Predicción: " + str(result))                
                pred_matrix[i][index] = result
            print()
        print()
    return pred_matrix
```
Finalmente, si la opción seleccionada es la diferencia con la media, se aplica su correspondiente fórmula, y al acabar se devuelve la matriz rellenada.