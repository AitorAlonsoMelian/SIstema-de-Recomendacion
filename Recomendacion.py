import argparse
import sys
from functools import reduce
from math import sqrt
from copy import deepcopy

# ****************************
# Declaración de funciones

def arg_handler():

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

    return parser.parse_args()


def sim(user1, user2, matrix, metric):
    if (user1 == user2):
        return 1
    
    user1_vector = []
    user2_vector = []
    for i in range(len(matrix[user1])):
        if (matrix[user1][i] != '-' and matrix[user2][i] != '-'):
            user1_vector.append(matrix[user1][i])
            user2_vector.append(matrix[user2][i])

    if (metric == 'pearson'):
        return pearson(user1_vector,user2_vector)



def is_incomplete(array):
    result = False
    for i in array:
        if (i == '-'):
            result = True
    return result

def incomplete_index(array):
    result = False
    for i in range(len(array)):
        if (array[i] == '-'):
            return i

def sum(a,b):
    return a+b

def mean(a,b):
    return (a+b)/2

def pearson(u: list,v: list):
    u_mean = reduce(sum,u)/len(u)
    v_mean = reduce(sum,v)/len(v)
    x = 0
    y1 = 0
    y2 = 0
    for i in range(len(u)):
        x += (u[i]-u_mean)*(v[i]- v_mean)
        y1 += (u[i] - u_mean)**2
        y2 += (v[i] - v_mean)**2
    result = x/(sqrt(y1)*sqrt(y2))
    return result

def cosine_distance(u: list, v:list):
    print()

def euclidean_distance(u: list, v: list):
    print()

def prediction(user_sim_matrix, matrix, neighbors, pred):
    pred_matrix = deepcopy(matrix)
    for i in range(len(pred_matrix)):
        while (is_incomplete(pred_matrix[i])):
            index = incomplete_index(pred_matrix[i])
            aux = deepcopy(user_sim_matrix[i])

            for j in range(len(aux)):
                if (matrix[j][index] == '-'):
                    aux.remove(user_sim_matrix[i][j])
            
            aux.sort(reverse=True) # Tener en cuenta que esto solo funciona para pearson
            best_neighbors_values = aux[0:neighbors+1]
            #print(user_sim_matrix[i])
            #print(best_neighbors_values)
            best_neighbors_indexs = []
            for x in range(len(best_neighbors_values)):
                best_neighbors_indexs.append(user_sim_matrix[i].index(best_neighbors_values[x]))
            
            #print("Indices mejores vecinos: " + str(best_neighbors_indexs))
            #print("Valores mejores vecinos: " + str(best_neighbors_values))
            x = 0
            y = 0
            if (pred == 'simple'):
                for j in best_neighbors_indexs:
                    x += user_sim_matrix[i][j] * matrix[j][index]
                    y += abs(user_sim_matrix[i][j])
                result = round(x/y, 2)
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
                    # print(user_sim_matrix[i][j])                    
                    # print(matrix[j][index])
                    # print(v_mean)
                    x += user_sim_matrix[i][j] * (matrix[j][index] - v_mean)
                    y += abs(user_sim_matrix[i][j])

                result = round(u_mean + (x/y), 2)
                pred_matrix[i][index] = result
                #print(u_mean)
                #print(x)
                #print(y)
    return pred_matrix



# ****************************
args = arg_handler()
fileMatrix = args.file.readlines()
matrix = []
for i in fileMatrix: # Voy rellenando una matriz con el formato [[Fila1],[Fila2]...] para tener los datos mas accesibles
    aux = []
    for j in i.split():
        if (j != '-'):
            aux.append(int(j))
        else:
            aux.append(j)
    matrix.append(aux)

user_sim_matrix = []
for i in range(len(matrix)): # Creo la matriz de similitudes entre usuarios.
    user_sim_matrix.append([])
    for j in range(len(matrix)):
        user_sim_matrix[i].append(round(sim(i, j, matrix, args.metric),4))


pred_matrix = prediction(user_sim_matrix, matrix, args.neighbors, args.pred)



f = open('out.txt','w')
for i in pred_matrix:
    for j in i:
        f.write("{:.2f}".format(j))
        f.write(" ")
    f.write("\n")

f.close()
