class graph:
    def __init__(self,gdict=None):
        self.visual = []
        if gdict is None:
            gdict = []
        self.gdict = gdict     
# Vertices
    def addVertices(self, v):
        if v not in self.gdict:
            self.gdict[v] = []

    def getVertices(self):
        return list(self.gdict.keys())
# Edges
    def addEdge(self, e):
        e = set(e)
        (v1, v2) = tuple(e)
        if v1 in self.gdict:
            self.gdict[v1].append(v2)
        else:
            self.gdict[v1] = [v2]

    def getEdges(self):
        return self.findEdges()
    
    def findEdges(self):
        edge = []
        for vertice in self.gdict:
            for nbr_vertice in self.gdict[vertice]:
                if {vertice,nbr_vertice} not in edge:
                    edge.append({vertice,nbr_vertice})
        return edge
# Loop
    def edges(self, vertice):
        return self.gdict[vertice]
    
    def __iter__(self):
        self._iter_obj = iter(self.gdict)
        return self._iter_obj

if __name__ == '__main__':
    # create initial dict
    subject = { "OOP"  : ["CAL","OOAD"],
                "OOAD" : ["CAL","DSA"],
                }
    g = graph(subject)
    # Show graph vertices
    print(g.getVertices())
    # Show graph edges
    print(g.getEdges())
    # Add vertice
    g.addVertices("Fund")
    g.addVertices("BE")
    # Add edges
    g.addEdge(["BE","OOAD"])
    g.addEdge(["Fund","CAL"])
    print("New vertices: ",g.getVertices())
    print("New Edge: ",g.getEdges())
    # show graph
    for item in g:
        print(f"Edges of {item} is: ",g.edges(item))
