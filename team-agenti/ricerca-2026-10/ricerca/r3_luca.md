# Ricerca R3: due idee di "regalo digitale" (Luca, e-commerce e regali online)

**Data:** 13 ottobre 2026 (circa 10 settimane a Natale; Black Friday il 27/11/2026)
**Idee analizzate:** (1) sito regalo "pianta un albero"; (2) sito regalo "dedica una stella".
**Vincoli del team:** budget massimo 1.000 euro, competenze digitali di base, prodotto digitale automatizzabile. La parte fiscale non è trattata.

> **Metodo e limiti (da leggere prima dei numeri).** Ho fatto 21 ricerche web in modalità standard. Il recupero diretto delle pagine (WebFetch/curl) era **bloccato dal proxy** dell'ambiente: i siti di Treedom, Tree-Nation e BusinessOnline non erano raggiungibili. Tutti i dati vengono quindi dagli estratti dei risultati di ricerca, e vanno ricontrollati sulle pagine ufficiali prima di spendere soldi. In tutto il documento uso queste etichette:
> - **[verificato]**: fonte primaria o ufficiale (IAU, help center del partner, listino ufficiale, Gazzetta/norma);
> - **[auto-dichiarato]**: numeri forniti dall'azienda stessa, oppure da un concorrente che fa marketing comparativo;
> - **[fonte debole]**: aggregatori, blog SEO o articoli vecchi o senza data;
> - **[stima Luca]**: mie ipotesi di calcolo, non dati.

---

# IDEA 1: "Sito regalo: pianta un albero"

## 1. Come si guadagna

**Modello.** Il cliente paga un regalo, cioè "un albero piantato a nome di qualcuno", e riceve certificato digitale, dedica, mappa e link di tracciamento. La piantumazione **non** la fai tu: la acquisti da un partner, via API o con crediti prepagati, e tieni la differenza. Il tuo valore aggiunto sta in confezione emotiva, personalizzazione, lingua italiana, consegna istantanea e scelta delle occasioni.

**Prezzi al pubblico dei concorrenti**

| Operatore | Prezzo al consumatore | Cosa include | Affidabilità del dato |
|---|---|---|---|
| Treedom (Firenze) | da **14,90 €** (cacao) a **69,90 €** (baobab) | piantumazione, geolocalizzazione, foto, paga al contadino, 10 anni di cura | [fonte debole]: articolo senza data (Sublime Magazine), probabilmente di qualche anno fa |
| Tree-Nation (vende anche direttamente ai privati) | **0,35–15 €** ad albero, secondo progetto e specie | pagamento unico per l'intero ciclo di vita dell'albero, certificato scaricabile, pagina dell'albero | [verificato]: help center Tree-Nation |
| Ecologi (UK) | ~0,89 $ ad albero (Impact Shop) | tracciamento per progetto, non per singolo albero | [verificato]: risposta ufficiale Ecologi sullo Shopify App Store |

**Costi per ordine "all'ingrosso" (partner e API)**

| Partner | Costo ad albero | Note |
|---|---|---|
| Tree-Nation API | 0,35–1 € (grandi progetti) fino a 15 € | API con le funzioni "buy credit", "plant tree", "list projects/species" (connettore Microsoft); per l'API consigliano i "species packages" a prezzo stabile [verificato] |
| Ecologi (app Shopify / Impact API) | **0,80 $** ad albero (app Shopify; i primi 50 gratis), £0,60 in GBP | Impact API per alberi, carbon removal e habitat; il prezzo per albero via API non è pubblicato [verificato per l'app] |
| Digital Humani (RaaS API) | **~1 $ ad albero** | prezzo da fonti terze; per l'account bisognava contattarli [fonte debole] |
| Evertreen (IT/UK) | **~£1–1,5** ad albero, con GPS del singolo albero e monitoraggio satellitare | dichiara API, funzione regalo e certificati geolocalizzati [auto-dichiarato: pagine comparative scritte da Evertreen stessa] |
| GoodAPI e simili | 0,40–1 $ (da 0,43 $) | blog del venditore [auto-dichiarato] |

**Margine per ordine** [stima Luca], con prezzo 14,90 € per un albero tracciabile (partner a ~1–1,5 €):

| Voce | € |
|---|---|
| Prezzo incassato | 14,90 |
| Albero dal partner (con cambio valuta) | −1,00 / −1,50 |
| Commissione di pagamento (Shopify Payments con carte UE: ~1,9% + 0,25 €, dato da community Shopify) | −0,53 |
| Generazione del certificato (Placid: ~19 $ per 500 crediti, 1 PDF di una pagina = 2 crediti) | −0,08 |
| **Margine lordo prima della pubblicità** | **~12,8–13,3 € (≈86–89%)** |

Nota: se il prezzo deve includere l'IVA (tema fiscale, non approfondito), il ricavo netto scende di circa il 18% e il margine diventa ~10 €.

**Il vero problema dei margini è il costo di acquisizione cliente (CAC), non il costo dell'albero.** I benchmark e-commerce danno su Meta un CPC tra ~0,20 e 1,20 $ secondo il settore, e su Google Search ~2,7 $ di media; nel Q4 i costi salgono (CPM Google al Black Friday 2025: +10,6% sull'anno precedente). Con un CPC di 0,50 € e una conversione dell'1,5% (sito nuovo e sconosciuto) il CAC è ~33 €, quindi in perdita su un ordine da 14,90 €. Diventa sostenibile solo con:
- scontrino medio più alto, per esempio un pacchetto "boschetto" da 3–5 alberi a 29–39 €;
- canali gratuiti: rete personale, social organici, SEO (troppo lenta per questo Natale);
- vendite B2B, per esempio piccole aziende che regalano 50–200 alberi ai clienti.

