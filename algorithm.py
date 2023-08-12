from ATS import generation_ATS,R2m,generation_mq0
from utility import action_sense_pair

def trans_dict(TS,action=['up','down','left','right']):
    t_d = {}
    for state in TS.nodes:
        t_d[state] = {}
        for a in action:
            t_d[state][a] = []
    for edge in TS.edges:
        start = edge[0]
        end = edge[1]
        a = TS.edges[edge]['action']
        t_d[start][a].append(end)
    return t_d

def Cpre(states,t_d,action=['up','down','left','right']):       # t_d is trans_dict
    cpre = []
    for state in t_d.keys():
        for a in action:
            if len(t_d[state][a]) > 0:
                flg = True
                for next_state in t_d[state][a]:
                    if next_state not in states:
                        flg = False
                if flg:
                    cpre.append(state)
                    break
    return cpre

# def Apre(states,t_d,action=['up','down','left','right']):
#     apre = []
#     for state in t_d.keys():
#         flg1 = True     # flg1: if state is in apre
#         for a in action:
#             if len(t_d[state][a]) > 0:
#                 flg2 = True     # flg2: successor of action a all not in given states
#                 for next_state in t_d[state][a]:
#                     if next_state in states:
#                         flg2 = False
#                 if flg2:
#                     flg1 = False
#                     break
#         if flg1:
#             apre.append(state)
#         else:
#             continue
#     return apre

def Attr(states,t_d,action=['up','down','left','right']):
    attractors = []
    attractors.append(states)
    num = len(list(t_d.keys()))
    l = 0       # len(attractor)-1
    while True:
        tmp = attractors[l] + Cpre(attractors[l],t_d,action)
        attractors.append(list(set(tmp))) 
        l = l+1
        if len(attractors[l]) == num or len(attractors[l]) == len(attractors[l-1]):
            break
    attractor = attractors[l]
    return attractor, attractors

# def Avoid(states,t_d,action=['up','down','left','right']):
#     avoid = []
#     avoid.append(states)
#     num = len(list(t_d.keys()))
#     l = 0       # len(attractor)-1
#     while True:
#         tmp = avoid[l] + Apre(avoid[l],t_d,action)
#         avoid.append(list(set(tmp))) 
#         l = l+1
#         if len(avoid[l]) == num or len(avoid[l]) == len(avoid[l-1]):
#             break
#     return avoid[l]


def val(q,P,Mq,MqF,R,Mq_t_d,pair):
    mq0 = generation_mq0(q,P)
    if mq0 in Attr(list(set(MqF)&set(R2m(Mq,R))),Mq_t_d,pair)[0]:
        return True
    else:
        return False

# R = random.choices(list(BTS.nodes),k=5)
# print(val(q,P,Mq,MqF,R,Mq_t_d,as_pair))

# td = trans_dict(LTS)
# print(td)
# cpre = Cpre([(2,2),(1,1),(0,0)],t_d=td)
# print(cpre)
# attr = Attr([(2,2),(1,1),(0,0)],td)
# print(attr)
# apre = Apre([(2,2),(1,1),(0,0)],t_d=td)
# print(apre)

def winningregion_construction(P,BTS,action=['up','down','left','right'],sense=['s1','s2']):
    dict = {}
    pair = action_sense_pair(action,sense)
    n = 0
    l = len(BTS.nodes)
    for q in BTS.nodes:
        if BTS.nodes[q]['init']:
            q_init = q
        Mq, MqF = generation_ATS(q,BTS,P,sense=sense)
        Mq_t_d = trans_dict(Mq,pair)
        dict[q] = [Mq,MqF,Mq_t_d]
        n = n+1
        print("generation ATS:", n, "/", l)

    R = []
    for q in BTS.nodes:
        if BTS.nodes[q]['init'] or BTS.nodes[q]['accept']:
            R.append(q)
    print("len(R): ",len(R))
    while True:
        tmp = []
        for q in R:
            Mq = dict[q][0]
            MqF = dict[q][1]
            Mq_t_d = dict[q][2]
            if val(q,P,Mq,MqF,R,Mq_t_d,pair):
                tmp.append(q)
        if len(tmp) == len(R):
            break
        else:
            R = tmp
    print("winning region construction finish, Qwin: ", len(R))
    return R, dict

def control_generation(m,Q_win,Mq,MqF,Mq_t_d,action=['up','down','left','right'],sense=['s1','s2']):
    pair = action_sense_pair(action,sense)
    # Mq_t_d = trans_dict(Mq,pair)
    attractors = Attr(list(set(MqF)&set(R2m(Mq,Q_win))),Mq_t_d,pair)[1]
    flg = False
    for i in range(len(attractors)-1):
        if m not in attractors[i] and m in attractors[i+1]:
            for p in pair:
                if len(Mq_t_d[m][p]) > 0 and set(Mq_t_d[m][p]).issubset(attractors[i]):
                    flg = True
                    # print(p)
                    return p
    if flg:
        print("strategy generation fail")
        return 0
        
