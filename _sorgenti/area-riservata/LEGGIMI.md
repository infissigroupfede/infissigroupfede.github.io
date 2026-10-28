# Area riservata: attivazione su Hostinger

Le pagine sono già nel sito (`/area-riservata/`, `/area-riservata/password/`, `/area-riservata/documenti/`).
Finché il server non è configurato mostrano l'avviso "L'area riservata non è ancora attiva" e i pulsanti restano spenti.
Sull'anteprima GitHub Pages resta sempre così, perché Pages non esegue PHP.

## Come funziona

- Registrazione con nome, cognome, email e password (almeno 10 caratteri), consenso privacy obbligatorio, consenso marketing facoltativo.
- Accesso con email e password; la sessione dura finché il browser resta aperto.
- Password dimenticata: link via email valido un'ora, usabile una volta.
- Documenti: elenco dei file di una cartella fuori da `public_html`, scaricabili solo da chi ha fatto l'accesso (`/api/area/scarica.php`).
- Il server è in `/api/area/` (PHP 8.1+ e MySQL), le pagine usano `/assets/area-riservata.js`.

## Passi su Hostinger (hPanel)

1. **PHP**: Avanzate > Configurazione PHP, versione 8.1 o successiva.
2. **Database**: Database > Database MySQL, crea database e utente. Poi phpMyAdmin > Importa `api/area/schema.sql`.
3. **Email mittente**: Email > crea `noreply@infissigroup.com` (o un'altra casella del dominio).
4. **Configurazione**: con File Manager, in `public_html/api/area/` copia `config.example.php` in `config.php` e compila database, email e sito.
   `config.php` non è nel repo (`.gitignore`) e `.htaccess` lo rende irraggiungibile dal web.
5. **Cartella dei file**: crea `area-riservata-file` accanto a `public_html` (non dentro), per esempio
   `/home/uXXXX/domains/infissigroup.com/area-riservata-file/`. Se il percorso è diverso, correggi `cartella_file` in `config.php`.
   - I file in cima alla cartella compaiono nella sezione "Documenti".
   - Ogni sottocartella è una sezione col suo nome (es. `Cataloghi`, `Schede tecniche`).
   - Il titolo mostrato è il nome del file senza estensione, con trattini e trattini bassi al posto degli spazi: `Catalogo-Finstral-2026.pdf` diventa "Catalogo Finstral 2026".
6. **HTTPS** attivo sul dominio (serve per il cookie di sessione sicuro).

## Prova dopo la messa online

1. Apri `/area-riservata/`: l'avviso "non ancora attiva" non deve comparire.
2. Registrati, controlla di finire su `/area-riservata/documenti/` e di vedere i file.
3. Esci, rientra con email e password.
4. Prova "Password dimenticata?" e controlla che la mail arrivi (anche nello spam).
5. Apri `/api/area/config.php` nel browser: deve rispondere 403.

## Da fare prima della pubblicazione

- **Informativa privacy** (`/privacy/`): aggiungere il trattamento dei dati dell'area riservata (finalità, base giuridica, conservazione). Va scritto o verificato dal consulente privacy.
- Gli iscritti si vedono in phpMyAdmin, tabella `area_utenti` (campo `marketing` = 1 per chi ha dato il consenso alle email).
- Il codice PHP non è stato eseguito in locale (sul computer di sviluppo PHP non c'è): va provato su Hostinger con i passi sopra.
- Le pagine sono generate da `genera.py` sul modello `privacy/index.html`: se cambiano header, footer o stile del sito, rilanciare `python _sorgenti/area-riservata/genera.py`.
