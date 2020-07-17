from room import Room
from player import Player
from world import World


import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


class Graph:

    def __init__(self):
        self.explored = {}
        self.path = []

    def reverse(self, direction):
        if direction == "n":
            return "s"
        if direction == "s":
            return "n"
        if direction == "e":
            return "w"
        if direction == "w":
            return "e"

    def traverse(self, starting_vertex):
        #add exits to starting room vector
        self.explored[starting_vertex] = player.current_room.get_exits()

        while len(room_graph) > len(self.explored):
            #if not explored add to graph, add exits to vector
            if player.current_room.id not in self.explored:

                self.explored[player.current_room.id] = player.current_room.get_exits()
            #if vector has no remaining unexplored routes, go back a step
            elif len(self.explored[player.current_room.id]) == 0:
                last_move = self.path[-1]
                #add to traversal path
                traversal_path.append(last_move)
                #move
                player.travel(last_move)
                #remove from path
                self.path.pop()
            else:
                #get an unexplored route
                exit = self.explored[player.current_room.id].pop()
                #add to traversal path
                traversal_path.append(exit)
                #move
                player.travel(exit)
                #add to path (reversed for going back)
                self.path.append(self.reverse(exit))

#this should run, updating traversal_path with a simplified DFT
Graph().traverse(player.current_room.id)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
