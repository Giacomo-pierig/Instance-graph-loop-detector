
from sys import argv

from back_end.graph import IgGraph
from front_end.app import App
from front_end.plot import Plot




if len(argv) == 1:

    # Istanzia un oggetto della classe App

    app = App()

    # Avvia l'applicazione

    app.start()

else:

    # Istanzia un grafo vuoto

    graph = IgGraph()

    # Legge il file, aggiungendo nodi e archi in esso definiti al grafo

    graph.read(argv[2])

    match argv[1]:

        case "detect":

            # Individua i cicli all'interno del grafo ed elimina le attività ripetuta

            new_graph,patterns = graph.detect(unpack=True)

            # Salva il risultato del rilevamento su file

            new_graph.exportAsPNML(argv[2].split("/")[-1].replace(".g",""),argv[3])
        
        case "show":

            Plot.show(argv[2],graph)

            input()

            Plot.close()
