from model.model import Model

mymodel = Model()

# 1. prendo il genere Rock come oggetto
generi = mymodel.getAllGeneri()
rock = None

for g in generi:
    if g.Name == "Rock":
        rock = g
        break

print("Genere scelto:", rock)

# 2. creo il grafo
mymodel.creaGrafo(rock)

n, m = mymodel.getGrafoDetails()
print(f"Grafo creato: {n} nodi, {m} archi")

# 3. stampo qualche arco per controllo
print("\nPrimi archi:")
for u, v in list(mymodel._grafo.edges)[:10]:
    peso = mymodel._grafo[u][v]["weight"]
    print(f"{u} -> {v} | peso: {peso}")

# 4. cerco AC/DC come oggetto
artista = None

for a in mymodel.getNodi():
    if a.Name == "AC/DC":
        artista = a
        break

print("\nArtista scelto:", artista)

# 5. controllo archi uscenti da AC/DC
print("\nArchi uscenti da AC/DC:")
for v in mymodel._grafo.successors(artista):
    peso = mymodel._grafo[artista][v]["weight"]
    print(f"{artista} -> {v} | peso: {peso}")

# 6. test cammino
cammino, score = mymodel.getPath(artista)

print("\nCammino trovato:")
for i in range(len(cammino) - 1):
    peso = mymodel.getPesoArco(cammino[i], cammino[i + 1])
    print(f"{cammino[i]} -> {cammino[i+1]} | peso: {peso}")

# 7. controllo successori dei successori di AC/DC
print("\nSuccessori dei successori di AC/DC:")

for v in mymodel._grafo.successors(artista):
    peso1 = mymodel._grafo[artista][v]["weight"]

    print(f"\nDa {artista} -> {v} | peso precedente: {peso1}")

    for x in mymodel._grafo.successors(v):
        peso2 = mymodel._grafo[v][x]["weight"]

        if peso2 > peso1:
            print(f"  POSSIBILE: {v} -> {x} | peso: {peso2}")

print("Score:", score)