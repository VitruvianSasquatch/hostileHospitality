import os
import sys
import pygame

from world import *

#return array of walks
def walk_direct(start_pos, end_pos, grid=None):
    route = []
    current = list(start_pos)
    #print(current)
    route.append((current[0], current[1]))
    while(current != list(end_pos)):
        #move
        if current[0] > end_pos[0]:
            current[0] -= 1
        elif current[0] < end_pos[0]:
            current[0] += 1

        elif current[1] > end_pos[1]: # change to if to move diagonally.
            current[1] -= 1
        elif current[1] < end_pos[1]:
            current[1] += 1

        if(current in route):
            print("character unable to pathfind. movement haulted.")
            break
        #print(current)
        route.append((current[0], current[1]))
    return route



#returns a path from start to finsih in tuples. Or None if it fails to make a route
def bfs_path(num_rows, num_columns, start, finish):

    row_q = []
    column_q = []

    move_count = 0
    movements = [start]

    nodes_left_in_layer = 0
    nodes_in_next_layer = 1

    found_finish = False

    visited = [[ False for i in range(num_columns)] for j in range(num_rows)]

    #n s e w
    dr = [-1,1,0,0]
    dc = [0,0,1,-1]
    row_q.append(start[0])
    column_q.append(start[1])

    visited[start[0]][start[1]] = True

    print(visited)

    while (len(row_q) > 0):
        r = row_q.pop()
        c = column_q.pop()
        print(r, c)
        if  r == finish[0] and c == finish[1]:
            found_finish = True
            break
        #explore neighbours
        for i in range(4):
            rr = r + dr[i]
            cc = c + dc[i]

            if rr<0 or cc<0 or rr>=num_rows or cc>=num_columns:
                continue

            if visited[rr][cc] == True:
                continue

            #todo if obstacle continue

            row_q.append(rr)
            column_q.append(cc)
            visited[r][c] = True

            nodes_in_next_layer +=1 
        #
        nodes_left_in_layer -= 1
        if nodes_left_in_layer == 0:
            nodes_left_in_layer = nodes_in_next_layer
            nodes_in_next_layer = 0
            move_count += 1
            movements.append((rr, cc))
    if found_finish == True:
        return movements
        #fix movements
    return None


def test_walk_direct():
    start_pos = (0,0)
    end_pos = (3,8)
    route = walk_direct(start_pos, end_pos, None)
    print(route)

def test_bfs():
    path = bfs_path(3, 5, (0,0), (1,1))
    print(path)
#def bfs_path(num_rows, num_columns, start, finish):


#test_pathing()
#test_bfs()