**Affiliazione invece di rivendita** (alternativa a costo zero):
- **Ecologi** ha un programma su Webgains, ma le commissioni riportate non concordano: £20 o £13 per abbonamento, oppure 5–10% [fonte debole: aggregatori].
- **Treedom**: nessun programma di affiliazione ufficiale trovato.
- **Tree-Nation** ha solo un "Ambassador program": regali gratuiti per chi ha già piantato almeno 150 alberi, senza commissioni [verificato].

Conclusione: con l'affiliazione si guadagnano pochi euro a vendita e il cliente resta del partner. Va bene come contenuto di supporto, non come business.

## 2. Prove di domanda ed esempi reali

- **Treedom:** circa 4–4,2 milioni di alberi piantati, 1,2–1,3 milioni di utenti privati, 11.000–12.000 aziende clienti, 15 Paesi (dati 2024) **[auto-dichiarato]**: presentazione aziendale e profilo SP-Edge, con cifre che non coincidono tra loro. Ha raccolto **10 milioni di euro** nel 2021 (round con Nico Rosberg e Giorgio Chiellini). È B Corp dal 2014 e Società Benefit dal 2020. **Non ho trovato il fatturato 2024-2025**: andrebbe preso dal bilancio depositato (Registro Imprese).
- Treedom fa campagne stagionali ricorrenti (Natale, San Valentino, Festa della Mamma; video di Natale con Maccio Capatonda): segnale che il "regalo albero" vende sulle ricorrenze.
- **Ecologi, Tree-Nation, Evertreen** puntano sempre più sul B2B: alberi per ogni vendita, app Shopify, API. La domanda B2B c'è, ma è presidiata da operatori con prezzi di 0,35–1,5 € ad albero.
- **Dato mancante:** non ho trovato volumi di ricerca italiani per "regalare un albero". Prima di investire, verificare su Google Trends e Keyword Planner (gratuiti).

## 3. Concorrenza e saturazione

- **Italia: alta.** Treedom è il marchio italiano di riferimento: prima piattaforma (2010), forte notorietà, stampa e testimonial. Evertreen (Milano) punta alle aziende.
- **Estero: alta.** Tree-Nation, Ecologi, One Tree Planted, Ecomatcher, più una dozzina di "API per piantare alberi" (Digital Humani, GoodAPI e altre).
- **Problema strutturale:** i fornitori sono anche concorrenti. Tree-Nation vende direttamente al privato a 0,35–15 € con il suo certificato. Un cliente che legge sul tuo certificato "piantato da Tree-Nation" può scoprire che l'albero costa 0,50 € e sentirsi preso in giro. La trasparenza (vedi §4) è quindi anche un tema reputazionale.
- **Spazi possibili:** nicchie di occasione (nascita, laurea, lutto o memoria, matrimoni con "bomboniera albero"), design del certificato molto curato, alberi in Italia o Europa (pochi operatori consumer), consegna "ultimo minuto" il 24 dicembre.

## 4. Regole, consumatori e partner

**Novità decisiva: le nuove regole anti-greenwashing valgono da questo Natale.** Il **d.lgs. 20 febbraio 2026, n. 30** (GU n. 56 del 9/3/2026) recepisce la **direttiva UE 2024/825 ("Empowering consumers for the green transition")** e modifica il Codice del Consumo, **con applicazione dal 27 settembre 2026** [verificato: QualEnergia, Certifico, DWF]. Secondo le guide consultate e il testo della direttiva, diventano **pratiche sempre vietate**:
- **affermazioni ambientali generiche** come "regalo green", "ecologico", "eco-friendly", "amico del clima" se non si può dimostrare un'eccellenza ambientale riconosciuta;
- dire, **sulla base di compensazioni di CO₂**, che un prodotto ha impatto **neutro, ridotto o positivo** sulle emissioni: "Natale a impatto zero", "compensa la CO₂ del tuo regalo", "carbon neutral";
- **marchi o bollini di sostenibilità auto-creati**, non basati su un sistema di certificazione o non istituiti da autorità pubbliche. Un badge tipo "Certificato Green" disegnato da noi sul certificato è a rischio.

