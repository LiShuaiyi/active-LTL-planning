from networkx.classes.digraph import DiGraph
import random
from utility import action_sense_pair

# class BeliefTransitionSystem(object):



def check_belief(b,P,s):        # check if all the product states in belief state b have the same observation under sensing action s
    tmp = random.choice(b)
    flg = True
    for state in b:
        if P.nodes[state][s] != P.nodes[tmp][s]:
            flg = False
    return flg

def belief_transition(q,P,a,s):       # given belief state b_start, action a, sensing action s, find the successor belief states
    states_succ = []
    q_succ = []
    tmp = {}
    qx_start = q[1]
    for state in qx_start:
        for next_state in P.succ[state]:
            if P.edges[state,next_state]["action"] == a and next_state not in states_succ:
                states_succ.append(next_state)      # states_succ is the set of all the successor states of states in b taking action a
    if len(states_succ) > 0:
        for state in states_succ:      # construct the dictionary for states_succ: key is the observation of sensing action a, value is the belief state
            obs = P.nodes[state][s]
            tmp[obs] = []
        for state in states_succ:
            obs = P.nodes[state][s]
            tmp[obs].append(state)
        for o in tmp.keys():
            q_next = []
            q_next.append(s)
            q_next.append(tuple(tmp[o]))
            q_succ.append(tuple(q_next))
        # print(belief_succ)
        return q_succ
    else: 
        return states_succ


def generation_BTS(P,action=['up','down','left','right'],sense=['s1','s2']):
    # each node in BTS is (qs,qx), e.g., qs = 's1', qx = (product state 1 = (TS state, automaton state), product state 2,)
    BTS = DiGraph()
    queue = []

    as_pair = action_sense_pair(action,sense)

    init_b = [sense[0]]
    for state in P.nodes:       # find initial product state, there is one and only one known initial product state
        if P.nodes[state]['init']:
            qx = []
            qx.append(state)
            init_b.append(tuple(qx))
            init_b = tuple(init_b)
            queue.append(init_b)
            BTS.add_node(init_b,init=True)
            if P.nodes[state]['accept']:
                BTS.nodes[init_b]['accept'] = False
    
    finish = []
    while len(queue) > 0: 
        b = queue[0]
        del queue[0]
        if b not in finish:      # add successor of belief state b and the transition into BTS
            if b != init_b:
                BTS.add_node(b,init=False,accept=False)
                bx = b[1]
                for state in bx:  
                    if P.nodes[state]['accept']:
                        BTS.nodes[b]['accept'] = True
                        print('accept')
                        break
            for (a,s) in as_pair:
                succ = belief_transition(b,P,a,s)
                if len(succ) > 0:
                    queue = queue + succ
                    for next_b in succ:
                        BTS.add_edge(b,next_b,action=(a,s))
                else:
                    continue
            finish.append(b)
        else:
            continue
    
    return BTS,init_b

