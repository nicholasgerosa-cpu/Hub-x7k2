#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEAM AGENTI - 10 agenti AI che lavorano con Ollama (in locale, gratis) per
trovare il modo migliore di monetizzare partendo da un budget di 1000 euro.

Il team lavora a "giri" fino alla scadenza (di default: lunedì alle 09:00):
  1. 5 ideatori propongono idee nuove, ognuno con un focus diverso a ogni giro
  2. 4 valutatori (finanza, critica, legale/fiscale, marketing) le giudicano
  3. le migliori vengono migliorate, incrociate e rivalutate (evoluzione)
  4. il CEO tira le somme, orienta il giro successivo e scrive i piani operativi

Tutto viene salvato nella cartella dei risultati dopo ogni passo: se il PC si
riavvia basta rilanciare lo script e riprende da dove era rimasto.
Apri report.html in qualunque momento per vedere la classifica aggiornata.

Uso:
  python team_agenti.py                       # parte o riprende, fino a lunedì 09:00
  python team_agenti.py --minuti 15           # prova breve (cartella separata)
  python team_agenti.py --modello gemma3:12b  # sceglie il modello
  python team_agenti.py --fino-a "2026-10-12 08:00"
  python team_agenti.py --solo-report         # rigenera il report senza usare l'AI

