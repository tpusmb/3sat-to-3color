#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import timeit
import logging.handlers
from color_problem import Graph, Coloration

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/3-sat-problem.log",
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


class Sat:

    def __init__(self, abs_path_graph_file_name):
        """
        Constructor to create a graph with nothing inside or with a save file
        :param abs_path_graph_file_name: (string) Absolute path to the graph file name
        """

        # For display
        self.clauses = []
        # Graph of the 3 color
        self.graph = Graph()
        self.coloration = Coloration()
        self.graph.add_node("T", ["F", "O"])
        self.graph.add_node("F", ["T", "O"])
        self.graph.add_node("O", ["F", "T"])

        with open(abs_path_graph_file_name) as file:
            lines = file.readlines()
            nb_literal, nb_clause = lines[1].split(' ')
            nb_literal = int(nb_literal)
            # Generate all the boolean literal
            for literal in range(1, nb_literal + 1):
                self.graph.add_node(str(literal), ["-{}".format(literal)])
                self.graph.add_node("O", [str(literal), "-{}".format(literal)])

            current_added_node = 1
            # Read all clause
            for line in lines[2:-1]:
                self.clauses.append(line.replace('\n', '').split(' '))
                current_added_node = self.__generate_gadget(current_added_node, *self.clauses[-1])

    def __generate_gadget(self, start_node_number, literal_1, literal_2, literal_3):

        # Generate S start_node_number, S start_node_number + 1, ..., S start_node_number + 4
        gadget = ["S{}".format(number) for number in range(start_node_number, start_node_number + 5)]
        # Triangle S1, S2, S3
        self.graph.add_node(gadget[0], [gadget[1], gadget[2]])
        self.graph.add_node(gadget[1], [gadget[2]])
        # S3
        # |
        # S4 - S5
        self.graph.add_node(gadget[2], [gadget[3]])
        self.graph.add_node(gadget[3], [gadget[4]])

        # literal_1 with S1
        self.graph.add_node(literal_1, [gadget[1]])
        # literal_2 with s2
        self.graph.add_node(literal_2, [gadget[2]])
        # literal_3 with s3
        self.graph.add_node(literal_3, [gadget[4]])

        # Now add the S4 and S5 with the true node
        self.graph.add_node("T", [gadget[3], gadget[4]])
        return start_node_number + 4

    def display_graph(self):
        """

        :return:
        """
        self.graph.display_graph(self.coloration)

    def generate_graph_file(self, output_file_name):
        """

        :param output_file_name:
        :return:
        """


    def __str__(self):

        res = "("
        for i in range(len(self.clauses)):
            clause = self.clauses[i]
            for j in range(len(clause) - 1):
                val = "X{} ou ".format(clause[j]) if '-' not in clause[j] else "not X{} ou ".format(clause[j][-1])
                res += val
            res += "X{})".format(clause[-1]) if '-' not in clause[-1] else "not X{})".format(clause[-1][-1])
            if i < len(self.clauses) - 1:
                res += " et ("
        return res


if __name__ == "__main__":
    sat = Sat("instances/3sat_vrais.txt")
    print(sat)
    sat.display_graph()