L'abbinamento compensazione/neutralità è riportato da fonti secondarie (ShippyPro, GS1 Italy). Va controllato sul testo del decreto con un consulente prima del lancio.

**Cosa si può promettere (formulazioni prudenti)**
- "Con questo regalo **finanzi la piantumazione di 1 albero di [specie] nel progetto [nome, Paese]**, realizzata dal partner **[nome]**. Puoi verificarlo qui: [link alla pagina del partner]."
- Dire **quando** viene piantato. I partner piantano nella stagione adatta, che può arrivare mesi dopo l'acquisto. Esempio: "sarà messo a dimora nella prossima stagione di piantumazione del progetto" (da verificare con il partner scelto).
- Indicare la CO₂ solo come **stima del partner**, con la sua fonte e il suo metodo, mai come "compensazione".
- **Trasparenza sul prezzo**, consigliata e non solo prudente: "Di 14,90 €, X € vanno al progetto di piantumazione; il resto copre certificato, piattaforma e servizio."

**Cosa è rischioso o da evitare**
- "L'albero è tuo" o "di tua proprietà". In Treedom, per esempio, l'albero **appartiene al contadino** che lo pianta.
- "Foto del tuo albero" o "GPS del tuo albero" se il partner traccia solo a livello di progetto. Ecologi e molte API non danno foto del singolo albero; Evertreen e Treedom dichiarano di farlo.
- Presentarlo come **donazione** o "beneficenza". È una vendita con margine, e chiamarla donazione è ingannevole. Può anche creare problemi con i processori di pagamento, che regolano diversamente la raccolta fondi (da verificare nelle condizioni di Stripe e PayPal).
- Sconti al Black Friday: per la regola Omnibus (art. 17-bis Codice del Consumo, riferimento non riconsultato in questa sessione) lo sconto va calcolato sul prezzo più basso degli ultimi 30 giorni.
- Contenuto digitale e recesso: per escludere il recesso di 14 giorni serve il consenso espresso del cliente al checkout (art. 59 Codice del Consumo, da far verificare).

**Affidabilità dei partner**
- Tree-Nation, Ecologi e Treedom sono operativi da anni e documentati. Treedom è B Corp e Società Benefit (dato auto-dichiarato ma verificabile).
- Il CEO di Treedom ammette che nei **grandi progetti** di riforestazione ci sono stati errori, come le monoculture, e che i crediti di carbonio spingono verso progetti enormi [intervista Altroconsumo]. Ne segue che il progetto scelto è un rischio reputazionale anche per noi.
- **Prima del lancio, ottenere per iscritto dal partner:**
  1. il permesso di **rivendere** al consumatore finale e di citare il suo nome o marchio;
  2. il prezzo garantito via API o con crediti;
  3. che cosa succede se il progetto fallisce: alberi morti, ripiantumazione;
  4. per quanto tempo restano attivi i link di verifica.
