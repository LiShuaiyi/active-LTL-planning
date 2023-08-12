from graphviz import Digraph

class Graph:
    def __init__(self):
        self.dot = Digraph()

    def title(self, str):
        self.dot.graph_attr.update(label=str)

    def node(self, name, label=None, accepting=False):
        num_peripheries = '2' if accepting else '1'
        self.dot.node(name, label, shape='circle', peripheries=num_peripheries)

    def edge(self, src, dst, label):
        self.dot.edge(src, dst, label)

    def show(self,name,form):
        self.dot.render(name,format=form,view=True)

    def save_render(self, path, on_screen):
        self.dot.render(path, view=on_screen)

    def save_dot(self, path):
        self.dot.save(path)

    def __str__(self):
        return str(self.dot)

############################################

def showAutomaton(A,form='jpg',name=None):
    graph = Graph()
    count = 1
    for i in A.nodes:
        if 'init' in i:
            graph.node(i,'init')
        elif 'accept' in i:
            graph.node(i,'acc',True)
        else:
            graph.node(i, str(count))
            count += 1
        for j in A.succ[i]:
            string = A.succ[i][j]['guard']
            if '(' and ')' in string:
                graph.edge(i,j,str(string[1:-1]))
            else:
                graph.edge(i,j, string)
    graph.show(name+'automaton.gv',form)

############################################

def showLTS(LTS,form='jpg',name=None):
    graph = Graph()
    for state in LTS.nodes:
        # print(LTS.nodes[state]["label"])
        if LTS.nodes[state]["init"]:
            graph.node(str(state),label=str(state)+'\n'+LTS.nodes[state]["label"]+'\n'+'init')
        else:
            graph.node(str(state),label=str(state)+'\n'+LTS.nodes[state]["label"])
        for next_state in LTS.succ[state]:
            graph.edge(str(state),str(next_state),LTS.edges[state,next_state]["action"])
    graph.show(name+'LTS.gv',form)

############################################

def showProduct(P,form='jpg',name=None):
    graph = Graph()
    # print(P)
    for state in P.nodes:
        if P.nodes[state]["init"] and 'accept' not in state[1]:
            graph.node(str(state),label=str(state)+'\n'+'init',accepting=False)
        elif P.nodes[state]["init"] and 'accept' in state[1]:
            graph.node(str(state),label=str(state)+'\n'+'init',accepting=True)
        elif not P.nodes[state]["init"] and 'accept' in state[1]:
            graph.node(str(state),accepting=True)
        else: 
            graph.node(str(state),accepting=False)
        for next_state in P.succ[state]:
            graph.edge(str(state),str(next_state),P.edges[state,next_state]["action"])
    graph.show(name+'product.gv',form)

############################################