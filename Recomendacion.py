import argparse
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

def sum(a,b):
    return a+b

def pearson(u: list,v: list):
    u_mean = reduce(sum,u)/len(u)
    #print(u_mean)
    v_mean = reduce(sum,v)/len(v)
    #print(v_mean)
    x = 0
    y1 = 0
    y2 = 0
    for i in range(len(u)):
        x += (u[i]-u_mean)*(v[i]- v_mean)
        y1 += (u[i] - u_mean)**2
        y2 += (v[i] - v_mean)**2
    #print(x)
    #print(y1,y2)
    result = x/(sqrt(y1)*sqrt(y2))
    #print(result)
    return result

def cosine_distance(u: list, v:list):
    print()

def euclidean_distance(u: list, v: list):
    print()

def simple():
    print()

def mean_difference():
    print()

def prediction(user_sim_matrix, matrix, neighbors):
    pred_matrix = deepcopy(matrix)
    for i in range(len(pred_matrix)):
        #while (is_incomplete(pred_matrix[i])):
        user_sim_matrix[i].sort(reverse=True) # Tener en cuenta que esto solo funciona para pearson
        best_neighbors_values = user_sim_matrix[i][1:neighbors]
        print(best_neighbors_values)
        best_neighbors_indexs = []
        for x in range(len(best_neighbors_values)):
            best_neighbors_indexs.append(user_sim_matrix[i].index(best_neighbors_values[x]))
        #print(best_neighbors_indexs)





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
        user_sim_matrix[i].append(sim(i, j, matrix, args.metric))

prediction(user_sim_matrix, matrix, args.neighbors)



