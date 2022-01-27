# Rilevamento cicli all'interno di grafi d'istanza

Progetto per il corso di Big Data Analytics e Machine Learning che prevede l'implementazione di un algoritmo per il rilevamento dei cicli all'interno dei grafi d'istanza.

L'applicazione implementa due diverse modalità di rilevamento:
- rilevamento base, che prevede l'identificazione dei cicli, la rimozione delle attività ripetute e il tracciamento di un arco backward per collegare l'ultima attività del ciclo alla prima;
- rilevamento avanzato, che prevede l'identificazione di cicli e sottoprocessi e la loro sostituzione con delle attività astratte.

L'algoritmo di rilevamento avanzato è basato sull'approccio descritto nell'articolo "Abstractions in Process Mining A Taxonomy of Pattern" di Bose e Aalst.


## Installazione


Per installare l'applicazione sul proprio ambiente di lavoro è necessario scaricare il repository da github, aprire un terminale all'interno della cartella del progetto e lanciare il comando:

```
pip3 install -r requirements.txt
```
Il precedente comando provvederà ad installare tutte le librerie esterne necessarie al funzionamento dell'applicazione.

L'applicazione è stata realizzata e testata utilizzando Python 3.10.1. Per un corretto funzionamento della GUI si consiglia di usare una versione abbastanza recente di Python.

## Utilizzo

Per avviare l'applicazione è sufficiente, una volta posizionati nella directory del progetto, lanciare il seguente comando:
```
python3 main.py
```
All'avvio dell'applicazione verrà mostrato un file dialog che permetterà di selezionare i file contenneti i grafi da processare con l'algoritmo di rilevamento. I file di input devono essere codificati secondo il formato associato all'estensione .g.

Selezionato il file verrà mostrata una finestra in cui configurare i parametri dell'algoritmo di rilevamento.
