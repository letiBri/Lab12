import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._bestPath = []
        self._bestScore = 0

    def buildGraph(self, country, anno):
        self._graph.clear()
        nodes = DAO.getAllRetailers(country)
        self._graph.add_nodes_from(nodes)
        print(len(self._graph.nodes))

        for n1 in self._graph.nodes:
            for n2 in self._graph.nodes:
                if n1 != n2:
                    peso = DAO.getPesi(n1, n2, anno)
                    if peso[0] > 0:
                        self._graph.add_edge(n1, n2, weight=peso[0])
        print(len(self._graph.edges))
        return len(self._graph.nodes), len(self._graph.edges)

    def calcolaVolume(self):
        volumi = {}
        for n in self._graph.nodes():
            peso = 0
            vicini = self._graph.neighbors(n)
            for vicino in vicini:
                # print(self._graph[n][vicino]["weight"])
                peso += self._graph[n][vicino]["weight"]
            volumi[n.Retailer_name] = peso
        sortato = sorted(volumi.items(), key=lambda x: x[1], reverse=True)
        return dict(sortato)

    def getPercorso(self, numArchi):
        self._bestScore = 0
        self._bestPath = []  # voglio una lista di tuple con (n1, n2, peso), (n2, n3, peso) ...
        parziale = []
        for start in self._graph.nodes:
            self._ricorsione(parziale, numArchi, start, [start])
        return self._bestScore, self._bestPath

    def _ricorsione(self, parziale, numArchi, start, visitati):
        # Se il percorso ha almeno un arco, deduco il nodo corrente dall'ultimo arco
        if len(parziale) > 0:
            nodoCorrente = parziale[-1][1]  # nodo a cui sono arrivata
        else:
            nodoCorrente = start  # all'inizio
        # condizione terminale
        if len(parziale) == numArchi:
            if nodoCorrente == start:
                if self.getSommaPesi(parziale) > self._bestScore:
                    self._bestScore = self.getSommaPesi(parziale)
                    self._bestPath = copy.deepcopy(parziale)
        else:
            for vicino in self._graph.neighbors(nodoCorrente):
                if vicino == start and len(parziale) == numArchi - 1:
                    # Ultimo passo: torna al nodo iniziale
                    parziale.append((nodoCorrente, vicino, self._graph[nodoCorrente][vicino]['weight']))
                    self._ricorsione(parziale, numArchi, start, visitati)
                    parziale.pop()
                elif vicino not in visitati:
                    parziale.append((nodoCorrente, vicino, self._graph[nodoCorrente][vicino]['weight']))
                    visitati.append(vicino)
                    self._ricorsione(parziale, numArchi, start, visitati)
                    visitati.remove(vicino)
                    parziale.pop()

    def getSommaPesi(self, parziale):
        pesoTot = 0
        for arco in parziale:
            pesoTot += arco[2]
        return pesoTot









