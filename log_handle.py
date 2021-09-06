import os
import ast

my_dict = dict()


def read_dict():
    global my_dict
    path = os.path.join(os.path.dirname(__file__), "log.txt")
    f = open(path, "r")
    dic = ast.literal_eval(f.read())
    f.close()
    my_dict = dic


def write_dict():
    global my_dict
    path = os.path.join(os.path.dirname(__file__), "log.txt")
    f = open(path, "w")
    f.write(str(my_dict))