Richiede solo Python 3.8+ e Ollama acceso. Nessun pip install.
"""

import argparse
import csv
import html
import json
import os
import random
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

BUDGET_EURO = 1000
CARTELLA_SCRIPT = Path(__file__).resolve().parent

# Usato se manca profilo.txt accanto allo script.
PROFILO_PREDEFINITO = """\
Siamo una persona/piccolo team che oggi vive in Italia. Abbiamo un PC con Ollama (AI in locale, gratis),
competenze digitali di base-intermedie e circa 10-15 ore a settimana da dedicare.
Vogliamo iniziare a guadagnare in fretta, con rischio contenuto, senza lasciare il lavoro attuale.
Siamo aperti anche a operare senza sede fiscale in Italia (clienti internazionali, attività gestibile da
qualunque paese, eventuale trasferimento all'estero), ma solo in modo pienamente legale.
"""

REGOLE_COMUNI = """\
Regole del team:
- Rispondi sempre in italiano, SOLO con un oggetto JSON valido che rispetta lo schema richiesto, senza testo prima o dopo.
- Sii concreto e specifico: numeri, prezzi in euro, canali, piattaforme e strumenti reali. Niente frasi generiche.
- Solo idee legali, etiche e realistiche: niente schemi piramidali/MLM, trading o scommesse, cripto speculative, contenuti ingannevoli o promesse di guadagno facile.
- Operare senza sede fiscale in Italia è ammesso solo se è legale: chi risiede fiscalmente in Italia paga le tasse in Italia su tutto il reddito, ovunque lo guadagni, e una società estera gestita di fatto dall'Italia è considerata italiana (esterovestizione). Niente società di comodo, prestanome o IVA non versata.
- Il team non ha accesso a internet: cifre e norme sono stime da verificare, trattale come tali."""

# Ogni agente ha un compito: un campo in cui cercare modi legali di monetizzare (fase 1, ricerca).
# Quelli con valuta=True giudicano anche le idee degli altri dal proprio punto di vista e scrivono la loro
# parte degli studi di fattibilità (fase 2). Roberto dirige, incrocia le idee e tira le somme.
AGENTI = {
    "matteo": dict(nome="Matteo", ruolo="Ricerca di mercato e trend", temp=0.9, valuta=True, compito=(
        "nicchie emergenti e bisogni non soddisfatti, in Italia e all'estero, scoperti analizzando trend, "
        "domanda, concorrenza e prezzi"), sistema=(
        "Sei Matteo, analista di mercato e cacciatore di trend. Individui nicchie emergenti e bisogni nuovi prima "
        "che diventino affollati, e ragioni su chi compra, quanto è grande la domanda, chi sono i concorrenti, "
        "che prezzi praticano e cosa li distingue. Progetti test rapidi ed economici per verificare la domanda "
        "con clienti veri (pagine di prenotazione, preordini, interviste) prima di investire.")),
    "marco": dict(nome="Marco", ruolo="Prodotti digitali e AI", temp=0.9, compito=(
        "prodotti digitali e strumenti basati su AI e automazione (template, guide, mini-corsi, micro-SaaS, "
        "automazioni) venduti in tutto il mondo tramite piattaforme che incassano e gestiscono l'IVA per conto "
        "tuo (merchant of record), sfruttando anche l'AI locale (Ollama)"), sistema=(
        "Sei Marco, esperto di prodotti digitali, AI e automazione: template, guide, mini-corsi, micro-SaaS, "
        "app no-code, automazioni (n8n, Make, script) e modelli AI locali (Ollama). Pensi a prodotti che si creano "
        "una volta e si vendono molte volte, anche in inglese e in altri mercati, senza promesse irrealistiche.")),
    "luca": dict(nome="Luca", ruolo="E-commerce internazionale", temp=0.9, compito=(
        "commercio online senza magazzino in casa: marketplace internazionali (Etsy, Amazon, eBay), "
        "print-on-demand, prodotti di nicchia con logistica affidata a terzi"), sistema=(
        "Sei Luca, esperto di commercio online: marketplace internazionali, print-on-demand, logistica affidata "
        "a terzi, prodotti di nicchia. Ragioni sempre su margini, resi, logistica e regole delle piattaforme.")),
    "paolo": dict(nome="Paolo", ruolo="CFO", temp=0.8, valuta=True, compito=(
        f"modelli a ricavi ricorrenti e alto margine (abbonamenti, contratti mensili, licenze) che rendono il "
        f"massimo dai {BUDGET_EURO} euro"), sistema=(
        "Sei Paolo, CFO prudente e concreto. Stimi costi, ricavi, margini e tempi con numeri realistici "
        "(spesso più bassi di quanto sperano gli altri). Il budget massimo è vincolante.")),
    "chiara": dict(nome="Chiara", ruolo="Avvocata del diavolo", temp=0.85, valuta=True, compito=(
        "monetizzazione a basso rischio: portare in nuovi paesi o lingue modelli di business già collaudati altrove"),
        sistema=(
        "Sei Chiara, l'avvocata del diavolo del team. Trovi i punti deboli: concorrenza, domanda inesistente, "
        "dipendenza da piattaforme, rischi nascosti, ipotesi ottimistiche. Sei severa ma giusta: riconosci "
        "anche quando un'idea è solida.")),
    "andrea": dict(nome="Andrea", ruolo="Legale e fiscale internazionale", temp=0.8, valuta=True, compito=(
        "attività pensate per essere gestite legalmente anche senza sede fiscale in Italia (da remoto, clienti "
        "internazionali), con la forma giuridica corretta e le condizioni perché sia legale"), sistema=(
        "Sei Andrea, consulente legale e fiscale con esperienza italiana e internazionale. Conosci partita IVA e "
        "regime forfettario, residenza fiscale delle persone (iscrizione AIRE, giorni di presenza, centro degli "
        "interessi), residenza delle società ed esterovestizione, società estere (es. Estonia, Irlanda, Regno "
        "Unito, USA), convenzioni contro le doppie imposizioni, IVA OSS per i servizi digitali in UE, piattaforme "
        "merchant of record, GDPR, diritto d'autore e regole dei marketplace. Distingui sempre ciò che è legale "
        "da ciò che è elusione o evasione.")),
    "francesca": dict(nome="Francesca", ruolo="Growth marketer", temp=0.9, valuta=True, compito=(
        "monetizzare un pubblico online: contenuti, newsletter, community, affiliazioni e sponsorizzazioni, "
        "anche in più lingue"), sistema=(
        "Sei Francesca, growth marketer. Ragioni su come trovare i primi 10 clienti paganti in modo concreto ed "
        "economico: canali, messaggi, costo di acquisizione, passaparola. Diffidi delle idee che 'si venderanno "
        "da sole'.")),
    "valentina": dict(nome="Valentina", ruolo="Responsabile comunicazione", temp=0.9, valuta=True, compito=(
        "attività in cui la comunicazione è il vantaggio: brand di contenuti, servizi di comunicazione per "
        "aziende, personal branding, contenuti in più lingue"), sistema=(
        "Sei Valentina, responsabile della comunicazione. Trasformi un'idea in un messaggio chiaro: nome, "
        "posizionamento, promessa in una frase, tono di voce, contenuti e testi di lancio. Riconosci quando "
        "un'offerta è difficile da spiegare e sai renderla immediata, senza promesse ingannevoli.")),
    "giorgio": dict(nome="Giorgio", ruolo="Responsabile operativo", temp=0.85, valuta=True, compito=(
        "attività semplici da gestire, con processi ripetibili, strumenti già pronti e fornitori esterni"),
        sistema=(
        "Sei Giorgio, responsabile operativo. Valuti cosa serve davvero per far funzionare un'attività ogni "
        "settimana: attività, ore, strumenti, fornitori, competenze. Smascheri le idee che sembrano semplici ma "
        "richiedono molto più tempo o lavoro di quanto si pensi.")),
    "roberto": dict(nome="Roberto", ruolo="CEO", temp=0.7, compito=(
        "servizi e affari con le aziende, in Italia e all'estero: servizi erogabili da remoto, partnership, "
        "intermediazione, rivendita di servizi di terzi con il proprio marchio (white label)"), sistema=(
        "Sei Roberto, CEO del team. Hai visione d'insieme, decidi su cosa puntare, combini le idee migliori e "
        "trasformi le idee in piani operativi eseguibili da subito. Conosci bene le piccole e medie imprese e i "
        "servizi per cui pagano subito. Sei pragmatico e orientato al primo incasso.")),
}
IDEATORI = list(AGENTI)
VALUTATORI = [k for k, a in AGENTI.items() if a.get("valuta")]
TEMPERATURA_VALUTAZIONE = 0.3

# chiave: (etichetta, peso, significato del voto per i valutatori)
DIMENSIONI = {
    "velocita": ("Velocità primo incasso", 0.14, "10 = primo incasso entro 1-2 settimane; 1 = oltre 6 mesi"),
    "potenziale": ("Potenziale di guadagno", 0.14, "10 = può arrivare a migliaia di euro al mese entro un anno; 1 = poche decine di euro"),
    "budget": ("Sostenibile col budget", 0.10, f"10 = si avvia con molto meno di {BUDGET_EURO} euro; 1 = il budget non basta"),
    "domanda": ("Domanda reale", 0.12, "10 = la gente già cerca e paga per questo; 1 = domanda solo ipotetica"),
    "concorrenza": ("Spazio sul mercato", 0.06, "10 = pochi concorrenti forti o un vantaggio netto su di loro; 1 = mercato saturo e senza differenze"),
    "rischio": ("Rischio basso", 0.10, "10 = si rischia poco e ci si può fermare senza perdite; 1 = alto rischio di perdere tutto"),
    "acquisizione": ("Facilità a trovare clienti", 0.09, "10 = canali chiari ed economici per arrivare ai clienti; 1 = non si sa come raggiungerli"),
    "comunicazione": ("Chiarezza del messaggio", 0.06, "10 = si spiega in una frase e il cliente capisce subito perché comprare; 1 = difficile da spiegare"),
    "facilita": ("Fattibilità operativa", 0.08, "10 = gestibile da 1 persona part-time con strumenti già pronti; 1 = serve un team o moltissime ore"),
    "legale": ("Semplicità legale/fiscale", 0.04, "10 = nessun adempimento particolare; 1 = licenze o autorizzazioni complesse"),
    "sede": ("Gestibile senza sede in Italia", 0.07, "10 = si gestisce legalmente da qualunque paese, con clienti internazionali; 1 = legata a un luogo o a licenze italiane"),
}
COMPETENZE = {
    "matteo": ["domanda", "concorrenza"],
    "paolo": ["velocita", "potenziale", "budget"],
    "chiara": ["rischio", "domanda"],
    "andrea": ["legale", "sede"],
    "francesca": ["acquisizione"],
    "valentina": ["comunicazione"],
    "giorgio": ["facilita"],
}
LISTA = {"type": "array", "items": {"type": "string"}}
EXTRA_VALUTAZIONE = {
    "matteo": ({"concorrenti": LISTA, "come_validare": {"type": "string"}},
               "- concorrenti: i principali concorrenti o le alternative che il cliente usa oggi, uno per voce\n"
               "- come_validare: un test economico da fare in 7 giorni con clienti veri per capire se la domanda c'è"),
    "paolo": ({"investimento_iniziale_euro": {"type": "number"}, "utile_mese3_euro": {"type": "number"}},
              "- investimento_iniziale_euro: quanto serve davvero per partire (numero in euro)\n"
              "- utile_mese3_euro: utile netto realistico al mese, al terzo mese (numero, può essere 0)"),
    "chiara": ({"rischi_principali": LISTA},
               "- rischi_principali: i 3 rischi più seri, uno per voce"),
    "andrea": ({"legale_ok": {"type": "boolean"}, "struttura_consigliata": {"type": "string"},
                "adempimenti": LISTA},
               "- legale_ok: true se l'idea, fatta come descritta, è legale; false se è illegale o si regge su "
               "elusione o evasione\n"
               "- struttura_consigliata: forma giuridica e paese da cui operare in modo legale (es. partita IVA "
               "forfettaria in Italia; oppure, solo con residenza fiscale reale all'estero, ditta o società nel "
               "paese di residenza) e le condizioni perché resti legale\n"
               "- adempimenti: cosa serve dal punto di vista legale e fiscale (es. partita IVA, IVA OSS, privacy, "
               "licenze), uno per voce"),
    "francesca": ({"canale_principale": {"type": "string"}, "primo_cliente": {"type": "string"}},
                  "- canale_principale: il canale migliore per vendere\n"
                  "- primo_cliente: come trovare concretamente il primo cliente pagante entro 2 settimane"),
    "valentina": ({"messaggio": {"type": "string"}},
                  "- messaggio: l'offerta spiegata al cliente in una frase, come la scriveresti in un annuncio"),
    "giorgio": ({"ore_settimana": {"type": "number"}, "cosa_serve": LISTA},
                "- ore_settimana: ore di lavoro a settimana necessarie a regime (numero)\n"
                "- cosa_serve: strumenti, fornitori e competenze necessari, uno per voce"),
}

# Ogni agente riceve a ogni giro un segmento e un vincolo a caso: evita che il team giri in tondo.
SEGMENTI = [
    "bar, ristoranti e B&B", "studi professionali (commercialisti, avvocati, dentisti)",
    "artigiani e produttori locali", "piccole aziende europee che vendono online", "clienti negli Stati Uniti",
    "nomadi digitali e lavoratori da remoto", "italiani che vivono all'estero",
    "aziende straniere che vogliono vendere in Italia", "chi all'estero ama il made in Italy (cucina, moda, design)",
    "chi studia l'italiano o ama la cultura italiana", "turisti stranieri in Italia", "studenti universitari",
    "genitori con figli piccoli", "anziani e le loro famiglie", "proprietari di cani e gatti",
    "appassionati di sport e outdoor", "gamer e appassionati di tecnologia", "creator e piccoli brand internazionali",
    "piccoli e-commerce già avviati", "startup e software house", "freelance di tutta Europa",
    "collezionisti (carte, vinili, vintage)", "insegnanti e formazione online", "chi cerca lavoro o cambia carriera",
    "piccole aziende manifatturiere che esportano", "professionisti in Svizzera, Germania o Regno Unito",
]
VINCOLI = [
    "primo incasso entro 7 giorni", "zero magazzino", "ricavi ricorrenti (abbonamento o contratto mensile)",
    "testabile spendendo meno di 100 euro", "sfrutta come vantaggio un PC con AI locale (Ollama)",
    "vendibile online in tutto il mondo", "gestibile da qualunque paese con un portatile",
    "incassi tramite piattaforme che gestiscono pagamenti e IVA", "si gestisce in 10 ore a settimana",
    "scalabile senza assumere", "si basa su competenze che si imparano in 2 settimane", "margine lordo sopra il 60%",
    "sfrutta una ricorrenza o stagionalità dei prossimi 3 mesi",
]

CAMPI_IDEA = ["titolo", "descrizione", "cliente_target", "mercato", "modello_ricavi", "prezzo_indicativo",
              "primo_passo"]
SCHEMA_IDEA = {
    "type": "object",
    "properties": {c: {"type": "string"} for c in CAMPI_IDEA},
    "required": CAMPI_IDEA,
}
SCHEMA_IDEE = {"type": "object", "properties": {"idee": {"type": "array", "items": SCHEMA_IDEA}}, "required": ["idee"]}
ISTRUZIONI_IDEA = """\
Per ogni idea:
- titolo: nome breve e specifico (massimo 10 parole)
- descrizione: cosa si vende, come funziona e perché ora (3-5 frasi)
- cliente_target: chi paga, descritto in modo preciso
- mercato: in quali paesi si vende e se si può gestire da qualunque paese o solo dall'Italia
- modello_ricavi: come entrano i soldi (una tantum, abbonamento, commissione...)
- prezzo_indicativo: prezzo al cliente in euro
- primo_passo: la prima azione concreta da fare lunedì"""

SCHEMA_DIREZIONE = {
    "type": "object",
    "properties": {
        "commento": {"type": "string"},
        "direzione": {"type": "string"},
        "da_evitare": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["commento", "direzione", "da_evitare"],
}
# Fase 2: lo studio di fattibilità. Ogni specialista scrive la sua parte (nell'ordine), poi Roberto tira le
# somme. Campi: nome -> (tipo, istruzione). Tipi: testo, numero, lista, budget.
GIUDIZI = ["fattibile", "fattibile_con_condizioni", "non_fattibile"]
SEZIONI_FATTIBILITA = [
    ("mercato", "matteo", "Mercato e domanda", {
        "clienti_tipo": ("testo", "chi compra esattamente e perché"),
        "dimensione_mercato": ("testo", "stima di quanti potenziali clienti ci sono e quanto spendono"),
        "concorrenti": ("lista", "concorrenti o alternative, ognuno con il suo punto debole"),
        "differenziazione": ("testo", "perché dovrebbero scegliere noi"),
        "test_di_validazione": ("lista", "test con clienti veri da fare nei primi 7 giorni, ognuno con la soglia "
                                         "che dice se ha funzionato"),
    }),
    ("operativa", "giorgio", "Fattibilità operativa", {
        "attivita_settimanali": ("lista", "cosa bisogna fare ogni settimana"),
        "ore_settimana": ("numero", "ore di lavoro a settimana a regime"),
        "strumenti": ("lista", "strumenti e servizi da usare, con il costo mensile"),
        "competenze_mancanti": ("lista", "cosa bisogna imparare o affidare a qualcuno"),
    }),
    ("economica", "paolo", "Fattibilità economica", {
        "allocazione_budget": ("budget", f"come spendere al massimo {BUDGET_EURO} euro, voce per voce, lasciando "
                                         "una riserva"),
        "costi_mensili_euro": ("numero", "costi fissi al mese"),
        "prezzo_e_margine": ("testo", "prezzo di vendita e margine per ogni vendita"),
        "utile_mese3_euro": ("numero", "utile netto realistico al mese, al terzo mese"),
        "utile_mese12_euro": ("numero", "utile netto realistico al mese, dopo un anno"),
        "pareggio": ("testo", "quando si recuperano i soldi investiti"),
        "scenario_pessimistico": ("testo", "cosa succede se le vendite sono la metà del previsto"),
    }),
    ("legale", "andrea", "Fattibilità legale e fiscale", {
        "forma_giuridica": ("testo", "forma giuridica consigliata e da quale paese operare"),
        "adempimenti": ("lista", "adempimenti fiscali e legali, uno per voce"),
        "costi_legali_euro": ("numero", "costi per aprire e gestire la forma giuridica il primo anno"),
        "senza_sede_in_italia": ("testo", "se e a quali condizioni si può gestire legalmente senza sede fiscale "
                                          "in Italia"),
    }),
    ("comunicazione", "valentina", "Comunicazione", {
        "nomi_proposti": ("lista", "3 possibili nomi per il progetto"),
        "messaggio_chiave": ("testo", "la promessa al cliente in una frase"),
        "tono": ("testo", "tono di voce e stile"),
        "contenuti_di_lancio": ("lista", "i contenuti da pubblicare nelle prime 2 settimane, con il canale"),
        "testo_di_lancio": ("testo", "un breve testo pronto da usare per presentare l'offerta (post o pagina)"),
    }),
    ("clienti", "francesca", "Come trovare i clienti", {
        "canali": ("lista", "canali per trovare clienti, in ordine di priorità"),
        "primi_10_clienti": ("testo", "come trovare concretamente i primi 10 clienti paganti"),
        "costo_acquisizione": ("testo", "quanto costa trovare un cliente"),
        "offerta_di_lancio": ("testo", "l'offerta per convincere i primi clienti"),
    }),
    ("rischi", "chiara", "Rischi e piano B", {
        "rischi": ("lista", "i rischi principali, ognuno con il modo di ridurlo"),
        "criterio_di_stop": ("testo", "quando fermarsi senza spendere altro"),
        "piano_b": ("testo", "cosa fare se non funziona"),
    }),
]
CHIAMATE_STUDIO = len(SEZIONI_FATTIBILITA) + 1
TIPI_SCHEMA = {
    "testo": {"type": "string"}, "numero": {"type": "number"}, "lista": LISTA,
    "budget": {"type": "array", "items": {"type": "object", "properties": {
        "voce": {"type": "string"}, "euro": {"type": "number"}}, "required": ["voce", "euro"]}},
}
SCHEMA_SINTESI_STUDIO = {
    "type": "object",
    "properties": {
        "motivazione": {"type": "string"},
        "condizioni": LISTA,
        "piano_4_settimane": {"type": "array", "items": {
            "type": "object", "properties": {"settimana": {"type": "integer"}, "obiettivo": {"type": "string"},
                                             "azioni": LISTA},
            "required": ["settimana", "obiettivo", "azioni"]}},
        "primi_passi": LISTA,
        "kpi": LISTA,
        "verifiche_da_fare": LISTA,
        "esito": {"type": "string", "enum": GIUDIZI},
    },
    "required": ["motivazione", "condizioni", "piano_4_settimane", "primi_passi", "kpi", "verifiche_da_fare",
                 "esito"],
}
ETICHETTE = {
    "utile_mese3_euro": "Utile al mese (3° mese)", "utile_mese12_euro": "Utile al mese (dopo un anno)",
    "primi_10_clienti": "Primi 10 clienti", "senza_sede_in_italia": "Senza sede fiscale in Italia",
    "legale_ok": "È legale", "investimento_iniziale_euro": "Investimento iniziale", "kpi": "KPI",
}
SCHEMA_VERDETTO = {
    "type": "object",
    "properties": {
        "idea_consigliata": {"type": "string"},
        "perche": {"type": "string"},
        "cosa_fare_lunedi": {"type": "array", "items": {"type": "string"}},
        "come_operare_legalmente": {"type": "string"},
        "piano_b": {"type": "string"},
        "avvertenze": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["idea_consigliata", "perche", "cosa_fare_lunedi", "come_operare_legalmente", "piano_b",
                 "avvertenze"],
}

GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre",
        "ottobre", "novembre", "dicembre"]
PAROLE_VUOTE = set("""di da in con su per tra fra il lo la gli le un uno una del della dei delle degli al alla
ai alle dal dalla nel nella sul sulla che the of and for your you con come non piu tuo tua chi""".split())


# ============================================================================
# UTILITA'
# ============================================================================

def data_estesa(dt):
    return f"{GIORNI[dt.weekday()]} {dt.day} {MESI[dt.month - 1]} {dt.year}, ore {dt:%H:%M}"


def leggi_testo(nome, predefinito=""):
    """Legge un file di testo accanto allo script; le righe che iniziano con # sono commenti."""
    percorso = CARTELLA_SCRIPT / nome
    try:
        try:
            righe = percorso.read_text(encoding="utf-8-sig").splitlines()
        except UnicodeDecodeError:  # file salvato dal Blocco note in "ANSI"
            righe = percorso.read_text(encoding="cp1252").splitlines()
    except OSError:
        return predefinito
    testo = "\n".join(r for r in righe if not r.lstrip().startswith("#")).strip()
    return testo or predefinito


def parole(testo):
    t = unicodedata.normalize("NFKD", (testo or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return {w for w in re.findall(r"[a-z0-9]+", t) if len(w) > 2 and w not in PAROLE_VUOTE}


def simili(a, b, soglia=0.5):
    pa, pb = parole(a), parole(b)
    if not pa or not pb:
        return False
    return len(pa & pb) / len(pa | pb) >= soglia


def numero(x):
    """Converte 1200, '1.200 euro', '€ 1200,50' in float; None se non è un numero."""
    if isinstance(x, bool) or x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).replace("€", "").replace("euro", "").strip()
    m = re.search(r"-?\d[\d.,]*", s)
    if not m:
        return None
    s = m.group(0)
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif s.count(".") > 1 or re.fullmatch(r"-?\d{1,3}\.\d{3}", s):
        s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


def voto(x):
    n = numero(x)
    if n is None:
        return None
    return max(1.0, min(10.0, n))


def lista_testi(x):
    if isinstance(x, list):
        return [str(v).strip() for v in x if str(v).strip()][:8]
    if isinstance(x, str) and x.strip():
        return [x.strip()]
    return []


def media(valori):
    valori = [v for v in valori if v is not None]
    return sum(valori) / len(valori) if valori else None


def euro(x):
    if x is None:
        return "-"
    return f"{x:,.0f} €".replace(",", ".")


def estrai_json(testo):
    testo = re.sub(r"<think>.*?</think>", "", testo or "", flags=re.S).strip()
    testo = re.sub(r"^```(?:json)?\s*|\s*```$", "", testo)
    try:
        return json.loads(testo)
    except ValueError:
        pass
    inizio, fine = testo.find("{"), testo.rfind("}")
    if inizio != -1 and fine > inizio:
        try:
            return json.loads(testo[inizio:fine + 1])
        except ValueError:
            pass
    return None


def conforme(dati, schema):
    """Controllo leggero: struttura e campi obbligatori (i tipi semplici vengono corretti dopo)."""
    tipo = schema.get("type")
    if dati is None and tipo is not None:
        return False
    if tipo == "object":
        if not isinstance(dati, dict):
            return False
        if any(k not in dati for k in schema.get("required", [])):
            return False
        return all(conforme(dati[k], s) for k, s in schema.get("properties", {}).items() if k in dati)
    if tipo == "array":
        return isinstance(dati, list) and all(conforme(v, schema.get("items", {})) for v in dati)
    if tipo in ("number", "integer"):
        return numero(dati) is not None
    return not isinstance(dati, (dict, list)) or tipo is None


def booleano(x):
    if isinstance(x, bool):
        return x
    testo = str(x).strip().lower()
    if testo in ("true", "si", "sì", "yes", "vero", "1"):
        return True
    if testo in ("false", "no", "falso", "0"):
        return False
    return None


def normalizza(x, schema):
    """Porta una risposta del modello al tipo previsto dallo schema."""
    tipo = schema.get("type")
    if tipo in ("number", "integer"):
        return numero(x)
    if tipo == "boolean":
        return booleano(x)
    if tipo == "array":
        if schema.get("items", {}).get("type") == "object":
            return [{k: normalizza(v.get(k), s) for k, s in schema["items"]["properties"].items()}
                    for v in (x if isinstance(x, list) else []) if isinstance(v, dict)]
        return lista_testi(x)
    return "" if x is None else str(x).strip()


def giudizio(x):
    testo = str(x or "").lower().replace(" ", "_")
    if "non" in testo:
        return "non_fattibile"
    if "condizion" in testo:
        return "fattibile_con_condizioni"
    return "fattibile" if "fattibile" in testo else None


def etichetta(campo):
    if campo in ETICHETTE:
        return ETICHETTE[campo]
    euro_finale = campo.endswith("_euro")
    testo = (campo[:-5] if euro_finale else campo).replace("_", " ").capitalize()
    return testo + (" (€)" if euro_finale else "")


def testo_campo(x):
    if isinstance(x, bool):
        return "sì" if x else "no"
    if isinstance(x, float):
        return f"{x:,.0f}".replace(",", ".")
    if isinstance(x, list):
        return "; ".join(testo_campo(v) for v in x)
    if isinstance(x, dict):
        return " ".join(testo_campo(v) for v in x.values())
    return "" if x is None else str(x)


def studio_aggiornato(idea):
    f = idea.get("fattibilita")
    return bool(f) and f.get("versione") == idea["versione"]


def esito_studio(idea):
    return idea["fattibilita"]["sintesi"].get("esito") if studio_aggiornato(idea) else None


def pulisci_idea(d):
    return {c: str(d.get(c, "")).strip()[:1500] for c in CAMPI_IDEA}


def formatta_idea(idea):
    return (f"Titolo: {idea['titolo']}\n"
            f"Descrizione: {idea['descrizione']}\n"
            f"Cliente target: {idea['cliente_target']}\n"
            f"Mercato: {idea.get('mercato', '')}\n"
            f"Come guadagna: {idea['modello_ricavi']}\n"
            f"Prezzo indicativo: {idea['prezzo_indicativo']}\n"
            f"Primo passo: {idea['primo_passo']}")


def punteggio_da(valutazioni):
    """Media pesata dei voti di tutte le valutazioni.
    -> (punteggio 0-100, voti medi, investimento, utile, dubbi_legali)"""
    raccolti = {d: [] for d in DIMENSIONI}
    investimenti, utili = [], []
    for giro in valutazioni:
        for chiave, v in giro.items():
            for d in COMPETENZE.get(chiave, []):
                if v.get("voto_" + d) is not None:
                    raccolti[d].append(v["voto_" + d])
        investimenti.append(giro.get("paolo", {}).get("investimento_iniziale_euro"))
        utili.append(giro.get("paolo", {}).get("utile_mese3_euro"))
    medie = {d: media(v) for d, v in raccolti.items() if v}
    investimento = media(investimenti)
    if investimento is not None and investimento > BUDGET_EURO:
        medie["budget"] = min(medie.get("budget", 1.0), 2.0)
    giudizi = [g.get("andrea", {}).get("legale_ok") for g in valutazioni]
    giudizi = [g for g in giudizi if g is not None]
    dubbi_legali = bool(giudizi) and 2 * giudizi.count(False) >= len(giudizi)
    if not medie:
        return 0.0, {}, investimento, media(utili), dubbi_legali
    peso = sum(DIMENSIONI[d][1] for d in medie)
    su_dieci = sum(medie[d] * DIMENSIONI[d][1] for d in medie) / peso
    punteggio = (su_dieci - 1) / 9 * 100
    if dubbi_legali:
        punteggio *= 0.4
    return round(punteggio, 1), {d: round(v, 1) for d, v in medie.items()}, investimento, media(utili), dubbi_legali


def aggiorna_punteggio(idea):
    (idea["punteggio"], idea["voti"], idea["investimento"], idea["utile_mese3"],
     idea["dubbi_legali"]) = punteggio_da(idea["valutazioni"])
    if esito_studio(idea) == "non_fattibile":  # bocciata dallo studio di fattibilità: lascia il posto alle altre
        idea["punteggio"] = round(idea["punteggio"] * 0.5, 1)


# ============================================================================
# OLLAMA
# ============================================================================

class ErroreOllama(Exception):
    pass


class Ollama:
    def __init__(self, url, contesto, timeout):
        self.url = url.rstrip("/")
        self.modello = None
        self.contesto = contesto
        self.timeout = timeout
        self.formato = "schema"  # se Ollama è vecchio scende a "json" e poi a "testo"
        self.pensiero = True  # invia think=false (più veloce sui modelli "thinking")
        # Ollama è in locale: ignora eventuali proxy di sistema.
        self.apri = urllib.request.build_opener(urllib.request.ProxyHandler({})).open
        self.ultima_durata = 0.0
        self.ultimi_token = 0

    def _richiesta(self, percorso, dati=None, timeout=30):
        corpo = None if dati is None else json.dumps(dati).encode("utf-8")
        req = urllib.request.Request(self.url + percorso, data=corpo, headers={"Content-Type": "application/json"})
        with self.apri(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))

    def modelli(self):
        return self._richiesta("/api/tags").get("models", [])

    def chat(self, sistema, utente, schema, temperatura, max_token):
        attese = [10, 30, 60, 120, 300]
        ultimo_errore = "nessuna risposta"
        attendi = False
        for tentativo in range(len(attese) + 1):
            if tentativo:
                time.sleep(attese[tentativo - 1] if attendi else 1)
            attendi = False
            testo_utente = utente
            if self.formato != "schema":
                testo_utente += "\n\nSchema JSON da rispettare:\n" + json.dumps(schema, ensure_ascii=False)
            corpo = {
                "model": self.modello,
                "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": testo_utente}],
                "stream": False,
                "keep_alive": "30m",
                "options": {"temperature": temperatura, "num_ctx": self.contesto, "num_predict": max_token},
            }
            if self.pensiero:
                corpo["think"] = False
            if self.formato == "schema":
                corpo["format"] = schema
            elif self.formato == "json":
                corpo["format"] = "json"
            inizio = time.time()
            try:
                risposta = self._richiesta("/api/chat", corpo, timeout=self.timeout)
            except urllib.error.HTTPError as e:
                dettaglio = e.read().decode("utf-8", "replace")[:300]
                if e.code == 404:
                    raise ErroreOllama(f"modello non trovato: {dettaglio}")
                if e.code == 400 and "think" in dettaglio.lower() and self.pensiero:
                    self.pensiero = False
                elif e.code == 400 and self.formato != "testo":
                    self.formato = "json" if self.formato == "schema" else "testo"
                    print(f"  (Ollama non accetta questo formato, passo a '{self.formato}': {dettaglio})", flush=True)
                ultimo_errore = f"HTTP {e.code}: {dettaglio}"
                attendi = e.code >= 500
                continue
            except (urllib.error.URLError, OSError) as e:
                ultimo_errore = f"connessione a Ollama fallita: {e}"
                attendi = True
                print(f"  ({ultimo_errore} - riprovo)", flush=True)
                continue
            self.ultima_durata = time.time() - inizio
            self.ultimi_token = (risposta.get("eval_count") or 0) + (risposta.get("prompt_eval_count") or 0)
            dati = estrai_json(risposta.get("message", {}).get("content", ""))
            if dati is not None and conforme(dati, schema):
                return dati
            ultimo_errore = "risposta non in formato JSON corretto"
            temperatura = min(1.0, temperatura + 0.1)
        raise ErroreOllama(ultimo_errore)


