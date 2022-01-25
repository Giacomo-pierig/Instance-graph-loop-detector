
##############################################################################
################################ Classe Trace ################################
##############################################################################
#                                                                            #
# All'interno della classe sono definiti tutti i metodi e le strutture dati  #
# necessari per rilevare pattern all'interno di una traccia.                 #
#                                                                            #
##############################################################################


class Trace:


    # Istanzia un oggetto della classe Trace.
    # Il costruttore non richiede nessun parametro.


    def __init__(self):

        # Inizializza la lista degli eventi presenti nella traccia

        self.events = []

        # Inizializza la lista di pattern presenti nella traccia

        self.patterns = []

    

    # Il metodo aggiunge l'evento passato per parametro alla traccia


    def add(self, event):

        self.events.append(event)


    
    # Il metodo rileva tutti i pattern presenti nella traccia, rimpiazzando
    # le sequenze che costituiscono i pattern con opportune astrazioni.
    #
    # Il metodo richiede come parametri:
    #   - un'istanza della classe trace;
    #   - il tipo di pattern da rilevare;
    #   - un valore di soglia delta (serve per stabilire se due pattern sono simili).

    
    def detect(self, pattern_type, delta):

        # Rileva tutti i pattern contenuti nella traccia

        patterns = pattern_type.detect(tuple(self.events),delta)

        # Controlla se all'interno della traccia è stato rilevato almeno un pattern

        if len(patterns) > 0:

            # Indice degli eventi nella traccia

            i = 0

            # Nuova traccia con i pattern rimpiazzati da astrazioni

            T = []

            # Converte la lista di patterns in iteratore

            patterns = iter(patterns)

            # Seleziona il primo pattern della traccia

            pattern = next(patterns,None)

            # Scansiona tutta la traccia rimpiazzando i pattern con astrazioni.
            # !!! NOTA !!! L'algoritmo funziona, perchè la lista di pattern è ordinata.

            while i < len(self.events):

                # Verifica se il pattern considerato inizia alla posizione i-esima

                if pattern and pattern.i == i:

                    # Aggiunge il pattern alla nuova traccia

                    T.append(pattern)

                    # Aggiunge il pattern alla lista di pattern rilevati nella traccia

                    self.patterns.append(pattern)

                    # Aggiona l'indice della traccia con la posizione corretta

                    i = pattern.end + 1

                    # Seleziona un altro pattern

                    pattern = next(patterns,None)
                
                else:

                    # Aggiunge l'i-esimo evento alla nuova traccia
                    
                    T.append(self.events[i])

                    # Incrementa l'indice della traccia

                    i += 1

            # Aggiorna il riferimento alla traccia

            self.events = T

    

    # Restituisce un riferimento alla lista degli eventi presenti nella traccia
    
    
    def get(self):

        return tuple(self.events)

    

    # Ridefinisce il metodo __iter__ in modo da rendere gli oggetti
    # della classe Trace iterabili. Iterando un oggetto della classe Trace
    # verranno iterati tutti gli eventi presenti nella traccia.
    
    
    def __iter__(self):

        self.counter = 0
        return self
        


    # Ridefinisce il metodo __next__ in modo da rendere gli oggetti
    # della classe Trace iterabili. Iterando un oggetto della classe Trace
    # verranno iterati tutti gli eventi presenti nella traccia.
    
    
    def __next__(self):

        if self.counter < len(self.events):

            self.counter += 1

            return self.events[self.counter - 1]
        
        else: raise StopIteration



    # Definisce il criterio per stabilire se due tracce sono uguali

    
    def __eq__(self, other):

        return self.events == other.events
    
    

    # Definisce il criterio per calcolare l'hash di una traccia

    
    def __hash__(self):
        
        return hash(tuple(self.events))
    
    

    # Definisce il criterio per eseguire il cast di una traccia in stringa

    
    def __str__(self):

        return str(self.events)