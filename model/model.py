import copy
from itertools import combinations
import matplotlib.pyplot as plt
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMapArtist = {}
        self._artist = []
        self._popD = {}
        self._bestCammino = []

    def getCammino(self, art):
        self._bestCammino = []
        parziale = [art]
        for i in self._grafo.successors(art):
            parziale.append(i)
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestCammino

    def _ricorsione(self, parziale):
        if len(parziale) > len(self._bestCammino):
            self._bestCammino = copy.deepcopy(parziale)
        for n in self._grafo.successors(parziale[-1]):
           if n not in parziale and self._grafo[parziale[-1]][n]["weight"] > self._grafo [parziale[-2]][parziale[-1]]["weight"]:
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()

    def getAllGenres(self):
        return DAO.getAllGen()

    def getAllPopo(self, genre):
        self._popD = {}
        self._popD = DAO.getAllPopol(genre)
        return self._popD

    def buildGrafo(self, genre):
        self._grafo.clear()

        nodi = self.getAllNodes(genre)
        self._grafo.add_nodes_from(nodi)
        self.getAllPopo(genre)
        self._grafo.clear_edges()

        lista = self.getAllEdges(genre)
        for e,f in lista:
            u = self._idMapArtist[e]
            v = self._idMapArtist[f]
            p1 = self._popD[e]
            p2 = self._popD[f]
            peso = p1 + p2
            if p1 > p2:
                self._grafo.add_edge(u, v, weight=peso)
            elif p2 > p1:
                self._grafo.add_edge(v, u, weight=peso)
            else:
                self._grafo.add_edge(u, v, weight=peso)
                self._grafo.add_edge(v, u, weight=peso)



    def bestInfluenza(self):
        bestNodo = None
        bestValue = -1
        for n in self._grafo.nodes:
            uscenti = sum(
                self._grafo[n][v]["weight"]
                for v in self._grafo.successors(n)
            )
            entranti = sum(
                self._grafo[u][n]["weight"]
                for u in self._grafo.predecessors(n)
            )
            influenza = uscenti - entranti
            if influenza > bestValue:
                bestValue = influenza
                bestNodo = n
        return bestNodo, bestValue

    def getTopArchi(self):
        archi = list(self._grafo.edges(data=True))
        archi.sort(key=lambda x: x[2]["weight"], reverse=True)
        return archi[:5]

    def getAllEdges(self, genre):
        return DAO.getAllEdges(genre)

    def getAllNodes(self, genre):
        self._artist = []
        self._idMapArtist = {}
        self._artist = DAO.getAllNodes(genre)
        for n in self._artist:
            self._idMapArtist[n.ArtistId] = n
        return self._artist

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

