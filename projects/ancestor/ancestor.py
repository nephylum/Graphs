class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)

def earliest_ancestor(ancestors, starting_node):
    #build graph for traversal
    g = Graph()
    for i in ancestors:
        g.add_vertex(i[0])
        g.add_vertex(i[1])
        #build edges #(reversed in lect)
        g.add_edge(i[1], i[0])
    q = Queue()
    q.enqueue([starting_node])
    max_path = 1
    ea = -1
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        if(len(path) >= max_path and v < ea) or (len(path) > max_path):
            ea = v
            max_path = len(path)
        for next in g.vertices[v]:
            copy = list(path)
            copy.append(next)
            q.enqueue(copy)
    return ea
