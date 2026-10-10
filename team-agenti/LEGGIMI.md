# Team agenti: 10 AI che cercano idee per guadagnare con 1000 €

Un team di 10 agenti AI che gira sul vostro PC con **Ollama** (gratis, in locale) e lavora
da solo **fino a lunedì alle 09:00**. Propone idee di business, le critica, le migliora e alla fine
consegna una classifica con i piani operativi e un verdetto su quale avviare.

Il **budget di 1000 €** è il capitale di partenza per l'idea: ogni proposta deve stare dentro
quella cifra. Far lavorare il team non costa nulla, a parte la corrente del PC.

## Il team: ognuno ha un compito per monetizzare

| Agente | Ruolo | Il suo compito: modi legali di monetizzare con... | Giudica anche |
|---|---|---|---|
| Giulia | Cacciatrice di trend | nicchie emergenti, in Italia e all'estero | |
| Marco | Prodotti digitali | template, guide, mini-corsi, micro-SaaS venduti nel mondo tramite piattaforme che gestiscono pagamenti e IVA | |
| Sara | Servizi B2B a distanza | servizi da remoto per aziende italiane ed estere | |
| Luca | E-commerce internazionale | marketplace internazionali, print-on-demand, logistica affidata a terzi | |
| Elena | AI e automazione | servizi e strumenti AI vendibili ovunque, anche con l'AI locale | |
| Paolo | CFO | abbonamenti, contratti mensili, licenze ad alto margine | costi e guadagni |
| Chiara | Avvocata del diavolo | modelli già collaudati portati in nuovi paesi o lingue | rischi e domanda |
| Andrea | Legale e fiscale internazionale | attività gestibili legalmente anche senza sede fiscale in Italia | legalità e struttura |
| Francesca | Growth marketer | contenuti, newsletter, community, affiliazioni, in più lingue | marketing |
| Roberto | CEO | partnership, intermediazione, rivendita di servizi di terzi con il proprio marchio | direzione, incroci, piani |

**Come lavorano.** A ogni giro **tutti e 10** propongono un'idea nel proprio campo, ognuno con un
focus estratto a caso (tipo di cliente + vincolo, ad esempio "italiani all'estero" + "gestibile da
qualunque paese"). Paolo, Chiara, Andrea e Francesca valutano le idee su 8 criteri: velocità del primo
incasso, potenziale, budget, rischio, domanda, facilità, semplicità legale e **gestibilità senza sede
in Italia**. Nessuno giudica le proprie idee: in quel caso il voto lo dà Roberto. Le idee migliori
vengono rivalutate per ridurre il "rumore" dei voti, poi migliorate dal loro autore e incrociate dal
CEO. Una versione migliorata sostituisce l'originale solo se prende un voto più alto. Il CEO commenta
ogni giro e orienta il successivo. Nell'ultimo 40% del tempo il team esplora meno e consolida di più.

## Legalità e "senza sede fiscale in Italia"

Solo idee legali: per ogni idea Andrea dice se è legale, quale forma giuridica usare e da quale paese.
Un'idea che giudica illegale, o basata su elusione o evasione, perde il 60% del punteggio e nel report
è segnata con "[dubbi di legalità]". Ogni piano operativo e il verdetto finale spiegano come operare
in modo legale.

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
| `report.html` | report finale: verdetto del CEO, top 5 con voti, critiche, struttura legale e piano operativo (budget voce per voce, 4 settimane, primi passi, KPI, quando fermarsi, come operare legalmente), il lavoro di ciascun agente, classifica completa |
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
