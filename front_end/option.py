
#####################################################################################
################################## Classe Option ####################################
#####################################################################################
#                                                                                   #
# La classe Option implementa un semplice widget contenente un menu a tendina e un  #
# radio button.                                                                     #
#                                                                                   #
# La classe eredita da Frame.                                                       #
#                                                                                   #
#####################################################################################


from tkinter import OptionMenu
from tkinter import Frame
from tkinter import Radiobutton
from tkinter import StringVar



class Option(Frame):


    # Istanzia un oggetto della classe Option

    def __init__(self, parent, nome, variable, color, width, option = None):

        # Invoca il costruttore della superclasse (costruisce un Frame)
        
        super().__init__(parent, width = width, bg=color)

        # Aggiunge un radio button al frame
        
        self.radio_button = Radiobutton(self, text = nome, bg = color, variable = variable, value = nome)
        
        self.radio_button.pack(fill="x", side="left", padx=4)

        # Istanzia una StringVar, che andrà a contenere il valore
        # selezionato nel menu a tendina

        self.option = StringVar(master = parent, value = option)

        # Aggiunge il menu a tendina

        if option:
            
            menu = OptionMenu(self, self.option, *range(1,4))
            menu.config(width = width//30, state = "disabled")
            menu.pack(side = "right",padx=10)
            self.radio_button.configure(command=lambda:menu.config(state = "normal"))
            self.disableMenu = lambda: menu.config(state = "disabled")
    

    
    # Il metodo restituisce il valore selezionato nel menu a tendina
    
    
    def get(self):

        return self.option.get()





        
    




        

