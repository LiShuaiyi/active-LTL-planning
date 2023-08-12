import os
from networkx.classes.digraph import DiGraph
import random
import networkx as nx
from copy import deepcopy

'''
I WILL REWRITE THESE INTO CLASSES, JUST NOT NOW... orz
'''

class Automaton(object):
    def __init__(self):
        self.A = DiGraph()

############################################

def extract_automaton(lib,file_name):   # extract automaton from file, file_name should be txt format
    A = DiGraph()
    node_list = []
    transition_dict = {}
    count = -1
    with open(os.path.join(lib,file_name), 'r') as f:
        for ann in f.readlines():
            ann = ann.strip('\n').strip(' ') 
            if ann.find('T') == 0 or ann.find('acc') == 0:
                count = count + 1
                tmp = ann.replace(':','')
                node_list.append(tmp)
                transition_dict[node_list[count]] = []
            if count >= 0:
                if ann.find("::") == 0:
                    tmp = ann.replace(":: ",'').split(" -> goto ")
                    transition_dict[node_list[count]].append(tmp)
    
    for start in transition_dict.keys():
        transitions = transition_dict[start]
        for transition in transitions:
            [formula, end] = transition
            A.add_edge(start, end, guard=formula)
    # print(len(A.nodes))
    # print(len(A.edges))    
    return A
# A1 = extract_automaton('.\\automaton','1.txt')
# showAutomaton(A1)

def check_satisfy(true_ap_set,bdd_formula): 
    # set('a') "a&!b"
    # remove space and ()
    tmp = ''
    for ch in bdd_formula:
        if(ch != ' ' and ch != '(' and ch != ')'):
            tmp += ch
    tmp = tmp.replace("&&",'&').replace("||",'|')
    bdd_formula = tmp
    # print(tmp)
    # (... & ..) | (.. &..) | (..&..) 

    # if(bdd_formula == '1'):
    if(bdd_formula == 'true'):
        return True
    formulas = bdd_formula.split('|')
    if(len(formulas) == 1):
        for i in range(len(bdd_formula)):
            if(bdd_formula[i] >= 'a' and bdd_formula[i] <= 'z'):
                if(i > 0 and bdd_formula[i-1] =='!'):
                    if (bdd_formula[i] in true_ap_set): # !a
                        return False
                else:
                    if (bdd_formula[i] not in true_ap_set): # a
                        return False
    else:
        ans = False
        for f in formulas:
            ans = ans or check_satisfy(true_ap_set,f)
        return ans
    return True
# print(check_satisfy('o','!a&!b&!c'))
# print(check_satisfy('a'," ((a) || (c)) "))

############################################

# class LTS(object):        # transfer this to object, maybe later...

