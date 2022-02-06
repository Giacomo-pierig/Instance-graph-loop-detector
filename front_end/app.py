

#########################################################################################
##################################### Classe App ########################################
#########################################################################################
#                                                                                       #
# La classe App implementa il front end dell'applicazione.                              #
#                                                                                       #
# Il front end permette di caricare un grafo da file e lanciare gli algoritmi di        #
# rilevamento.                                                                          #      
#                                                                                       #
# La classe eredita da Tk.                                                              #
#                                                                                       #
#########################################################################################


from tkinter import Tk
from tkinter import StringVar
from tkinter import Button
from tkinter import Label
from tkinter.filedialog import askopenfilenames, askdirectory
from tkinter.messagebox import showerror

from .loader import Loader
from .option import Option
from .plot import Plot

from threading import Thread
from os import _exit

from back_end.graph import IgGraph
from back_end.process import Loop
from back_end.process import Subprocess



class App(Tk):


    # Istanzia un oggetto della classe App


    def __init__(self ,width=440, height=300, color="#DFE9E9"):

        # Invoca il costruttore della superclasse

        super().__init__()

        # Inizializza la lista che andrà a contenere i grafi caricati nell'applicazione

        self.graphs = []

        # Impedisce alla finestra di essere ridimensionata
        
        self.resizable(0,0)

        # Imposta il titolo dell'applicazione

        self.title("Seleziona impostazioni rilevamento")

        # Imposta il colore di sfondo dell'applicazione

        self.configure(background = color)

        # Imposta la posizione e le dimensioni della finestra

        self.geometry(str(width)+"x"+str(height)+"+"+str((self.winfo_screenwidth()-width)//2)+"+"+str((self.winfo_screenheight()-height)//2))

        # Aggiunge i radio buttons per la scelta del tipo di rilevamento
        
        Label(self,text="Tipo rilevamento:",bg=color).pack(anchor="w",padx=6,pady=(width//36,0))
        self.tipo_rilevamento = StringVar(master = self, value = "Rilevamento cicli base")
        basic_detection = Option(self, "Rilevamento cicli base", self.tipo_rilevamento, color, width)
        basic_detection.pack(fill="x",pady=(width//160,0))
        self.advanced_detection = Option(self, "Rilevamento avanzato", self.tipo_rilevamento, color, width, "Numero iterazioni")
        self.advanced_detection.pack(fill="x")
        basic_detection.radio_button.configure(command=self.advanced_detection.disableMenu)

        # Aggiunge i radio buttons per la scelta del tipo di tandem repeat
        
        Label(self,text="Tandem repeat type:",bg=color).pack(anchor="w",padx=6,pady=(width//36,0))
        self.tandem_repeat_type = StringVar(master = self, value = "Solo ripetizioni esatte")
        exact_tandem_repeat = Option(self, "Solo ripetizioni esatte", self.tandem_repeat_type, color, width)
        exact_tandem_repeat.pack(fill="x",pady=(width//160,0))
        self.approximate_tandem_repeat = Option(self, "Consenti ripetizioni approssimate", self.tandem_repeat_type, color, width, "Edit distance")
        self.approximate_tandem_repeat.pack(fill="x")
        exact_tandem_repeat.radio_button.configure(command=self.approximate_tandem_repeat.disableMenu)

        # Aggiunge i radio buttons per la scelta del tipo di maximal repeat
        
        Label(self,text="Maximal repeat:",bg=color).pack(anchor="w",padx=6,pady=(width//36,0))
        self.maximal_repeat = StringVar(master = self, value = "Solo ripetizioni esatte")
        exact_maximal_repeat = Option(self, "Solo ripetizioni esatte", self.maximal_repeat, color, width)
        exact_maximal_repeat.pack(fill="x",pady=(width//160,0))
        self.approximate_maximal_repeat = Option(self, "Consenti ripetizioni approssimate", self.maximal_repeat, color, width, "Edit distance")
        self.approximate_maximal_repeat.pack(fill="x")
        exact_maximal_repeat.radio_button.configure(command=self.approximate_maximal_repeat.disableMenu)

        # Aggiunge il pulsante per avviare il rilevamento dei pattern

        detect_button = Button(self, text = "Detect", highlightbackground = color, command = self.detect)
        detect_button.pack(fill="x",padx=width//3,pady=(height//20,height//100))

        # Nasconde la finestra

        self.withdraw()



    # Il metodo esegue il rilevamento dei cicli all'interno dei grafi caricati nell'applicazione.

        
    def detect(self):

        # Vengono decodificate le opzioni scelte per il rilevamento e viene costruito il detector
        # Il detector è la funzione che va ad eseguire il rilevamento dei cicli sul grafo.

        match self.tipo_rilevamento.get():

            case "Rilevamento cicli base":

                iteration_number = 1

                options = {"pattern_type": Loop, "unpack": True}

                if self.tandem_repeat_type.get() == "Consenti ripetizioni approssimate":
                
                    try: options["delta"] = int(self.approximate_tandem_repeat.get())

                    except: 
                        
                        showerror("Loop detector", "Specificare il valore della distanza di edit da usare per il rilevamento dei cicli")
                        return

                detector = lambda x: x.detect(**options)[0]

            case "Rilevamento avanzato":

                try: iteration_number = int(self.advanced_detection.get())

                except: 
                    
                    showerror("Loop detector", "Selezionare il numero di iterazioni che dovrà eseguire l'algoritmo")
                    return

                options1 = {"pattern_type": Loop}
                options2 = {"pattern_type": Subprocess}

                if self.tandem_repeat_type.get() == "Consenti ripetizioni approssimate":
                
                    try: options1["delta"] = int(self.approximate_tandem_repeat.get())

                    except: 
                        
                        showerror("Loop detector", "Specificare il valore della distanza di edit da usare per il rilevamento dei cicli")
                        return
                
                if self.maximal_repeat.get() == "Consenti ripetizioni approssimate":
                
                    try: options2["delta"] = int(self.approximate_maximal_repeat.get())

                    except: 
                        
                        showerror("Loop detector", "Specificare il valore della distanza di edit da usare per il rilevamento dei sottoprocessi")
                        return

                detector_aux = lambda x: [y := x.detect(**options1),y[0].detect(**options2,patterns=y[1])]
                detector = lambda x: detector_aux(x)[1][0]

        # Apre la finestra per selezionare la directory in cui salvare i grafi ottenuti dopo il rilevamento

        directory = askdirectory(title='Selezionare una destinazione per i risultati del rilevamento',initialdir='.')

        # Controlla se è stata scelta una directory o se si è premuto il pulsante annulla 

        if directory:
            
            # Mostra la finestra di caricamento e nasconde quella principale

            loader = Loader()
            self.withdraw()

            # Funzione che esegue il rilevamento cicli sui grafi e salva il risulato su file

            def run():

                # Su ogni grafo caricato nell'app si esegue il rilevamento cicli.
                # I risultati sono salvati su file.

                for file_name,graph in self.graphs:
                    
                    try: 

                        # Esegue il rilevamento (n° iterazioni)
                        
                        for i in range(iteration_number): graph = detector(graph)

                        # Salva i risultati su file

                        graph.save(directory,file_name)

                    except:

                        # Se si verifica un'eccezione, viene visualizzato un messaggio d'errore

                        showerror("Loop detector", "Errore durante il rilevamento dei cicli ["+file_name+"]")
                        return

                # Se il rilevamento è stato eseguito solo su un grafo, i risultati vengono visualizzati a schermo

                if len(self.graphs) == 1: self.after(1000,lambda:[Plot.show(file_name, self.graphs[0][1], "Before loop detection", graph, "After loop detection"),loader.destroy()])

                # Altrimenti, l'applicazione viene chiusa

                else: _exit(0)
            
            # Il rilevamento viene lanciato in background, su un thread parallelo

            Thread(target=run).start()
        
        # Se non viene scelta nessuna directory, viene visualizzato un messaggio d'errore
        
        else: showerror("Loop detector", "Selezionare il percorso dove salvare i risultati del rilevamento")

    

    # Il metodo permette di avviare l'applicazione

    
    def start(self):

        # Apre la finestra per selezionare i file da caricare

        file_names = askopenfilenames(title='Selezionare un grafo', defaultextension = ".g", filetypes = (("Grafi","*.g"),("Tutti i file","*.*")))

        # Se viene selezionato almeno un file, viene avviata l'applicazione
        
        if len(file_names):

            try:

                # Ogni file selezionato viene decodificato

                for file_name in file_names:

                    # Istanzia un grafo vuoto

                    graph = IgGraph()

                    # Legge il file, aggiungendo nodi e archi in esso definiti al grafo

                    graph.read(file_name)

                    # Aggiunge il grafo ad una lista

                    self.graphs.append((file_name.split("/")[-1],graph))
            
            except:

                # Se si verifica un'eccezione, viene visualizzato un messaggio d'errore

                showerror("Loop detector", "Il file selezionato non può essere aperto dall'applicazione")
                return

            # Visualizza la finestra dell'applicazione

            self.deiconify()

            # Avvia l'applicazione

            self.mainloop()