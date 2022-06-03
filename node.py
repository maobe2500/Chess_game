import matplotlib.pyplot as plt
import networkx as nx



class Node():
    def __init__(self, name):
        self.name = name
        self.neighbors = []
        self.neighbor = {}
        self.piece = None

    def __str__(self):
        return self.name

class Graph_board():
    def __init__(self, adj):
        self.adj_list = adj

    def add_node(self, node, neighbors):
        self.adj_list[node] = neighbors

        

def create_board_graph():
    adj_list = {}
    pos_list = {}
    rows = '87654321'
    cols = 'abcdefgh'

    # Top middle row and bottom middle row
    for i in range(1, len(cols)-1):
        t_east = Node(cols[i+1] + '8')
        t_west = Node(cols[i-1] + '8')
        t_southeast = Node(cols[i+1] + '7')
        t_southwest = Node(cols[i-1] + '7')
        t_south = Node(cols[i] + '7')
        t_current = Node(cols[i] + '8')
        t_current.neighbors = [t_east, t_west, t_southeast, t_southwest, t_south] 

        t_current.neighbor['e'] = t_east
        t_current.neighbor['w'] = t_west
        t_current.neighbor['se'] = t_southeast
        t_current.neighbor['sw'] = t_southwest
        t_current.neighbor['s'] = t_south
        adj_list[t_current] = t_current.neighbors
        pos_list[t_current] = (i,0)

        b_east = Node(cols[i+1] + '1')
        b_west = Node(cols[i-1] + '1')
        b_northeast = Node(cols[i+1] + '2')
        b_northwest = Node(cols[i-1] + '2')
        b_north = Node(cols[i] + '2')
        b_current = Node(cols[i] + '1')
        b_current.neighbors = [b_east, b_west, b_northeast, b_northwest, b_north] 

        b_current.neighbor['e'] = b_east
        b_current.neighbor['w'] = b_west
        b_current.neighbor['ne'] = b_northeast
        b_current.neighbor['nw'] = b_northwest
        b_current.neighbor['n'] = b_north
        adj_list[b_current] = b_current.neighbors
        pos_list[b_current] = (i,8)

    # Right and left middle column
    for i in range(1, len(rows)-1):
        l_north = Node('a' + rows[i-1])
        l_south = Node('a' + rows[i+1])
        l_northeast = Node('b' + rows[i-1])
        l_southeast = Node('b' + rows[i+1])
        l_east = Node('b' + rows[i])
        l_current = Node('a' + rows[i])
        l_current.neighbors = [l_north, l_northeast, l_east, l_southeast, l_south]

        l_current.neighbor['n'] = l_north
        l_current.neighbor['e'] = l_east
        l_current.neighbor['ne'] = l_northeast
        l_current.neighbor['se'] = l_southeast
        l_current.neighbor['s'] = l_south
        adj_list[l_current] = l_current.neighbors
        pos_list[l_current] = (0,i)


        r_north = Node('h' + rows[i-1])
        r_south = Node('h' + rows[i+1])
        r_northwest = Node('g' + rows[i-1])
        r_west = Node('g' + rows[i])
        r_southwest = Node('g' + rows[i+1])
        r_current = Node('h' + rows[i])
        r_current.neighbors = [r_north, r_northwest, r_west, r_southwest, r_south]

        r_current.neighbor['n'] = r_north
        r_current.neighbor['s'] = r_south
        r_current.neighbor['sw'] = r_southwest
        r_current.neighbor['nw'] = r_northwest
        r_current.neighbor['w'] = r_west
        adj_list[r_current] = r_current.neighbors
        pos_list[r_current] = (8,i)


    # Corners
    current_nw = Node('a8')
    current_nw.neighbors = [Node('a7'),Node('b8'),Node('b7')]
    current_nw.neighbor['s'] = current_nw.neighbors[0]
    current_nw.neighbor['e'] = current_nw.neighbors[1]
    current_nw.neighbor['se'] = current_nw.neighbors[2]
    adj_list[current_nw] = current_nw.neighbors
    pos_list[current_nw] = (0,0)

    current_ne = Node('h8')
    current_ne.neighbors = [Node('h7'),Node('g8'),Node('g7')]
    current_ne.neighbor['s'] = current_ne.neighbors[0]
    current_ne.neighbor['w'] = current_ne.neighbors[1]
    current_ne.neighbor['sw'] = current_ne.neighbors[2]
    adj_list[current_ne] = current_ne.neighbors
    pos_list[current_ne] = (8,0)

    current_se = Node('a1') 
    current_se.neighbors = [Node('a2'),Node('b1'),Node('b2')]
    current_se.neighbor['n'] = current_se.neighbors[0]
    current_se.neighbor['e'] = current_se.neighbors[1]
    current_se.neighbor['ne'] = current_se.neighbors[2]
    adj_list[current_se] = current_se.neighbors
    pos_list[current_se] = (8,8)

    current_sw = Node('h1') 
    current_sw.neighbors = [Node('h2'),Node('g1'),Node('g2')]
    current_sw.neighbor['n'] = current_sw.neighbors[0]
    current_sw.neighbor['w'] = current_sw.neighbors[1]
    current_sw.neighbor['nw'] = current_sw.neighbors[2]
    adj_list[current_sw] = current_sw.neighbors
    pos_list[current_sw] = (0,8)

    # Middle squares
    for j in range(1,len(cols)-1):
        for i in range(1,len(rows)-1):
            current = Node(cols[j] + rows[i])
            east = Node(cols[j] + rows[i+1])
            west = Node(cols[j] + rows[i-1])
            northeast = Node(cols[j-1] + rows[i+1])
            southeast = Node(cols[j+1] + rows[i+1])
            northwest = Node(cols[j+1] + rows[i-1])
            southwest = Node(cols[j-1] + rows[i-1])
            north = Node(cols[j+1] + rows[i])
            south = Node(cols[j-1] + rows[i])
            current.neighbors = [east, west, northeast, northwest, southeast, southwest, north, south]

            current.neighbor['e'] = east
            current.neighbor['w'] = west
            current.neighbor['ne'] = northeast
            current.neighbor['se'] = southeast
            current.neighbor['nw'] = northwest
            current.neighbor['sw'] = southwest
            current.neighbor['n'] = north
            current.neighbor['s'] = south
            adj_list[current] = current.neighbors
            pos_list[current] = (i,j)
            
    return adj_list, pos_list

print('after')

adj_list, pos_list = create_board_graph()
g = Graph_board(adj_list)
g = nx.from_dict_of_lists(g.adj_list)
print(g)
nx.draw_networkx(g, pos=pos_list)
#board, board_pos= create_board_graph(pos=True)
#G = nx.from_dict_of_lists(board)
#print(G)
#nx.draw_networkx(G, pos=board_pos)
plt.show()











