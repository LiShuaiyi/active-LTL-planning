from networkx.classes.digraph import DiGraph
from utility import action_sense_pair


def m2q(m):           # return the corresponding belief state of augmented state m, \delta(m) in paper
    ms = m[0]
    mx = m[1]

    q = []
    qs = ms
    qx = []
    q.append(qs)
    for item in mx:
        qx.append(item[0])
    q.append(tuple(qx))
    return tuple(q)

def generation_mq0(q,P):
    ms0 = q[0]          # mq0 = (ms0,mx0=((product state 1, 1),(product state 2, 0),...))
    qx0 = list(q[1])
    mx0 = []
    for state in qx0:
        tmp = []
        tmp.append(state)
        # if P.nodes[state]['accept'] == True:
        #     tmp.append(1)
        # else:
        #     tmp.append(0)
        tmp.append(0)
        mx0.append(tuple(tmp))
    mq0 = []
    mq0.append(ms0)
    mq0.append(tuple(mx0))
    mq0 = tuple(mq0)
    return mq0

def augmented_transition(m,P,a,s):
    mx = m[1]
    tmp = {}
    mx_succ = []
    m_succ = []
    for item in mx:
        (state,flg) = item
        for next_state in P.succ[state]:
            if P.edges[state,next_state]["action"] == a:
                if flg == 0 and P.nodes[next_state]['accept'] == False:
                    mx_succ.append((next_state,0)) 
                else:
                    mx_succ.append((next_state,1)) 
    mx_succ = list(set(mx_succ))
    if len(mx_succ) > 0:
        for item in mx_succ:      # construct the dictionary for mx_succ: key is the observation of sensing action a, value is the set of product state and flag pairs
            (state,flg) = item
            obs = P.nodes[state][s]
            tmp[obs] = []
        for item in mx_succ:
            (state,flg) = item
            obs = P.nodes[state][s]
            tmp[obs].append(item)
        for o in tmp.keys():
            m_next = []
            m_next.append(s)
            m_next.append(tuple(tmp[o]))
            m_succ.append(tuple(m_next))
        # print(belief_succ)
        return m_succ
    else: 
        return mx_succ       
    

def generation_ATS(q,BTS,P,action=['up','down','left','right'],sense=['s1','s2']):
    ATS = DiGraph()
    MqF = []

    mq0 = generation_mq0(q,P)
            
    queue = []
    queue.append(mq0)
    finish = []
    as_pair = action_sense_pair(action,sense)

    while len(queue) > 0:
        m = queue[0]
        del queue[0]
        ms = m[0]
        mx = m[1]
        
        if m not in finish:
            flg_acpt = True         # if m is accepting augmented state, then flg_acpt is true
            for item in mx:
                if item[1] == 0:
                    flg_acpt = False
            if flg_acpt:            # if m is accepting augmented state, then no further transition
                ATS.add_node(m,accept=True)
                MqF.append(m)
                finish.append(m)
            else:
                ATS.add_node(m,accept=False)
                finish.append(m)
                for (a,s) in as_pair:
                    succ = augmented_transition(m,P,a,s)
                    if len(succ) > 0:
                        queue = queue + succ
                        for next_m in succ:
                            ATS.add_edge(m,next_m,action=(a,s))
                    else:
                        continue

    
    # print(len(finish))
    # for m in ATS.nodes:
    #     if ATS.nodes[m]['accept']:
            # print(m)
    # print(ATS.nodes)

    return ATS, MqF

def R2m(Mq,R):       # transfer belief region R into set of augmented states m in ATS Mq (the function Mq in the paper)
    s = []
    for m in Mq.nodes:
        if m2q(m) in R:
            s.append(m)
    s = list(set(s))
    return s