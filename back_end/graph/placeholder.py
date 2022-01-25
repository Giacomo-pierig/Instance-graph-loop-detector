
#####################################################################################
################################ Classe Placeholder #################################
#####################################################################################
#                                                                                   #
# Un oggetto della classe Placeholder viene utilizzato per collassare più sequenze  #
# di nodi in un nodo solo.                                                          #
#                                                                                   #
# Eredita dalla classe Node.                                                        #
#                                                                                   #
#####################################################################################


from .node import Node

class Placeholder(Node):


    # Istanzia un oggetto della classe Placeholder.
    # Il costruttore richiede come parametri l'id da associare al placeholder.


    def __init__(self,id): super().__init__(id,frozenset())

    

    # Il metodo aggiunge il percorso passato per parametro all'interno del nodo
    # placeholder.


    def append(self,path): self.label = self.label.union([path])
  
    

    # Definisce il criterio per eseguire il cast di un placeholder in stringa

    
    def __str__(self): return "v "+str(self.id)+" placeholder"