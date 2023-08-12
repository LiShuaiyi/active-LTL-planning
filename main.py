# from copyreg import constructor
# from mimetypes import init
# from operator import truediv
# from queue import Empty
# from re import T
# from networkx.classes.digraph import DiGraph
# import networkx as nx
# from copy import deepcopy
import random
import time,datetime

from visualize import showLTS,showAutomaton,showProduct
from utility import generation_LTS,extract_automaton,product,action_sense_pair,max_Mq
from BTS import generation_BTS
from ATS import generation_mq0
from algorithm import winningregion_construction,control_generation


def main(automaton='2.txt',num=[4,4],ndetermin=3,num_observation=4,num_label=4,p_observation=0.8,num_experiment=100,sense=['s1','s2']):
    exist_solution = 0
    Qwin_time = 0
    action_time = 0
    P_nodes = 0
    P_edges = 0
    BTS_nodes = 0
    BTS_edges = 0
    Mq_nodes = 0
    Mq_edges = 0

    for i in range(num_experiment):
        print(i)
        A = extract_automaton('.\\automaton','1.txt')
        # showAutomaton(A,name='test')
        # LTS = generation_LTS(num=num,ndetermin=ndetermin,num_observation=num_observation,p_observation=p_observation,num_label=random.randint(4,12),sense=sense)
        LTS = generation_LTS(num=num,ndetermin=ndetermin,num_label=num_label,num_observation=num_observation,p_observation=p_observation,sense=sense)
        # showLTS(LTS,name='test')
        print("LTS generation finish")

        P = product(A,LTS,sense=sense)
        # showProduct(P,name='test')
        print("product system generation finish")

        start1 = time.time()
        BTS,init_b = generation_BTS(P,sense=sense)
        print("generation belief system finish")
        if len(BTS.nodes) < num[0]*num[1]:
            i = i - 1
            continue
        # print("BTS:",BTS)
        # q = random.choice(list(BTS.nodes))
        # Mq, MqF = generation_ATS(q,BTS,P)
        # print(1,BTS)
        Qwin, dict = winningregion_construction(P,BTS,sense=sense)
        print("generation winning region finish")
        end1 = time.time()
        time1 = end1 - start1
        Qwin_time = Qwin_time + time1
        BTS_edges = BTS_edges + len(BTS.edges)
        BTS_nodes = BTS_nodes + len(BTS.nodes)
        P_edges = P_edges + len(P.edges)
        P_nodes = P_nodes + len(P.nodes)

        if len(Qwin) > 0 and init_b in Qwin:
            exist_solution = exist_solution + 1
            # q = max_Mq(Qwin,dict)
            q = random.choice(Qwin)
            # q = init_b

            start2 = time.time()
            Mq,MqF,Mq_t_d = dict[q]
            m = generation_mq0(q,P)
            control_generation(m,Qwin,Mq,MqF,Mq_t_d,sense=sense)
            end2 = time.time()
            print("Mq: ",Mq)
            Mq_edges = Mq_edges + len(Mq.edges)
            Mq_nodes = Mq_nodes + len(Mq.nodes)
            time2 = end2 - start2
            action_time = action_time + time2
        else:
            print("no solution")
    
    avg_Qwin_time = Qwin_time/num_experiment
    avg_action_time = action_time/exist_solution
    Mq_nodes = Mq_nodes/exist_solution
    Mq_edges = Mq_edges/exist_solution
    BTS_nodes = BTS_nodes/num_experiment
    BTS_edges = BTS_edges/num_experiment
    P_nodes = P_nodes/num_experiment
    P_edges = P_edges/num_experiment
    print("average winning region construction time:", avg_Qwin_time)
    print("average strategy generation time:", avg_action_time)
    print("P: nodes-", P_nodes, " edges-", P_edges)
    print("BTS: nodes-", BTS_nodes, " edges-", BTS_edges)
    print("Mq: nodes-", Mq_nodes, " edges-", Mq_edges)
    print("theta: ", exist_solution/num_experiment)

main(num=[6,6],ndetermin=15,num_observation=6,num_label=9,num_experiment=1,sense=['s1','s2'])
# main()