
#####################################################################################
################################### Classe Plot #####################################
#####################################################################################
#                                                                                   #
# La classe Plot definisce tutti i metodi necessari per visualizzare un grafo sullo #
# schermo.                                                                          #
#                                                                                   #
# Il grafo viene visualizzato usando le api fornite dalla libreria networkX.        #
#                                                                                   #
#####################################################################################


from networkx import draw
from networkx import draw_networkx_edges

class Plot:


    # Distanza tra due nodi lungo l'asse x

    DELTA_X = 0.15

    # Distanza tra due nodi lungo l'asse y

    DELTA_Y = 0.26



    # La funzione visualizza sullo schermo il grafo distanza passato per parametro.
    #
    # La funzione richiede come parametri:
    #   - il grafo da visualizzare;
    #   - l'asse in cui tracciare il grafo;
    #   - il titolo della finestra.


    def draw(graph, ax, title):

        # Colori usati nel grafo

        color1 = '#646367'
        color2 = "#EEEEEE"

        # Layout del grafo

        pos = {node: Plot.nodePosition(graph,node) for node in graph.nodes}

        # Lista degli archi backward

        backward_edges = []

        # Lista degli archi forward

        forward_edges = []

        # Lista degli autoanelli

        self_loops = []

        # Classifica gli archi presenti nel grafo

        for edge in graph.edges:

            match edge:

                case x if x[0].id < x[1].id: forward_edges.append(edge)
                
                case x if x[0].id == x[1].id: self_loops.append(edge)

                case x if x[0].id > x[1].id: backward_edges.append(edge)

        # Traccia gli autoanelli all'interno della figura

        draw_networkx_edges(

            graph, 
            pos = pos, 
            edge_color = color1,
            edgelist = self_loops,
            ax = ax

        )

        # Traccia gli archi backward all'interno della figura

        draw_networkx_edges(

            graph, 
            pos = pos, 
            edge_color = color1,
            edgelist = backward_edges,
            connectionstyle = "arc3, rad = -0.9",
            min_target_margin=16,
            ax = ax

        )

        # Traccia il resto del grafo sulla figura

        draw(

            graph, 
            pos = pos, 
            with_labels = True, 
            labels = {nodo: "\n".join(str(nodo).replace("v ","").split(" ")) for nodo in graph.nodes},
            node_color = color2,
            node_size = 1000,
            linewidths = 2,
            edgelist = forward_edges,
            edgecolors = color1,
            edge_color = color1,
            font_size = 8,
            font_family = "Comic Sans MS",
            font_weight = "bold",
            font_color = color1,
            ax = ax

        )

        # Imposta il titolo della finestra

        ax.set_title(title, fontname="Comic Sans MS", fontweight="bold")

        # Imposta i limiti degli assi

        ax.set_xlim([-Plot.DELTA_X/3,min(Plot.nodePosition(graph,next(graph.endNodes()))[0]+Plot.DELTA_X/2,Plot.DELTA_X*10)])
        ax.set_ylim([-Plot.DELTA_Y*5/3,Plot.DELTA_Y*5/3])
    


    # La funzione associa ad ogni nodo del grafo una posizione sullo spazio bidimensionale.
    #
    # La funzione richiede come parametri:
    #   - il grafo d'istanza contenente il nodo di cui si vuole cacolare la posizione;
    #   - il nodo di cui si vuole cacolare la posizione.


    def nodePosition(graph, node):

        # La funzione calcola l'ordinata da associare ad un nodo nel caso questo
        # appartenga ad un percorso parallelo all'interno del grafo

        def calculateOrdinate(parallel_nodes):

            n = len(parallel_nodes)
                
            y = parallel_nodes.index(node) - n//2

            return n - 1 if not n % 2 and not y else y

        match len(list(graph.predecessors(node))):

            # Se il nodo è una sorgente, gli viene assegnata ascissa nulla

            case z if not z: return (0,calculateOrdinate(list(graph.startNodes()))*Plot.DELTA_Y)

            # Se il nodo ha un solo predecessore, avrà la stessa ordinata del nodo precedente e sarà
            # posizionato un pò più a destra

            case z if z == 1:

                prec = next(graph.predecessors(node))

                x,y = Plot.nodePosition(graph,prec)
                
                return (x+Plot.DELTA_X,calculateOrdinate(list(graph.successors(prec)))*Plot.DELTA_Y if len(list(graph.successors(prec))) > 1 else y)

            # Se sul nodo convergono più percorsi paralleli (possiede più di un predecessore), viene
            # impostato 0 come valore dell'ordinata. Il nodo sarà spostato un pò più a destra dei precedenti.

            case z if z > 1: return (max(map(lambda x: Plot.nodePosition(graph,x),graph.predecessors(node)),key=lambda x: x[0])[0]+Plot.DELTA_X,0)