"""
TSP for Nearest neighbour

Author : Dheeraj
Date: 21/09/2019
Python Version: 3.6.8

Approach : 1  (Heauristic)
"""

import math
import random


def open_tsp(filename):
    coordinates = []
    coordinates_int= []
    with open(filename,'r') as file:
        num_vertex = file.readline()   # gets the total number of vertexes from the file
        lines = [line.strip() for line in file.readlines()]
        for coordinate in lines:
            coordinates.append(coordinate.split(' ')) # gets coordinates of all the vertexes(x,y)

    for item in coordinates:
        coordinates = [int(x) for x in item]
        coordinates_int.append(coordinates)  #Converts the string coordinates tom int

    return num_vertex , coordinates_int  # Returns the total vertex and list of coordinates for each vertex



def vertex_generation(filename):

    vertex_list = open_tsp(filename)
    vertex_list_len = vertex_list[0]
    vertex_coordinates = vertex_list[1]
    original_vertex_list = []

    for i in range(1,int(vertex_list_len)+1):
        original_vertex_list.append(i)   # creates a list of all the original present verticies

    # random_vertex_list = []
    random_vertex_list = random.sample(original_vertex_list,2)  # Generates a random list of initial two vertex

    unattended_vertex = [x for x in original_vertex_list if x not in random_vertex_list]  # All the remaining vertices added to unattended list
    print('Random Vertex', random_vertex_list)
    print('Unattended Vertex', unattended_vertex)

    return random_vertex_list, unattended_vertex, vertex_coordinates



def optimal_route(random_vertex_list, unattended_vertex, vertex_coordinates):

    """
    1 . Now we will calculate the distance of the Random vertex each with the random number from the Unattended Vertex
    2.  Delete the vertex choosen randomly from the Unattended Vertex list
    3.  Calculate the minimum of the distance calculated and push the vertex selected from Unattended vertex list just after
        vertex with which it has minimum distance

    """
    shortest_route_weight = 0
    while len(unattended_vertex) !=0:

        weight_list = []
        #selecting a random vertex from unattended_vertex list
        random_unattended_vertex = random.choice(unattended_vertex)

        #TODO : Calculate the distance of the random_unattended_vertex from rach vertex in random_vertex_list

        # Calculating the Euclidean Distane

        for element in random_vertex_list:
            coord_a_x = vertex_coordinates[element-1][1]
            coord_b_x = vertex_coordinates[random_unattended_vertex-1][1]

            coord_a_y = vertex_coordinates[element-1][2]
            coord_b_y = vertex_coordinates[random_unattended_vertex-1][2]
            # print(coord_a_x,coord_b_x)
            # print(coord_a_y,coord_b_y)

            weight = round(math.sqrt((coord_a_x - coord_b_x) ** 2 + (coord_a_y - coord_b_y) ** 2))

            weight_list.append(weight)

        final_weight = min(weight_list)
        min_distance_loc  = weight_list.index(final_weight)
        random_vertex_list.insert(min_distance_loc+1, random_unattended_vertex)

        shortest_route_weight += final_weight
        unattended_vertex.remove(random_unattended_vertex)

    print("Optimal Route Weight: ", shortest_route_weight )
    print("Optimal Route:" , random_vertex_list)

    return shortest_route_weight, random_vertex_list


def generate_tsp(shortest_route_weight, random_vertex_list, filename):
    with open(filename, 'w') as file:
        file.write(str(shortest_route_weight)+'\n')
        for route_number in random_vertex_list:
            file.write(str(route_number))
            file.write('\n')


# Adding the main class
if __name__ == '__main__':
    random_vertex_list, unattended_vertex, vertex_coordinates = vertex_generation('inst-0.tsp')
    shortest_route_weight, random_vertex_list = optimal_route(random_vertex_list, unattended_vertex, vertex_coordinates)
    generate_tsp(shortest_route_weight, random_vertex_list,'sol_1.tsp')






