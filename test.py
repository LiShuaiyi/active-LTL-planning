# from copyreg import constructor
# from mimetypes import init
# from operator import truediv
# from queue import Empty
# from re import T
# from networkx.classes.digraph import DiGraph
# import networkx as nx
# from copy import deepcopy
import random
import time

from visualize import showLTS,showAutomaton,showProduct
from utility import generation_LTS,extract_automaton,product,action_sense_pair
from BTS import generation_BTS
from ATS import generation_mq0
from algorithm import winningregion_construction,control_generation

A = extract_automaton('.\\automaton','2.txt')
# showAutomaton(A,name='test')

LTS = generation_LTS(num=[4,4],ndetermin=5,num_observation=1)
# showLTS(LTS,name='test')

P = product(A,LTS)
# showProduct(P,name='test')


BTS,init_b = generation_BTS(P)
print(BTS.nodes)

# q = random.choice(list(BTS.nodes))
# Mq, MqF = generation_ATS(q,BTS,P)
# print(1,BTS)


Qwin, dict = winningregion_construction(P,BTS)   
q = random.choice(Qwin)
Mq,MqF,Mq_t_d = dict[q]
m = generation_mq0(q,P)
control_generation(m,Qwin,Mq,MqF,Mq_t_d)
