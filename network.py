#! /usr/bin/python

import sys

import networkx as nx
from networkx.algorithms import find_cliques
import matplotlib.pyplot as plt

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Pass in starting file name'
        exit()

    fn = sys.argv[1]

    G = nx.Graph()
    with open(fn, 'r') as f:
        f.readline() # Skip the header
        for line in f:
            u1, u2 = line.strip().split(',')
            # print u1, u2
            G.add_edge(u1, u2)
            # exit()

    print G.number_of_nodes()
    print G.number_of_edges()

    # for x in find_cliques(G):
    #     print x

    # nx.draw_random(G)
    # plt.show()

    # nx.draw_random(G)
    # plt.show()
