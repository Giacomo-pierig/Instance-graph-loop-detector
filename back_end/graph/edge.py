
##############################################################################
################################# Classe Edge ################################
##############################################################################
#                                                                            #
# All'interno della classe è definita la struttura dati utilizzata per       # 
# rappresentare gli archi di un grafo.                                       #
#                                                                            #
##############################################################################


from .node import Node

class Edge:


    # Istanzia un oggetto della classe Edge.
    # Il costruttore richiede come parametro i due estremi dell'arco.


    def __init__(self,node1,node2):

        if not isinstance(node1,Node) or not isinstance(node2,Node): raise TypeError("Nodes of an edge must be instances of Node")

        self.nodes = (node1,node2)
    


    # Il metodo esegue il parsing di una rappresentazione in stringa di un arco, restituendo
    # come risultato una tupla contenente i due estremi dell'arco.


    def parse(string):

        edge = string.replace("e ","").replace("\n","").replace("__"," ").split(" ")

        if len(edge) == 4: return Node(edge[0],edge[2]),Node(edge[1],edge[3])

        else: return None
        


    # Definisce il criterio per stabilire se un arco è uguale a un altro


    def __eq__(self,other): return isinstance(other,Edge) and self.nodes[0] == other.nodi[0] and self.nodes[1] == other.nodi[1]
    
    

    # Definisce il criterio per eseguire il cast di un arco in stringa

    
    def __str__(self): return "e "+str(self.nodes[0].id)+" "+str(self.nodes[1].id)+" "+str(self.nodes[0].label)+"__"+str(self.nodes[1].label)