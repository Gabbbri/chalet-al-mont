# Chalet al Mont

Esportazione statica completa della versione finale del 13 ottobre 2026.

## Struttura
- `docs/`: sito pronto per GitHub Pages, con HTML, CSS, JavaScript e tutte le foto locali.
- `docs/en/`, `docs/de/`: versioni inglese e tedesca.
- `source-assets/`: fotografie originali e ritoccate conservate alla massima qualità disponibile.
- `scripts/`: generatori delle versioni linguistiche e delle immagini, testi approvati e dizionari.

## Anteprima locale
Dalla directory del progetto:

```sh
python3 -m http.server 8000 --directory docs
```
Apri http://localhost:8000/ . Non aprire gli HTML direttamente con `file://`: il calendario usa moduli JavaScript.

## Pubblicazione
GitHub Pages: branch `main`, cartella `/docs`. Nessuna compilazione o dipendenza Node richiesta.
Repository previsto: `Gabbbri/chalet-al-mont`.
I percorsi delle risorse sono relativi e funzionano anche con un dominio personalizzato.

## Modifiche ai testi
I testi italiani sono in `docs/index.html`; quelli inglesi e tedeschi nelle rispettive cartelle.
Il generatore `python3 scripts/build-languages.py` ricostruisce EN/DE dal dizionario nel file Python.
Aggiorna anche quel dizionario se vuoi che le modifiche sopravvivano alla rigenerazione.

## Servizi esterni
Le foto sono incluse nel repository. Restano esterni Google Fonts, la mappa Google Maps e i collegamenti WhatsApp.
Il modulo apre una bozza WhatsApp per Leonardo: non invia email e non conferma automaticamente la disponibilità.
Il calendario seleziona le date, non legge un calendario di prenotazioni in tempo reale.
