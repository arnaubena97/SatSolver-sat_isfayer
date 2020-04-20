#!/usr/bin/env python3
import sys
import random
import networkx
import os


class Graph():
    def __init__(self, file_name):
        self.graph = networkx.Graph()

        self.file_name = file_name
        self.num_vertex = 0
        self.num_colors = 0
        self.edges = []

        self.readfile(file_name)
        self.solution = self.call_solver(file_name)
        self.set_vertexs()
        self.set_edges()
        self.list_colors = self.create_colors()

    def readfile(self, file_name):
        """File reader and parser the num of vertex"""
        with open(file_name) as all_file:
            for line in all_file:
                if line.startswith('c'): continue
                if line.startswith('p'): continue  # ignore comments
                if line.startswith('-'):
                    self.edges.append(list(map(int, line[:-3].split(' '))))
                    continue
                if int(line[0]) > 0:
                    self.num_colors = len(line.split(' ')) - 1
                    self.num_vertex += 1


    def create_colors(self): #feta i acabada correctament
        """Return a list with the random color"""
        color = [ "#{:06x}".format(random.randint(0, 0xFFFFFF)) for _ in range(self.num_colors)]
        return color

    def set_vertexs(self): #feta i acabada correctament
        for vertex in range(self.num_vertex):
            self.graph.add_node(vertex)

    def set_edges(self):
        for tuple in self.edges:
            if self.operation_one(tuple[0]) != self.operation_one(tuple[1]):
                self.graph.add_edge(self.operation_one(tuple[0])-1, self.operation_one(tuple[1])-1)

    def operation_one(self, number):
        return next_int(number*-1/self.num_colors)


    def call_solver(self, file):
        command = "python3.6 sat_isfayer.py " + str(file) + " > t.txt"
        os.system(command)

        for l in open("t.txt", "r"):
            if l[0]== "v":
                solution = list(map(int, l[2:-3].split(" ")))
        os.system("rm t.txt")
        return solution

    def decide_colors(self):
        colors = []

        for x in range(self.num_vertex):
            positive = -sys.maxsize
            trunc = self.solution[x*self.num_colors:self.num_colors*(x+1)]
            for var in trunc:
                if var > positive:
                    positive = var
            colors.append(trunc.index(positive))

        return colors

    def showGraph(self):

        g = networkx.nx_agraph.to_agraph(self.graph)
        g.node_attr['style'] = 'filled'
        g.node_attr['shape'] = 'circle'
        g.node_attr['fixedsize'] = 'true'
        g.edge_attr['color'] = '#000000'
        how_color = self.decide_colors()
        for x in range(self.num_vertex):
            g.get_node(x).attr['fillcolor'] = str(self.list_colors[how_color[x]])
        g.layout()
        g.draw("out.png",prog="circo")






def next_int(number):
    if number > int(number):
        return int(number)+1
    return int(number)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("\n Command: python %s <file_name.txt> <num_colors>\n" %sys.argv[0])
        exit(0)


    graph = Graph(file_name)

    graph.showGraph()

