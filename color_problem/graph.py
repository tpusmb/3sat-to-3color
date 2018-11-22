#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A file with a graph class
"""

from __future__ import absolute_import
import os
import matplotlib.pyplot as plt
import networkx as nx
import logging.handlers
from color_problem.coloration import Coloration

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/Graphe.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


class Graph:
    """
    Class graph to represent a graph
    """

    def __init__(self, abs_path_graph_file_name=None):
        """
        Constructor to create a graph with nothing inside or with a save file
        :param abs_path_graph_file_name: (string) Absolute path to the graph file name
        """
        self.graph = {}
        if abs_path_graph_file_name is None:
            return
        with open(abs_path_graph_file_name) as file:
            lines = file.readlines()
            for line in lines[2:-1]:
                node1, node2 = line.replace('\n', '').split('-')
                self.add_node(node1, [node2])

    def add_node(self, node_name, links):
        """
        Function to add a node to the graph with bidirectional link
        If you add S1 link with S2 this function will add the S2 node in the graph
        Note: You can add new link on a node just by calling this function a new time
        :param node_name: (string) Key name of the node
        :param links: (list of string) All the nodes linked to the created node
        """

        # control if the input node is in the graph
        if node_name not in self.graph:
            self.graph[node_name] = links

        for node in links:
            # Control if the node in link is not already in the input node
            if node not in self.graph[node_name]:
                self.graph[node_name].append(node)

            # Add the bidirectional link
            if node not in self.graph:
                self.graph[node] = [node_name]
            elif node_name not in self.graph[node]:
                self.graph[node].append(node_name)

    def generate_graph_file(self, output_file_name):
        """

        :param output_file_name:
        :return:
        """
        with open(output_file_name, "w") as f:
            f.write("Graph{\n")
            f.write(' '.join(self.get_nodes()))
            f.write('\n')
            writen_link = []
            for node in self.graph:
                for neighbour in self.graph[node]:
                    str_link = "{}-{}".format(node, neighbour)
                    str_link_oposit = "{}-{}".format(neighbour, node)
                    if str_link not in writen_link and str_link_oposit not in writen_link:
                        f.write("{}\n".format(str_link))
                        writen_link.extend([str_link, str_link_oposit])
            f.write("}")
        PYTHON_LOGGER.info("Export done !")

    def get_nodes(self):
        """
        Function to get all nodes of the graph
        :return: (list) All the graph's nodes
        """

        return list(self.graph.keys())

    def get_neighbour(self, node):
        """
        Get allt he neighbour of the input node
        :param node: (string) Node to get all his neighbour
        :return: (list of string) all the neighbour of the input node, empty list if the node not existe
        """
        try:
            return self.graph[node]
        except Exception:
            return []

    def all_node_have_color(self, coloration):
        """
        Function to now if all the nodes have a coloration
        :param coloration: (Coloration) Coloration of the nodes
        :return: (boolean) True all the nodes have a color else False
        """
        for node in self.get_nodes():
            if coloration.get_node_color(node) is None:
                return False
        return True

    def display_graph(self, coloration):
        """
        Display the graph in window. Display the node in gray if is have no attributed color
        :param coloration: (coloration) coloration for each node
        """
        graph_nx = nx.Graph()
        labels = {}
        for node in self.graph:
            for neighbour in self.graph[node]:
                graph_nx.add_edge(node, neighbour)
            color = 'gray' if coloration.get_node_color(node) is None else coloration.get_node_color(node)
            labels[node] = node + " " + color
        nx.draw(graph_nx, with_labels=True, labels=labels)
        plt.axis('off')
        plt.show()


if __name__ == "__main__":
    g = Graph("../instances/3c_faux.txt")
    coloration = Coloration()
    coloration.color_node("s1", coloration.BLUE)
    coloration.color_node("s2", coloration.GREEN)
    coloration.color_node("s3", coloration.RED)
    g.display_graph(coloration)
