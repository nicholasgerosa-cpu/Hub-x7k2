# Team agenti: 10 AI che cercano il business giusto da avviare con 1000 €

Un team di 10 agenti AI che gira sul vostro PC con **Ollama** (gratis, in locale) e lavora
da solo **fino a lunedì alle 09:00**, in due fasi:

1. **Ricerca del business**: tutti propongono idee nel proprio campo, gli specialisti le valutano,
   le migliori vengono migliorate e incrociate.
2. **Valutazione di fattibilità**: sulle idee migliori il team scrive uno studio di fattibilità
   completo (mercato, operatività, economia, aspetti legali, comunicazione, clienti, rischi) e il CEO
   decide se sono fattibili.

Alla fine consegna una classifica, gli studi di fattibilità e un verdetto su quale idea avviare.

Il **budget di 1000 €** è il capitale di partenza per l'idea: ogni proposta deve stare dentro
quella cifra. Far lavorare il team non costa nulla, a parte la corrente del PC.

## Il team

Ogni agente ha un **compito per monetizzare** (il campo in cui cerca idee nella fase 1). Sette di loro
sono anche **specialisti**: valutano le idee degli altri e scrivono la loro parte degli studi di fattibilità.

| Agente | Ruolo | Fase 1: cerca modi legali di monetizzare con... | Fase 2: valuta e scrive |
|---|---|---|---|
| Matteo | Ricerca di mercato e trend | nicchie emergenti e bisogni non soddisfatti, in Italia e all'estero | domanda e concorrenza · *Mercato e domanda* (con i test per verificare la domanda in 7 giorni) |
| Marco | Prodotti digitali e AI | template, guide, mini-corsi, micro-SaaS e automazioni AI venduti nel mondo tramite piattaforme che gestiscono pagamenti e IVA | migliora le proprie idee |
| Luca | E-commerce internazionale | marketplace internazionali, print-on-demand, logistica affidata a terzi | migliora le proprie idee |
| Paolo | CFO | abbonamenti, contratti mensili, licenze ad alto margine | velocità, potenziale, budget · *Fattibilità economica* |
| Chiara | Avvocata del diavolo | modelli già collaudati portati in nuovi paesi o lingue | rischio e domanda · *Rischi e piano B* |
| Andrea | Legale e fiscale internazionale | attività gestibili legalmente anche senza sede fiscale in Italia | legalità e sede · *Fattibilità legale e fiscale* |
| Francesca | Growth marketer | contenuti, newsletter, community, affiliazioni, in più lingue | facilità a trovare clienti · *Come trovare i clienti* |
| Valentina | Responsabile comunicazione | brand di contenuti, servizi di comunicazione, personal branding | chiarezza del messaggio · *Comunicazione* (nomi, messaggio chiave, tono, contenuti e testo di lancio) |
| Giorgio | Responsabile operativo | attività semplici da gestire con processi ripetibili e fornitori esterni | fattibilità operativa · *Fattibilità operativa* (attività, ore a settimana, strumenti) |
| Roberto | CEO | servizi e affari con le aziende: servizi da remoto, partnership, intermediazione, rivendita di servizi di terzi con il proprio marchio | dirige, incrocia le idee, decide gli esiti degli studi e il verdetto |

**Fase 1, ricerca (primo 60% del tempo).** A ogni giro **tutti e 10** propongono un'idea nel proprio
campo, ognuno con un focus estratto a caso (tipo di cliente + vincolo, ad esempio "italiani all'estero"
+ "gestibile da qualunque paese"). I 7 specialisti valutano ogni idea su 11 criteri: velocità del primo
incasso, potenziale, budget, domanda, spazio sul mercato, rischio, facilità a trovare clienti, chiarezza
del messaggio, fattibilità operativa, semplicità legale e **gestibilità senza sede in Italia**. Nessuno
giudica le proprie idee: in quel caso il voto lo dà Roberto. Le idee migliori vengono rivalutate per
ridurre il "rumore" dei voti, poi migliorate dal loro autore e incrociate dal CEO. Una versione
migliorata sostituisce l'originale solo se prende un voto più alto. Il CEO commenta ogni giro e orienta
il successivo. Già in questa fase la prima della classifica riceve uno studio di fattibilità.