def generation_LTS(gridworld=True,num=[4,4],initpos=None,label=['a','b','c','d'],num_label=4,action=None,ndetermin=3,num_observation=2,p_observation=0.2,sense=['s1','s2'],map_input=None,obs_input=None,label_input=None):
    LTS = DiGraph()
    states = []
    trans = []
    # obs_func = {}
    # if map_input != None and obs_input != None and label_input != None:
    #     for [start,a,end] in map_input:
    #         LTS.add_edge(start,end,action=a)
    #     for state in label_input.keys():
    #         LTS.nodes[state]["label"] = label_input[state]
    #     for state in obs_input.keys():
    #         obs_dict = obs_input[state]
    #         for s in obs_dict.keys():
    #             LTS.nodes[state][s] = obs_dict[s]
    #     return LTS

    if map_input != None:
        for [start,a,end] in map_input:
            LTS.add_edge(start,end,action=a)
            trans.append([start,a,end])
            if start not in states:
                states.append(start)
    else:
        if gridworld:       # grid world structure
            # num_state = num[0]*num[1]
            # num_trans = 2*((num[0]-1)*num[1]+(num[1]-1)*num[0])
            action = ['up','down','left','right']
            for x in range(num[0]):     # add state
                for y in range(num[1]):
                    states.append((x,y))
    
            for (x,y) in states:         # add transition
                if (x+1,y) in states:
                    trans.append([(x,y),'right',(x+1,y)])
                    LTS.add_edge((x,y),(x+1,y),action='right')
                if (x-1,y) in states:
                    trans.append([(x,y),'left',(x-1,y)])
                    LTS.add_edge((x,y),(x-1,y),action='left')
                if (x,y+1) in states:
                    trans.append([(x,y),'up',(x,y+1)])
                    LTS.add_edge((x,y),(x,y+1),action='up')
                if (x,y-1) in states:
                    trans.append([(x,y),'down',(x,y-1)])
                    LTS.add_edge((x,y),(x,y-1),action='down')
            
            # print(len(trans))

            ndeter_states = []      # add non deterministic transitions
            cnt = 0
            while cnt < ndetermin:
                ndeter_state = random.choice(states)
                (x,y) = ndeter_state
                states_tmp = []
                flg = True
                while flg:
                    action_tmp = random.choice(action)
                    if action_tmp == 'up':
                        if (x+1,y+1) in states:
                            states_tmp.append((x+1,y+1))
                        if (x-1,y+1) in states:
                            states_tmp.append((x-1,y+1)) 
                    if action_tmp == 'down':
                        if (x+1,y-1) in states:
                            states_tmp.append((x+1,y-1))
                        if (x-1,y-1) in states:
                            states_tmp.append((x-1,y-1))
                    if action_tmp == 'left':
                        if (x-1,y-1) in states:
                            states_tmp.append((x-1,y-1))
                        if (x-1,y+1) in states:
                            states_tmp.append((x-1,y+1))
                    if action_tmp == 'right':
                        if (x+1,y-1) in states:
                            states_tmp.append((x+1,y-1))
                        if (x+1,y+1) in states:
                            states_tmp.append((x+1,y+1)) 
                    if len(states_tmp) > 0:
                        next_tmp = random.choice(states_tmp)
                        if [(x,y),action_tmp,next_tmp] not in trans:
                            trans.append([(x,y),action_tmp,next_tmp])
                            LTS.add_edge((x,y),next_tmp,action=action_tmp)
                            cnt = cnt + 1
                    flg = False
                            
                # if ndeter_state not in ndeter_states:
                #     ndeter_states.append(ndeter_state)
                #     cnt = cnt+1
            #     ndeter_states.append(ndeter_state)
            #     cnt = cnt + 1
            # for (x,y) in ndeter_states:
            #     states_tmp = []
            #     flg = True
            #     while flg:
            #         action_tmp = random.choice(action)
            #         if action_tmp == 'up':
            #             if (x+1,y+1) in states:
            #                 states_tmp.append((x+1,y+1))
            #             if (x-1,y+1) in states:
            #                 states_tmp.append((x-1,y+1)) 
            #         if action_tmp == 'down':
            #             if (x+1,y-1) in states:
            #                 states_tmp.append((x+1,y-1))
            #             if (x-1,y-1) in states:
            #                 states_tmp.append((x-1,y-1))
            #         if action_tmp == 'left':
            #             if (x-1,y-1) in states:
            #                 states_tmp.append((x-1,y-1))
            #             if (x-1,y+1) in states:
            #                 states_tmp.append((x-1,y+1))
            #         if action_tmp == 'right':
            #             if (x+1,y-1) in states:
            #                 states_tmp.append((x+1,y-1))
            #             if (x+1,y+1) in states:
            #                 states_tmp.append((x+1,y+1)) 
            #         if len(states_tmp) > 0:
            #             next_tmp = random.choice(states_tmp)
            #             if [(x,y),action_tmp,next_tmp] not in trans:
            #                 flg = False
            #                 trans.append([(x,y),action_tmp,next_tmp])
            #                 LTS.add_edge((x,y),next_tmp,action=action_tmp)

            # print(len(LTS.edges))

        else:       # random generate graph structure
            num_state = num[0]*num[1]
            num_trans = 2*((num[0]-1)*num[1]+(num[1]-1)*num[0])
            states = list(range(num_state))
            tmp = 0
            num_action = len(action)
            while tmp < num_trans:
                a = action[random.randint(num_action)]
                start = random.randint(num_state)
                end = random.randint(num_state)
                if [start,a,end] not in trans:
                    trans.append([start,a,end])
                    LTS.add_edge(start,end,action=a)
                    tmp = tmp+1
    
    if label_input != None:     # random assign label, the number of states having label is num_label, others' label is 'o'
        for state in states:
            # LTS.add_node(state)
            LTS.nodes[state]["label"] = label_input[state]
    else:
        for state in states:
            # LTS.add_node(state)
            LTS.nodes[state]["label"] = 'o'
        state_with_label = random.sample(states,num_label)
        for i in range(num_label):
            state = state_with_label[i]
            if i < len(label):      # make sure doesnt exist label not assigned to states
                LTS.nodes[state]["label"] = label[i]
            else:
                LTS.nodes[state]["label"] = random.choice(label)
    
    if obs_input != None:       # assign observations
        for state in states:
            obs_dict = obs_input[state]
            for s in obs_dict.keys():
                LTS.nodes[state][s] = obs_dict[s]
    else:
        cnt = 0
        for state in states:        # initially set all states distinguishable
            cnt = cnt + 1
            for s in sense:
                LTS.nodes[state][s] = 'o' + str(cnt)
        mid_states = []     # states in the middle part, having transition in all four directions
        for x in range(1,num[0]):
            for y in range(1,num[1]):
                mid_states.append((x,y))
        # indist_states = random.sample(mid_states,2*num_observation)     # indistinguishable states in pairs
        
        mid_obs = []
        for i in range(num_observation):
            mid_obs.append('o' + str(cnt+1+i))
        for state in mid_states:
            for s in sense:
                LTS.nodes[state][s] = random.choice(mid_obs)
        
        # for i in range(num_observation):
        #     # state1 = indist_states[2*i]
        #     # state2 = indist_states[2*i+1]
        #     state1 = random.choice(mid_states)
        #     state2 = random.choice(mid_states)
        #     s1 = sense[0]
        #     LTS.nodes[state2][s1] = LTS.nodes[state1][s1]       # s1 is the same
        #     for j in range(1,len(sense)):       # s2...sn each have probability p to distinguish states, if sm can distinguish, then sm+1...sn all can distinguish
        #         s = sense[j]
        #         if random.random() > p_observation:
        #             LTS.nodes[state2][s] = LTS.nodes[state1][s]
        #         else:
        #             break

    if initpos == None:     # set initial position, note that the initial position is different from the automaton's initial state (also with the product system's initial state) with the same attribute 'init'
        init = random.choice(states)
        # print(init)
        for state in LTS.nodes:
            if state == init:
                LTS.nodes[state]["init"] = True
            else:
                LTS.nodes[state]["init"] = False
    else:
        for state in LTS.nodes:
            if state == initpos:        # e.g. initpos = (0,0)
                LTS.nodes[state]["init"] = True
            else:
                LTS.nodes[state]["init"] = False
    
    return LTS

