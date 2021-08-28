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
def bfs_path(start, finish, world):

    num_rows, num_columns = world.width, world.height

    row_q = []
    column_q = []

    move_count = 0
    prev = []
    prev_route = []

    nodes_left_in_layer = 1
    nodes_in_next_layer = 0

    found_finish = False

    visited = [[ False for i in range(num_columns)] for j in range(num_rows)]

    #n s e w
    dr = [-1,1,0,0]
    dc = [0,0,1,-1]

    row_q.append(start[0])
    column_q.append(start[1])
    prev.append(start)  #(x, y , how we got here)
    prev_route.append(None)

    visited[start[0]][start[1]] = True

    while (len(row_q) > 0):
        r = row_q.pop(0)
        c = column_q.pop(0)
        if  r == finish[0] and c == finish[1]:
            found_finish = True
            break
        #explore neighbours
        for i in range(4):
            rr = r + dr[i]
            cc = c + dc[i]

            #Bound checking included in isCollision()
            #if rr<0 or cc<0:
            #    continue
            #if rr>=num_rows or cc>=num_columns:
            #    continue

            if visited[rr][cc] == True:
                continue

            #if obstacle skip
            if world.isCollision((rr,cc)):
                continue

            row_q.append(rr)
            column_q.append(cc)
            prev.append((rr, cc))
            prev_route.append(prev.index((r,c)))
            visited[rr][cc] = True
            nodes_in_next_layer +=1 

        #
        nodes_left_in_layer -= 1
        if nodes_left_in_layer == 0:
            nodes_left_in_layer = nodes_in_next_layer
            nodes_in_next_layer = 0
            move_count += 1
    if found_finish == True:
        return reconstruct_path_bfs(start, finish, prev, prev_route)
    return None


def reconstruct_path_bfs(s, e, prev, routes):
    path = []
    at_index = prev.index(e)
    while(at_index != None):
        path.append(prev[at_index])
        at_index = routes[at_index]
    path.reverse()
    if path[0] != s:
        print("character unable to find route.")
        return None
    return path



#testing
def test_walk_direct():
    start_pos = (0,0)
    end_pos = (3,8)
    route = walk_direct(start_pos, end_pos, None)
    print(route)

def test_bfs():
    R = 10
    C = 10
    s = (0,0)
    e = (3,8)
    world = World((R, C))
    path = bfs_path(s, e, world)
    print("bfs test result:")
    print(path)


if __name__ == "__main__":
    test_bfs()