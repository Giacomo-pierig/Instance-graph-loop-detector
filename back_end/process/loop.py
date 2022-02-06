
######################################################################
########################### Classe Loop ##############################
######################################################################
#                                                                    #
# All'interno della classe sono definiti tutti i metodi necessari    #
# per il rilevamento di cicli all'interno di tracce.                 #
#                                                                    #
# La classe eredita da Pattern.                                      #
#                                                                    #
######################################################################


from .pattern import Pattern


class Loop(Pattern):


    # Il metodo permette di modificare il numero di ripetizioni associate
    # al tandem array (n° iterazioni del ciclo).
    # 
    # Il metodo richiede come parametri:
    #   - un'istanza della classe Loop;
    #   - il nuovo numero di ripetizioni del tandem array.
    #
    # Non viene restituito alcun valore.
    
    def setNumberOfRepetitions(self, k):

        self.k = k
        self.end = self.i + (self.repeat_length*self.k) - 1
    


    # Il metodo restituisce True se l'oggetto a cui ci si riferisce è un tandem array
    # di tipo primitivo (la ripetizione ad esso associata non è un tandem array).
    # 
    # Il metodo richiede come parametro un'istanza della classe Loop.


    def isPrimitiveTandemArray(self):

        # Controlla se la repeat associata all'istanza è un tandem array

        return not Loop.isTandemArray(self.repeat)
    


    # Il metodo verifica se la traccia passata per parametro è un tandem array.
    # Una traccia T è un tandem array se può essere espressa nella forma sc*k, 
    # cioè T è data da k ripetizioni di una sottostringa sc). 
    # 
    # Si può dare una definizione più generale di tandem array, in cui le k 
    # ripetizioni che costituiscono la traccia non devono essere necessariamente 
    # uguali tra di loro, ma è sufficiente che siano simili. In questo caso si parla 
    # di tandem array approssimati. 
    # 
    # Come criterio di similarità viene usata la distanza di Levenshtein. 
    # Se la distanza di edit tra due sottostringhe è minore di una certa soglia, 
    # queste sono considerate simili.
    # 
    # Il metodo richiede come parametri:
    #   - la traccia T da analizzare;
    #   - un valore di soglia delta. 
    # 
    # Come valore, nel caso la traccia sia un tandem array, viene restituita una tupla 
    # contenente la sottostringa ripetuta e il numero di ripetizioni. 
    # 
    # Altrimenti, viene restituita la tupla (None,0)


    def isTandemArray(T,delta):

        # Lunghezza della traccia (numero di eventi presenti)

        n = len(T)

        # Per verificare se la traccia sia o meno un tandem array, 
        # si va a verificare se è costituita da k ripetizioni di una stessa sottostringa. 
        # 
        # La verifica viene svolta per sottostringhe di diversa lunghezza (da 1 a n/2). 
        # I due casi limite sono:
        #   - T è un tandem array in cui la sottostringa base viene ripetuta n volte (l=1)
        #   - T è un tandem array in cui la sottostringa base viene ripetuta 2 volte (l=n/2)

        for l in range(1, n//2+1):

            # Se n non è divisibile per l, non può esistere nessuna ripetizione di lunghezza l (è inutile cercare)

            if not n%l:

                # k è il numero di ripetizioni della sottostringa

                k = n//l

                # La traccia T viene scomposta in k sottostringhe per poi verificare se sono simili tra loro

                for i in range(k):

                    # Si seleziona una sottostringa sc

                    sc = T[i*l:(i+1)*l]

                    # Verifica se la traccia è un tandem array con ripetizione sc

                    if Loop.isTandemArrayWithRepeatSc(T,sc,delta): return (sc,k)
        
        return (None,0)
    


    # Il metodo verifica se la traccia passata per parametro è un tandem array con ripetizione sc.
    # 
    # Il metodo richiede come parametri:
    #   - la traccia T da analizzare;
    #   - una sottostringa sc;
    #   - un valore di soglia delta. 
    # 
    # Il metodo restituisce True se la traccia T è un tandem array con ripetizione sc, False altrimenti.
    
    
    def isTandemArrayWithRepeatSc(T,sc,delta):

        # Lunghezza della sottostringa base (primitive tandem repeat type)

        l = len(sc)

        # Divide T in k sottostringhe di uguale lunghezza e verifica se sono simili a sc.

        for i in range(len(T)//l):

            if not Loop.isSimilar(T[i*l:(i+1)*l],sc,delta): return False
        
        return True



    # Il metodo va a rilevare tutti i tandem array contenuti all'interno di una traccia.
    # 
    # Il metodo richiede come parametri:
    #   - la traccia T da analizzare;
    #   - un valore di soglia delta. 
    # 
    # Il metodo restituisce una lista di tandem array.
    

    def detect(T,delta):

        # Lista che andrà a contenere tutti i tandem array rilevati

        tandem_arrays = []

        # Lunghezza della traccia

        n = len(T)

        # Ad ogni iterazione del ciclo vengo rilevati tutti i tandem array di lunghezza l.
        # Non è possibile avere tandem array di lunghezza unitaria.

        for l in range(2,n+1):

            # La traccia viene scandita dall'inizio alla fine, controllando per ogni sottostringa di 
            # lunghezza l se questa sia o meno un tandem array.
            #
            # In caso positivo viene istanziato un oggetto della classe Loop e viene aggiunto alla lista
            # dei tandem array rilevati.

            for i in range(n-l+1):

                alpha,k = Loop.isTandemArray(T[i:i+l],delta)

                if k: tandem_arrays.append(Loop(i,alpha,k))
        
        # La lista dei tandem array viene ordinata in base alla posizione in cui inizia la sottostringa. 
        # In caso di due tandem array con stessa posizione iniziale, viene messo prima quello più lungo.

        tandem_arrays.sort()

        # La lista viene filtrata eliminando i tandem array sovrapposti

        return Loop.filter(tandem_arrays)



    # Il metodo filtra la lista di tandem array passata per parametro, scartando
    # quelli che si sovrappongono.
    # 
    # Il metodo richiede come parametro la lista di tandem array da filtrare.
    # 
    # Il metodo restituisce la lista di tandem array filtrata.
    

    def filter(tandem_arrays):

        # Lista che andrà a contenere tutti i tandem array filtrati

        filtered_tandem_arrays = []

        # Riferimento al tandem array precedente (inizializzato a None)

        prec = None

        # Viene scandita tutta la lista scartando i tandem array sovrapposti

        for tandem_array in tandem_arrays:

            # Verifica se il tandem array corrente è contenuto in quello precedente

            if not tandem_array.isContained(prec):

                # Verifica se i due tandem array sono sovrapposti

                if tandem_array.isOverlapped(prec):

                    # Numero di ripetizioni aggiorn ato

                    k = (tandem_array.i - prec.i) // tandem_array.repeat_length

                    # Se la repeat associata al tandem array corrente è più lunga
                    # di quella associata al precedente, quest'ultimo viene accorciato. 
                    # 
                    # Se accorciando il tandem array sio ottiene un valore di k minore di 2,
                    # il tandem array non viene accorciato.

                    if prec.repeat_length < tandem_array.repeat_length and k > 1:
                        
                        # Aggiorna il numero di ripetizioni del tandem array precedente

                        prec.setNumberOfRepetitions(k)

                        # Aggiunge il tandem array corrente alla lista dei pattern filtrati

                        filtered_tandem_arrays.append(tandem_array)

                        # Aggiorna il riferimento al tandem array precedente

                        prec = tandem_array
                else:

                    # Se i due tandem array non sono sovrapposti, 
                    # quello corrente viene aggiunto alla lista dei pattern filtrati

                    filtered_tandem_arrays.append(tandem_array)

                    # Aggiorna il riferimento al tandem array precedente

                    prec = tandem_array
        
        return filtered_tandem_arrays



    # Ridefinisce il metodo __iter__ in modo da rendere gli oggetti
    # della classe Loop iterabili. Iterando un oggetto della classe Loop
    # verrà iterata la tandem repeat type ad esso associata.
    

    def __iter__(self):

        self.counter = 0
        
        return self
    


    # Ridefinisce il metodo __next__ in modo da rendere gli oggetti
    # della classe Loop iterabili. Iterando un oggetto della classe Loop
    # verrà iterata la tandem repeat type ad esso associata.
    
    
    def __next__(self):

        events = ("BEGIN",) + self.repeat + ("END",)

        if self.counter < len(events):

            self.counter += 1

            return events[self.counter - 1]
        
        else: raise StopIteration