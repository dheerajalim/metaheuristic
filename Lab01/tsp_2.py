"""
TSP for Nearest neighbour

Author : Dheeraj
Date: 21/09/2019
Python Version: 3.6.8
"""

import math
import random
import sys

def open_tsp(filename):
    coordinates = []
    with open(filename,'r') as file:
        next(file)
        lines = [line.strip() for line in file.readlines()]
        for coordinate in lines:
            coordinates.append(coordinate.split(' '))
    return coordinates


def euclidean_distance(coordinates):
    result_list = []
    for i in range(0,len(coordinates)):
        for j in range(i+1,len(coordinates)):
            (int(coordinates[j][1])-int(coordinates[i][1]))**2
            weight = round(math.sqrt((int(coordinates[j][1])-int(coordinates[i][1]))**2 + (int(coordinates[j][2])-int(coordinates[i][2]))**2))

            result_list.append([i, j, weight])  # Creating a List of weights from each node


    return len(coordinates), result_list


def weight_graph(matrix_size,result_list):

    distance_matrix = [0] * matrix_size
    for i in range(matrix_size):
        distance_matrix[i] = [0] * matrix_size

    loc = 0
    for i in range(matrix_size-1):
        value = result_list[loc]
        for j in range(i+1,matrix_size):

            distance_matrix[i][j] = value[2]
            distance_matrix[j][i] = value[2]
            loc = loc + 1
            if loc == len(result_list):
                break
            value = result_list[loc]

    return distance_matrix  # Returns the matrix of distances calculated from Node (A) to Node (B) where A,B is set(All nodes), A!= B


def shortest_route(distance_matrix,start):

    T = distance_matrix
    partial_list = []
    weight_list = []
    final_weight_list = []

    partial_list.append(start)   # Adding the already traversed vertex to the list

    for j in range(0,len(T)):
        for i in range(0,len(T)):
            if i in partial_list:
                continue            # Not accounting the vertex already traversed
            weight_list.append(T[start][i])     # Creating the weight list for the specific vertex

        final_weight = min(weight_list)  # Finding the minimum weight for the traversd vertex
        final_weight_list.append(min(weight_list))
        vertex = T[start].index(final_weight)
        if vertex in partial_list:
            cc = vertex

            for item in T[start][vertex+1:]:
                cc = cc + 1
                if item == final_weight:
                    vertex = cc
                    break

        partial_list.append(vertex)

        start = partial_list[-1]
        weight_list = []

        if len(partial_list) == len(T):  # Condition to check if the last node available is reached
            final_weight_list.append(T[start][partial_list[0]]) # List of weights of the travelled path
            partial_list.append(partial_list[0])  # List of the vertex followed in the path
            print(f'The shortest path is {partial_list}')
            print(f'The sum of minimum weight {sum(final_weight_list)}')
            return partial_list, sum(final_weight_list)


def generate_tsp(shortest_path,final_weight,filename):
    with open(filename, 'w') as file:
        file.write(str(final_weight)+'\n')
        for route_number in shortest_path:
            file.write(str(route_number))
            file.write('\n')


if __name__ == "__main__":
    filename = sys.argv[1]
    coordinates = open_tsp(filename)
    weight_matrix = euclidean_distance(coordinates)
    distance_matrix = weight_graph(weight_matrix[0],weight_matrix[1])
    shortest_path = shortest_route(distance_matrix , start=random.randint(0, len(coordinates)-1))
    generate_tsp(shortest_path[0],shortest_path[1], filename = sys.argv[2])
