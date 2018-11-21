#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import timeit
import logging.handlers

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

        self.clauses = []
        with open(abs_path_graph_file_name) as file:
            lines = file.readlines()
            for line in lines[2:-1]:
                self.clauses.append(line.replace('\n', '').split(' '))

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
