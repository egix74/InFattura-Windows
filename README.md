# InFattura per Windows

Calcolatore di parcelle professionali con calcolo diretto e scorporo dal netto.

## Funzioni

- Calcolo da onorari o da netto a pagare.
- Spese esenti e non esenti, Cassa, IVA, ritenuta e maggiorazione forfettaria.
- Percentuali modificabili e dettaglio degli importi.
- Funzionamento locale, senza invio di dati.

## Avvio dal codice sorgente

Su Windows, con Python 3 e Tkinter installati, esegui:

```powershell
python app.py
```

## Versione portatile

Il file `launcher_portatile.cs` è il codice dell'avviatore della versione portatile. Per usarlo occorrono, nella stessa cartella, `app.py`, `calcolo.py` e una cartella `runtime` contenente Python per Windows con Tkinter. Il solo codice sorgente scaricato da GitHub non comprende il runtime né l'eseguibile già compilato.

## Ipotesi e limiti

La maggiorazione forfettaria si calcola sugli onorari. Le spese non esenti sono incluse nelle basi di Cassa, IVA e ritenuta; le spese esenti sono aggiunte al netto. Verificare il trattamento fiscale nel caso concreto. I risultati dello scorporo possono differire di pochi centesimi per arrotondamento.

Il programma non emette o trasmette fatture elettroniche e non gestisce bollo o casi fiscali particolari. Il calcolo va verificato prima dell'utilizzo.
