import os
import sys
import pygame

from world import *

#return array of walks
def walk_direct(start_pos, end_pos, grid=None):
    route = []
    current = list(start_pos)
    print(current)
    route.append((current[0], current[1]))
    while(current != list(end_pos)):
        #move
        if current[0] > end_pos[0]:
            current[0] -= 1
        elif current[0] < end_pos[0]:
            current[0] += 1

        if current[1] > end_pos[1]:
            current[1] -= 1
        elif current[1] < end_pos[1]:
            current[1] += 1

        if(current in route):
            print("character unable to pathfind. movement haulted.")
            break
        print(current)
        route.append((current[0], current[1]))


    return route


def test_pathing():
    start_pos = (0,0)
    end_pos = (3,8)
    route = walk_direct(start_pos, end_pos, None)
    print(route)


test_pathing()