############################################

def product(A,LTS,sense=['s1','s2']):
    P = DiGraph()
    for x in LTS.nodes:
        if LTS.nodes[x]["init"]:
            init_LTS = x
    for q in A.nodes:
        if 'init' in q:
            init_A = q

    # product_states = []
    # tmp = []

    Product_nodes = []

    init_product = (init_LTS,init_A)        # determine initial state
    for init_A_next in A.succ[init_A]:
        if check_satisfy(LTS.nodes[init_LTS]["label"],A.edges[init_A,init_A_next]["guard"]):
            init_product = (init_LTS,init_A_next)
    
    for i in LTS.edges:     # all the possible transitions: random choose LTS edge and automaton edge to see if a transition can happen, so this will include many impossible product transitions, which will be cropped later
        for j in A.edges:
            if check_satisfy(LTS.nodes[i[1]]["label"],A.edges[j]["guard"]):
                P.add_edge((i[0],j[0]),(i[1],j[1]),action=LTS.edges[i]["action"])
                if (i[0],j[0]) not in Product_nodes:
                    Product_nodes.append((i[0],j[0]))
                    P.nodes[(i[0],j[0])]["label"] = LTS.nodes[i[0]]["label"]
                    for s in sense:
                        P.nodes[(i[0],j[0])][s] = LTS.nodes[i[0]][s]
                if (i[1],j[1]) not in Product_nodes:
                    Product_nodes.append((i[1],j[1]))
                    P.nodes[(i[1],j[1])]["label"] = LTS.nodes[i[1]]["label"]
                    for s in sense:
                        P.nodes[(i[1],j[1])][s] = LTS.nodes[i[1]][s]    

 
    for state in P.nodes:       # label initial state and accepting states
        if state != init_product:
            P.nodes[state]["init"] = False
        else:
            P.nodes[state]["init"] = True
        if "accept" in state[1]:
            P.nodes[state]["accept"] = True
        else:
            P.nodes[state]["accept"] = False


    states_ = deepcopy(P.nodes())       # crop the transition system
    for state_ in states_:
        if nx.has_path(P,init_product,state_):
            continue
        else:
            P.remove_node(state_)
    # print(P)

    return P

############################################

def action_sense_pair(action=['up','down','left','right'],sense=['s1','s2']):
    as_pair = []
    for a in action:
        for s in sense:
            if (a,s) not in as_pair:
                as_pair.append((a,s))
    return as_pair

############################################

def max_Mq(Qwin,dict):
    max = random.choice(Qwin)
    Mq_max = dict[max][0]
    num = len(Mq_max.nodes)
    for q in Qwin:
        Mq,MqF,Mq_t_d = dict[q]
        if len(Mq.nodes) > num:
            max = q
            num = len(Mq.nodes)
    return max

############################################
