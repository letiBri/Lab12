import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        for i in range(2015, 2019):
            self._view.ddyear.options.append(ft.dropdown.Option(i))

        nazioni = DAO.getAllNazioni()
        nazioni.sort()
        for n in nazioni:
            self._view.ddcountry.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        if self._view.ddyear.value is None:
            self._view.create_alert("Selezionare un anno!")
            self._view.update_page()
            return
        if self._view.ddcountry.value is None:
            self._view.create_alert("Selezionare una nazione!")
            self._view.update_page()
            return
        numNodi, numArchi = self._model.buildGraph(self._view.ddcountry.value, self._view.ddyear.value)
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {numNodi} Numero di archi: {numArchi}"))
        self._view.btn_volume.disabled = False
        self._view.btn_path.disabled = False
        self._view.txtN.disabled = False
        self._view.update_page()

    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        diz = self._model.calcolaVolume()
        for chiave, valore in diz.items():
            self._view.txtOut2.controls.append(ft.Text(f"{chiave} --> {valore}"))
        self._view.update_page()

    def handle_path(self, e):
        self._view.txtOut3.controls.clear()
        if self._view.txtN.value is None or self._view.txtN.value == "":
            self._view.create_alert("Inserire il numero di archi del percorso")
            self._view.update_page()
            return
        try:
            numArchi = int(self._view.txtN.value)
        except ValueError:
            self._view.create_alert("Il valore inserito non è un intero")
            self._view.update_page()
            return
        if numArchi <= 1:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Inserire un valore intero uguale a 2 o superiore")
            self._view.update_page()
            return

        score, path = self._model.getPercorso(numArchi)
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {score}"))
        for p in path:
            self._view.txtOut3.controls.append(ft.Text(f"{p[0].Retailer_name} --> {p[1].Retailer_name}: {p[2]}"))
        self._view.update_page()
