
##############################################################################
################################# Classe Node ################################
##############################################################################
#                                                                            #
# All'interno della classe è definita la struttura dati utilizzata per       # 
# rappresentare i nodi di un grafo.                                          #
#                                                                            #
##############################################################################


class Node:


    # Istanzia un oggetto della classe Node.
    # Il costruttore richiede come parametri l'id e l'etichetta del nodo.


    def __init__(self,id,label):

        self.id = int(id)
        self.label = label
        


    # Il metodo esegue il parsing di una rappresentazione in stringa di un nodo, restituendo
    # un oggetto della classe Node.


    def parse(string):

        node = string.replace("v ","").replace("\n","").split(" ")

        if len(node) == 2: return Node(*node)

        else: return None
                


    # Definisce il criterio per calcolare l'hash di un oggetto della classe Node


    def __hash__(self): return hash((self.id,self.label))
            


    # Definisce il criterio per stabilire se un nodo è uguale a un altro


    def __eq__(self,other): return isinstance(other,Node) and self.label == other.label
  
    

    # Definisce il criterio per eseguire il cast di un nodo in stringa

    
    def __str__(self): return "v "+str(self.id)+" "+str(self.label)