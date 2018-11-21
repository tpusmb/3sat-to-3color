#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script with 2 algorithm implementation to solve 3 color problem @ Blanc Swan & LE BRAS Clément

Usage:
   problem_3_coloration.py <input-file> [--generate-and-test --solve-back-tracking --show]

Options:
    -h --help                         Show this screen.
    <input-file>                      absolute path to the input file to read the graph
    --generate-and-test               Function to generate all possibles coloration of a graph and check
                                      if there is at least one valid 3-coloration
    --solve-back-tracking             Function to solve the 3c problem with a back tracking algorithm
    --show                            Show the load graph
"""

from __future__ import absolute_import
from graph import Graph
from coloration import Coloration
import os
import itertools
import logging.handlers
from docopt import docopt

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/problem_3_coloration.log",
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


def check_certificate(graph_to_test, coloration_to_test):
    """
    Function to check a coloration is a valid 3-coloration for his graph
    :param graph_to_test: (Graph) The graph we want to test
    :param coloration_to_test: (Coloration) The graph's coloration
    :return: (boolean) True if the 3-coloration is valid, False if it is not
    """

    for node in graph_to_test.graph:
        color_node = coloration_to_test.get_node_color(node)
        if color_node is None:
            continue
        for link in graph_to_test.graph[node]:
            color_link = coloration_to_test.get_node_color(link)
            if color_link is not None and color_node == color_link:
                return False
    return True


def generate_and_test(graph_to_test):
    """
    Function to generate all possibles coloration of a graph and check if there is at least one valid 3-coloration
    :param graph_to_test: (Graph) The graph we want to test
    :return: (boolean) True if there is a valid 3-coloration for this graph, False if it's not the case
    """

    nb_node = len(graph_to_test.get_nodes())
    all_color_combination = [list(combination)
                             for combination in itertools.product([Coloration.RED,
                                                                   Coloration.GREEN,
                                                                   Coloration.BLUE], repeat=nb_node)]
    for combination in all_color_combination:
        coloration = Coloration()
        for node, color in zip(graph_to_test.get_nodes(), combination):
            coloration.color_node(node, color)
        if check_certificate(graph_to_test, coloration):
            return True, coloration
    return False, coloration


def solve_back_tracking(graph_to_test):
    """
        Function to solve the 3c problem with a back tracking algorithm
        :param graph_to_test: (Graph) The graph we want to test
        :return: (boolean) True if there is a valid 3-coloration for this graph, False if it's not the case
    """

    def aux(current_node, explore_nodes, coloration, last_color):
        """
        Aux function to implement the back tracking algorithm
        :param current_node: (string) Current explore node
        :param explore_nodes: (list of string) List of all the explore nodes
        :param last_color: (string) last color used by the neighbour
        :param coloration: (Coloration) current coloration state of the graph
        :return: (boolean) True we found a solution else False
        """
        # Chack if the node is not explore
        if current_node in explore_nodes:
            return

        # Test all the colors
        for color in [Coloration.RED, Coloration.GREEN, Coloration.BLUE]:

            # Control if the neighbour color is not the same
            if color == last_color:
                continue
            # Set the color
            coloration.color_node(current_node, color)
            # Control if the graph is ok
            graph_is_ok = check_certificate(graph_to_test, coloration)
            if not graph_is_ok:
                coloration.delete_color(current_node)
                continue
            # If we explore all the nodes and the graph is ok we finish
            elif graph_is_ok and graph_to_test.all_node_have_color(coloration):
                return True
            # explore all the neighbours of the current node
            for neighbour in graph_to_test.get_neighbour(current_node):
                # If the aux function found a solution we have finish
                if aux(neighbour, explore_nodes + [current_node], coloration, color):
                    return True
            coloration.delete_color(current_node)
        return False

    coloration = Coloration()
    res = aux(graph_to_test.get_nodes()[0], [], coloration, None)
    return res, coloration


if __name__ == "__main__":
    arguments = docopt(__doc__)
    my_graph = Graph(arguments["<input-file>"])

    if arguments["--generate-and-test"]:
        res, coloration = generate_and_test(my_graph)
        PYTHON_LOGGER.info("Generate and test: {}".format(res))
        if arguments["--show"]:
            my_graph.display_graph(coloration)

    if arguments["--solve-back-tracking"]:
        res, coloration = solve_back_tracking(my_graph)
        PYTHON_LOGGER.info("Back tracking algorithm: {}".format(res))
        if arguments["--show"]:
            my_graph.display_graph(coloration)
