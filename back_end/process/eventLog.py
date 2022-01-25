
##############################################################################
############################## Classe EventLog ###############################
##############################################################################
#                                                                            #
# All'interno della classe sono definiti tutti i metodi e le strutture dati  #
# necessari per rilevare pattern all'interno di un event log.                #
#                                                                            #
##############################################################################


class EventLog:


    # Istanzia un oggetto della classe EventLog.
    # Il costruttore non richiede come parametro una lista di patterns,
    # ottenuta ad esempio da rilevamenti precedenti.    


    def __init__(self, patterns=[]):
        
        self.traces = []
        self.event_log = set()
        self.patterns = patterns

    

    # Il metodo aggiunge la traccia passata per parametro al registro degli eventi.

    
    def add(self, trace):

        self.traces.append(trace)
        self.event_log.add(trace.get())



    # Il metodo va a rilevare tutti i pattern presenti all'interno del registro
    # degli eventi. Terminato il rilevamento viene generato il poset contenente
    # tutti gli alfabeti di ripetizione per individuare gli elementi massimali.
    #
    # Per ogni elemento massimale viene definita un astrazione, che andrà a 
    # rimpiazzare i pattern individuati nelle tracce.
    #
    # La funzione richiede come parametri:
    #   - un'istanza della classe EventLog;
    #   - il tipo di pattern da rilevare;
    #   - un valore di soglia delta (serve per stabilire se due pattern sono simili).
    #
    # La sostituzione viene fatta sul posto, il metodo non restituisce, quindi,
    # alcun valore.


    def detect(self, pattern_type, delta=0):

        # Imposta l'event log come variabile di classe della classe pattern_type
        
        pattern_type.event_log = self.event_log

        # Indvidua e sostituisce i pattern presenti all'interno delle tracce presenti nel registro

        for trace in self.traces:
            
            trace.detect(pattern_type,delta)
            self.patterns += trace.patterns

        # Dizionario contenente coppie della forma (elemento_massimale,astrazione)

        elementi_massimali = {}

        # Contatore del numero di astrazioni generate

        counter = 0

        # Scansiona l'intera lista di pattern individuando per ciascuno il corrispondente
        # elemento massimale

        for p1 in self.patterns:

            # Ottiene l'alfabeto delle ripetizioni associato al pattern p1

            maximal_element = p1.getRepeatAlphabet()

            # Confronta il pattern p1 con tutti gli altri pattern della lista
            
            for p2 in self.patterns:

                # Ottiene l'alfabeto delle ripetizioni associato al pattern p2

                elem = p2.getRepeatAlphabet()

                # Se l'alfabeto delle ripetizioni di p2 copre quello di p1,
                # questo viene temporaneamente selezionato come elemento massimale

                if maximal_element.issubset(elem): maximal_element = elem

            # In questa fase vengono generate le astrazioni
            
            # Se l'elemento massimale individuato, non era ancora mai stato trovato (nuovo raggruppamento),
            # viene generata una nuova astrazione (evento della form Ai).
            
            if maximal_element not in elementi_massimali.keys(): 

                # Associa l'astrazione all'elemento massimale
                
                elementi_massimali[maximal_element] = "A"+str(counter)

                # Incrementa il contatore delle astrazioni

                counter += 1
            
            # Associa l'elemento massimale individuato e la corrispondente astrazione al pattern p1

            p1.setMaximalElement(maximal_element,elementi_massimali[maximal_element])
    
    

    # Ridefinisce il metodo __iter__ in modo da rendere gli oggetti
    # della classe EventLog iterabili. Iterando un oggetto della classe EventLog
    # verranno iterate tutte le tracce del registro degli eventi.
    
    
    def __iter__(self):

        self.counter = 0
        return self
            


    # Ridefinisce il metodo __next__ in modo da rendere gli oggetti
    # della classe EventLog iterabili. Iterando un oggetto della classe EventLog
    # verranno iterate tutte le tracce del registro degli eventi.
    
    
    def __next__(self):

        if self.counter < len(self.traces):

            self.counter += 1

            return self.traces[self.counter - 1]
        
        else: raise StopIteration