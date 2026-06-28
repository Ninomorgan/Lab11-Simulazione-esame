import copy
import itertools

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):

      #METODI PER CREARE GRAFICI
        #self._grafo = nx.Graph()  # grafo semplice non diretto
        self._grafo = nx.DiGraph() #grafo diretto

        self._artisti=[] #lista nodi
        self._idMapPopolarity={}


        self._idMapArtisti = None
        self._bestCammino = []
        self._bestScore = 0

    def getAllGeneri(self):
        return DAO.getAllGeneri()

    def getALLArtist(self, genere):
        return DAO.getAllArtist(genere)

    def getAllEdges(self):
        return

    def getClienteArtista(self, genere):
        return DAO.getClienteArtista(genere)

    #complicato
    def creaGrafo(self, genere):
        self._grafo.clear()

        self._artisti = self.getALLArtist(genere)
        self._grafo.add_nodes_from(self._artisti)

        self._idMapArtisti = {a.ArtistId: a for a in self._artisti}

        # mappa
        self._idMapPopolarity = DAO.getPopolarity(genere)

        # 4. acquisti cliente-artista
        acquisti = DAO.getClienteArtista(genere)

        clienti = {}

        for row in acquisti:
            idCliente = row["CustomerId"]
            idArtista = row["ArtistId"]

            if idArtista in self._idMapArtisti:

                artista = self._idMapArtisti[idArtista]

                if idCliente not in clienti:
                    clienti[idCliente] = set()

                clienti[idCliente].add(artista)

        for artistiCliente in clienti.values():

        # archi diretti pesat
            for p1, p2 in itertools.combinations(artistiCliente, 2):

                pop1 = self._idMapPopolarity.get(p1.ArtistId, 0)
                pop2 = self._idMapPopolarity.get(p2.ArtistId, 0)

                if pop1 == 0 or pop2 == 0:
                    continue

                peso = pop1 + pop2

                if pop1 > pop2:  # da 1- a 2
                    self._grafo.add_edge(p1, p2, weight=peso)

                elif pop2 > pop1:  # da 2 a 1
                    self._grafo.add_edge(p2, p1, weight=peso)

                else:  # entrambi uguale
                    self._grafo.add_edge(p1, p2, weight=peso)

                    self._grafo.add_edge(p2, p1, weight=peso)


    #dettagli grafo
    def getNodi(self):
        return self._grafo.nodes()

    def getPesoArco(self, v1, v2):
        return self._grafo[v1][v2]["weight"]

    def getGrafoDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    #uguali
    def getBestArtist(self):
        result = []
        for p in self._grafo.nodes:
            totUscenti = 0
            totEntranti = 0
            score = 0
            for o, d in self._grafo.in_edges(p):  # origine , destinazione
                peso = self._grafo[o][d]['weight']
                totEntranti += peso

            for o, d in self._grafo.out_edges(p):
                peso = self._grafo[o][d]['weight']
                totUscenti += peso

            score = totUscenti - totEntranti
            result.append((p, score))

        result.sort(key=lambda x: x[1], reverse=True)

        return result[0]

    def getBestEdges(self):
        result = []
        for o,d in self._grafo.edges(): #origine , destinazione
            peso= self._grafo[o][d]['weight']
            result.append((o,d,peso))

        result.sort(key=lambda x: x[2], reverse=True) #ordino per il TERZO PARAMETRO x[2]

        return result[:5] #prendo i primi [5]

    #RICORSIONE
    def getPath(self, artista):  # partenza, arrivo, lunghezza max
        self._bestCammino = []
        self._bestScore = 0

        parziale = [artista]

        # ripeto in ricoscrione

        #parto con un nodo quindi aggiujngo i successri
        for v in self._grafo.successors(artista):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestCammino, self._bestScore

    def _ricorsione(self, parziale):
        if self._score(parziale) > self._bestScore:
            self._bestCammino = copy.deepcopy(parziale)
            self._bestScore = self._score(parziale)


        for v in self._grafo.successors(parziale[-1]):
            #    arco deve essere più grande dell'ultimo arco che ho agiunto
            peso = self._grafo[parziale[-1]][v]["weight"]  # arco che sto provando ad aggiungere

            # ultimo arco aggiunto
            if self._grafo[parziale[-2]][parziale[-1]]["weight"] < peso and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def _score(self, parziale):  # UGUALE

        # arrivano nodi e preso il parziale e quellodopo prende il peso e lo somma a score
        score = 0
        for i in range(0, len(parziale) - 1):
            score += self._grafo[parziale[i]][parziale[i + 1]]["weight"]

        return score