- La Digital Humani API (fonti un po' datate) richiedeva di contattarli per avere l'account: è un possibile rallentamento.

## 5. Strumenti e costi per partire

| Funzione | Opzione consigliata | Costo indicativo |
|---|---|---|
| Negozio | Shopify Basic | 29 $/mese con pagamento annuale, 39 $/mese con pagamento mensile; +2% se non usi Shopify Payments [fonti terze 2026] |
| Negozio (alternativa più economica) | WordPress + WooCommerce su hosting condiviso | ~5–10 €/mese (stima) |
| Pagamenti | Shopify Payments (~1,9% + 0,25 € con carte UE, dato community), Stripe, PayPal | solo commissioni |
| Piantumazione | Tree-Nation (crediti prepagati + API) oppure Evertreen o Ecologi | 0,35–1,5 € ad albero; si parte con 100–150 € di crediti |
| Certificato automatico | Placid (~19 $/mese, 500 crediti) o APITemplate.io (piano gratuito da 50 PDF/mese; piani a pagamento da ~9–29 $/mese, fonti discordanti) | 0–19 $/mese |
| Collegamento ordine → API → certificato → email | Make.com o Zapier (piano gratuito o base) | 0–10 €/mese |
| Mappa | link alla pagina del progetto o dell'albero del partner, oppure mappa statica (OpenStreetMap) nel certificato | 0 € |
| Testi legali (privacy, cookie, termini) | generatore a pagamento (per esempio iubenda) | ~30–100 €/anno (da verificare) |
| Grafica | Canva (piano gratuito o Pro) | 0–12 €/mese |

## 6. Automazione

**Si automatizza davvero**
- checkout e pagamento;
- webhook dell'ordine → Make → chiamata API "plant tree" al partner, con nome del destinatario e dedica;
- generazione del certificato PDF con nome, dedica, specie, progetto, link e QR code di verifica;
- invio email al cliente o al destinatario, anche programmato, per esempio il 25/12 alle 8:00;
- email di aggiornamento periodiche che rimandano alla pagina del partner.

**Resta manuale**
- ricaricare i crediti del partner e controllare che gli ordini via API siano andati a buon fine (gli errori API capitano);
- assistenza clienti, per esempio "quando vedo la foto?" o "dov'è il mio albero?";
- gestione delle campagne pubblicitarie e dei contenuti social;
- controllo periodico dei progetti, perché claim e progetti devono restare veri;
- eventuali ordini B2B: preventivi, fatture, certificati multipli.

**Ore realistiche** [stima Luca]
- avvio: **35–50 ore**, di cui l'integrazione API più i test sono la parte più "da smanettoni";
- a regime fuori stagione: **2–4 ore a settimana**;
- da metà novembre al 24 dicembre: **8–12 ore a settimana**, soprattutto pubblicità e assistenza.

## 7. Budget di avvio (massimo 1.000 €)

| Voce | € |
|---|---|
| Dominio (.it o .com) | 15 |
| Shopify Basic per 3 mesi (o WooCommerce + hosting per 12 mesi) | 100 |
| Make.com e strumento certificati (Placid o APITemplate) per 3 mesi | 90 |
| Credito prepagato per gli alberi (circa 100–150 alberi) | 150 |
| Testi legali e privacy | 60 |
| Grafica e modello del certificato (Canva Pro o grafico su Fiverr) | 50 |
| Ordini di prova e test | 20 |
| **Pubblicità Natale 2026**: ~80 € di test tra il 1° e il 20 novembre (Black Friday e Giornata nazionale degli alberi del 21/11), poi ~370 € dal 1° al 23 dicembre su Meta (Reels, Stories) con messaggio "regalo dell'ultimo minuto, consegna immediata" | 450 |
| Riserva per imprevisti (API, eventuale app Shopify) | 65 |
| **Totale** | **1.000** |

## 8. Tempo al primo euro e ricavi realistici

- **Primo euro:** 2–4 settimane, cioè sito pronto tra fine ottobre e inizio novembre e prime vendite alla rete personale. Le prime vendite pagate arrivano verosimilmente con il Black Friday o a dicembre.
- **Scenari** [stima Luca]. Ipotesi: scontrino medio 18 €, margine lordo ~85% prima della pubblicità, CAC 20–35 € a pagamento.

| Scenario | 3 mesi (fino a metà gennaio 2027): fatturato | 3 mesi: utile dopo pubblicità | 12 mesi: fatturato |
|---|---|---|---|
| Pessimistico | 15–25 ordini, ~300–450 € | negativo (−300 / −450 €) | 600–1.200 € |
| Realistico | 60–120 ordini, ~1.100–2.200 € | ~0–500 € | 3.000–6.000 € (picchi: Natale, San Valentino, Giornata della Terra 22/4, Festa della Mamma, lauree) |
| Ottimistico | 250+ ordini più 1–2 aziende (100–500 alberi a 3–5 € ciascuno) | 5.000–8.000 € di fatturato, ~2.500–4.000 € di utile | 15.000–25.000 € |

Lo scenario ottimistico richiede quasi sempre il B2B, che è vendita attiva e non "lavoro zero".

## 9. Rischi principali

1. **Greenwashing e nuove regole dal 27/9/2026:** un claim sbagliato ("impatto zero", "compensa", bollino auto-creato) è una pratica commerciale scorretta. Le sanzioni AGCM sono un rischio reale, non teorico.
2. **Margine "visibile":** il cliente può scoprire che l'albero costa 0,35–1,5 € dal fornitore, con effetti su recensioni e reputazione. Va gestito con trasparenza e valore aggiunto vero.
3. **CAC:** con un prezzo sotto i 20 € la pubblicità a freddo rischia di non ripagarsi.
4. **Dipendenza dal partner:** cambio di prezzi o condizioni d'uso, chiusura dell'API, progetto fallito, link di verifica che smettono di funzionare.
5. **Concorrenza** di Treedom (marchio italiano forte) e di partner che vendono direttamente al consumatore.

## 10. La versione migliore e sostenibile

**"Il regalo-albero onesto e tracciabile, per occasioni specifiche".**
- Un solo partner con **tracciamento del singolo albero** (Evertreen o Tree-Nation, a seconda della specie e del progetto) e **link di verifica pubblico** stampato sul certificato con QR code.
- **Prezzo trasparente** ("X € vanno alla piantumazione") e **nessun claim CO₂ o "impatto zero"**: si comunicano solo fatti verificabili (specie, luogo, partner, quando viene piantato).
- **Prodotti per occasione**, con certificati di design forte e testi per destinatario: "Un albero per la nascita di…", "In memoria di…", "Bomboniera albero" (B2C ad alto valore emotivo e scontrino medio più alto con pacchetti da 5–20 alberi per matrimoni ed eventi).
- **Consegna istantanea o programmata** come vantaggio per il "regalo dell'ultimo minuto" del 24 dicembre.
- **Un canale B2B leggero**: pagina "regala alberi ai tuoi clienti" per piccole aziende locali, con preventivo standard da form.
- Prima di partire: **conferma scritta del partner** sulla rivendita e **revisione dei testi** da parte di un legale o di un'associazione di categoria, alla luce del d.lgs. 30/2026.

---

# IDEA 2: "Sito regalo: compra o dedica una stella"

## 1. Come si guadagna

**Modello.** Si vende un pacchetto con "nome della stella" a scelta, certificato, mappa del cielo con la stella evidenziata, coordinate e a volte un'app o pagina per "trovarla". La stella è una stella reale presa da un catalogo pubblico. Il "nome" vive solo nel database privato del venditore.

**Prezzi dei concorrenti**
- Pacchetti solo digitali: **20–40 $**. Kit stampati: **50–100 $**. Kit premium con cornice: **100–190 $** [fonte debole: thepricer.org].
- Fonti italiane: **25–190 €** (Trend-Online), **10–150 €** (BusinessOnline).
- OSR (Online Star Register, osr.org, molto citato in Italia): **73–126 €** nel 2022 [fonte debole: dato datato].

**Costi per ordine (versione solo digitale)** [stima Luca]
- pagamento: ~0,55–0,70 €;
- generazione di certificato e mappa: ~0,05–0,10 € (Placid o APITemplate; la mappa può essere generata con librerie open source come d3-celestial, che usano cataloghi stellari pubblici; riferimento non verificato in questa sessione);
- totale costo variabile: **< 1 €**.

Con un prezzo di 19,90–29,90 € il **margine lordo prima della pubblicità è ~95%**. Una versione stampata con stampa on-demand aggiungerebbe circa 10–20 € più spedizione, con il rischio di consegna in ritardo per Natale: meglio solo digitale con PDF "stampabile a casa".

**Come per gli alberi, il collo di bottiglia è il CAC.** Con un CPC di 0,50 € e una conversione dell'1,5% servono ~33 € per ordine, cioè un pareggio solo con prezzi di 30 € o più, oppure con traffico organico.

## 2. Prove di domanda ed esempi reali

- Un titolo di BusinessOnline parla di **"2 milioni di certificati l'anno"** venduti nel mondo: **non verificabile**, fonte del numero sconosciuta e articolo non consultabile.
- **OSR:** TrustScore Trustpilot ~4,5/5 con ~160–175 recensioni per versione nazionale. È un volume modesto, ma segnala un'attività reale e duratura [verificato: Trustpilot].
- **International Star Registry (ISR):** attiva da decenni e citata da Focus, TechCrunch e Space.com come principale operatore. Nessun dato di fatturato pubblico trovato.
- **Stagionalità** [auto-dichiarato]: il general manager di un'azienda del settore dice che gli acquisti hanno picchi **a Natale e a San Valentino** (Almanac). Anche fonti divulgative più vecchie osservano pubblicità concentrata su quelle ricorrenze.
- **Dato mancante:** volumi di ricerca italiani per "regalare una stella" e "comprare una stella". Da controllare su Google Trends prima di investire. Esistono molte pagine-FAQ italiane come "quanto costa comprare una stella alla NASA?", segno di curiosità di ricerca persistente.

## 3. Concorrenza e saturazione

- **Internazionale: molto alta e "vecchia".** ISR, OSR (multilingue, anche in italiano), Star Registry e decine di cloni. Su Etsy e nei negozi online c'è un'offerta enorme di **"mappe del cielo personalizzate"**, il prodotto affine. Marchi noti come The Night Sky o Mapiful **non sono stati verificati** in questa ricerca.
- **Italia:** OSR presidia le ricerche italiane, a cui si aggiungono siti italiani più piccoli e i venditori Etsy.
- Il SEO è difficile: le prime pagine sono piene di articoli "è una truffa?" (Focus, Space.com, Star Walk, Starlust) che **frenano la conversione** e spingono i clienti a cercare garanzie.

## 4. Regole, consumatori e partner

**Posizione IAU [verificato].** L'Unione Astronomica Internazionale dice che i "nomi" venduti dalle aziende **"non hanno alcuna validità formale o ufficiale"** e che l'IAU **"si dissocia completamente"** dalla pratica commerciale di "vendere" nomi di stelle fittizi. I nomi ufficiali li assegna solo il suo Working Group on Star Names (WGSN). In più non esiste proprietà possibile sui corpi celesti: va ricordato al cliente, senza bisogno di citare norme specifiche.

**Casi legali e sanzioni noti**
- **New York, 1998:** il Department of Consumer Affairs della città di New York (commissario Jules Polonetsky) ha contestato all'**International Star Registry** una **pratica commerciale ingannevole**. L'azienda ha continuato aggiungendo avvertenze in piccolo [fonte secondaria: MEL Magazine; il dato è citato da più fonti].
- **UE, 2019:** la Commissione di ricorso dell'**EUIPO** ha respinto il marchio **"Mystar Global Star Registry"** perché **ingannevole** per il consumatore: la parola "registry" fa pensare a un registro ufficiale [Novagraaf].
- **Italia (AGCM) e Regno Unito (ASA):** nelle mie ricerche **non ho trovato** provvedimenti specifici sul naming di stelle. Non è una prova che non esistano.
- Un caso italiano analogo: l'AGCM ha chiesto che un bollino di "certificazione" commerciale spieghi chiaramente cosa garantisce davvero (caso "Zero Truffe", GreenMe). Il principio si applica pari pari a un "certificato di stella".

**Cosa è rischioso** (Codice del Consumo, artt. 21–23 su azioni e omissioni ingannevoli; riferimento normativo non riconsultato in questa sessione)
- "Registrazione **ufficiale**", "registro **internazionale**", "**riconosciuto** da…", "depositato presso la Biblioteca/l'Osservatorio…", "**comprare**/**possedere** una stella", "la stella è tua per sempre", loghi o sigilli simili a enti scientifici, accenni alla NASA. "Registro" nel nome del marchio è già stato giudicato ingannevole dall'EUIPO.
- **Omissione ingannevole:** mettere l'avvertenza solo nelle FAQ o in piccolo, come ha fatto ISR, non basta a stare tranquilli. Deve essere visibile **prima dell'acquisto**.
- **Lutti e memoria** ("dedica una stella a chi non c'è più"): domanda forte ma clienti vulnerabili. Serve trasparenza massima e niente pressione commerciale.
- "Per sempre": se il sito chiude, il "nome" sparisce. Si può promettere solo "finché il servizio è attivo", oppure dare al cliente un PDF completo e autonomo.

**Formulazione onesta consigliata**, visibile in pagina prodotto, nel checkout e sul certificato: *"Regalo simbolico. La dedica è registrata solo nel nostro archivio privato e non ha valore scientifico né ufficiale. L'Unione Astronomica Internazionale non riconosce nomi commerciali e nessuno può possedere una stella. La stella indicata è reale: queste sono le sue coordinate e la sua designazione di catalogo."* Il prodotto va chiamato **"Dedica una stella"** o **"Il tuo cielo"**, non "Compra una stella" né "Registro".

**Piattaforme.** Le policy pubblicitarie di Meta e Google vietano i contenuti fuorvianti (Google con la policy "Misrepresentation"): annunci che dicono "compra una stella ufficiale" possono essere rifiutati, e il rischio di blocco dell'account va verificato. Nei pagamenti il rischio vero sono gli **storni "not as described"**: un disclaimer chiaro, accettato con una spunta al checkout, è anche la migliore difesa. Nessun partner esterno è necessario, quindi **non c'è rischio di affidabilità dei partner**, a parte gli strumenti software.

## 5. Strumenti e costi per partire

| Funzione | Opzione | Costo indicativo |
|---|---|---|
| Negozio | Shopify Basic (29–39 $/mese) oppure WooCommerce (~5–10 €/mese); per prodotti digitali semplici anche piattaforme come Payhip o Gumroad, che trattengono una percentuale (da verificare) | 0–39 $/mese |
| Campi personalizzati (nome, dedica, data, luogo) | Shopify: app gratuita o economica di "product options"; WooCommerce: plugin | 0–10 $/mese |
| Scelta della stella | foglio con alcune migliaia di stelle reali da un catalogo pubblico (per esempio Hipparcos o Yale Bright Star; dati liberi), assegnate in sequenza da Make | 0 € (lavoro una tantum) |
| Mappa del cielo | immagine di costellazione pre-generata per ogni costellazione (circa 88 template) con la stella evidenziata; oppure generatore da data e luogo con d3-celestial (richiede codice) o un'API astronomica (da verificare) | 0–20 $/mese |
| Certificato PDF | Placid (~19 $/mese) o APITemplate.io (piano gratuito da 50 PDF/mese) | 0–19 $/mese |
| Automazione | Make.com | 0–10 €/mese |
| Pagina "trova la tua stella" | pagina statica con coordinate e link a Stellarium Web (gratuito) | 0 € |
| Testi legali | generatore (per esempio iubenda) | ~30–100 €/anno |

## 6. Automazione

**Si automatizza davvero (quasi al 100%)**
- ordine e pagamento;
- assegnazione automatica della stella successiva dal foglio;
- generazione di certificato e mappa in PDF;
- email di consegna immediata o programmata;
- pagina pubblica di "verifica dedica" nel nostro database, se la vogliamo.

**Resta manuale**
- assistenza: "non vedo la stella a occhio nudo" (molte stelle vendute sono troppo deboli per essere viste senza telescopio, come notano i critici); "è ufficiale?"; richieste di rimborso;
- moderazione dei nomi offensivi;
- pubblicità e social.

**Ore realistiche** [stima Luca]
- avvio: **25–40 ore**;
- a regime: **1–3 ore a settimana**;
- picchi di Natale e San Valentino: **6–10 ore a settimana**.

## 7. Budget di avvio (massimo 1.000 €)

| Voce | € |
|---|---|
| Dominio | 15 |
| Shopify Basic per 3 mesi (o WooCommerce + hosting per 12 mesi) | 100 |
| App opzioni prodotto, Make e Placid/APITemplate per 3 mesi | 90 |
| Grafica di certificato e mappe (Canva Pro o grafico su Fiverr) | 80 |
| Testi legali, privacy e termini, più **un'ora di revisione legale dei claim** (raccomandata) | 160 |
| **Pubblicità Natale 2026**: ~80 € di test a novembre, poi ~370 € dal 1° al 23 dicembre su Meta (Reels, Stories), puntando sul regalo dell'ultimo minuto con consegna immediata | 450 |
| Riserva, da tenere per San Valentino 2027 (14/2) | 105 |
| **Totale** | **1.000** |

## 8. Tempo al primo euro e ricavi realistici

- **Primo euro:** 1–3 settimane. È più veloce dell'albero perché non c'è nessun partner da integrare.
- **Scenari** [stima Luca]. Ipotesi: prezzo medio 24 €, margine lordo ~95%, CAC 20–40 €.

| Scenario | 3 mesi (fino a metà gennaio 2027): fatturato | 3 mesi: utile dopo pubblicità | 12 mesi: fatturato |
|---|---|---|---|
| Pessimistico | 10–20 ordini, ~250–500 € | negativo (−200 / −400 €) | 500–1.000 € |
| Realistico | 50–100 ordini, ~1.200–2.400 € | ~200–900 € | 3.000–5.000 € (Natale, San Valentino, compleanni) |
| Ottimistico | 250+ ordini con un contenuto social diventato virale | ~4.000–6.000 € di utile | 10.000–15.000 € |

Senza pubblicità e SEO le vendite crollano fuori stagione: il business è fortemente stagionale.

## 9. Rischi principali

1. **Pubblicità ingannevole e reputazione.** Il prodotto "nome di una stella" è intrinsecamente vicino all'inganno: ci sono stati il caso di New York del 1998, la decisione EUIPO del 2019 e una posizione IAU netta. Un disclaimer debole espone a segnalazioni AGCM, storni e recensioni "truffa".
2. **Rifiuto degli annunci** su Meta e Google per contenuti fuorvianti, se la comunicazione non è prudente.
3. **Saturazione:** concorrenti con decenni di SEO e migliaia di mappe del cielo su Etsy.
4. **Stagionalità:** gran parte dei ricavi si concentra in circa 6–8 settimane all'anno.
5. **Rischio etico** nel segmento lutto e memoria.

## 10. La versione migliore e sostenibile

**"Il tuo cielo": mappa del cielo reale più dedica simbolica dichiarata.**
- Il prodotto principale è **vero e verificabile**: la mappa astronomica del cielo visto da un luogo in una data (nascita, primo appuntamento, matrimonio), con costellazioni e stelle reali, più la **designazione di catalogo** della stella "dedicata".
- La "dedica" è venduta esplicitamente come **gesto simbolico** con il testo onesto del §4, e il prodotto **non si chiama "registro" né "acquisto"**.
- **Solo digitale, consegna istantanea**, come regalo dell'ultimo minuto a Natale e a San Valentino.
- **Valore aggiunto reale:** guida "come trovarla stasera" con link a Stellarium Web, scelta di una stella **visibile a occhio nudo** dal luogo indicato (differenziante rispetto ai concorrenti che vendono stelle invisibili) e frase o poesia personalizzata.
- **Eventuale estensione futura:** collaborazione con osservatori o planetari italiani per una serata osservativa abbinata. Diventa un'esperienza reale, ma non è automatizzabile.

---

# Confronto rapido (vista di Luca)

| | Albero | Stella |
|---|---|---|
| Costo variabile per ordine | 1–2 € (partner più pagamento) | < 1 € |
| Margine lordo prima della pubblicità | ~85–89% | ~95% |
| Prezzo tipico di mercato | 15–70 € (Treedom); 0,35–15 € (Tree-Nation diretto) | 20–190 € |
| Complessità tecnica | media (API del partner) | bassa o media |
| Rischio legale | **alto da settembre 2026** (green claims) ma gestibile con fatti verificabili | **alto per natura del prodotto**, gestibile solo con disclaimer molto chiari |
| Dipendenza da terzi | alta (partner di piantumazione) | bassa |
| Ore a settimana a regime | 2–4 | 1–3 |
| Valore percepito ed etico | alto, se trasparente | basso o medio ("è una bufala?"), salvo la versione "mappa del cielo" |

---

## Fonti

**Albero: partner, prezzi, API**
- https://kb.tree-nation.com/knowledge/tree-pricing
- https://kb.tree-nation.com/knowledge/tree-planting-for-companies?hsLang=en
- https://kb.tree-nation.com/knowledge/species-plans
- https://kb.tree-nation.com/knowledge/become-an-ambassador?hsLang=en
- https://kb.tree-nation.com/knowledge/my-tree-certificate
- https://kb.tree-nation.com/knowledge/tree-gift
- https://learn.microsoft.com/en-us/connectors/treenationip/
- https://apps.shopify.com/tree-nation/reviews
- https://apps.shopify.com/ecologi
- https://learn.microsoft.com/en-us/connectors/ecologiip/
- https://learn.microsoft.com/en-us/connectors/digitalhumaniip/
- https://cyclr.com/blog/how-can-we-automate-offsetting-our-carbon-footprint-with-a-raas
- https://www.thegoodapi.com/blog/best-tree-planting-apis-for-developers/
- https://www.evertreen.com/news/evertreen-vs-tree-nation
- https://www.evertreen.com/news/evertreen-vs-treedom
- https://www.evertreen.com/news/evertreen-vs-ecologi
- https://www.evertreen.com/videos/how-much-does-corporate-tree-planting-cost-mvt7tn
- https://forbes.it/2024/10/10/evertreen-accompagna-aziende-verso-sostenibilita/
- https://webgains.com/advertiser-spotlight-ecologi/
- https://getlasso.co/affiliate/ecologi/
- https://www.revshare.so/programs/advertiser/ecologi-fcf1fbd8
- https://getlasso.co/affiliate/treedom-uk/

**Albero: Treedom e domanda**
- https://sublimemagazine.com/a-present-for-today-s-climate/
- https://www.greenme.it/lifestyle/spesa-sostenibile/san-valentino-albero/
- https://www.greenme.it/?p=837553
- https://www.altroconsumo.it/vita-privata-famiglia/vivere-sostenibile/speciali/intervista-federico-garcea
- https://sp-edge.com/companies/223727
- https://www.aics.gov.it/wp-content/uploads/2024/07/AICS-AID-012313_02_2-1.pdf
- https://www.tecnoandroid.it/news/treedom-gli-obiettivi-di-sostenibilita-ambientale-raggiunti-nel-2021-sono-eccezionali-1101124/

**Albero: norme anti-greenwashing**
- https://www.qualenergia.it/articoli/italia-recepisce-nuova-direttiva-europea-anti-greenwashing/
- https://certifico.com/ambiente/documenti-ambiente/green-claims-guida-sintetica-alla-nuova-direttiva-europea-2024-825-ue
- https://dwfgroup.com/it-it/news-and-insights/insights/2026/2/empowering-consumers-for-the-green-transition
- https://www.shippypro.com/blog/it/en/the-green-claims-directive-greenwashing-obligations-from-september-27-2026
- https://gs1it.org/files/sharing/1784907498/4217/gs1-italy-volantino-nuove-regole-comunicazione-ambientale.pdf
- https://eur-lex.europa.eu/eli/dir/2024/825/oj (testo della direttiva, riferimento normativo; non consultato direttamente in questa sessione)

**Stella**
- https://www.iau.org/Iau/Science/What-we-do/Buying-Stars-and-Star-Names.aspx
- https://iauarchive.eso.org/public/themes/buying_star_names/
- https://melmagazine.com/en-us/story/star-registry-scam
- https://novagraaf.com/jp/node/970
- https://www.focus.it/scienza/spazio/cose-linternational-star-registry
- https://www.trend-online.com/lusso/regalare-stella-costi-siti-affidabili/
- https://www.businessonline.it/news/il-business-dei-certificati-di-propriet-di-stelle-che-non-si-possono-possedere-eppure-se-ne-vendono-2-milioni-lanno_n86164.html
- https://www.thepricer.org/how-much-does-it-cost-to-buy-a-star/
- https://at.trustpilot.com/review/www.osr.org
- https://pt.trustpilot.com/review/starregistry.com
- https://www.almanac.com/can-you-really-name-star
- https://techcrunch.com/2011/02/08/looking-for-the-perfect-valentines-day-gift-dont-buy-your-loved-one-a-star
- https://www.space.com/naming-star-is-it-worth-money
- https://starwalk.space/en/news/can-i-buy-a-star
- https://www.greenme.it/?p=849158 (caso AGCM sul bollino di "certificazione", come analogia)

**Strumenti, pagamenti, pubblicità (comuni alle due idee)**
- https://sellfy.com/it/blog/prezzi-shopify/
- https://www.trendtrack.io/it/blog-post/quanto-costa-shopify-per-vendita-2026
- https://m8d.io/it/quanto-costa-shopify/
- https://community.shopify.com/t/calcolo-commissioni-totali/23487
- https://gappsy.com/tools/apitemplate-io/
- https://templated.io/blog/top-placid-alternatives-for-image-generation/
- https://www.emarketer.com/content/industry-kpis--meta-ads-show-widening-cpc-gap-between-retail-ecommerce
- https://influee.co/it/blog/good-cpc-facebook-ads
- https://topgrowthmarketing.com/ecommerce-ads-cpc-benchmarks/
- https://www.triplewhale.com/blog/google-ads-black-friday.md
- https://github.com/ofrohn/d3-celestial (libreria open source per mappe del cielo; riferimento non verificato in questa sessione)
