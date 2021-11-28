# Sistema de recomendación
# Autor: Aitor Alonso Melián

import argparse
import sys
from functools import reduce
from math import sqrt
from copy import deepcopy

# ****************************
# Declaración de funciones

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



def is_incomplete(array): # Función que devuelve True si hay algun valor en el array que sea '-', y false en caso contrario.
    result = False
    for i in array:
        if (i == '-'):
            result = True
    return result

def incomplete_index(array): # Función que devuelve el índice del elemento del array que contenga '-'
    result = False
    for i in range(len(array)):
        if (array[i] == '-'):
            return i

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

def cosine_distance(u: list, v:list): # Devuelve la distancia coseno entre 2 arrays (Cada array representa un usuario)
    x = 0
    y1 = 0
    y2 = 0
    for i in range(len(u)):
        x += u[i] * v[i]
        y1 += u[i]**2
        y2 += v[i]**2
    result = x / (sqrt(y1)*sqrt(y2))
    return result

def euclidean_distance(u: list, v: list): # Devuelve la distancia euclidea entre 2 arrays (Cada array representa un usuario)
    x = 0
    for i in range(len(u)):
        x += (u[i]- v[i])**2
    result = sqrt(x)
    return result

def prediction(user_sim_matrix, matrix, neighbors, pred, metric): # Función que itera sobre todas las filas de la matriz y la va rellenando con las predicciones realizadas
    pred_matrix = deepcopy(matrix)
    for i in range(len(pred_matrix)):
        print("ITERACION PARA EL USUARIO " + str(i) + ":")
        while (is_incomplete(pred_matrix[i])):
            index = incomplete_index(pred_matrix[i])
            
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
            x = 0
            y = 0
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

# ****************************

# PROGRAMA PRINCIPAL
args = arg_handler()
fileMatrix = args.file.readlines()

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

# Se crea la matriz de similitudes entre usuarios
user_sim_matrix = []
for i in range(len(matrix)):
    user_sim_matrix.append([])
    for j in range(len(matrix)):
        user_sim_matrix[i].append(round(sim(i, j, matrix, args.metric),7))

# Se llama a la función predicción, pasandole la matriz de similitudes, la matriz de productos, el número de vecinos, la predicción y la métrica seleccionada.
pred_matrix = prediction(user_sim_matrix, matrix, args.neighbors, args.pred, args.metric)

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
