# Team agenti: 10 AI che cercano idee per guadagnare con 1000 €

Un team di 10 agenti AI che gira sul vostro PC con **Ollama** (gratis, in locale) e lavora
da solo **fino a lunedì alle 09:00**. Propone idee di business, le critica, le migliora e alla fine
consegna una classifica con i piani operativi e un verdetto su quale avviare.

Il **budget di 1000 €** è il capitale di partenza per l'idea: ogni proposta deve stare dentro
quella cifra. Far lavorare il team non costa nulla, a parte la corrente del PC.

## Il team

| Agente | Ruolo | Cosa fa |
|---|---|---|
| Giulia | Cacciatrice di trend | nicchie emergenti, bisogni nuovi |
| Marco | Prodotti digitali | template, mini-corsi, micro-SaaS, community |
| Sara | Servizi locali e B2B | servizi per negozi, artigiani, studi, B&B |
| Luca | E-commerce e commercio | marketplace, print-on-demand, vintage, margini |
| Elena | AI e automazione | servizi basati su AI locale e automazioni |
| Paolo | CFO | costi, investimento, utile realistico, budget |
| Chiara | Avvocata del diavolo | rischi, concorrenza, domanda reale |
| Andrea | Legale e fiscale | partita IVA, licenze, GDPR, regole |
| Francesca | Growth marketer | canali, primi 10 clienti |
| Roberto | CEO | incrocia le idee migliori, dà la direzione, scrive i piani |

**Come lavorano.** A ogni giro i 5 ideatori propongono idee nuove, ognuno con un focus diverso
estratto a caso (tipo di cliente + vincolo, ad esempio "B&B" + "zero magazzino"). I 4 valutatori
danno i voti su 7 criteri: velocità del primo incasso, potenziale, budget, rischio, domanda,
facilità, aspetti legali. Le idee migliori vengono rivalutate per ridurre il "rumore" dei voti,
poi migliorate dal loro autore e incrociate tra loro dal CEO. Una versione migliorata sostituisce
l'originale solo se prende un voto più alto. Il CEO commenta ogni giro e orienta il successivo.
Nell'ultimo 40% del tempo il team esplora meno e consolida di più le idee migliori.

## Cosa serve

- **Python 3.8 o superiore.** Su Windows si installa da python.org, spuntando "Add to PATH".
- **Ollama acceso** con almeno un modello scaricato. Lo script sceglie da solo il modello più grande
  sotto i 12 GB. Se non ne avete uno adatto, uno di questi va bene:
  - `ollama pull gemma3:12b`: ottimo in italiano, serve una GPU da 12 GB o 16 GB di RAM
  - `ollama pull gemma3:4b`: per PC meno potenti
  - `ollama pull qwen3:8b`: buona alternativa

Non serve installare nient'altro (niente `pip install`).

## Avvio in 3 passi

1. **Personalizzate `profilo.txt`**: città, competenze, ore disponibili, cosa vi piace e cosa no.
   Più è preciso, più le idee saranno su misura.
2. **Fate una prova di 10 minuti** per verificare che tutto funzioni:
   ```
   python team_agenti.py --minuti 10
   ```
   Su Windows potete usare `py` al posto di `python`. La prova scrive in una cartella separata
   (`risultati_prova/`), quindi non sporca il lavoro vero.
3. **Lanciate il lavoro del weekend**: doppio clic su `AVVIA_WINDOWS.bat`, oppure su
   `avvia_mac_linux.command` su Mac, oppure da terminale:
   ```
   python team_agenti.py
   ```
   Lavora fino a lunedì alle 09:00. Per un'altra scadenza: `--fino-a "2026-10-12 08:00"`.

## Durante il weekend

- **Classifica in tempo reale**: aprite `risultati_team/report.html` nel browser.
  La pagina si aggiorna da sola ogni 5 minuti.
- **Orientare il team**: scrivete in `direttive.txt`, ad esempio "niente e-commerce" oppure
  "approfondite i servizi per i B&B". Gli agenti lo leggono dalla chiamata successiva, senza riavviare.
- **Fermare e riprendere**: Ctrl+C salva tutto. Rilanciando lo stesso comando riprende da dove era
  rimasto, con la stessa scadenza. Vale anche dopo un riavvio o un blackout.
- **Sospensione del PC**: su Windows e Mac lo script impedisce lo standby finché è acceso. Su un
  portatile tenetelo **collegato alla corrente** e impostate "chiudendo il coperchio: non fare nulla"
  (oppure lasciatelo aperto). Su Linux lanciatelo con `systemd-inhibit python3 team_agenti.py`.
- **Seguirlo dal telefono**: con `--cartella` potete salvare i risultati in una cartella sincronizzata
  (OneDrive, Google Drive, Dropbox) e aprire `report.html` dal telefono.

## Lunedì mattina

In `risultati_team/` trovate:

| File | Contenuto |
|---|---|
| `report.html` | report finale: verdetto del CEO, top 5 con voti, critiche e piano operativo (budget voce per voce, 4 settimane, primi passi, KPI, quando fermarsi), classifica completa |
| `report.md` | lo stesso in Markdown |
| `idee.csv` | tutte le idee valutate, da aprire con Excel |
| `diario.log` | tutto quello che è successo, minuto per minuto |
| `stato.json` | i dati completi (servono per riprendere) |

## Opzioni

```
--modello NOME        modello Ollama da usare (es. gemma3:12b)
--fino-a "DATA ORA"   scadenza diversa (es. "2026-10-12 09:00" o "12/10/2026 09:00")
--minuti N            lavora solo N minuti (prova)
--cartella PERCORSO   dove salvare i risultati
--solo-report         rigenera il report dai dati salvati, senza usare l'AI
--nuovo               archivia il lavoro precedente e riparte da zero
--ollama-url URL      se Ollama gira su un altro PC (default http://localhost:11434)
--contesto N          finestra di contesto in token (default 8192)
```

## Quanto fidarsi

I modelli locali **non hanno accesso a internet**: prezzi, concorrenti e norme sono stime del modello.
Ogni piano include una sezione "Da verificare prima di spendere": fatelo davvero prima di investire
anche un euro. Il team serve a generare e filtrare molte idee in poco tempo, non a sostituire
una verifica sul campo con clienti veri.

La velocità dipende dal PC. Con una GPU e un modello da 7-12B un giro dura 5-15 minuti; solo con la
CPU anche un'ora. In entrambi i casi entro lunedì il team avrà fatto decine o centinaia di giri.
