
######################################################################
######################### Classe Subprocess ##########################
######################################################################
#                                                                    #
# All'interno della classe sono definiti tutti i metodi necessari    #
# per il rilevamento di sottoprocessi con funzionalità comuni        #
# all'interno di tracce.                                             #
#                                                                    #
# La classe eredita da Pattern.                                      #
#                                                                    #
######################################################################


from .pattern import Pattern


class Subprocess(Pattern):


    # Dimensione minima di un sottoprocesso
    # !!! NOTA !!! sottoprocessi di dimensione minore di MIN_SIZE non saranno rilevati

    MIN_SIZE = 3



    # Viene ridefinito il costruttore della superclasse

    def __init__(self, i, repeat):

        super().__init__(i, repeat)
    


    # Il metodo va a rilevare tutte le regioni di lunghezza compresa tra l_min e l_max 
    # presenti all'interno di un event log.
    # 
    # Il metodo richiede come parametri:
    #   - il registro degli eventi (lista di tracce) dove rilevare le regioni;
    #   - la lunghezza minima delle regioni da rilevare;
    #   - la lunghezza massima delle regioni da rilevare.
    #
    # Viene restituito un set contenente tutte le regioni rilevate.
    # Gli elementi all'interno dei set non sono ordinati e non possono essere ripetuti.


    def findRegions(event_log,l_min,l_max):

        regioni = set()
        
        for traccia in event_log:

            n = len(traccia)

            for l in range(max(0,l_min),min(l_max,n)+1):

                for i in range(n-l+1):
                    
                    regioni.add(tuple(traccia[i:i+l]))

        return regioni



    # Il metodo verifica se la traccia passata per parametro è una regione conservativa.
    # Una sottotraccia T è una regione conservativa se è presente anche in altri punti
    # dell'event log in cui si trova (stessa traccia o altra traccia del registro).
    #
    # Il rilevamento delle regioni conservative permette di individuare insiemi di funzionalità comuni
    # a cui un processo accede durante la sua esecuzione o durante diverse esecuzioni.
    #
    # Queste regioni possono essere astratte come sottoprocessi.
    # 
    # Si può dare una definizione più generale di regione conservativa. Possiamo considerare regioni 
    # conservative anche sequenze di eventi che condividono solo una parte delle loro funzionalità 
    # con altre aree del processo. In questo caso si parla di regioni conservative k-approssimate, dove
    # k è la distanza di edit tra le due regioni.
    # 
    # Come criterio di similarità viene usata la distanza di Levenshtein. 
    # Se la distanza di edit tra due regioni è minore di una certa soglia, 
    # queste sono considerate simili.
    # 
    # Il metodo richiede come parametri:
    #   - la traccia T in cui è contenuta la regione da analizzare;
    #   - l'indice in cui inizia la regione;
    #   - la regione della traccia da analizzare;
    #   - un valore di soglia delta. 
    # 
    # Come valore, nel caso la traccia sia regione conservativa, viene restituito True.
    # 
    # Altrimenti, viene restituito False.

    
    def isConservedRegion(T,i,si,delta):

        # Genera una copia dell'event log e rimuove la traccia che si sta analizzando

        event_log = Subprocess.event_log.copy()
        event_log.remove(T)

        # Lunghezza della regione considerata
        
        l = len(si)

        # Aggiunge all'event log la traccia corrente, dopo aver rimosso la regione da analizzare

        event_log.add(T[:i])
        event_log.add(T[i+l:])

        # Cerca tutte le regioni di lunghezza compresa tra l-delta e l+delta presenti nell'event log

        regioni = Subprocess.findRegions(event_log,l-delta,l+delta)

        # Se la regione si è simile (condivide alcune funzionalità) ad almeno una delle regioni presenti 
        # nell'event log viene restituito True.

        for sc in regioni:

            if Subprocess.isSimilar(si,sc,delta): return True

        # Se non viene trovata nessuna corrispondenza, allora viene restituito False.

        return False

    

    # Il metodo va a rilevare tutte le regioni conservative contenute all'interno di una traccia.
    # L'event log in cui cercare le regioni conservative va passato come variabile statica di classe.
    # 
    # Il metodo richiede come parametri:
    #   - la traccia T da analizzare;
    #   - un valore di soglia delta. 
    # 
    # Il metodo restituisce una lista di regioni conservative.
                    
    
    def detect(T,delta):

        # Lista che andrà a contenere tutte le regioni conservative rilevate

        conserved_regions = []

        # Lungehzza della traccia

        n = len(T)

        # Ad ogni iterazione del ciclo vengo rilevati tutti i sottoprocessi di lunghezza l.
        # I sottoprocessi rilevati contengono almeno MIN_SIZE eventi.

        for l in range(Subprocess.MIN_SIZE,n+1):

            # La traccia viene scandita dall'inizio alla fine, controllando per ogni sottostringa di 
            # lunghezza l se questa sia o meno una regione conservativa.
            #
            # In caso positivo viene istanziato un oggetto della classe Subprocess e viene aggiunto alla lista
            # delle regioni conservative rilevate.

            for i in range(n-l+1):

                # Viene selezionata una regione

                si = tuple(T[i:i+l])

                # Se la regione selezionata è conservativa, viene aggiunta alla lista dei pattern rilevati

                if Subprocess.isConservedRegion(T,i,si,delta): conserved_regions.append(Subprocess(i,si))
        
        # La lista delle regioni conservative viene ordinata in base alla posizione in cui inizia la sottostringa. 
        # In caso di due regioni conservative con stessa posizione iniziale, viene messa prima quella più lunga.
        
        conserved_regions.sort()

        # La lista viene filtrata eliminando le regioni sovrapposte
        
        return Subprocess.filter(conserved_regions)

    

    # Il metodo filtra la lista di regioni conservative passata per parametro, scartando
    # quelle che si sovrappongono.
    # 
    # Il metodo richiede come parametro la lista di regioni conservative da filtrare.
    # 
    # Il metodo restituisce la lista di regioni conservative filtrata.
    

    def filter(conserved_regions):

        # Lista che andrà a contenere tutte le regioni conservative filtrate

        filtered_conserved_regions = []

        # Riferimento alla regione conservativa precedente (inizializzato a None)

        prec = None

        # Viene scandita tutta la lista scartando le regioni conservative sovrapposte

        for conserved_region in conserved_regions:

            # Verifica se la regione considerata è contenuta o sovrapposta con la precedente

            if not (conserved_region.isContained(prec) or conserved_region.isOverlapped(prec)):

                # Aggiunge la regione conservativa alla lista dei pattern filtrati

                filtered_conserved_regions.append(conserved_region)

                # Aggiorna il riferimento al pattern precedente

                prec = conserved_region

        # Restituisce la lista contenente le regioni filtrate
        
        return filtered_conserved_regions