def scegli_modello(modelli, richiesto):
    nomi = [m.get("name", "") for m in modelli]
    if richiesto:
        for n in (richiesto, richiesto + ":latest"):
            if n in nomi:
                return n
        raise SystemExit(f"Modello '{richiesto}' non trovato in Ollama.\nDisponibili: {', '.join(nomi) or 'nessuno'}\n"
                         f"Per scaricarlo: ollama pull {richiesto}")
    chat = [m for m in modelli if "embed" not in m.get("name", "").lower() and m.get("size", 0) > 300_000_000]
    if not chat:
        raise SystemExit("Nessun modello di chat in Ollama. Scaricane uno, ad esempio:\n  ollama pull gemma3:12b\n"
                         "(oppure gemma3:4b se il PC non è molto potente)")
    speciali = ("coder", "llava", "vision", "moondream", "math")
    # Il più grande sotto i 12 GB: buon compromesso qualità/velocità per 60 ore di lavoro.
    adatti = [m for m in chat if m["size"] <= 12e9] or [min(chat, key=lambda m: m["size"])]
    adatti.sort(key=lambda m: (any(s in m["name"].lower() for s in speciali), -m["size"]))
    return adatti[0]["name"]


# ============================================================================
# IL TEAM
# ============================================================================

class Team:
    def __init__(self, llm, stato, cartella):
        self.llm = llm
        self.stato = stato
        self.cartella = cartella

    # ---------------------------------------------------------------- utilità
    def log(self, messaggio, diario=False):
        adesso = datetime.now()
        riga = f"[{GIORNI[adesso.weekday()][:3]} {adesso:%H:%M}] {messaggio}"
        print(riga, flush=True)
        with open(self.cartella / "diario.log", "a", encoding="utf-8") as f:
            f.write(riga + "\n")
        if diario:
            self.stato["diario"].append({"ora": datetime.now().isoformat(timespec="minutes"), "testo": messaggio})
            self.stato["diario"] = self.stato["diario"][-300:]

    def salva(self):
        salva_stato(self.cartella, self.stato)

    def scadenza(self):
        return datetime.fromisoformat(self.stato["scadenza"])

    def margine(self):
        """Tempo da tenere per la chiusura: completare gli studi della top 5 e il verdetto."""
        totale = self.scadenza() - datetime.fromisoformat(self.stato["inizio_sessione"])
        s = self.stato
        secondi = s["secondi_ai"] / s["chiamate"] if s["chiamate"] else 30
        mancanti = sum(1 for i in self.classifica()[:5] if not studio_aggiornato(i))
        stima = timedelta(seconds=secondi * (CHIAMATE_STUDIO * mancanti + 2) * 1.2)
        return min(totale * 0.15, max(timedelta(minutes=20), stima))

    def tempo_scaduto(self):
        return datetime.now() >= self.scadenza() - self.margine()

    def fase_fattibilita(self):
        return self.progresso() >= 0.6

    def progresso(self):
        inizio = datetime.fromisoformat(self.stato["inizio_sessione"])
        totale = (self.scadenza() - inizio).total_seconds() or 1
        return max(0.0, min(1.0, (datetime.now() - inizio).total_seconds() / totale))

    def classifica(self):
        valutate = [i for i in self.stato["idee"].values() if i["stato"] == "valutata"]
        return sorted(valutate, key=lambda i: i["punteggio"], reverse=True)

    def nome(self, chiave):
        a = AGENTI.get(chiave, {"nome": chiave, "ruolo": ""})
        return f"{a['nome']} ({a['ruolo']})"

    def contesto(self):
        testo = (f"OGGI: {data_estesa(datetime.now())}\n"
                 f"CHI SIAMO:\n{leggi_testo('profilo.txt', PROFILO_PREDEFINITO)}\n"
                 f"BUDGET MASSIMO DI PARTENZA: {BUDGET_EURO} euro (tutto compreso: strumenti, pubblicità, materiali).\n"
                 "OBIETTIVO: guadagnare soldi veri e legali il prima possibile, poi crescere. Va bene vendere in "
                 "Italia o all'estero; sono un vantaggio le attività gestibili legalmente da qualunque paese.\n")
        direttive = leggi_testo("direttive.txt")
        if direttive:
            testo += f"INDICAZIONI DEL CAPO (priorità massima):\n{direttive}\n"
        return testo

    def chiedi(self, chiave, utente, schema, max_token=2000, temperatura=None):
        a = AGENTI[chiave]
        dati = self.llm.chat(a["sistema"] + "\n\n" + REGOLE_COMUNI, utente, schema,
                             a["temp"] if temperatura is None else temperatura, max_token)
        self.stato["chiamate"] += 1
        self.stato["secondi_ai"] += self.llm.ultima_durata
        self.stato["token"] += self.llm.ultimi_token
        return dati

    def duplicato(self, titolo, escludi=None, extra=()):
        for i in list(self.stato["idee"].values()) + list(extra):
            if i.get("id") != escludi and i.get("stato") != "scartata" and simili(titolo, i["titolo"]):
                return i
        return None

    def crea_idea(self, dati, autore, genitori=None):
        self.stato["contatore"] += 1
        idea = {
            "id": f"I{self.stato['contatore']:04d}", "autore": autore, "giro": self.stato["giro"],
            "creata": datetime.now().isoformat(timespec="minutes"), "versione": 1, "genitori": genitori or [],
            "stato": "da_valutare", "valutazioni": [], "punteggio": None, "voti": {}, "investimento": None,
            "utile_mese3": None, "dubbi_legali": False, "miglioramenti": 0, "tentativi_falliti": 0, "storia": [],
            "fattibilita": None,
        }
        idea.update(pulisci_idea(dati))
        self.stato["idee"][idea["id"]] = idea
        return idea

    # ------------------------------------------------------------ valutazione
    def prompt_valutazione(self, idea, chiave):
        campi, istruzioni = EXTRA_VALUTAZIONE[chiave]
        criteri = "\n".join(f"- voto_{d} (da 1 a 10): {DIMENSIONI[d][2]}" for d in COMPETENZE[chiave])
        return (f"{self.contesto()}\nIDEA DA VALUTARE:\n{formatta_idea(idea)}\n\n"
                f"Valuta l'idea dal punto di vista di: {AGENTI[chiave]['ruolo']}. Sii realistico e severo: "
                "usa tutta la scala da 1 a 10 (5 = nella media, 8 o più solo se davvero convincente).\n"
                f"- analisi: il tuo giudizio in 2-4 frasi\n{istruzioni}\n{criteri}")

    def schema_valutazione(self, chiave):
        campi, _ = EXTRA_VALUTAZIONE[chiave]
        props = {"analisi": {"type": "string"}}
        props.update(campi)
        props.update({"voto_" + d: {"type": "integer"} for d in COMPETENZE[chiave]})
        return {"type": "object", "properties": props, "required": list(props)}

    def valuta(self, idea, autore):
        """Un giro di valutazione completo (tutti i valutatori) -> {chiave_valutatore: risposta normalizzata}.
        Nessuno giudica le proprie idee: in quel caso il punto di vista lo prende Roberto."""
        risultato = {}
        for chiave in VALUTATORI:
            giudice = "roberto" if chiave == autore else chiave
            r = self.chiedi(giudice, self.prompt_valutazione(idea, chiave), self.schema_valutazione(chiave), 1200,
                            temperatura=TEMPERATURA_VALUTAZIONE)
            v = {"analisi": str(r.get("analisi", "")).strip()}
            for d in COMPETENZE[chiave]:
                v["voto_" + d] = voto(r.get("voto_" + d))
            for campo, schema in EXTRA_VALUTAZIONE[chiave][0].items():
                v[campo] = normalizza(r.get(campo), schema)
            if giudice != chiave:
                v["giudice"] = giudice
            risultato[chiave] = v
        return risultato

    def riassunto_valutazioni(self, idea):
        if not idea["valutazioni"]:
            return "(nessuna valutazione)"
        ultima = idea["valutazioni"][-1]
        voti = ", ".join(f"{DIMENSIONI[d][0]} {x}" for d, x in idea.get("voti", {}).items())
        righe = [f"Punteggio complessivo: {idea['punteggio']}/100. Voti: {voti}"]
        for chiave in VALUTATORI:
            v = ultima.get(chiave)
            if not v:
                continue
            extra = "; ".join(f"{etichetta(c)}: {testo_campo(v.get(c))}" for c in EXTRA_VALUTAZIONE[chiave][0]
                              if v.get(c) not in (None, "", []))
            righe.append(f"- {AGENTI[chiave]['nome']} ({AGENTI[chiave]['ruolo']}): {v.get('analisi', '')} [{extra}]")
        return "\n".join(righe)

    def valuta_in_attesa(self):
        for idea in [i for i in self.stato["idee"].values() if i["stato"] == "da_valutare"]:
            if self.tempo_scaduto():
                return
            idea["valutazioni"].append(self.valuta(idea, idea["autore"]))
            aggiorna_punteggio(idea)
            idea["stato"] = "valutata"
            avviso = "  [dubbi di legalità]" if idea["dubbi_legali"] else ""
            self.log(f"  {idea['punteggio']:5.1f}/100  {idea['titolo']}  ({AGENTI[idea['autore']]['nome']}){avviso}")
            self.salva()

    # --------------------------------------------------------------- ideazione
    def ideazione(self, autori, quante):
        classifica = self.classifica()
        migliori = "\n".join(f"- {i['titolo']} ({i['punteggio']:.0f}/100)" for i in classifica[:6]) or "- nessuna ancora"
        recenti = sorted(self.stato["idee"].values(), key=lambda i: i["id"], reverse=True)[:45]
        gia = {i["titolo"] for i in classifica[:15]} | {i["titolo"] for i in recenti}
        bocciate = ""
        if len(classifica) > 8:
            bocciate = "\nPERCHÉ SONO STATE BOCCIATE LE IDEE PEGGIORI (impara dagli errori):\n" + "\n".join(
                f"- {i['titolo']}: {i['valutazioni'][-1].get('chiara', {}).get('analisi', '')[:200]}"
                for i in classifica[-3:])
        direzione = self.stato.get("direzione") or {}
        guida = ""
        if direzione:
            guida = (f"\nDIREZIONE DEL CEO PER QUESTO GIRO: {direzione.get('direzione', '')}\n"
                     f"DA EVITARE: {'; '.join(direzione.get('da_evitare', []))}\n")
        for chiave in autori:
            if self.tempo_scaduto():
                return
            segmento, vincolo = random.choice(SEGMENTI), random.choice(VINCOLI)
            prompt = (f"{self.contesto()}{guida}\n"
                      f"IL TUO COMPITO NEL TEAM: trovare modi legali di monetizzare in questo campo: "
                      f"{AGENTI[chiave]['compito']}.\n"
                      f"FOCUS DI QUESTO GIRO PER TE: clienti = {segmento}; vincolo = {vincolo}.\n"
                      "Resta nel tuo campo; puoi allontanarti dal focus solo se hai un'idea nettamente migliore.\n\n"
                      f"IDEE MIGLIORI FINORA (non ripeterle, ma impara da cosa funziona):\n{migliori}\n"
                      f"{bocciate}\n\nIDEE GIÀ PROPOSTE (NON riproporre idee uguali o simili):\n"
                      + "\n".join(f"- {t}" for t in sorted(gia)) +
                      f"\n\nProponi {quante} idee NUOVE, diverse tra loro e specifiche (non generiche come "
                      f"'aprire un e-commerce' o 'fare consulenza').\n{ISTRUZIONI_IDEA}")
            risposta = self.chiedi(chiave, prompt, SCHEMA_IDEE, 2500)
            nuove = []
            for d in risposta.get("idee", [])[:quante]:
                d = pulisci_idea(d)
                if len(d["titolo"]) < 4:
                    continue
                doppione = self.duplicato(d["titolo"], extra=nuove)
                if doppione:
                    self.stato["doppioni_scartati"] += 1
                    self.log(f"  {AGENTI[chiave]['nome']}: '{d['titolo']}' scartata (simile a '{doppione['titolo']}')")
                    continue
                nuove.append(self.crea_idea(d, chiave))
                self.log(f"  {AGENTI[chiave]['nome']} propone: {d['titolo']}")
            self.salva()

    # --------------------------------------------------------------- evoluzione
    def migliora(self, idea):
        autore = idea["autore"] if idea["autore"] in AGENTI else "roberto"
        prompt = (f"{self.contesto()}\nECCO UN'IDEA DEL TEAM E LE VALUTAZIONI RICEVUTE:\n{formatta_idea(idea)}\n\n"
                  f"{self.riassunto_valutazioni(idea)}\n\n"
                  "Riscrivi l'idea migliorandola: risolvi i rischi principali, rendila più concreta, più veloce da "
                  f"monetizzare e sostenibile con al massimo {BUDGET_EURO} euro. Mantieni l'essenza, oppure fai un "
                  f"pivot se serve davvero. Restituisci UNA sola idea.\n{ISTRUZIONI_IDEA}")
        candidata = pulisci_idea(self.chiedi(autore, prompt, SCHEMA_IDEA, 1500, temperatura=0.7))
        doppione = self.duplicato(candidata["titolo"], escludi=idea["id"])
        if doppione:
            idea["tentativi_falliti"] += 1
            self.log(f"  versione migliorata di '{idea['titolo']}' scartata (uguale a '{doppione['titolo']}')")
            return
        valutazioni = [self.valuta(candidata, autore)]
        nuovo = punteggio_da(valutazioni)[0]
        if nuovo > idea["punteggio"] + 1.5:
            idea["storia"].append({"versione": idea["versione"], "titolo": idea["titolo"],
                                   "punteggio": idea["punteggio"], "giro": self.stato["giro"]})
            idea.update(candidata)
            idea["versione"] += 1
            idea["valutazioni"] = valutazioni
            idea["miglioramenti"] += 1
            idea["tentativi_falliti"] = 0
            vecchio = idea["punteggio"]
            aggiorna_punteggio(idea)
            self.log(f"  migliorata da {AGENTI[autore]['nome']}: '{idea['titolo']}' {vecchio:.0f} -> "
                     f"{idea['punteggio']:.0f} (v{idea['versione']})", diario=True)
        else:
            idea["tentativi_falliti"] += 1
            self.log(f"  tentativo di miglioramento di '{idea['titolo']}' non convincente "
                     f"({nuovo:.0f} vs {idea['punteggio']:.0f})")

    def verifica(self, idea):
        """Seconda (e terza) opinione: i voti di un LLM oscillano, la media rende la classifica affidabile."""
        prima = idea["punteggio"]
        idea["valutazioni"].append(self.valuta(idea, idea["autore"]))
        aggiorna_punteggio(idea)
        self.log(f"  riverificata '{idea['titolo']}': {prima:.0f} -> {idea['punteggio']:.0f} "
                 f"({len(idea['valutazioni'])} valutazioni)")

    def incrocio(self):
        candidati = self.classifica()[:8]
        coppie = [(a, b) for n, a in enumerate(candidati) for b in candidati[n + 1:] if a["autore"] != b["autore"]]
        fatte = {tuple(sorted(i["genitori"])) for i in self.stato["idee"].values() if i["genitori"]}
        coppie = [c for c in coppie if tuple(sorted((c[0]["id"], c[1]["id"]))) not in fatte]
        if not coppie:
            return
        a, b = random.choice(coppie)
        prompt = (f"{self.contesto()}\nIDEA A:\n{formatta_idea(a)}\n\nIDEA B:\n{formatta_idea(b)}\n\n"
                  "Combina il meglio delle due idee in UNA nuova idea ibrida, più forte di entrambe "
                  "(ad esempio lo stesso cliente con un'offerta migliore, o lo stesso prodotto su un canale più "
                  f"efficace).\n{ISTRUZIONI_IDEA}")
        d = pulisci_idea(self.chiedi("roberto", prompt, SCHEMA_IDEA, 1500, temperatura=0.8))
        doppione = self.duplicato(d["titolo"])
        if doppione:
            self.log(f"  incrocio scartato: '{d['titolo']}' simile a '{doppione['titolo']}'")
            return
        idea = self.crea_idea(d, "roberto", [a["id"], b["id"]])
        self.log(f"  Roberto incrocia '{a['titolo']}' + '{b['titolo']}' -> '{idea['titolo']}'", diario=True)
        self.valuta_in_attesa()

    # ------------------------------------------------- fase 2: studio di fattibilità
    def studio_fattibilita(self, idea):
        """Ogni specialista scrive la sua parte dello studio, poi Roberto decide: fattibile o no."""
        self.log(f"Studio di fattibilità: '{idea['titolo']}'")
        base = (f"{self.contesto()}\nIDEA DA STUDIARE:\n{formatta_idea(idea)}\n\nVALUTAZIONI DEL TEAM:\n"
                f"{self.riassunto_valutazioni(idea)}\n")
        sezioni, gia_scritte = {}, ""
        for chiave, autore, titolo, campi in SEZIONI_FATTIBILITA:
            giudice = "roberto" if autore == idea["autore"] else autore
            props = {c: TIPI_SCHEMA[t] for c, (t, _) in campi.items()}
            props.update({"sintesi": {"type": "string"}, "giudizio": {"type": "string", "enum": GIUDIZI}})
            schema = {"type": "object", "properties": props, "required": list(props)}
            prompt = (f"{base}{gia_scritte}\nScrivi la tua parte dello studio di fattibilità: {titolo.upper()}. "
                      "Sii concreto e realistico; dove servono numeri, stimali.\n"
                      + "\n".join(f"- {c}: {istruzione}" for c, (_, istruzione) in campi.items()) +
                      "\n- sintesi: la tua conclusione in 2-3 frasi\n"
                      "- giudizio: fattibile, fattibile_con_condizioni oppure non_fattibile")
            r = self.chiedi(giudice, prompt, schema, 2500, temperatura=0.4)
            if chiave == "economica":
                totale = sum(v.get("euro") or 0 for v in normalizza(r.get("allocazione_budget"), TIPI_SCHEMA["budget"]))
                if totale > BUDGET_EURO:
                    r = self.chiedi(giudice, prompt + f"\n\nATTENZIONE: nella bozza precedente il budget sommava "
                                    f"{totale:.0f} euro, oltre il massimo di {BUDGET_EURO}. Riduci le voci.",
                                    schema, 2500, temperatura=0.4)
            sezione = {c: normalizza(r.get(c), s) for c, s in props.items()}
            sezione["giudizio"] = giudizio(r.get("giudizio")) or "fattibile_con_condizioni"
            sezione["autore"] = giudice
            if chiave == "economica":
                righe = sezione["allocazione_budget"]
                totale = sum(v.get("euro") or 0 for v in righe)
                if totale > BUDGET_EURO:  # ultimo rimedio: riscala in proporzione
                    for v in righe:
                        v["euro"] = round((v.get("euro") or 0) * BUDGET_EURO / totale)
            sezioni[chiave] = sezione
            gia_scritte += f"\nPARTE '{titolo}' ({sezione['giudizio']}): {sezione['sintesi']}"
            self.salva()
        dettagli = "\n\n".join(
            f"{titolo.upper()} - {AGENTI[sezioni[chiave]['autore']]['nome']} ({sezioni[chiave]['giudizio']}):\n"
            + "\n".join(f"- {etichetta(c)}: {testo_campo(sezioni[chiave][c])[:400]}" for c in campi)
            + f"\n- Conclusione: {sezioni[chiave]['sintesi']}"
            for chiave, _, titolo, campi in SEZIONI_FATTIBILITA)
        prompt = (f"{base}\nSTUDIO DI FATTIBILITÀ SCRITTO DAL TEAM:\n{dettagli}\n\n"
                  "Tira le somme come CEO. Sii onesto: se una parte è non fattibile e non si può risolvere, "
                  "l'idea è non fattibile.\n"
                  "- motivazione: perché, in 3-4 frasi\n"
                  "- condizioni: cosa deve essere vero perché funzioni (vuoto se non ce ne sono)\n"
                  "- piano_4_settimane: per le settimane 1-4 un obiettivo misurabile e le azioni\n"
                  "- primi_passi: le prime 5 azioni da fare lunedì, in ordine\n"
                  "- kpi: i numeri da misurare per capire se funziona\n"
                  "- verifiche_da_fare: cosa controllare nel mondo reale prima di spendere (prezzi, concorrenti, "
                  "norme), visto che il team non ha accesso a internet\n"
                  "- esito: fattibile, fattibile_con_condizioni oppure non_fattibile")
        r = self.chiedi("roberto", prompt, SCHEMA_SINTESI_STUDIO, 3000, temperatura=0.4)
        sintesi = {c: normalizza(r.get(c), s) for c, s in SCHEMA_SINTESI_STUDIO["properties"].items()}
        sintesi["esito"] = giudizio(r.get("esito")) or "fattibile_con_condizioni"
        idea["fattibilita"] = {"versione": idea["versione"], "data": datetime.now().isoformat(timespec="minutes"),
                               "sezioni": sezioni, "sintesi": sintesi}
        prima = idea["punteggio"]
        aggiorna_punteggio(idea)
        esito = sintesi["esito"].replace("_", " ").upper()
        self.log(f"  -> {esito}: '{idea['titolo']}'" +
                 (f" (punteggio {prima:.0f} -> {idea['punteggio']:.0f})" if idea["punteggio"] != prima else ""),
                 diario=True)
        self.salva()

    # ------------------------------------------------------------------ regia
    def direzione(self, nuove_del_giro):
        classifica = self.classifica()
        if not classifica:
            return
        top = "\n".join(f"{n}. {i['titolo']} - {i['punteggio']:.0f}/100 ({AGENTI[i['autore']]['nome']})"
                        + (f" - studio di fattibilità: {esito_studio(i)}" if esito_studio(i) else "")
                        for n, i in enumerate(classifica[:8], 1))
        peggiori = sorted(nuove_del_giro, key=lambda i: i["punteggio"] or 0)[:3]
        flop = "\n".join(f"- {i['titolo']} - {i['punteggio']:.0f}/100: "
                         f"{i['valutazioni'][-1].get('chiara', {}).get('analisi', '')[:200]}"
                         for i in peggiori if i["valutazioni"]) or "- nessuna"
        fase = ("2, valutazione di fattibilità (approfondire e rafforzare le migliori)" if self.fase_fattibilita()
                else "1, ricerca del business (trovare idee nuove e promettenti)")
        precedente = (self.stato.get("direzione") or {}).get("direzione", "nessuna")
        prompt = (f"{self.contesto()}\nGiro {self.stato['giro']} concluso. Fase attuale: {fase}. "
                  f"Idee valutate finora: {len(classifica)}.\n\nCLASSIFICA ATTUALE:\n{top}\n\n"
                  f"LE IDEE PEGGIORI DI QUESTO GIRO E PERCHÉ:\n{flop}\n\nDIREZIONE CHE AVEVI DATO: {precedente}\n\n"
                  "Scrivi:\n- commento: 2-3 frasi su come sta andando e cosa sta emergendo\n"
                  "- direzione: istruzioni concrete per gli ideatori per il prossimo giro (su cosa puntare, quali "
                  "territori nuovi esplorare)\n- da_evitare: temi o tipi di idee da non proporre più")
        d = self.chiedi("roberto", prompt, SCHEMA_DIREZIONE, 1200, temperatura=0.5)
        self.stato["direzione"] = {"commento": str(d.get("commento", "")), "direzione": str(d.get("direzione", "")),
                                   "da_evitare": lista_testi(d.get("da_evitare"))}
        self.log(f"Roberto (CEO), giro {self.stato['giro']}: {self.stato['direzione']['commento']}", diario=True)
        self.log(f"  Direzione: {self.stato['direzione']['direzione']}")

    # ------------------------------------------------------------- ciclo
    def giro(self):
        self.stato["giro"] += 1
        consolidamento = self.fase_fattibilita()
        self.stato["fase"] = "2 - valutazione di fattibilità" if consolidamento else "1 - ricerca del business"
        self.log(f"===== GIRO {self.stato['giro']} - fase {self.stato['fase']} - scadenza "
                 f"{data_estesa(self.scadenza())} =====")
        prima = set(self.stato["idee"])

        self.valuta_in_attesa()  # idee rimaste a metà da una sessione interrotta
        if consolidamento:
            self.ideazione(random.sample(IDEATORI, 4), 1)
        else:
            self.ideazione(IDEATORI, 1)
        self.log(f"Valutazione delle nuove idee ({', '.join(AGENTI[k]['nome'] for k in VALUTATORI)}):")
        self.valuta_in_attesa()

        quanti = 3 if consolidamento else 2
        da_studiare = 2 if consolidamento else 1  # in fase 1 si studia solo la prima della classifica
        if not self.tempo_scaduto():
            da_verificare = [i for i in self.classifica()[:10] if len(i["valutazioni"]) < 3][:quanti]
            for idea in da_verificare:
                if self.tempo_scaduto():
                    break
                self.verifica(idea)
                self.salva()
        if not self.tempo_scaduto():
            candidate = [i for i in self.classifica()[:12] if i["tentativi_falliti"] < 3]
            candidate.sort(key=lambda i: (i["miglioramenti"] + i["tentativi_falliti"], -i["punteggio"]))
            for idea in candidate[:quanti]:
                if self.tempo_scaduto():
                    break
                self.migliora(idea)
                self.salva()
        if not self.tempo_scaduto() and len(self.classifica()) >= 4:
            self.incrocio()
            self.salva()
        for _ in range(da_studiare):
            candidate = [i for i in self.classifica()[:5 if consolidamento else 1] if not studio_aggiornato(i)]
            if not candidate or self.tempo_scaduto():
                break
            self.studio_fattibilita(candidate[0])
        if not self.tempo_scaduto():
            self.direzione([self.stato["idee"][k] for k in set(self.stato["idee"]) - prima
                            if self.stato["idee"][k]["stato"] == "valutata"])
        self.salva()
        scrivi_report(self.stato, self.cartella)
        self.stampa_stato()

    def stampa_stato(self):
        s = self.stato
        mancano = self.scadenza() - datetime.now()
        ore = max(0, int(mancano.total_seconds() // 3600))
        media_s = s["secondi_ai"] / s["chiamate"] if s["chiamate"] else 0
        self.log(f"Stato: {len(self.classifica())} idee valutate, {s['chiamate']} chiamate all'AI "
                 f"(~{media_s:.0f}s l'una), mancano ~{ore} ore. Report: {self.cartella / 'report.html'}")
        for n, i in enumerate(self.classifica()[:3], 1):
            self.log(f"  #{n} {i['punteggio']:.0f}/100  {i['titolo']}")

    def chiusura(self):
        self.log("===== TEMPO SCADUTO: chiusura dei lavori =====", diario=True)
        for _ in range(10):  # un'idea bocciata scende e ne entra un'altra nella top 5
            candidate = [i for i in self.classifica()[:5] if not studio_aggiornato(i)]
            if not candidate:
                break
            try:
                self.studio_fattibilita(candidate[0])
            except ErroreOllama as e:
                self.log(f"  studio di '{candidate[0]['titolo']}' non riuscito: {e}")
                break
        classifica = self.classifica()
        if classifica:
            podio = "\n\n".join(
                f"#{n} ({i['punteggio']:.0f}/100)\n{formatta_idea(i)}\n{self.riassunto_valutazioni(i)}"
                + (f"\nSTUDIO DI FATTIBILITÀ: {esito_studio(i)} - {i['fattibilita']['sintesi'].get('motivazione', '')}"
                   if esito_studio(i) else "")
                for n, i in enumerate(classifica[:5], 1))
            prompt = (f"{self.contesto()}\nIl team ha lavorato per tutto il weekend. Ecco le 5 idee migliori:\n\n"
                      f"{podio}\n\nDai il verdetto finale: quale idea avviare lunedì (scegli tra quelle risultate "
                      "fattibili) e perché, le prime azioni da "
                      "fare, come operare legalmente, un piano B e le avvertenze importanti.\n"
                      "- idea_consigliata: il titolo dell'idea\n"
                      "- perche: 3-5 frasi\n- cosa_fare_lunedi: azioni concrete in ordine\n"
                      "- come_operare_legalmente: forma giuridica e paese, e se e a quali condizioni si può "
                      "operare legalmente senza sede fiscale in Italia\n"
                      "- piano_b: cosa fare se l'idea consigliata non funziona entro 30 giorni\n"
                      "- avvertenze: rischi e cose da verificare")
            try:
                self.stato["verdetto"] = self.chiedi("roberto", prompt, SCHEMA_VERDETTO, 2500, temperatura=0.4)
                self.log(f"VERDETTO: {self.stato['verdetto'].get('idea_consigliata')}", diario=True)
            except ErroreOllama as e:
                self.log(f"  verdetto finale non riuscito: {e}")
        self.stato["concluso"] = True
        self.salva()
        scrivi_report(self.stato, self.cartella, finale=True)

    def esegui(self):
        while not self.tempo_scaduto():
            try:
                self.giro()
            except ErroreOllama as e:
                self.salva()
                self.log(f"Problema con Ollama ({e}). Pausa di 2 minuti e poi riprendo.")
                time.sleep(120)
        self.chiusura()


# ============================================================================
# STATO E REPORT
# ============================================================================

def nuovo_stato(modello, scadenza):
    adesso = datetime.now().isoformat(timespec="seconds")
    return {"versione_formato": 1, "creato": adesso, "inizio_sessione": adesso, "scadenza": scadenza.isoformat(),
            "modello": modello, "budget": BUDGET_EURO, "giro": 0, "contatore": 0, "chiamate": 0, "secondi_ai": 0.0,
            "token": 0, "doppioni_scartati": 0, "idee": {}, "diario": [], "direzione": None, "verdetto": None,
            "fase": "1 - ricerca del business", "concluso": False}


# Ruoli accorpati nel passaggio da 13 a 10 agenti.
AGENTI_UNITI = {"giulia": "matteo", "elena": "marco", "sara": "roberto"}


def migra_stato(stato):
    """Aggiunge i campi nuovi alle idee salvate da versioni precedenti dello script."""
    stato.setdefault("fase", "1 - ricerca del business")
    for idea in stato["idee"].values():
        idea.setdefault("mercato", "")
        idea.pop("piano", None)  # i vecchi piani operativi sono sostituiti dagli studi di fattibilità
        idea.pop("piano_versione", None)
        idea.setdefault("fattibilita", None)
        idea["autore"] = AGENTI_UNITI.get(idea["autore"], idea["autore"])
        if idea["autore"] not in AGENTI:
            idea["autore"] = "roberto"
        if idea["valutazioni"]:
            aggiorna_punteggio(idea)
        else:
            idea.setdefault("dubbi_legali", False)
    return stato


def carica_stato(cartella):
    try:
        return json.loads((cartella / "stato.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def salva_stato(cartella, stato):
    tmp = cartella / "stato.json.tmp"
    tmp.write_text(json.dumps(stato, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, cartella / "stato.json")


def classifica_da(stato):
    valutate = [i for i in stato["idee"].values() if i["stato"] == "valutata"]
    return sorted(valutate, key=lambda i: i["punteggio"], reverse=True)


def scrivi_report(stato, cartella, finale=False):
    classifica = classifica_da(stato)
    _scrivi_csv(classifica, cartella / "idee.csv")
    (cartella / "report.md").write_text(_report_md(stato, classifica, finale), encoding="utf-8")
    (cartella / "report.html").write_text(_report_html(stato, classifica, finale), encoding="utf-8")


ESITI = {"fattibile": ("Fattibile", "ok"), "fattibile_con_condizioni": ("Fattibile con condizioni", "cond"),
         "non_fattibile": ("Non fattibile", "no")}
SEZIONE_DI = {autore: titolo for _, autore, titolo, _ in SEZIONI_FATTIBILITA}


def _scrivi_csv(classifica, percorso):
    with open(percorso, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["posizione", "punteggio", "titolo", "proposta da", "giro", "versione", "valutazioni",
                    "fattibilità", "investimento €", "utile/mese al 3° mese €", "legalità", "struttura consigliata",
                    "cliente", "mercato", "come guadagna", "prezzo", "descrizione"])
        for n, i in enumerate(classifica, 1):
            w.writerow([n, i["punteggio"], i["titolo"], AGENTI.get(i["autore"], {}).get("nome", i["autore"]),
                        i["giro"], i["versione"], len(i["valutazioni"]), _esito(i),
                        "" if i["investimento"] is None else round(i["investimento"]),
                        "" if i["utile_mese3"] is None else round(i["utile_mese3"]),
                        "DUBBI" if i.get("dubbi_legali") else "ok", _andrea(i).get("struttura_consigliata", ""),
                        i["cliente_target"], i.get("mercato", ""), i["modello_ricavi"], i["prezzo_indicativo"],
                        i["descrizione"]])


def _andrea(idea):
    return idea["valutazioni"][-1].get("andrea", {}) if idea["valutazioni"] else {}


def _titolo(idea):
    return idea["titolo"] + (" [dubbi di legalità]" if idea.get("dubbi_legali") else "")


def _esito(idea):
    return ESITI[esito_studio(idea)][0] if esito_studio(idea) else ""


def _per_agente(classifica):
    """Per ogni agente: (chiave, dati, numero di idee valutate, idea migliore o None)."""
    righe = []
    for chiave, a in AGENTI.items():
        sue = [i for i in classifica if i["autore"] == chiave]
        righe.append((chiave, a, len(sue), sue[0] if sue else None))
    return righe


def _ruolo_fase2(chiave):
    if chiave in SEZIONE_DI:
        valuta = ", ".join(DIMENSIONI[d][0] for d in COMPETENZE.get(chiave, []))
        return f"valuta {valuta}; nello studio di fattibilità scrive «{SEZIONE_DI[chiave]}»"
    if chiave == "roberto":
        return "dirige il team, incrocia le idee e decide gli esiti degli studi"
    return "migliora le proprie idee in base alle critiche del team"


def _bocciate(classifica):
    return [i for i in classifica if esito_studio(i) == "non_fattibile"]


def _riassunto_numeri(stato, classifica):
    inizio = datetime.fromisoformat(stato["creato"])
    ore = (datetime.now() - inizio).total_seconds() / 3600
    studiate = [i for i in classifica if esito_studio(i)]
    fattibili = len(studiate) - len(_bocciate(classifica))
    return (f"{len(classifica)} idee valutate · {len(studiate)} studi di fattibilità ({fattibili} fattibili) · "
            f"{stato['giro']} giri · {stato['chiamate']} chiamate all'AI · {ore:.1f} ore di lavoro · "
            f"modello {stato['modello']}")


def _valore(campo, tipo, valore):
    if tipo == "numero" and campo.endswith("_euro"):
        return euro(valore)
    return testo_campo(valore)


def _report_md(stato, classifica, finale):
    r = [f"# Team agenti: idee per monetizzare con {euro(stato['budget'])}", "",
         f"{'**REPORT FINALE**' if finale else 'Report intermedio, fase ' + stato.get('fase', '')} · aggiornato "
         f"{data_estesa(datetime.now())}  ", _riassunto_numeri(stato, classifica) + "  ",
         f"Scadenza: {data_estesa(datetime.fromisoformat(stato['scadenza']))}", ""]
    v = stato.get("verdetto")
    if finale and v:
        r += ["## Verdetto del CEO", "", f"**Idea consigliata: {v.get('idea_consigliata', '')}**", "",
              str(v.get("perche", "")), "", "**Cosa fare lunedì:**"]
        r += [f"{n}. {x}" for n, x in enumerate(lista_testi(v.get("cosa_fare_lunedi")), 1)]
        r += ["", f"**Come operare legalmente:** {v.get('come_operare_legalmente', '')}", "",
              f"**Piano B:** {v.get('piano_b', '')}", "", "**Avvertenze:**"]
        r += [f"- {x}" for x in lista_testi(v.get("avvertenze"))] + [""]
    r += ["## Classifica", "", "| # | Punti | Idea | Da | Fattibilità | Investimento | Utile/mese (mese 3) |",
          "|---|---|---|---|---|---|---|"]
    for n, i in enumerate(classifica[:25], 1):
        r.append(f"| {n} | {i['punteggio']:.0f} | {_titolo(i).replace('|', '/')} | "
                 f"{AGENTI.get(i['autore'], {}).get('nome', '')} | {_esito(i) or '-'} | {euro(i['investimento'])} | "
                 f"{euro(i['utile_mese3'])} |")
    if _bocciate(classifica):
        r += ["", "## Bocciate dallo studio di fattibilità", ""]
        r += [f"- **{i['titolo']}**: {i['fattibilita']['sintesi'].get('motivazione', '')}"
              for i in _bocciate(classifica)[:10]]
    r += ["", "## Il lavoro di ciascun agente", "", "| Agente | Compito (fase 1) | Ruolo nella fase 2 | Idee | "
          "La sua idea migliore |", "|---|---|---|---|---|"]
    for chiave, a, quante, migliore in _per_agente(classifica):
        top = f"{migliore['titolo']} ({migliore['punteggio']:.0f})" if migliore else "-"
        r.append(f"| {a['nome']} ({a['ruolo']}) | {a['compito']} | {_ruolo_fase2(chiave)} | {quante} | "
                 f"{top.replace('|', '/')} |")
    r += ["", "## Le 5 migliori in dettaglio", ""]
    for n, i in enumerate(classifica[:5], 1):
        ult = i["valutazioni"][-1] if i["valutazioni"] else {}
        r += [f"### {n}. {_titolo(i)} ({i['punteggio']:.0f}/100)", "", i["descrizione"], "",
              f"- **Cliente:** {i['cliente_target']}", f"- **Mercato:** {i.get('mercato', '')}",
              f"- **Come guadagna:** {i['modello_ricavi']}", f"- **Prezzo:** {i['prezzo_indicativo']}",
              f"- **Primo passo:** {i['primo_passo']}",
              "- **Voti:** " + " · ".join(f"{DIMENSIONI[d][0]} {x}" for d, x in i["voti"].items()), ""]
        for chiave in VALUTATORI:
            val = ult.get(chiave)
            if val:
                extra = "; ".join(f"*{etichetta(c)}:* {testo_campo(val.get(c))}" for c in EXTRA_VALUTAZIONE[chiave][0]
                                  if val.get(c) not in (None, "", []))
                r += [f"**{AGENTI[chiave]['nome']} ({AGENTI[chiave]['ruolo']}):** {val.get('analisi', '')} {extra}", ""]
        r += _studio_md(i)
    r += ["## Diario del team", ""]
    r += [f"- {d['ora'].replace('T', ' ')}: {d['testo']}" for d in reversed(stato["diario"][-30:])]
    return "\n".join(r) + "\n"


def _studio_md(idea):
    if not studio_aggiornato(idea):
        return []
    f = idea["fattibilita"]
    s = f["sintesi"]
    r = [f"#### Studio di fattibilità: {ESITI[s['esito']][0]}", "", f"**Roberto (CEO):** {s.get('motivazione', '')}", ""]
    if s.get("condizioni"):
        r += ["*Condizioni:*"] + [f"- {x}" for x in s["condizioni"]] + [""]
    for chiave, _, titolo, campi in SEZIONI_FATTIBILITA:
        sez = f["sezioni"].get(chiave)
        if not sez:
            continue
        r += [f"**{titolo}** ({AGENTI[sez['autore']]['nome']}, {ESITI[sez['giudizio']][0].lower()}): "
              f"{sez.get('sintesi', '')}", ""]
        for c, (tipo, _) in campi.items():
            valore = sez.get(c)
            if tipo == "budget":
                totale = sum(x.get("euro") or 0 for x in valore or [])
                r += ["", "| Voce | Euro |", "|---|---|"]
                r += [f"| {x.get('voce', '')} | {euro(x.get('euro'))} |" for x in valore or []]
                r += [f"| **Totale** | {euro(totale)} |", ""]
            elif valore not in (None, "", []):
                r.append(f"- *{etichetta(c)}:* {_valore(c, tipo, valore)}")
        r.append("")
    r += ["**Prime 4 settimane:**", ""]
    for w in sorted(s.get("piano_4_settimane", []), key=lambda w: w.get("settimana") or 0):
        r.append(f"- Settimana {testo_campo(w.get('settimana'))}: {w.get('obiettivo', '')} - "
                 + "; ".join(w.get("azioni") or []))
    r += ["", "**Primi passi:**"] + [f"{k}. {x}" for k, x in enumerate(s.get("primi_passi", []), 1)]
    r += ["", f"**KPI:** {'; '.join(s.get('kpi', []))}",
          f"**Da verificare prima di spendere:** {'; '.join(s.get('verifiche_da_fare', []))}", ""]
    return r


CSS = """
:root{--bg:#f6f4ef;--card:#fff;--ink:#1d1b18;--muted:#6b665d;--line:#e4dfd5;--accent:#a8563a;--good:#2f7d4f;
--bar:#ece7dd;--ok-bg:#e3f1e8;--cond:#875800;--cond-bg:#fbefd6;--no:#a3322a;--no-bg:#f8e1df}
@media (prefers-color-scheme:dark){:root{--bg:#161513;--card:#201f1c;--ink:#eeeae2;--muted:#a49e93;
--line:#34322d;--accent:#e08a66;--good:#5cc489;--bar:#2c2a26;--ok-bg:#1d3326;--cond:#e7b54f;--cond-bg:#3a2f17;
--no:#f08a80;--no-bg:#3d201d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:920px;margin:0 auto;padding:24px 16px 64px}h1{font-size:1.6rem;margin:0 0 4px}
h2{font-size:1.2rem;margin:36px 0 12px}h3{margin:0 0 6px;font-size:1.1rem}h4{margin:18px 0 6px}
.meta{color:var(--muted);font-size:.9rem}.card{background:var(--card);border:1px solid var(--line);
border-radius:12px;padding:16px 18px;margin:12px 0}.verdetto{border-color:var(--accent);border-width:2px}
.score{float:right;font-weight:700;font-size:1.3rem;color:var(--accent)}.small{font-size:.9rem;color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:.92rem}td,th{padding:7px 6px;border-bottom:1px solid var(--line);
text-align:left;vertical-align:top}th{color:var(--muted);font-weight:600}.num{text-align:right;white-space:nowrap}
.voti{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:6px 16px;margin:10px 0}
.voto{font-size:.85rem}.barra{height:6px;background:var(--bar);border-radius:3px}
.barra i{display:block;height:6px;border-radius:3px;background:var(--good)}
details{margin-top:10px}summary{cursor:pointer;color:var(--accent);font-weight:600}
ul,ol{padding-left:22px}.tab{overflow-x:auto}.agenti{list-style:none;padding:0;margin:0}
.agenti li{padding:9px 0;border-bottom:1px solid var(--line)}.agenti li:last-child{border-bottom:0}
.esito{display:inline-block;font-size:.78rem;font-weight:600;padding:1px 8px;border-radius:10px;
vertical-align:middle;white-space:nowrap}.esito.ok{background:var(--ok-bg);color:var(--good)}
.esito.cond{background:var(--cond-bg);color:var(--cond)}.esito.no{background:var(--no-bg);color:var(--no)}
"""


def _ul(voci, tag="ul"):
    return f"<{tag}>" + "".join(f"<li>{html.escape(str(x))}</li>" for x in voci) + f"</{tag}>"


def _chip(esito):
    nome, classe = ESITI[esito]
    return f"<span class='esito {classe}'>{html.escape(nome)}</span>"


def _report_html(stato, classifica, finale):
    e = html.escape
    stato_lavori = "<b>REPORT FINALE</b>" if finale else f"Fase {e(stato.get('fase', ''))} · si aggiorna da solo"
    out = [f"<!doctype html><html lang='it'><head><meta charset='utf-8'>"
           f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
           f"{'' if finale else '<meta http-equiv=refresh content=300>'}"
           f"<title>Team agenti - idee</title><style>{CSS}</style></head><body><main>",
           f"<h1>Idee per monetizzare con {e(euro(stato['budget']))}</h1>",
           f"<div class='meta'>{stato_lavori} · {e(data_estesa(datetime.now()))}<br>"
           f"{e(_riassunto_numeri(stato, classifica))}<br>"
           f"Scadenza: {e(data_estesa(datetime.fromisoformat(stato['scadenza'])))}</div>"]
    v = stato.get("verdetto")
    if finale and v:
        out.append(f"<div class='card verdetto'><h2 style='margin-top:0'>Verdetto del CEO</h2>"
                   f"<h3>{e(str(v.get('idea_consigliata', '')))}</h3><p>{e(str(v.get('perche', '')))}</p>"
                   f"<b>Cosa fare lunedì</b>{_ul(lista_testi(v.get('cosa_fare_lunedi')), 'ol')}"
                   f"<p><b>Come operare legalmente:</b> {e(str(v.get('come_operare_legalmente', '')))}</p>"
                   f"<p><b>Piano B:</b> {e(str(v.get('piano_b', '')))}</p>"
                   f"<b>Avvertenze</b>{_ul(lista_testi(v.get('avvertenze')))}</div>")
    if not classifica:
        out.append("<p>Nessuna idea valutata per ora: il team è al lavoro.</p>")
    out.append("<h2>Le migliori</h2>")
    for n, i in enumerate(classifica[:5], 1):
        ult = i["valutazioni"][-1] if i["valutazioni"] else {}
        voti = "".join(f"<div class='voto'>{e(DIMENSIONI[d][0])} <b>{x}</b><div class='barra'>"
                       f"<i style='width:{x * 10:.0f}%'></i></div></div>" for d, x in i["voti"].items())
        pareri = ""
        for chiave in VALUTATORI:
            val = ult.get(chiave)
            if not val:
                continue
            extra = "".join(f"<br><b>{e(etichetta(c))}:</b> {e(testo_campo(val.get(c)))}"
                            for c in EXTRA_VALUTAZIONE[chiave][0] if val.get(c) not in (None, "", []))
            pareri += (f"<p><b>{e(AGENTI[chiave]['nome'])}</b> <span class='small'>{e(AGENTI[chiave]['ruolo'])}"
                       f"</span><br>{e(val.get('analisi', ''))}<span class='small'>{extra}</span></p>")
        chip = (" " + _chip(esito_studio(i))) if esito_studio(i) else ""
        out.append(
            f"<div class='card'><span class='score'>{i['punteggio']:.0f}</span><h3>{n}. {e(_titolo(i))}{chip}</h3>"
            f"<div class='small'>proposta da {e(AGENTI.get(i['autore'], {}).get('nome', ''))} · v{i['versione']} · "
            f"{len(i['valutazioni'])} valutazioni · investimento {e(euro(i['investimento']))} · utile/mese al 3° mese "
            f"{e(euro(i['utile_mese3']))}</div><p>{e(i['descrizione'])}</p>"
            f"<p class='small'><b>Cliente:</b> {e(i['cliente_target'])}<br><b>Mercato:</b> "
            f"{e(i.get('mercato', ''))}<br><b>Come guadagna:</b> {e(i['modello_ricavi'])}<br><b>Prezzo:</b> "
            f"{e(i['prezzo_indicativo'])}<br><b>Primo passo:</b> {e(i['primo_passo'])}<br><b>Struttura legale "
            f"(Andrea):</b> {e(_andrea(i).get('struttura_consigliata', '') or '-')}</p><div class='voti'>{voti}</div>"
            f"<details><summary>Cosa ne pensa il team</summary>{pareri}</details>{_studio_html(i)}</div>")
    if len(classifica) > 5:
        out.append("<h2>Classifica completa</h2><div class='tab'><table><tr><th>#</th><th class='num'>Punti</th>"
                   "<th>Idea</th><th class='num'>Investim.</th><th class='num'>Utile/mese</th></tr>")
        for n, i in enumerate(classifica[5:60], 6):
            chip = (_chip(esito_studio(i)) + " ") if esito_studio(i) else ""
            out.append(f"<tr><td>{n}</td><td class='num'>{i['punteggio']:.0f}</td><td>{e(_titolo(i))}"
                       f"<div class='small'>{chip}{e(i['cliente_target'][:140])}</div></td>"
                       f"<td class='num'>{e(euro(i['investimento']))}</td><td class='num'>{e(euro(i['utile_mese3']))}</td></tr>")
        out.append("</table></div>")
    if _bocciate(classifica):
        out.append("<h2>Bocciate dallo studio di fattibilità</h2><div class='card'><ul class='agenti'>")
        out += [f"<li><b>{e(i['titolo'])}</b><div class='small'>{e(i['fattibilita']['sintesi'].get('motivazione', ''))}"
                f"</div></li>" for i in _bocciate(classifica)[:10]]
        out.append("</ul></div>")
    out.append("<h2>Il lavoro di ciascun agente</h2><div class='card'><ul class='agenti'>")
    for chiave, a, quante, migliore in _per_agente(classifica):
        top = (f"{e(migliore['titolo'])} <b>{migliore['punteggio']:.0f}</b>" if migliore else "nessuna idea valutata")
        out.append(f"<li><b>{e(a['nome'])}</b> · {e(a['ruolo'])}<div class='small'>Fase 1, compito: "
                   f"{e(a['compito'])}<br>Fase 2: {e(_ruolo_fase2(chiave))}"
                   f"</div><div>Migliore: {top} <span class='small'>({quante} idee)</span></div></li>")
    out.append("</ul></div>")
    if stato["diario"]:
        out.append("<h2>Diario del team</h2><div class='card'><ul>")
        out += [f"<li><span class='small'>{e(d['ora'].replace('T', ' '))}</span> {e(d['testo'])}</li>"
                for d in reversed(stato["diario"][-40:])]
        out.append("</ul></div>")
    out.append("<p class='small'>Stime generate da un modello AI locale senza accesso a internet: verifica prezzi, "
               "concorrenza e norme prima di spendere.</p></main></body></html>")
    return "\n".join(out)


def _studio_html(idea):
    if not studio_aggiornato(idea):
        return ""
    e = html.escape
    f = idea["fattibilita"]
    s = f["sintesi"]
    parti = [f"<details open><summary>Studio di fattibilità</summary><p>{_chip(s['esito'])}</p>"
             f"<p><b>Roberto (CEO):</b> {e(s.get('motivazione', ''))}</p>"]
    if s.get("condizioni"):
        parti.append("<b>Condizioni</b>" + _ul(s["condizioni"]))
    for chiave, _, titolo, campi in SEZIONI_FATTIBILITA:
        sez = f["sezioni"].get(chiave)
        if not sez:
            continue
        parti.append(f"<h4>{e(titolo)} {_chip(sez['giudizio'])} <span class='small'>"
                     f"{e(AGENTI[sez['autore']]['nome'])}</span></h4><p>{e(sez.get('sintesi', ''))}</p>")
        for c, (tipo, _) in campi.items():
            valore = sez.get(c)
            if tipo == "budget":
                totale = sum(x.get("euro") or 0 for x in valore or [])
                parti.append("<table>" + "".join(f"<tr><td>{e(x.get('voce', ''))}</td><td class='num'>"
                                                 f"{e(euro(x.get('euro')))}</td></tr>" for x in valore or [])
                             + f"<tr><th>Totale</th><th class='num'>{e(euro(totale))}</th></tr></table>")
            elif tipo == "lista" and valore:
                parti.append(f"<b>{e(etichetta(c))}</b>{_ul(valore)}")
            elif valore not in (None, "", []):
                parti.append(f"<p><b>{e(etichetta(c))}:</b> {e(_valore(c, tipo, valore))}</p>")
    settimane = "".join(f"<li><b>Settimana {e(testo_campo(w.get('settimana')))}:</b> {e(w.get('obiettivo', ''))}"
                        f"{_ul(w.get('azioni') or [])}</li>"
                        for w in sorted(s.get("piano_4_settimane", []), key=lambda w: w.get("settimana") or 0))
    parti.append(f"<h4>Prime 4 settimane</h4><ul>{settimane}</ul><h4>Primi passi lunedì</h4>"
                 f"{_ul(s.get('primi_passi', []), 'ol')}<p><b>KPI:</b> {e('; '.join(s.get('kpi', [])))}</p>"
                 f"<b>Da verificare prima di spendere</b>{_ul(s.get('verifiche_da_fare', []))}</details>")
    return "".join(parti)


# ============================================================================
# AVVIO
# ============================================================================

def prossimo_lunedi_alle_9(adesso):
    giorni = (0 - adesso.weekday()) % 7
    lunedi = adesso.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=giorni)
    return lunedi if lunedi > adesso else lunedi + timedelta(days=7)


def leggi_data(testo):
    for formato in (None, "%d/%m/%Y %H:%M", "%d/%m/%Y"):
        try:
            return datetime.fromisoformat(testo) if formato is None else datetime.strptime(testo, formato)
        except ValueError:
            continue
    raise SystemExit(f"Data non valida: '{testo}'. Usa ad esempio \"2026-10-12 09:00\" o \"12/10/2026 09:00\".")


def impedisci_standby():
    """Evita che il PC vada in sospensione mentre il team lavora."""
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)  # CONTINUOUS | SYSTEM_REQUIRED
            return "standby disattivato finché lo script è in esecuzione"
        except Exception:
            pass
    elif sys.platform == "darwin":
        try:
            subprocess.Popen(["caffeinate", "-i", "-w", str(os.getpid())])
            return "standby disattivato con caffeinate"
        except OSError:
            pass
    return "ricordati di disattivare la sospensione automatica del PC"


def main():
    for flusso in (sys.stdout, sys.stderr):
        try:
            flusso.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser(description="Team di 10 agenti AI (Ollama) che cercano idee per monetizzare.")
    p.add_argument("--modello", help="modello Ollama da usare (default: scelto in automatico)")
    p.add_argument("--fino-a", help='scadenza, es. "2026-10-12 09:00" (default: lunedì prossimo alle 09:00)')
    p.add_argument("--minuti", type=float, help="lavora solo per N minuti (prova)")
    p.add_argument("--cartella", help="dove salvare i risultati (default: risultati_team accanto allo script)")
    p.add_argument("--ollama-url", default="http://localhost:11434")
    p.add_argument("--contesto", type=int, default=8192, help="finestra di contesto in token (default 8192)")
    p.add_argument("--timeout", type=int, default=900, help="secondi massimi per una risposta (default 900)")
    p.add_argument("--solo-report", action="store_true", help="rigenera il report dai dati salvati e termina")
    p.add_argument("--nuovo", action="store_true", help="archivia il lavoro precedente e riparte da zero")
    args = p.parse_args()

    if args.cartella:
        cartella = Path(args.cartella)
    else:
        cartella = CARTELLA_SCRIPT / ("risultati_prova" if args.minuti else "risultati_team")
    cartella.mkdir(parents=True, exist_ok=True)
    stato = carica_stato(cartella)
    if stato:
        migra_stato(stato)

    if args.solo_report:
        if not stato:
            raise SystemExit(f"Nessun lavoro salvato in {cartella}")
        scrivi_report(stato, cartella, finale=stato.get("concluso", False))
        print(f"Report aggiornato: {cartella / 'report.html'}")
        return

    if stato and args.nuovo:
        archivio = cartella / f"stato_archiviato_{datetime.now():%Y%m%d_%H%M}.json"
        os.replace(cartella / "stato.json", archivio)
        print(f"Lavoro precedente archiviato in {archivio}")
        stato = None

    adesso = datetime.now()
    if args.minuti:
        scadenza = adesso + timedelta(minutes=args.minuti)
    elif args.fino_a:
        scadenza = leggi_data(args.fino_a)
    elif stato and not stato.get("concluso"):
        scadenza = datetime.fromisoformat(stato["scadenza"])
    elif stato:
        raise SystemExit("Il lavoro in questa cartella è già concluso (vedi report.html).\n"
                         "Per continuarlo con una nuova scadenza:  --fino-a \"AAAA-MM-GG HH:MM\"\n"
                         "Per ripartire da zero:                   --nuovo")
    else:
        scadenza = prossimo_lunedi_alle_9(adesso)
    if scadenza <= adesso:
        raise SystemExit(f"La scadenza {scadenza:%d/%m/%Y %H:%M} è già passata.")

    llm = Ollama(args.ollama_url, args.contesto, args.timeout)
    try:
        modelli = llm.modelli()
    except (urllib.error.URLError, OSError, ValueError) as e:
        raise SystemExit(f"Non riesco a contattare Ollama su {args.ollama_url} ({e}).\n"
                         "Avvia l'app Ollama (oppure 'ollama serve' in un terminale) e riprova.")
    richiesto = args.modello
    if not richiesto and stato and any(m.get("name") == stato.get("modello") for m in modelli):
        richiesto = stato["modello"]
    llm.modello = scegli_modello(modelli, richiesto)

    if stato is None:
        stato = nuovo_stato(llm.modello, scadenza)
    else:
        if stato.get("concluso") or args.minuti or args.fino_a:
            stato["inizio_sessione"] = adesso.isoformat(timespec="seconds")
        stato["concluso"] = False
        stato["verdetto"] = None
        stato["modello"] = llm.modello
        stato["scadenza"] = scadenza.isoformat()
    salva_stato(cartella, stato)

    print("=" * 72)
    print(f" TEAM AGENTI - {len(AGENTI)} agenti - budget {euro(BUDGET_EURO)} - modello {llm.modello}")
    print("=" * 72)
    for chiave, a in AGENTI.items():
        print(f"  {a['nome']:<10} {a['ruolo']:<32} {a['compito'][:60]}")
    print(f"\n Fase 1:        ricerca del business (60% del tempo): tutti propongono idee nel proprio campo,\n"
          f"                {len(VALUTATORI)} specialisti le valutano, le migliori vengono migliorate e incrociate")
    print(" Fase 2:        valutazione di fattibilità: studi completi sulle migliori, poi il verdetto")
    print(f"\n Lavora fino a: {data_estesa(scadenza)}")
    print(f" Risultati in:  {cartella}")
    print(f" Standby:       {impedisci_standby()}")
    if stato["idee"]:
        print(f" Ripresa:       {len(stato['idee'])} idee già in archivio, giro {stato['giro']}")
    print(" Per fermare:   Ctrl+C (il lavoro resta salvato; rilancia per riprendere)")
    print("=" * 72, flush=True)

    team = Team(llm, stato, cartella)
    try:
        team.esegui()
    except KeyboardInterrupt:
        team.salva()
        scrivi_report(stato, cartella)
        print(f"\nInterrotto. Lavoro salvato: rilancia lo stesso comando per riprendere.\nReport: {cartella / 'report.html'}")
        return
    print(f"\nFatto! Report finale: {cartella / 'report.html'}")


if __name__ == "__main__":
    main()