**Fase 2, fattibilità (ultimo 40%).** Si cercano meno idee nuove e si approfondiscono le migliori: per
ogni idea della top 5 i 7 specialisti scrivono, uno dopo l'altro, la loro parte dello studio di
fattibilità, e Roberto decide: **fattibile**, **fattibile con condizioni** o **non fattibile**, con il
piano delle prime 4 settimane. Un'idea non fattibile perde metà del punteggio e lascia il posto alla
successiva, che viene studiata a sua volta. Prima della scadenza tutta la top 5 ha il suo studio.

## Legalità e "senza sede fiscale in Italia"

Solo idee legali: per ogni idea Andrea dice se è legale, quale forma giuridica usare e da quale paese.
Un'idea che giudica illegale, o basata su elusione o evasione, perde il 60% del punteggio e nel report
è segnata con "[dubbi di legalità]". Ogni studio di fattibilità ha una parte legale e fiscale, e il
verdetto finale spiega come operare in modo legale.

La regola di fondo che il team applica (e che conviene verificare con un commercialista):

- **Se vivete in Italia** (residenza fiscale italiana) pagate le tasse in Italia su tutto quello che
  guadagnate, anche da clienti esteri o con una società all'estero. Una società estera gestita di
  fatto dall'Italia è considerata italiana dal fisco: si chiama **esterovestizione** ed è illegale.
- **Operare legalmente senza sede fiscale in Italia** è possibile se vi **trasferite davvero**
  all'estero (residenza reale e iscrizione AIRE), oppure se la società è gestita davvero da fuori
  Italia.
- Vendere in tutto il mondo tramite piattaforme che incassano e versano l'IVA per voi
  (merchant of record) semplifica molto gli adempimenti, ovunque risiediate.

Per questo è importante scrivere in `profilo.txt` dove avete la residenza oggi e se siete
disposti a trasferirvi.

## Dopo: la fase di esecuzione

Questo team serve a **individuare il business** e a verificarne la fattibilità. Una volta scelta
l'idea, servirà un team diverso, pensato per avviarla, con figure che adesso non servono:

- **il cliente tipo**, che si immedesima nei clienti dell'idea scelta e solleva le loro obiezioni;
- **il venditore**, che prepara i messaggi e gli script per contattare i primi clienti.

## Cosa serve

- **Python 3.8 o superiore.** Su Windows si installa da python.org, spuntando "Add to PATH".
- **Ollama acceso** con almeno un modello scaricato. Lo script sceglie da solo il modello più grande
  sotto i 12 GB. Se non ne avete uno adatto, uno di questi va bene:
  - `ollama pull gemma3:12b`: ottimo in italiano, serve una GPU da 12 GB o 16 GB di RAM
  - `ollama pull gemma3:4b`: per PC meno potenti
  - `ollama pull qwen3:8b`: buona alternativa

Non serve installare nient'altro (niente `pip install`).

## Avvio in 3 passi

1. **Personalizzate `profilo.txt`**: città, competenze, lingue, ore disponibili, residenza fiscale,
   cosa vi piace e cosa no. Più è preciso, più le idee saranno su misura.
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
- **Aggiornare lo script a metà lavoro**: fermatelo con Ctrl+C, sostituite i file e rilanciatelo.
  Le idee già trovate restano; per ripartire da zero con il team nuovo aggiungete `--nuovo`.
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
| `report.html` | report finale: verdetto del CEO, top 5 con voti, pareri dei 7 specialisti e studio di fattibilità completo (mercato, operatività, budget voce per voce, aspetti legali, comunicazione, clienti, rischi, prime 4 settimane), idee bocciate e perché, il lavoro di ciascun agente, classifica completa |
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

La velocità dipende dal PC. Ogni giro fa circa 130 chiamate all'AI (10 idee valutate da 7 specialisti,
più miglioramenti e studi): con una GPU e un modello da 7-12B un giro dura 15-30 minuti, solo con la CPU
anche 2-3 ore. In entrambi i casi entro lunedì il team avrà valutato decine o centinaia di idee.