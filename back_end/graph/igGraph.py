
#####################################################################################
################################## Classe IgGraph ###################################
#####################################################################################
#                                                                                   #
# La classe IgGraph definisce la struttura dati utilizzata dall'applicazione per    #
# rappresentare i grafi d'istanza                                                   #
#                                                                                   #
# Eredita dalla classe DiGraph, definita nella libreria esterna NetworkX.           #
#                                                                                   #
#####################################################################################


from networkx import DiGraph

from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.exporter.exporter import apply
from pm4py.objects.petri_net.utils.initial_marking import discover_initial_marking
from pm4py.objects.petri_net.utils.petri_utils import add_place
from pm4py.objects.petri_net.utils.petri_utils import add_transition
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to
from pm4py.objects.petri_net.utils.petri_utils import remove_place

from .placeholder import Placeholder

from .node import Node
from .edge import Edge

from back_end.process import EventLog
from back_end.process import Loop
from back_end.process import Trace



class IgGraph(DiGraph):


    # Restituisce una vista dei nodi iniziali del grafo (sorgenti)


    def startNodes(self): return filter(lambda x: not next(self.predecessors(x),None), self.nodes)

    

    # Restituisce una vista dei nodi finali del grafo (pozzi)


    def endNodes(self): return filter(lambda x: not next(self.successors(x),None), self.nodes)



    # Definisce una vista dei nodi successori del nodo passato per parametro


    def successors(self, n): return filter(lambda x: x.id > n.id,super().successors(n))



    # Definisce una vista dei nodi predecessori del nodo passato per parametro
    

    def predecessors(self, n): return filter(lambda x: x.id < n.id,super().predecessors(n))



    # Il metodo legge e decodifica un file con estensione .g, aggiungendo i nodi e gli archi
    # presenti nel file all'interno del grafo.
    #
    # Il metodo richiede come parametri:
    #   - un'istanza della classe IgGraph;
    #   - il percorso da cui leggere il file.


    def read(self,path):

        # Legge i dati contenuti nel file

        file = open(path, "r")

        try: data = file.readlines()

        except: raise ValueError

        finally: file.close()

        # Esegue il parsing del file aggiungendo gli archi e i nodi definiti al grafo

        for line in data:

            match line[0]:

                case "v": self.add_node(Node.parse(line))

                case "e": self.add_edge(*Edge.parse(line))
    


    # Il metodo scrive su file la lista di tutti i nodi e di tutti gli archi associati
    # all'istanza del grafo passata per parametro.
    #
    # Il metodo richiede come parametri:
    #   - un'istanza della classe IgGraph,
    #   - la directory in cui salvare il grafo;
    #   - il nome con cui salvare il file.


    def save(self,directory,file_name):

        file = open(directory+"/"+file_name,"w")
        try: file.write(str(self))
        finally: file.close()
    


    # Il metodo va a rilevare tutti i pattern presenti all'interno del grafo.
    # Prima vengono analizzati i percorsi di attività in parallelo. Questi vengono
    # considerati alla stregua di tracce. Su di questi si eseguono gli stesi algoritmi di 
    # rilevamento usati per le tracce.
    #
    # Successivamente il grafo viene appiattito, facendo collassare i percorsi paralleli in un
    # unico nodo, per poi applicare l'algoritmo di rilevamento sul percorso ottenuto.
    #
    # Dopo il rilevamento viene ricostruito il grafo contenente le astrazioni.
    #
    # Il metodo richiede come parametri:
    #   - un'istanza della classe IgGraph;
    #   - il tipo di pattern da rilevare;
    #   - un flag (unpack) che indica se rimpiazzare o meno i cicli con un'astrazione;
    #   - una lista di pattern individuati in rilevamenti precedenti;
    #   - un valore di soglia delta, usato per stabilire quando due pattern sono simili.
    #
    # La funzione restituisce un nuovo grafo, dove i pattern sono sostituiti da astrazioni.
    
    
    def detect(self, pattern_type=Loop, unpack=False, patterns=[], delta=0):

        # Genera una copia del grafo

        flatten_graph = self.copy()

        # Crea un nuovo event log

        event_log = EventLog(patterns)

        # Vengono individuati i nodi che hanno grado uscente maggiore di uno, cioè i nodi
        # in cui il grafo d'istanza si dirama in più percorsi parallelli.
        # 
        # Per ciascun nodo si vanno ad individuare tutte le diramazioni. Su ciascuna diramazione
        # viene poi applicato l'algoritmo di rilevamento dei pattern. 

        for node in filter(lambda x: len(list(self.successors(x))) > 1, self.nodes):

            # Inizializza la lista di convergenza.
            # In questa lista vengono aggiunti i nodi in cui terminano
            # le diramazioni.

            convergence_list = []

            # Genera un nodo placeholder in cui far collassare tutte le diramazioni

            placeholder = Placeholder(node.id+1)

            # Ogni diramazione viene percorsa, aggiungendo i nodi attraversati in una traccia

            for curr in self.successors(node):

                # Crea una traccia vuota

                path = Trace()

                # Ogni nodo attraversato viene tolto dal grafo e aggiunto alla traccia

                while len(list(self.predecessors(curr))) == 1:
                    
                    path.add(curr.label)
                    flatten_graph.remove_node(curr)
                    curr = next(self.successors(curr))
                
                # L'ultimo nodo attraversato viene aggiunto alla lista di convergenza
                
                convergence_list.append(curr)

                # Aggiunge la traccia all'interno del placeholder

                placeholder.append(path)

                # Aggiunge la traccia nell'event log

                event_log.add(path)
            
            # Controlla se tutte le diramazioni convergono allo stesso nodo (tutti gli elementi della lista di convergenza sono uguali)
            # Se non c'è convergenza viene lanciata un'eccezione

            if not all(item == convergence_list[0] for item in convergence_list): raise ValueError("Parallel activities paths not converge")

            # Il placeholder viene aggiunto al grafo, rimpiazzando i percorsi paralleli

            flatten_graph.add_edge(node,placeholder)
            flatten_graph.add_edge(placeholder,curr)

        # Ottiene un riferimento alla sorgente del grafo (inizio del percorso)        

        curr = next(flatten_graph.startNodes())

        # Crea una traccia vuota

        path = Trace()

        # Aggiunge i nodi del grafo appiattito all'interno della traccia

        while curr:
            
            path.add(curr.label)
            curr = next(flatten_graph.successors(curr),None)

        # Aggiunge la traccia all'event log

        event_log.add(path)

        # Esegue il rilevamento dei pattern su tutte le tracce dell'event log

        event_log.detect(pattern_type, delta, not unpack)

        # Crea un nuovo grafo vuoto
        
        graph = IgGraph()

        # Ricostruisce il grafo a partire dai percorsi

        graph.addPath(path,unpack=unpack)

        return graph,patterns
    
    

    # Il metodo aggiunge un percorso all'interno di un grafo.
    #
    # Il metodo richiede come parametri:
    #   - un'istanza della classe IgGraph;
    #   - una sequenza di etichette;
    #   - la lista dei predecessori del primo nodi del percorso;
    #   - un flag (unpack) che indica se rimpiazzare o meno i cicli con un'astrazione.
    #
    # La funzione restituisce un nuovo grafo, dove i pattern sono sostituiti da astrazioni.
    
    
    def addPath(self, labels, predecessors=[], unpack=True):

        # Per ogni etichetta presente nella lista viene creato un nodo e collegato col nodo precedente del percordo

        for label in labels:

            match label:

                # Se l'etichetta è un frozenset (sequenza di percorsi), la funzione viene invocata in maniera ricorsiva
                # Questo caso si verifica quando viene scansionato un nodo placeholder

                case x if isinstance(x,frozenset): predecessors = [self.addPath(path,predecessors,unpack) for path in label]
                
                # Se il flag unpack è vero e l'etichetta è un'istanza della classe Loop,
                # l'oggetto della classe Loop viene decompresso ottenendo una sequenza di
                # etichette.
                #
                # Il percorso viene aggiunto al grafo invocando la funzione in maniera ricorsiva.
                # Si aggiunge poi un arco backward, che collega l'ultimo nodo del ciclo col primo.

                case x if isinstance(x,Loop) and unpack:

                    id = self.number_of_nodes()+1
                    
                    curr = self.addPath(label,predecessors, unpack=unpack)
                    
                    self.add_edge(curr,Node(id,next(iter(label))))

                    predecessors = [curr]
                
                # Negli altri casi si aggiunge il nodo al grafo e lo si collega con un arco a
                # quello che lo precede

                case _:

                    curr = Node(self.number_of_nodes()+1,label)
                    
                    self.add_node(curr)

                    for node in predecessors: self.add_edge(node,curr)

                    predecessors = [curr]
        
        return predecessors[-1]
    

    def exportAsPNML(self, title, directory):

        net = PetriNet(title)

        nodes = {}

        i = 0

        for node in self.nodes:
            
            if node.label != "BEGIN" and node.label != "END": nodes[node.id] = add_transition(net,"t"+str(node.id),node.label)
            else:

                nodes[node.id] = add_place(net,"p"+str(i))
                i += 1

        for edge in self.edges:

            node1 = nodes[edge[0].id]
            node2 = nodes[edge[1].id]

            if isinstance(node1,PetriNet.Place) or isinstance(node2,PetriNet.Place):

                if edge[0].label == "END" and edge[1].label == "BEGIN":

                    t = add_transition(net)

                    add_arc_from_to(node1,t,net)
                    add_arc_from_to(t,node2,net)
                
                else: add_arc_from_to(node1,node2,net)

            else:
            
                p = add_place(net,"p"+str(i))
                add_arc_from_to(node1,p,net)
                add_arc_from_to(p,node2,net)
                i += 1
        
        if not isinstance(nodes[1],PetriNet.Place): add_arc_from_to(add_place(net,"start"),nodes[1],net)
        if not isinstance(nodes[len(nodes.keys())],PetriNet.Place): add_arc_from_to(nodes[len(nodes.keys())],add_place(net,"end"),net)

        apply(net,discover_initial_marking(net),directory+"/"+title+".pnml")


    # Definisce il criterio per eseguire il cast di un grafo in stringa

    
    def __str__(self):

        # Genera una stringa vuota

        s = ""

        # Aggiunge alla stringa tutti i nodi del grafo

        for node in self.nodes: s += str(node) + "\n"

        # Lascia una riga vuota tra la lista di nodi e quella degli archi

        s += "\n"

        # Aggiunge alla stringa tutti gli archi del grafo

        for edge in self.edges: s += str(Edge(*edge)) + "\n"

        return s