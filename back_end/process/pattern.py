
##############################################################################
################################ Classe Pattern ##############################
##############################################################################
#                                                                            #
# All'interno della classe sono definiti tutti i metodi e le strutture dati  #
# necessarie per eseguire confronti tra due generici pattern (tandem array   #
# o regioni conservative).                                                   #
#                                                                            #
##############################################################################


class Pattern:

    # Inizializza il registro degli eventi (lista di tracce)

    event_log = []

    # Istanzia un oggetto della classe pattern.
    #
    # Il costruttore richiede come parametri:
    #   - un riferimento ad un'istanza della classe (self);
    #   - la posizione in cui inizia il pattern all'interno della traccia;
    #   - la ripetizione associata al pattern (tandem repeat type o maximal repeat);
    #   - il numero di ripetizioni (per le regioni conservative è sempre pari a 1).

    
    def __init__(self,i,repeat,k=1):

        # Posizione in cui inizia il pattern

        self.i = i

        # Repeat associata al pattern

        self.repeat = repeat

        # Lunghezza della repeat

        self.repeat_length = len(self.repeat)

        # Numero di ripetizioni

        self.k = k

        # Posizione in cui termina il pattern

        self.end = self.i + (self.repeat_length*self.k) - 1

        # Elemento massimale del poset in cui è contenuto il pattern.
        # Permette di eseguire astrazioni sul pattern.
        # Viene inizializzato con l'alfabeto delle ripetizioni del pattern.

        self.maximal_element = self.getRepeatAlphabet()

        # Etichetta associata al pattern (viene restituita quando si esegue il cast in stringa)

        self.label = str(repeat)+("*"+str(k) if k > 1 else "")



    # Il metodo calcola la distanza di Levenshtein tra le due tracce passate per parametro.


    def editDistance(a,b):

        # Caso base della ricorsione.
        # Se una delle due tracce è vuota, la distanza di edit è pari alla lunghezza dell'altra traccia.

        if not len(b): return len(a)
        if not len(a): return len(b)

        # Se i pattern in testa alle due tracce sono identici, la distanza di edit sarà pari a quella tra le due code

        if a[0] == b[0]: return Pattern.editDistance(a[1:],b[1:])

        return 1 + min(Pattern.editDistance(a[1:],b), Pattern.editDistance(a,b[1:]), Pattern.editDistance(a[1:],b[1:]))



    # Il metodo verifica se i due pattern passati per parametro sono simili. Il terzo parametro (delta)
    # rappresenta la soglia che permette di discriminare i pattern in base alla distanza di edit.
    #
    # Il metodo restituisce True se i due pattern sono simili (distanza di edit <= delta), False altrimenti.

    
    def isSimilar(si,sc,delta):

        # Se delta == 0, si lavora con pattern esatti.
        # Calcolare la distanza di edit e vedere se è pari a zero sarebbe inutile,
        # basta un banale confronto.
        #
        # È un'ottimizzazione. Il calcolo della distanza di edit può risultare molto oneroso.

        if not delta: return True if si == sc else False

        # Verifica se la distanza di edit è minore o uguale alla soglia

        else: return True if Pattern.editDistance(si,sc) < min(delta,len(si)-1)+1 else False



    # Il metodo restituisce True se i due pattern passati per parametro sono sovrapposti, False altrimenti.
    

    def isOverlapped(self,other):

        return True if other and (other.i <= self.i <= other.end or self.i <= other.i <= self.end) else False


    
    # Il metodo restituisce True se i due pattern passati per parametro sono uno contenuto nell'altro, False altrimenti.

    def isContained(self,other):

        return True if other and (other.i <= self.i and other.end >= self.end) else False


    
    # Il metodo restituisce l'alfabeto delle ripetizioni associato al pattern.
    # L'alfabeto delle ripetizioni è costituito da tutti gli eventi presenti nella
    # ripetizione del pattern.
    #
    # Viene costruita una lista contenente tutti gli eventi presenti nella ripetizione del pattern,
    # poi si eliminano i duplicati. Ciò è equivalente a inserire gli eventi in un frozenset (set immutabile).


    def getRepeatAlphabet(self):

        return frozenset(self.repeat)

    

    # Gli alfabeti delle ripetizioni associati ai pattern rilevati all'interno delle tracce possono essere
    # organizzati all'interno di un poset (insieme parzialmente ordinato).
    #
    # Tra gli alfabeti è possibile definire una relazione di copertura. Un alfabeto è coperto da un altro,
    # se tutti i simboli che esso contiene sono contenuti anche nell'altro.
    #
    # La relazione di copertura permette di raggruppare gli alfabeti, definendo un ordinamento parziale. 
    # Ad ogni gruppo sarà associato un elemento massimale, che copre tutti gli elementi dell'insieme.
    # Gli elementi massimali permettono di definire astrazioni sui pattern.
    #
    # Il metodo considerato permette di associare al pattern un alfabeto di ripetizione massimale.
    #
    # Il metodo richiede come parametri:
    #   - l'elemento massimale del poset;
    #   - l'etichetta dell'astrazione da associare al pattern.
    #
    # La funzione non restituisce nessun valore.


    def setMaximalElement(self,maximal_element,label):

        self.maximal_element = maximal_element
        self.label = label



    # Definisce il criterio per stabilire se un pattern è minore di un altro
    

    def __lt__(self,other):

        return self.end > other.end if self.i == other.i else self.i < other.i
    


    # Definisce il criterio per stabilire se un pattern è uguale a un altro

    def __eq__(self,other):

        return self.maximal_element == other.maximal_element if isinstance(other,Pattern) else False

    

    # Definisce il criterio per calcolare l'hash di un pattern

    
    def __hash__(self):
        
        return hash(self.maximal_element)

    

    # Definisce il criterio per eseguire il cast di un pattern in stringa

    
    def __str__(self):

        return self.label