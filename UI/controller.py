import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._categorie= None
        self._artisti=None




    def handleCreaGrafo(self,e):
        genere = self._categorie #se uso fill-read metto questo -> non value


        # cotnrollo dei parametri

        if genere is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Seleziona un genere", color="red"))
            self._view.update_page()
            return



        # creo grafo
        self._model.creaGrafo(genere)
        n, m = self._model.getGrafoDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(
            f"Grafo creato correttamente\n"
            f"Numero di nodi: {n} \n"
            f"Numero di archi: {m}"))

        #miglio artista
        bestProd = self._model.getBestArtist()

        self._view.txt_result.controls.append(ft.Text("Artista con maggiore influenza:", color="green"))
        p, score = bestProd
        self._view.txt_result.controls.append(ft.Text(f"{p} --> {score}", ))

        self._view.update_page()

        #top archi
        bestEdges= self._model.getBestEdges()

        self._view.txt_result.controls.append(ft.Text("Top 5 archi", color="green"))
        for o,d, score in bestEdges:
            self._view.txt_result.controls.append(ft.Text(f"{o} --> {d}: {score}"))

        self.fillDDArtist()

        self._view.update_page()

    def handleCammino(self,e):
        artista= self._artisti

        if artista is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Seleziona un artista", color="red"))
            self._view.update_page()
            return

        cammino, score = self._model.getPath(artista)

        self._view.txt_result.controls.clear()

        if len(cammino) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Nessun cammino trovato da {artista} ")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Percorso ottimo da {artista}:")
        )

        #print NODI E PESO
        for i in range(len(cammino) - 1):
            peso = self._model.getPesoArco(cammino[i], cammino[i + 1])
            self._view.txt_result.controls.append(
                ft.Text(f"{cammino[i]} -> {cammino[i + 1]} | peso: {peso}")
            )

        self._view.txt_result.controls.append(
            ft.Text(f"Peso totale: {score}")
        )
        self._view.update_page()

    def fillDDGenre(self):
        generi= self._model.getAllGeneri()
        self._view._ddGenre.options.clear()
        for n in generi:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(
                    text=str(n),
                    data=n,
                    on_click=self.readDDStart
                )
            )
    def readDDStart(self, e):
        if e.control.data is None:
            self._categorie= None
        else:
            self._categorie = e.control.data
        print (f"selezionato genere {self._categorie}")

    def fillDDArtist(self):
        artisti = self._model.getNodi()
        self._view._ddArtist.options.clear()

        for n in artisti:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(
                    text=str(n),
                    data=n,
                    on_click=self.readDDArtist
                )
            )
    def readDDArtist(self,e):
        if e.control.data is None:
            self._artisti= None
        else:
            self._artisti = e.control.data
        print (f"selezionato Artista {self._artisti}")
