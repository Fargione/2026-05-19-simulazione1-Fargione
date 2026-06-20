import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genre = None
        self._art = None

    def fillDDGenre(self):
        for i in self._model.getAllGenres():
            self._view._ddGenre.options.append(ft.dropdown.Option(key=i, data=i, on_click=self._genChoice))
        self._view.update_page()

    def _genChoice(self,e):
        self._genre = e.control.data
        print(f"Hai scelto il genere {self._genre}")

    def handleCreaGrafo(self,e):
        if self._genre is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire uno stile!", color="red"))
            self._view.update_page()
            return
        self._model.buildGrafo(self._genre)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato: ", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodes()} ", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumEdges()} ", color="green"))
        self._view.update_page()
        art, quan = self._model.bestInfluenza()
        self._view.txt_result.controls.append(
            ft.Text(f"Artista più influente: {art}, con influenza: {quan} ", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Top 5 archi: ", color="green"))
        self._view.update_page()
        archi = self._model.getTopArchi()
        for i in archi:
            self._view.txt_result.controls.append(
                ft.Text(f"{i[0].Name} - > {i[1].Name} : {i[2]['weight']}", color="green"))
        self.fillDDArtist()
        self._view.update_page()

    def fillDDArtist(self):
        for i in self._model._grafo.nodes:
            self._view._ddArtist.options.append(ft.dropdown.Option(key=i.Name, data=i, on_click=self._artChoice))
        self._view.update_page()

    def _artChoice(self,e):
        self._art = e.control.data
        print(f"Hai scelto l'artista {self._art}")

    def handleCammino(self,e):
        if self._art is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un artista!", color="red"))
            self._view.update_page()
            return
        if self._genre is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire uno stile!", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Il cammino più lungo: {len(self._model.getCammino(self._art))}", color="green"))
        for u in self._model.getCammino(self._art):
            self._view.txt_result.controls.append(
                ft.Text(f"{u}", color="green"))
        self._view.update_page()