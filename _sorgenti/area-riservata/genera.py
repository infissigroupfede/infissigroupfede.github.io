"""
AREA RISERVATA: genera le tre pagine statiche dal modello privacy/index.html
(stile, header, footer, dialog e script del sito restano identici).

  /area-riservata/            accesso e registrazione
  /area-riservata/password/   recupero e nuova password
  /area-riservata/documenti/  file scaricabili, solo con accesso

Uso: python _sorgenti/area-riservata/genera.py (dalla cartella del sito).
Se cambia il modello, rilanciarlo.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
MODELLO = (ROOT / "privacy" / "index.html").read_text(encoding="utf-8")

CSS = """
/* =====================================================================
   AREA RISERVATA: pannelli bianchi su calce, filetto superiore brand come le schede recensione
   ===================================================================== */
.riservata { padding-block: 0 var(--section-space); }
.riservata__head { display: grid; gap: var(--space-16); max-width: 46ch; margin-block: var(--space-16) clamp(32px, 4vw, 56px); }
.riservata__head h1 { font-size: var(--fs-h1); line-height: 1.08; letter-spacing: -0.02em; }
.riservata__grid { row-gap: var(--space-32); }
.riservata__panel { display: grid; align-content: start; gap: var(--space-24); padding: var(--space-32) var(--space-24); border: 1px solid var(--color-line-calce); border-top: 2px solid var(--color-brand); border-radius: var(--radius); background: var(--color-bg); }
.riservata__panel h2 { font-size: var(--fs-h3); line-height: 1.2; letter-spacing: -0.01em; }
.riservata__panel form { display: grid; gap: var(--space-24); }
.riservata__panel [hidden] { display: none; }
@media (min-width: 768px) { .riservata__panel { padding: var(--space-48) 40px; } }
@media (min-width: 1024px) {
  .riservata__panel--a { grid-column: 1 / span 5; }
  .riservata__panel--b { grid-column: 6 / -1; }
  .riservata__panel--solo { grid-column: 1 / span 7; }
}
.riservata__benefits { display: grid; gap: var(--space-8); }
.riservata__benefits li { display: grid; grid-template-columns: 20px minmax(0, 1fr); gap: var(--space-12); color: var(--color-ardesia); }
.riservata__benefits .icon { width: 20px; height: 20px; margin-top: 3px; color: var(--color-brand); }
.riservata__row { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: var(--space-8) var(--space-24); }
.riservata-alert { display: flex; align-items: flex-start; gap: var(--space-12); padding: var(--space-16); border: 1px solid var(--color-error); border-radius: var(--radius); color: var(--color-error); font-size: var(--fs-small); }
.riservata-alert[hidden] { display: none; }
.riservata-off { display: grid; gap: var(--space-8); margin-bottom: var(--space-32); padding: var(--space-16) var(--space-24); border-left: 2px solid var(--color-brand); background: var(--color-bg); }
.riservata-off[hidden] { display: none; }
.riservata-off p:first-child { font-weight: 600; }
/* Password con pulsante Mostra dentro il campo */
.pw { position: relative; }
.pw .input { padding-right: 96px; }
.pw__toggle { position: absolute; top: 4px; right: 4px; min-width: 80px; min-height: 40px; padding: 0 12px; border: 0; border-radius: var(--radius); background: transparent; color: var(--color-brand); font: 500 0.9375rem var(--font-text); cursor: pointer; }
.pw__toggle:hover { background: var(--color-calce); color: var(--color-brand-dark); }
/* Documenti: righe intere cliccabili con icona, nome, formato e peso, azione a destra */
.riservata__user { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: var(--space-16); margin-bottom: clamp(32px, 4vw, 56px); padding-block: var(--space-16); border-block: 1px solid var(--color-line-calce); }
.riservata__user[hidden] { display: none; }
.docs { display: grid; gap: clamp(40px, 5vw, 64px); }
.docs__title { margin-bottom: var(--space-16); font-size: var(--fs-h3); line-height: 1.2; letter-spacing: -0.01em; }
.docs__list { display: grid; border-top: 1px solid var(--color-line-calce); }
.doc__link { display: grid; grid-template-columns: 24px minmax(0, 1fr) auto; align-items: center; gap: var(--space-16); min-height: 72px; padding: var(--space-16) var(--space-8); border-bottom: 1px solid var(--color-line-calce); color: var(--color-ink); text-decoration: none; transition: background-color var(--dur-fast) var(--ease); }
.doc__link:hover { background: var(--color-bg); }
.doc__icon { width: 24px; height: 24px; color: var(--color-brand); }
.doc__body { display: grid; gap: 2px; }
.doc__name { font-weight: 500; overflow-wrap: anywhere; }
.doc__meta { color: var(--color-ardesia); font-size: var(--fs-small); }
.doc__cta { color: var(--color-brand); font-weight: 500; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 4px; }
.doc__link:hover .doc__cta { color: var(--color-brand-dark); }
.docs__loading { color: var(--color-ardesia); }
"""

OFF = """      <div class="riservata-off" data-area-off role="status" hidden>
        <p>L'area riservata non è ancora attiva.</p>
        <p>Nel frattempo, per ricevere cataloghi e schede tecniche scrivi a <a class="text-link" href="mailto:info@infissigroup.com">info@infissigroup.com</a> o chiama lo <a class="text-link" href="tel:+39051781570">051&nbsp;781570</a>.</p>
      </div>"""

ALERT = '            <div class="riservata-alert" role="alert" hidden></div>'


def email(id_):
    return f"""              <div class="field">
                <label for="{id_}">Email</label>
                <input class="input" id="{id_}" name="email" type="email" autocomplete="email" inputmode="email" spellcheck="false" required data-error="Inserisci un indirizzo email valido, per esempio nome@dominio.it.">
              </div>"""


def password(id_, label, auto, nuova=False):
    """Campo password col pulsante Mostra; quella nuova chiede almeno 10 caratteri, come il server"""
    extra = f' minlength="10" data-hint="{id_}-hint" aria-describedby="{id_}-hint"' if nuova else ""
    err = "La password deve avere almeno 10 caratteri." if nuova else "Inserisci la password."
    hint = f'\n                <p class="field__hint" id="{id_}-hint">Almeno 10 caratteri.</p>' if nuova else ""
    return f"""              <div class="field">
                <label for="{id_}">{label}</label>
                <div class="pw">
                  <input class="input" id="{id_}" name="password" type="password" autocomplete="{auto}" required{extra} data-error="{err}">
                  <button class="pw__toggle" type="button" data-pw-toggle aria-pressed="false" aria-controls="{id_}">Mostra</button>
                </div>{hint}
              </div>"""


def testa(titolo, lead="", briciole=""):
    crumbs = '<li><a href="/">Home</a></li>' + (briciole or f'<li><span aria-current="page">{titolo}</span></li>')
    lead = f'\n        <p class="lead">{lead}</p>' if lead else ""
    return f"""      <nav class="breadcrumb" aria-label="Percorso">
        <ol>{crumbs}</ol>
      </nav>
      <div class="riservata__head">
        <h1 id="page-title">{titolo}</h1>{lead}
      </div>
{OFF}"""


PAGINE = {
  "area-riservata": dict(
    titolo="Area riservata",
    descr="Accedi o registrati all'area riservata di Infissi Group per scaricare cataloghi, schede tecniche e documenti dei prodotti.",
    main=f"""{testa("Area riservata", "Cataloghi, schede tecniche e documenti per progettare con i nostri prodotti. Ti registri una volta e li scarichi quando vuoi.")}
      <div class="grid riservata__grid">
        <div class="riservata__panel riservata__panel--a">
          <h2 id="accedi-title">Accedi</h2>
          <form data-area-form="accedi" aria-labelledby="accedi-title" novalidate>
            <div class="fields">
{email("acc-email")}
{password("acc-pw", "Password", "current-password")}
            </div>
{ALERT}
            <div class="riservata__row">
              <button class="btn btn--primary" type="submit">Accedi</button>
              <a class="link" href="/area-riservata/password/">Password dimenticata?</a>
            </div>
          </form>
        </div>

        <div class="riservata__panel riservata__panel--b">
          <h2 id="reg-title">Registrati</h2>
          <ul class="riservata__benefits">
            <li><svg class="icon" aria-hidden="true"><use href="#i-check"/></svg>Cataloghi aggiornati dei marchi che trattiamo</li>
            <li><svg class="icon" aria-hidden="true"><use href="#i-check"/></svg>Schede tecniche, capitolati e certificazioni</li>
            <li><svg class="icon" aria-hidden="true"><use href="#i-check"/></svg>Registrazione gratuita, senza impegno</li>
          </ul>
          <form data-area-form="registrati" aria-labelledby="reg-title" novalidate>
            <div class="fields fields--2">
              <div class="field">
                <label for="reg-nome">Nome</label>
                <input class="input" id="reg-nome" name="nome" type="text" autocomplete="given-name" required data-error="Inserisci il nome.">
              </div>
              <div class="field">
                <label for="reg-cognome">Cognome</label>
                <input class="input" id="reg-cognome" name="cognome" type="text" autocomplete="family-name" required data-error="Inserisci il cognome.">
              </div>
            </div>
            <div class="fields">
{email("reg-email")}
{password("reg-pw", "Password", "new-password", nuova=True)}
            </div>
            <div class="checks">
              <div class="check-field">
                <input id="reg-privacy" name="privacy" type="checkbox" required data-error="Per registrarti accetta l'informativa privacy.">
                <label for="reg-privacy">Ho letto l'<a class="text-link" href="/privacy/" target="_blank" rel="noopener">informativa privacy<span class="sr-only"> (si apre in una nuova scheda)</span></a> e acconsento al trattamento dei dati per l'accesso all'area riservata. Obbligatorio.</label>
              </div>
              <div class="check-field">
                <input id="reg-marketing" name="marketing" type="checkbox">
                <label for="reg-marketing">Voglio ricevere via email novità e inviti agli eventi in showroom. Facoltativo.</label>
              </div>
            </div>
            <div class="qd__hp" aria-hidden="true">
              <label for="reg-website">Non compilare questo campo</label>
              <input id="reg-website" name="website" type="text" tabindex="-1" autocomplete="off">
            </div>
{ALERT}
            <div><button class="btn btn--primary" type="submit">Crea l'account</button></div>
          </form>
        </div>
      </div>"""),

  "area-riservata/password": dict(
    titolo="Password dimenticata",
    descr="Reimposta la password dell'area riservata di Infissi Group.",
    main=f"""{testa("Password dimenticata", briciole='<li><a href="/area-riservata/">Area riservata</a></li><li><span aria-current="page">Password</span></li>')}
      <div class="grid riservata__grid">
        <div class="riservata__panel riservata__panel--solo">
          <form data-area-form="password-richiesta" aria-labelledby="page-title" novalidate>
            <p>Scrivi l'email con cui ti sei registrato: ti mandiamo un link per scegliere una nuova password.</p>
            <div class="fields">
{email("rec-email")}
            </div>
{ALERT}
            <div class="riservata__row">
              <button class="btn btn--primary" type="submit">Invia il link</button>
              <a class="link" href="/area-riservata/">Torna all'accesso</a>
            </div>
          </form>

          <div class="stack" data-area-sent hidden>
            <h2 tabindex="-1">Controlla la posta</h2>
            <p>Se l'email è registrata, tra pochi minuti ricevi un link valido un'ora. Se non lo trovi, guarda anche nella posta indesiderata.</p>
            <div><a class="link" href="/area-riservata/">Torna all'accesso</a></div>
          </div>

          <form data-area-form="password-nuova" aria-labelledby="nuova-title" novalidate hidden>
            <h2 id="nuova-title">Scegli una nuova password</h2>
            <input name="token" type="hidden">
            <div class="fields">
{password("new-pw", "Nuova password", "new-password", nuova=True)}
            </div>
{ALERT}
            <div><button class="btn btn--primary" type="submit">Salva e accedi</button></div>
          </form>
        </div>
      </div>"""),

  "area-riservata/documenti": dict(
    titolo="I tuoi documenti",
    descr="Documenti scaricabili dell'area riservata di Infissi Group.",
    main=f"""{testa("I tuoi documenti", "Cataloghi, schede tecniche e certificazioni da scaricare. Li aggiorniamo quando escono nuove versioni.", '<li><a href="/area-riservata/">Area riservata</a></li><li><span aria-current="page">Documenti</span></li>')}
      <div class="riservata__user" data-area-user hidden>
        <p>Ciao <strong data-area-name></strong>, hai effettuato l'accesso.</p>
        <button class="btn btn--secondary" type="button" data-area-logout>Esci</button>
      </div>
      <div class="docs" data-area-docs aria-live="polite">
        <p class="docs__loading">Caricamento dei documenti…</p>
      </div>
      <p data-area-empty hidden>Al momento non ci sono documenti. Torna a trovarci presto.</p>
      <p class="riservata-alert" data-area-error role="alert" hidden>Non riusciamo a caricare i documenti. Ricarica la pagina tra poco.</p>"""),
}


def pagina(percorso, p):
    s = MODELLO
    url = f"https://infissigroup.com/{percorso}/"
    titolo = f"{p['titolo']}: Infissi Group"
    intestazione = (f"<!--\n  INFISSI GROUP, {p['titolo'].upper()} (/{percorso}/)\n"
                    "  Pagina generata da _sorgenti/area-riservata/genera.py sul modello privacy/index.html: non modificarla a mano.\n"
                    "  Moduli e documenti in /assets/area-riservata.js, server in /api/area/ (PHP su Hostinger).\n-->")
    s = re.sub(r"<!--\n  INFISSI GROUP, INFORMATIVA PRIVACY.*?-->", lambda m: intestazione, s, count=1, flags=re.S)
    s = re.sub(r"<title>.*?</title>", f"<title>{titolo}</title>", s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{p["descr"]}">\n<meta name="robots" content="noindex, nofollow">', s, count=1)
    s = re.sub(r'<link rel="canonical"[^>]*>\n(<link rel="alternate"[^>]*>\n)+', f'<link rel="canonical" href="{url}">\n', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{titolo}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{p["descr"]}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', s, count=1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", s, count=1, flags=re.S)
    s = s.replace("\n</style>", CSS + "</style>", 1)
    s, n = re.subn(r'(<script src="/assets/accessibilita\.js[^"]*" defer></script>)', r'\1\n<script src="/assets/area-riservata.js" defer></script>', s, count=1)
    assert n == 1, (percorso, "script accessibilità non trovato")
    main = f'<main id="main" tabindex="-1">\n  <section class="section--calce riservata" aria-labelledby="page-title">\n    <div class="container">\n{p["main"]}\n    </div>\n  </section>\n</main>'
    s = re.sub(r'<main id="main" tabindex="-1">.*?</main>', lambda m: main, s, count=1, flags=re.S)
    s = s.replace('href="/privacy/" aria-current="page"', 'href="/privacy/"')
    # Selettore lingua: l'area riservata esiste solo in italiano, EN porta alla home inglese
    s = s.replace('<a href="/privacy/" hreflang="it" lang="it" aria-current="true">', f'<a href="/{percorso}/" hreflang="it" lang="it" aria-current="true">')
    s = s.replace('<a href="/en/privacy/" hreflang="en" lang="en">', '<a href="/en/" hreflang="en" lang="en">')
    for k in ("INFORMATIVA PRIVACY", "/en/privacy/", "Informativa privacy:"):
        assert k not in s.split("<main")[0], (percorso, k)
    out = ROOT / percorso / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s, encoding="utf-8", newline="")
    print("scritto", out.relative_to(ROOT))


for percorso, p in PAGINE.items():
    pagina(percorso, p)
