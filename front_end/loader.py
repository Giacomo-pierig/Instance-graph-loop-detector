

#########################################################################################
################################## Classe Loader ########################################
#########################################################################################
#                                                                                       #
# La classe Loader implementa una semplice barra di caricamento che viene mostrata      #
# mentre si attende il completamento del rilevamento dei cicli all'interno del grafo    #
#                                                                                       #
# La classe eredita da Toplevel.                                                        #
#                                                                                       #
#########################################################################################


from tkinter import Toplevel
from tkinter import Label
from tkinter.ttk import Progressbar
from tkinter.ttk import Style


class Loader(Toplevel):


    # Istanzia un oggetto della classe Loader


    def __init__(self, width=300, height=100, color="#DFE9E9"):

        # Invoca il costruttore della superclasse

        super().__init__(bg=color)

        # Imposta le dimensioni e la posizione della finestra

        self.geometry(str(width)+"x"+str(height)+"+"+str((self.winfo_screenwidth()-width)//2)+"+"+str((self.winfo_screenheight()-height)//2))

        # Definisce lo stile della barra di caricamento

        style = Style()
        style.theme_use('alt')
        style.configure("blue.Horizontal.TProgressbar",background='#2487C3')

        # Aggiunge l'etichetta "loading..." alla finestra
        
        Label(self,text="Loading...",font=("Arial",12,"bold"),bg=color,fg="#2487C3").pack(fill="x",pady=(height//5,height//14))

        # Aggiunge e attiva la progress bar

        loader = Progressbar(self,mode='determinate',style="blue.Horizontal.TProgressbar")
        loader.start()
        loader.pack(fill="x",padx=width//10)

        # Elimina i pulsanti e il bordo della finestra

        self.update_idletasks()
        self.overrideredirect(True)