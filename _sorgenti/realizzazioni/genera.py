"""Genera la sezione Realizzazioni dai dati di progetti.json:
  /realizzazioni/              elenco con numeri, barra dei filtri, griglia di card con "Dettagli" e "Carica altre"
  /realizzazioni/inliving/ e /outdoor/   le due linee: i loro progetti e tutte le foto della raccolta
Impaginazione ispirata alle pagine progetti di Viabizzuno (2026-10-15): griglia regolare, scheda tecnica,
foto grandi in sequenza editoriale, barra delle sezioni in basso.
  /realizzazioni/<slug>/       pagina di ogni progetto
  /en/projects/ e /en/projects/<slug>/   le stesse in inglese
Le pagine elenco attuali fanno da guscio (head, header, footer, dialog, script): si sostituiscono
intestazione, dati strutturati e <main>. Stile e script dei componenti li aggiunge componenti.py.

Uso, dalla cartella del sito:  python _sorgenti/realizzazioni/genera.py
"""
import html, json, pathlib, re, struct

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SITE = "https://infissigroup.com"
IMG_DIR = ROOT / "assets/img/realizzazioni"

DATA = json.loads((HERE / "progetti.json").read_text(encoding="utf-8"))
PROJECTS = DATA["progetti"]

L = {
    "it": dict(base="/realizzazioni/", home="/", section="Realizzazioni", crumb_label="Percorso",
               quote="/preventivo/", todo="Da inserire",
               list_title="Realizzazioni: i nostri lavori a Bologna",
               list_desc="Lavori reali, clienti reali: le realizzazioni di Infissi Group a Bologna e provincia, con i prodotti usati, le foto e i dettagli di ogni progetto.",
               list_lead="Lavori reali, clienti reali: guarda cosa abbiamo realizzato a Bologna e dintorni, con i prodotti usati e le foto di ogni progetto.",
               projects_title="I progetti",
               f_tipo="Tipo", f_prodotto="Prodotto", f_all="Tutti", f_group_tipo="Filtra per tipo", f_group_prodotto="Filtra per prodotto",
               one="1 realizzazione", many="{n} realizzazioni", empty="Nessuna realizzazione con questi filtri.", reset="Mostra tutte", more="Carica altre",
               lines_h2="Le due linee", lines_lead="Le realizzazioni divise tra interni ed esterni, con tutte le foto dei lavori finiti.", line_count="{p} progetti e {f} foto",
               list_cta="Il prossimo lavoro può essere a casa tua",
               cta_p="La consulenza è senza impegno. Ti rispondiamo entro un giorno lavorativo con le prime indicazioni e, se serve, fissiamo il rilievo a domicilio.",
               quote_txt="Richiedi preventivo",
               p_title="{t}: una realizzazione Infissi Group", p_desc="{t}: le foto, i prodotti usati e i dettagli del lavoro di Infissi Group{where}.",
               sheet_title="Scheda rapida", details="Dettagli", s_place="Luogo", s_year="Anno", s_cat="Categoria", s_int="Tipo di intervento", s_prod="Prodotti", s_qty="Quantità e dimensioni", s_dur="Durata del cantiere", s_part="Partner",
               h_req="La richiesta", h_sol="La soluzione", h_cmp="Prima e dopo", h_gal="Galleria", h_res="Il risultato",
               cmp_label="Trascina per confrontare prima e dopo", before="Prima", after="Dopo", before_todo="Foto del prima da inserire",
               gal_lead="Clicca una foto per vederla a schermo intero.",
               p_cta="Hai un progetto simile?", p_cta_p="Richiedi un sopralluogo: ti rispondiamo entro un giorno lavorativo e veniamo a vedere gli spazi con te.", p_cta_btn="Richiedi un sopralluogo",
               related="Altre realizzazioni", all_projects="Tutte le realizzazioni",
               pnav_label="Sezioni del progetto", n_det="Dettagli", n_prog="Il progetto", n_foto="Foto", n_rel="Correlati", see_gallery="Guarda la galleria",
               list_leads=["Lavori reali, clienti reali: guarda cosa abbiamo realizzato a Bologna e dintorni.",
                           "Ogni progetto ha la sua scheda tecnica, con i prodotti usati e le foto: utile anche ad architetti e progettisti che cercano soluzioni già messe alla prova."],
               lb_label="Foto a schermo intero", lb_close="Chiudi", lb_prev="Foto precedente", lb_next="Foto successiva",
               t_place="luogo e anno", t_data="quantità e durata", t_req="il punto di partenza: cosa voleva il cliente, problemi e vincoli (2-3 righe)", t_sol="le scelte fatte e perché, riferite alla foto accanto", t_result="risultati concreti (comfort, risparmio, estetica)", t_quote="testimonianza del cliente"),
    "en": dict(base="/en/projects/", home="/en/", section="Projects", crumb_label="Breadcrumb",
               quote="/en/quote/", todo="To be added",
               list_title="Projects: our work in Bologna",
               list_desc="Real work for real customers: Infissi Group projects in and around Bologna, with the products used, the photos and the details of each one.",
               list_lead="Real work for real customers: see what we have done in and around Bologna, with the products used and photos of each project.",
               projects_title="Projects",
               f_tipo="Type", f_prodotto="Product", f_all="All", f_group_tipo="Filter by type", f_group_prodotto="Filter by product",
               one="1 project", many="{n} projects", empty="No projects match these filters.", reset="Show all", more="Load more",
               lines_h2="Two lines", lines_lead="Our projects split between interiors and exteriors, with all the photos of the finished work.", line_count="{p} projects and {f} photos",
               list_cta="Your home could be our next project",
               cta_p="Advice comes with no obligation. We reply within one working day with some first suggestions and, if needed, we book an on-site survey.",
               quote_txt="Request a quote",
               p_title="{t}: an Infissi Group project", p_desc="{t}: photos, products used and details of this Infissi Group project{where}.",
               sheet_title="At a glance", details="Details", s_place="Place", s_year="Year", s_cat="Category", s_int="Type of work", s_prod="Products", s_qty="Quantity and size", s_dur="Time on site", s_part="Partners",
               h_req="The brief", h_sol="The solution", h_cmp="Before and after", h_gal="Gallery", h_res="The result",
               cmp_label="Drag to compare before and after", before="Before", after="After", before_todo="Before photo to be added",
               gal_lead="Click a photo to see it full screen.",
               p_cta="Got a similar project?", p_cta_p="Book a site survey: we reply within one working day and come to look at the space with you.", p_cta_btn="Book a site survey",
               related="More projects", all_projects="All projects",
               pnav_label="Project sections", n_det="Details", n_prog="The project", n_foto="Photos", n_rel="Related", see_gallery="View the gallery",
               list_leads=["Real work for real customers: see what we have done in and around Bologna.",
                           "Each project has its own technical sheet, with the products used and the photos: useful for architects and designers too, looking for solutions already put to the test."],
               lb_label="Full-screen photo", lb_close="Close", lb_prev="Previous photo", lb_next="Next photo",
               t_place="place and year", t_data="quantity and time on site", t_req="the starting point: what the customer wanted, problems and constraints (2-3 lines)", t_sol="the choices made and why, relating to the photo alongside", t_result="concrete benefits (comfort, savings, looks)", t_quote="customer testimonial"),
}
TIPI = {"casa": ("Casa", "Residential"), "commerciale": ("Commerciale", "Commercial"),
        "ristrutturazione": ("Ristrutturazione", "Renovation"), "nuova-costruzione": ("Nuova costruzione", "New build")}
PRODOTTI = {"finestre": ("Finestre", "Windows"), "porte": ("Porte", "Doors"), "outdoor": ("Outdoor", "Outdoor"),
            "oscuramento": ("Oscuramento", "Shading"), "arredo": ("Arredo", "Interiors")}
QUOTE_CAT = {"finestre": "finestre", "porte": "porte", "outdoor": "outdoor", "oscuramento": "persiane"}
TEMPLATE_LINES = [
    "Pagina generata dal modello index.html: stile, header, footer, barra mobile, dialog, banner cookie",
    "e script sono identici. Se cambiano nel modello, vanno aggiornati anche qui.",
    "Percorsi assoluti (/assets/...): la pagina va vista tramite un server, non aprendo il file.",
    "NON MODIFICARE A MANO <main>, titolo e dati strutturati: li genera _sorgenti/realizzazioni/genera.py",
    "da progetti.json. Per cambiare un progetto si cambiano i dati e si rilancia lo script.",
]

def esc(t): return html.escape(t, quote=True).replace("&#x27;", "'")
def tr(v, lang): return None if v is None else v[lang] if isinstance(v, dict) else v
def todo(lang, what, block=False):
    return f'<span class="todo{" todo--block" if block else ""}">{L[lang]["todo"]}: {what}</span>'
def label(lang, key):
    return (TIPI.get(key) or PRODOTTI[key])[0 if lang == "it" else 1]

# ------------------------------------------------------------------ foto
def jpeg_size(p):
    b = p.read_bytes(); i = 2
    while i < len(b):
        if b[i] != 0xFF: i += 1; continue
        marker, length = b[i + 1], struct.unpack(">H", b[i + 2:i + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", b[i + 5:i + 9]); return w, h
        i += 2 + length
    raise ValueError(p)

def widths(name):
    ws = sorted(int(p.stem.rsplit("-", 1)[1]) for p in IMG_DIR.glob(f"{name}-*.jpg") if p.stem.rsplit("-", 1)[1].isdigit())
    if not ws: raise SystemExit(f"foto non trovata: {name}")
    return ws

def src(name, w): return f"/assets/img/realizzazioni/{name}-{w}.jpg"
def largest(name): return src(name, widths(name)[-1])

def img(name, alt, sizes, min_w=768, eager=False, cls="media"):
    ws = [w for w in widths(name) if w >= min_w] or widths(name)
    base = 1536 if eager and 1536 in ws else 768 if 768 in ws else ws[0]
    w, h = jpeg_size(IMG_DIR / f"{name}-{ws[0]}.jpg")
    srcset = ", ".join(f"{src(name, x)} {x}w" for x in ws)
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img class="{cls}" src="{src(name, base)}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}" {load} decoding="async">'

HERO = "(min-width: 1440px) 91vw, 92vw"
CARD = "(min-width: 1440px) 29vw, (min-width: 1024px) 30vw, (min-width: 768px) 46vw, 92vw"
CARD_BIG = "(min-width: 1440px) 44vw, (min-width: 768px) 46vw, 92vw"
HALF = "(min-width: 1440px) 44vw, (min-width: 1024px) 46vw, 92vw"
THUMB = "(min-width: 1024px) 30vw, 46vw"
CARD_HALF = "(min-width: 1440px) 44vw, (min-width: 768px) 46vw, 92vw"
SEQ_HALF = "(min-width: 1440px) 44vw, (min-width: 768px) 46vw, 92vw"
STORY = "(min-width: 1440px) 52vw, (min-width: 1024px) 55vw, 92vw"

# ------------------------------------------------------------------ pezzi comuni
def url(p, lang): return L[lang]["base"] + p["slug"][lang] + "/"

def icon(name, cls="icon"): return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'

def ptag(lang, key): return f'<span class="ptag">{label(lang, key)}</span>'

def val(p, key, lang, what=None):
    v = tr(p[key], lang) if key != "anno" else (str(p["anno"]) if p["anno"] else None)
    return esc(v) if v else todo(lang, what or key)

def products(p, lang, links=True):
    if not p["prodotti_usati"]: return todo(lang, L[lang]["s_prod"].lower())
    if not links: return esc(", ".join(tr(x["nome"], lang) for x in p["prodotti_usati"]))
    return ", ".join(f'<a href="{tr(x["pagina"], lang)}">{esc(tr(x["nome"], lang))}</a>' for x in p["prodotti_usati"])

def specs(rows, cls="specs"):
    return f'<dl class="{cls}">' + "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in rows) + "</dl>"

def card(p, lang):
    """Card come nella reference: foto, titolo con l'etichetta della categoria, "Dettagli" apribile con la scheda tecnica."""
    t, c, u = L[lang], p["copertina"], url(p, lang)
    rows = [(t["s_place"], val(p, "luogo", lang, t["s_place"].lower())), (t["s_year"], val(p, "anno", lang, t["s_year"].lower())),
            (t["s_int"], val(p, "intervento", lang, t["s_int"].lower())), (t["s_prod"], products(p, lang, links=False)),
            (t["s_qty"], val(p, "quantita", lang, t["s_qty"].lower())), (t["s_dur"], val(p, "durata", lang, t["s_dur"].lower()))]
    return (f'        <li class="pcard" data-tipo="{" ".join(p["tipo"])}" data-prodotto="{" ".join(p["prodotto"])}">\n'
            f'          <a class="pcard__media" href="{u}" tabindex="-1" aria-hidden="true">{img(c["foto"], tr(c["didascalia"], lang), CARD)}</a>\n'
            f'          <div class="pcard__head"><h3 class="pcard__title"><a href="{u}">{esc(tr(p["titolo"], lang))}</a></h3>{ptag(lang, p["prodotto"][0])}</div>\n'
            f'          <details class="pcard__details"><summary>{t["details"]}{icon("chevron-down")}</summary>{specs(rows)}</details>\n'
            '        </li>\n')

def crumbs(lang, items):
    lis = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for u, n in items[:-1]) + f'<li><span aria-current="page">{esc(items[-1][1])}</span></li>'
    return f'  <nav class="container breadcrumb" aria-label="{L[lang]["crumb_label"]}">\n    <ol>{lis}</ol>\n  </nav>\n'

def cta_band(lang, h2, p, btn, cat=None):
    dc = f' data-category="{cat}"' if cat else ""
    return ('  <section class="cta-band on-ink" aria-labelledby="cta-title">\n    <div class="container grid cta-band__inner">\n'
            f'      <h2 id="cta-title">{h2}</h2>\n      <div class="cta-band__aside">\n        <p>{p}</p>\n'
            f'        <a class="btn btn--on-ink" href="{L[lang]["quote"]}" data-quote{dc}>{btn}</a>\n      </div>\n    </div>\n  </section>\n')

def main(*parts): return '<main id="main" tabindex="-1">\n' + "\n".join(x for x in parts if x) + "</main>"

# ------------------------------------------------------------------ pagine elenco: tutte le realizzazioni e le due linee
LINES = {
    "inliving": {
        "it": dict(path="/realizzazioni/inliving/", crumb="InLiving", name="Infissi Group InLiving", cover="inliving-07",
                   title="Infissi Group InLiving: lavori negli interni",
                   desc="I lavori Infissi Group negli interni a Bologna e dintorni: finestre, portefinestre, porte e oscuranti, con i progetti e tutte le foto.",
                   lead="Finestre, portefinestre, porte e oscuranti negli interni delle case dove abbiamo lavorato.",
                   lead2="Ogni progetto ha la sua scheda: luogo, prodotti, quantità e tempi di cantiere, con le foto dei lavori finiti.",
                   card="Finestre, portefinestre, porte e oscuranti negli interni.",
                   photos_h2="Tutte le foto", photos_lead="{n} foto da soggiorni, cucine, bagni, camere e ingressi. Clicca per vederle a schermo intero.",
                   cta="Raccontaci la tua casa, ti diciamo cosa serve"),
        "en": dict(path="/en/projects/inliving/", crumb="InLiving", name="Infissi Group InLiving", cover="inliving-07",
                   title="Infissi Group InLiving: interior projects",
                   desc="Infissi Group interior projects in and around Bologna: windows, French windows, doors and shutters, with the projects and all the photos.",
                   lead="Windows, French windows, doors and shutters inside the homes where we have worked.",
                   lead2="Each project has its own sheet: place, products, quantities and time on site, with photos of the finished work.",
                   card="Windows, French windows, doors and shutters in interiors.",
                   photos_h2="All the photos", photos_lead="{n} photos of living rooms, kitchens, bathrooms, bedrooms and entrances. Click to see them full screen.",
                   cta="Tell us about your home and we will tell you what it needs"),
    },
    "outdoor": {
        "it": dict(path="/realizzazioni/outdoor/", crumb="Outdoor", name="Infissi Group Outdoor", cover="outdoor-14",
                   title="Infissi Group Outdoor: pergole e verande",
                   desc="I lavori Infissi Group all'esterno a Bologna e dintorni: pergole bioclimatiche e verande vetrate, con i progetti e tutte le foto.",
                   lead="Pergole bioclimatiche e verande vetrate: gli spazi esterni che abbiamo progettato e installato.",
                   lead2="Ogni progetto ha la sua scheda: luogo, prodotti, quantità e tempi di cantiere, con le foto dei lavori finiti.",
                   card="Pergole bioclimatiche e verande vetrate.",
                   photos_h2="Tutte le foto", photos_lead="{n} foto, di giorno e di sera, con le vetrate aperte o chiuse. Clicca per vederle a schermo intero.",
                   cta="Progettiamo insieme il tuo spazio esterno"),
        "en": dict(path="/en/projects/outdoor/", crumb="Outdoor", name="Infissi Group Outdoor", cover="outdoor-14",
                   title="Infissi Group Outdoor: pergolas and verandas",
                   desc="Infissi Group outdoor projects in and around Bologna: bioclimatic pergolas and glazed verandas, with the projects and all the photos.",
                   lead="Bioclimatic pergolas and glazed verandas: the outdoor spaces we have designed and installed.",
                   lead2="Each project has its own sheet: place, products, quantities and time on site, with photos of the finished work.",
                   card="Bioclimatic pergolas and glazed verandas.",
                   photos_h2="All the photos", photos_lead="{n} photos, by day and in the evening, with the glass walls open or closed. Click to see them full screen.",
                   cta="Let's design your outdoor space together"),
    },
}
ARCHIVIO = json.loads((HERE / "archivio.json").read_text(encoding="utf-8"))

def chips(lang, key, options, projects):
    t = L[lang]
    used = {k for p in projects for k in p[key]}
    if len(used) < 2: return None  # una sola voce non filtra niente
    out = f'<button class="chip" type="button" data-filter="{key}" data-value="" aria-pressed="true">{t["f_all"]}</button>'
    for k in options:
        if k not in used: continue  # solo le categorie con almeno un progetto: nessun filtro porta a una lista vuota
        out += f'<button class="chip" type="button" data-filter="{key}" data-value="{k}" aria-pressed="false">{label(lang, k)}</button>'
    return out

def projects_section(lang, projects, cls="section section--flush"):
    """Barra dei filtri tra due filetti e griglia regolare a 3 colonne; i progetti in evidenza vengono per primi."""
    t = L[lang]
    ordered = [p for p in projects if p.get("evidenza")] + [p for p in projects if not p.get("evidenza")]
    return (f'  <section class="{cls}" aria-labelledby="progetti-title">\n    <div class="container" data-projects data-page="9">\n'
            f'      <h2 class="sr-only" id="progetti-title">{t["projects_title"]}</h2>\n'
            '      <div class="filters" data-filters hidden>\n'
            + "".join(f'        <div class="filters__group" role="group" aria-label="{t["f_group_" + key]}"><span class="filters__label" aria-hidden="true">{t["f_" + key]}</span>{c}</div>\n'
                      for key, opts in (("tipo", TIPI), ("prodotto", PRODOTTI)) if (c := chips(lang, key, opts, projects)))
            + f'        <p class="filters__status" data-status data-one="{t["one"]}" data-many="{t["many"]}" aria-live="polite"></p>\n'
            '      </div>\n'
            f'      <ul class="pgrid{" pgrid--two" if len(ordered) <= 2 else ""}" data-grid>\n{"".join(card(p, lang) for p in ordered)}      </ul>\n'
            f'      <div class="projects__empty" data-empty hidden><p>{t["empty"]}</p><button class="btn btn--secondary" type="button" data-reset>{t["reset"]}</button></div>\n'
            f'      <div class="projects__more"><button class="btn btn--secondary" type="button" data-more hidden>{t["more"]}</button></div>\n'
            '    </div>\n  </section>\n')

def page_head(title, leads):
    ps = f'<p class="lead">{leads[0]}</p>' + "".join(f'<p>{x}</p>' for x in leads[1:])
    return ('  <section class="page-head page-head--intro" aria-labelledby="page-title">\n    <div class="container grid page-head__grid">\n'
            f'      <h1 id="page-title">{title}</h1>\n      <div class="page-head__lead intro-cols">{ps}</div>\n    </div>\n  </section>\n')

def lightbox(lang):
    t = L[lang]
    return (f'  <dialog class="lightbox" id="lightbox" aria-label="{t["lb_label"]}">\n'
            f'    <div class="lightbox__bar"><span class="lightbox__count"></span><button class="lightbox__btn" type="button" data-lb-close aria-label="{t["lb_close"]}">{icon("x")}</button></div>\n'
            '    <figure class="lightbox__figure"><img class="lightbox__img" alt=""></figure>\n'
            f'    <div class="lightbox__foot"><button class="lightbox__btn" type="button" data-lb-prev aria-label="{t["lb_prev"]}">{icon("chevron-left")}</button>'
            f'<p class="lightbox__caption"></p><button class="lightbox__btn" type="button" data-lb-next aria-label="{t["lb_next"]}">{icon("chevron-right")}</button></div>\n'
            '  </dialog>\n')

def photo(g, lang, sizes, cls=""):
    cap = esc(tr(g["didascalia"], lang))
    return (f'<figure class="{cls}"><a href="{largest(g["foto"])}" data-lightbox data-caption="{cap}">{img(g["foto"], tr(g["didascalia"], lang), sizes)}</a>'
            f"<figcaption>{cap}</figcaption></figure>")

def photo_grid(lang, items, h2, lead, cls, sid="galleria-title"):
    lis = "".join(f'        <li>{photo(g, lang, THUMB)}</li>\n' for g in items)
    return (f'  <section class="{cls}" aria-labelledby="{sid}">\n    <div class="container">\n      <div class="section-head">\n'
            f'        <h2 class="attach" id="{sid}">{h2}</h2>\n        <p class="lead">{lead}</p>\n      </div>\n'
            f'      <ul class="pgallery">\n{lis}      </ul>\n    </div>\n  </section>\n')

def list_page(lang):
    t = L[lang]
    lines = ""
    for key in LINES:
        c = LINES[key][lang]
        alt = next(g["didascalia"][lang] for g in ARCHIVIO[key] if g["foto"] == c["cover"])
        n = sum(1 for p in PROJECTS if p["linea"] == key)
        lines += (f'        <li class="pcard">\n          <a class="pcard__media" href="{c["path"]}" tabindex="-1" aria-hidden="true">{img(c["cover"], alt, CARD_HALF)}</a>\n'
                  f'          <div class="pcard__head"><h3 class="pcard__title"><a href="{c["path"]}">{c["name"]}</a></h3><span class="ptag">{t["line_count"].format(p=n, f=len(ARCHIVIO[key]))}</span></div>\n'
                  f'          <p class="pcard__text">{c["card"]}</p>\n        </li>\n')
    arch = (f'  <section class="section section--calce" aria-labelledby="linee-title">\n    <div class="container">\n      <div class="section-head">\n'
            f'        <h2 class="attach" id="linee-title">{t["lines_h2"]}</h2>\n        <p class="lead">{t["lines_lead"]}</p>\n      </div>\n'
            f'      <ul class="pgrid pgrid--two">\n{lines}      </ul>\n    </div>\n  </section>\n')
    return main(crumbs(lang, [(t["home"], "Home"), (t["base"], t["section"])]) + page_head(t["section"], t["list_leads"]),
                projects_section(lang, PROJECTS), arch, cta_band(lang, t["list_cta"], t["cta_p"], t["quote_txt"]))

def line_page(lang, key):
    t, c = L[lang], LINES[key][lang]
    projects = [p for p in PROJECTS if p["linea"] == key]
    photos = ARCHIVIO[key]
    return main(crumbs(lang, [(t["home"], "Home"), (t["base"], t["section"]), (c["path"], c["crumb"])]) + page_head(c["name"], [c["lead"], c["lead2"]]),
                projects_section(lang, projects) if projects else "",
                photo_grid(lang, photos, c["photos_h2"], c["photos_lead"].format(n=len(photos)), "section section--calce"),
                cta_band(lang, c["cta"], t["cta_p"], t["quote_txt"]), lightbox(lang))

# ------------------------------------------------------------------ pagina progetto
def related(p, lang):
    others = [q for q in PROJECTS if q is not p]
    others.sort(key=lambda q: -len(set(q["prodotto"]) & set(p["prodotto"])))
    return others[:3]

def is_wide(name):
    w, h = jpeg_size(IMG_DIR / f"{name}-{widths(name)[0]}.jpg")
    return w / h >= 1.3

def sequence(items, lang):
    """Sequenza editoriale: una foto orizzontale a tutta larghezza, poi una coppia, poi una foto a metà destra, e così via.
    Le foto verticali o quadrate vanno sempre in coppia o a metà, mai a tutta larghezza."""
    out, i, step = [], 0, 0
    while i < len(items):
        g = items[i]
        if step % 3 == 0 and is_wide(g["foto"]):
            out.append(f'        <div class="seq seq--full">{photo(g, lang, HERO)}</div>\n'); i += 1
        elif i + 1 < len(items) and step % 3 != 2:
            tall = " seq--tall" if not (is_wide(g["foto"]) or is_wide(items[i + 1]["foto"])) else ""
            out.append(f'        <div class="seq seq--pair{tall}">{photo(g, lang, SEQ_HALF)}{photo(items[i + 1], lang, SEQ_HALF)}</div>\n'); i += 2
        else:
            tall = "" if is_wide(g["foto"]) else " seq--tall"
            out.append(f'        <div class="seq seq--half{tall}">{photo(g, lang, SEQ_HALF)}</div>\n'); i += 1
        step += 1
    return "".join(out)

def project_page(p, lang):
    t = L[lang]
    title = tr(p["titolo"], lang)
    c = p["copertina"]
    main_cat = p["prodotto"][0]

    head = ('  <section class="page-head project-head" aria-labelledby="page-title">\n    <div class="container grid project-head__row">\n'
            f'      <h1 id="page-title">{esc(title)}</h1>\n      <div class="project-head__tags">{"".join(ptag(lang, k) for k in p["tipo"] + p["prodotto"])}</div>\n    </div>\n'
            f'    <div class="container page-head__media page-head__media--16x9">\n      {img(c["foto"], tr(c["didascalia"], lang), HERO, eager=True)}\n    </div>\n  </section>\n')

    nav = (f'  <nav class="pnav" aria-label="{t["pnav_label"]}">\n    <div class="container pnav__inner">\n      <ul class="pnav__links">'
           + "".join(f'<li><a href="#{a}">{b}</a></li>' for a, b in (("dettagli", t["n_det"]), ("progetto", t["n_prog"]), ("foto", t["n_foto"]), ("correlati", t["n_rel"])))
           + f'</ul>\n      {ptag(lang, main_cat)}\n    </div>\n  </nav>\n')

    rows = [(t["s_place"], val(p, "luogo", lang, t["s_place"].lower())), (t["s_year"], val(p, "anno", lang, t["s_year"].lower())),
            (t["s_cat"], " · ".join(label(lang, k) for k in p["tipo"] + p["prodotto"])),
            (t["s_int"], val(p, "intervento", lang, t["s_int"].lower())), (t["s_prod"], products(p, lang)),
            (t["s_qty"], val(p, "quantita", lang, t["s_qty"].lower())), (t["s_dur"], val(p, "durata", lang, t["s_dur"].lower())),
            (t["s_part"], val(p, "partner", lang, t["s_part"].lower()))]
    credits = (f'  <section class="section section--flush" id="dettagli" aria-labelledby="dettagli-title">\n    <div class="container grid credits">\n'
               f'      <h2 class="credits__title" id="dettagli-title">{t["n_det"]}</h2>\n      {specs(rows, "specs specs--credits")}\n    </div>\n  </section>\n')

    def text(v, what):
        if not v: return f'<p>{todo(lang, what, block=True)}</p>'
        return "".join(f"<p>{esc(par)}</p>" for par in tr(v, lang).split("\n\n"))
    sol = "".join(text(r["testo"], t["t_sol"]) for r in p["soluzione"])
    lead_photo = p["soluzione"][0]
    prima = p.get("foto_prima")
    prima_html = (f'<figure class="story-intro__before">{img(prima["foto"], tr(prima["didascalia"], lang), SEQ_HALF)}<figcaption>{esc(tr(prima["didascalia"], lang))}</figcaption></figure>' if prima else "")
    story = (f'  <section class="section" id="progetto" aria-labelledby="progetto-title">\n    <div class="container grid story-intro">\n'
             f'      <div class="story-intro__text prose">\n        <h2 id="progetto-title">{t["n_prog"]}</h2>\n'
             f'        <h3>{t["h_req"]}</h3>{text(p["richiesta"], t["t_req"])}{prima_html}\n        <h3>{t["h_sol"]}</h3>{sol}\n'
             f'        <p><button class="btn btn--secondary" type="button" data-lightbox-open>{t["see_gallery"]}</button></p>\n      </div>\n'
             f'      <figure class="story-intro__media">{img(lead_photo["foto"], tr(lead_photo["didascalia"], lang), STORY)}<figcaption>{esc(tr(lead_photo["didascalia"], lang))}</figcaption></figure>\n'
             '    </div>\n  </section>\n')

    seq = (f'  <section class="section section--flush" id="foto" aria-labelledby="foto-title">\n    <div class="container">\n'
           f'      <h2 class="sr-only" id="foto-title">{t["n_foto"]}</h2>\n      <div class="sequence">\n{sequence(p["galleria"][:10], lang)}      </div>\n    </div>\n  </section>\n')

    cmp_html = ""
    pd = p.get("prima_dopo")
    if pd:
        dopo = img(pd["dopo"], f'{t["after"]}: {tr(c["didascalia"], lang)}', HERO)
        before = (img(pd["prima"], t["before"], HERO) if pd["prima"] else f'<span class="todo">{t["before_todo"]}</span>')
        cmp_html = (f'  <section class="section" aria-labelledby="confronto-title">\n    <div class="container">\n      <div class="section-head">\n'
                    f'        <h2 class="attach" id="confronto-title">{t["h_cmp"]}</h2>\n      </div>\n'
                    f'      <div class="compare">\n        {dopo}\n        <div class="compare__before">{before}</div>\n'
                    f'        <span class="compare__label compare__label--before">{t["before"]}</span><span class="compare__label compare__label--after">{t["after"]}</span>\n'
                    f'        <input class="compare__range" type="range" min="0" max="100" value="50" aria-label="{t["cmp_label"]}">\n'
                    f'        <span class="compare__handle" aria-hidden="true">{icon("chevron-left")}{icon("chevron-right")}</span>\n'
                    '      </div>\n    </div>\n  </section>\n')

    if p.get("risultato"):
        res = '<ul class="pillars pillars--3">' + "".join(f'<li class="pillar"><h3>{esc(tr(r["titolo"], lang))}</h3><p>{esc(tr(r["testo"], lang))}</p></li>' for r in p["risultato"]) + "</ul>"
    else:
        res = f"<p>{todo(lang, t['t_result'], block=True)}</p>"
    q = p.get("testimonianza")
    quote = (f'<blockquote class="quote result__quote"><p>«{esc(tr(q["testo"], lang))}»</p><footer>{esc(q["autore"])}</footer></blockquote>' if q
             else f'<p class="result__quote">{todo(lang, t["t_quote"], block=True)}</p>')
    result = (f'  <section class="section section--calce" aria-labelledby="risultato-title">\n    <div class="container">\n      <div class="section-head">\n'
              f'        <h2 class="attach" id="risultato-title">{t["h_res"]}</h2>\n      </div>\n      {res}\n      {quote}\n    </div>\n  </section>\n')

    rel = (f'  <section class="section" id="correlati" aria-labelledby="correlati-title">\n    <div class="container">\n      <div class="section-head">\n'
           f'        <h2 class="attach" id="correlati-title">{t["related"]}</h2>\n        <a class="link" href="{t["base"]}">{t["all_projects"]}</a>\n      </div>\n'
           f'      <ul class="pgrid">\n{"".join(card(r, lang) for r in related(p, lang))}      </ul>\n    </div>\n  </section>\n')

    cat = next((QUOTE_CAT[k] for k in p["prodotto"] if k in QUOTE_CAT), None)
    return main(crumbs(lang, [(t["home"], "Home"), (t["base"], t["section"]), (url(p, lang), title)]) + head,
                credits, story, seq, cmp_html, result, rel,
                cta_band(lang, t["p_cta"], t["p_cta_p"], t["p_cta_btn"], cat), nav, lightbox(lang))

# ------------------------------------------------------------------ guscio: intestazione, head, dati strutturati
def sub1(pat, rep, s, flags=0):
    s2, n = re.subn(pat, rep, s, count=1, flags=flags)
    if not n: raise SystemExit(f"nel guscio manca: {pat[:70]}")
    return s2

def page(shell, lang, *, path, it, en, title, desc, og, comment, crumbs_ld, kind, main_html, nav_current, noindex):
    s = shell.replace(NOINDEX, "")
    if noindex:
        s = sub1(r'(<meta name="viewport"[^>]*>\n)', lambda m: m.group(1) + NOINDEX, s)
    body = "\n".join("  " + l if l else "" for l in comment)
    s = sub1(r"(<!--\n)  INFISSI GROUP.*?\n(?=\n  DATI COMPILATI)", lambda m: m.group(1) + body + "\n", s, re.S)
    if lang == "en":
        s = sub1(r"<!-- VERSIONE INGLESE[^\n]*-->", f"<!-- VERSIONE INGLESE di {it}: generata insieme alla pagina italiana -->", s)
    s = sub1(r"<title>.*?</title>", lambda m: f"<title>{esc(title)}</title>", s)
    s = sub1(r'<meta name="description" content="[^"]*">', lambda m: f'<meta name="description" content="{esc(desc)}">', s)
    s = sub1(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{SITE}{path}">', s)
    s = sub1(r'<link rel="alternate" hreflang="it" href="[^"]*">', f'<link rel="alternate" hreflang="it" href="{SITE}{it}">', s)
    s = sub1(r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="{SITE}{en}">', s)
    s = sub1(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', f'<link rel="alternate" hreflang="x-default" href="{SITE}{it}">', s)
    s = sub1(r'<meta property="og:title" content="[^"]*">', lambda m: f'<meta property="og:title" content="{esc(title)}">', s)
    s = sub1(r'<meta property="og:description" content="[^"]*">', lambda m: f'<meta property="og:description" content="{esc(desc)}">', s)
    s = sub1(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{SITE}{path}">', s)
    s = sub1(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{SITE}{og}">', s)
    s = re.sub(r'(<a href=")[^"]*(" hreflang="it")', rf"\g<1>{it}\2", s)
    s = re.sub(r'(<a href=")[^"]*(" hreflang="en")', rf"\g<1>{en}\2", s)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (u, n) in enumerate(crumbs_ld)]},
        {"@type": kind, "@id": f"{SITE}{path}#pagina", "url": SITE + path, "name": title, "description": desc, "inLanguage": lang,
         "isPartOf": {"@id": f"{SITE}/#sito"}}]}
    s = sub1(r'(<script type="application/ld\+json">\n).*?(\n</script>)', lambda m: m.group(1) + json.dumps(ld, indent=2, ensure_ascii=False) + m.group(2), s, re.S)
    # voce "Tutte le realizzazioni" del menu attiva solo sull'elenco
    s = re.sub(r'(<li class="nav__all nav__divided"><a href="' + re.escape(L[lang]["base"]) + r'")(?: aria-current="page")?>',
               lambda m: m.group(1) + (' aria-current="page">' if nav_current else ">"), s)
    s = sub1(r'<main id="main" tabindex="-1">\n.*?\n</main>', lambda m: main_html, s, re.S)
    return s

NOINDEX = '<meta name="robots" content="noindex">\n'
DEMO_LINE = "CONTIENE DATI INVENTATI DI ESEMPIO (pagina in noindex): sostituirli con quelli veri prima della pubblicazione."

def write(path, s):
    f = ROOT / path.lstrip("/") / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(s.encode("utf-8"))

def run():
    demo = [tr(p["titolo"], "it") for p in PROJECTS if p.get("esempio")]
    shells = {lang: (ROOT / L[lang]["base"].lstrip("/") / "index.html").read_bytes().decode("utf-8") for lang in L}
    for lang in L:
        t = L[lang]
        cover = PROJECTS[0]["copertina"]["foto"]
        s = page(shells[lang], lang, path=t["base"], it=L["it"]["base"], en=L["en"]["base"], title=t["list_title"], desc=t["list_desc"],
                 og=src(cover, 1024), kind="CollectionPage", nav_current=True, noindex=bool(demo),
                 comment=["INFISSI GROUP, REALIZZAZIONI: I NOSTRI LAVORI A BOLOGNA (/realizzazioni/)", *TEMPLATE_LINES,
                          *([DEMO_LINE] if demo else [])],
                 crumbs_ld=[(t["home"], "Home"), (t["base"], t["section"])], main_html=list_page(lang))
        write(t["base"], s)
        for key in LINES:
            c = LINES[key][lang]
            other = {"it": LINES[key]["it"]["path"], "en": LINES[key]["en"]["path"]}
            shell = (ROOT / c["path"].lstrip("/") / "index.html").read_bytes().decode("utf-8")
            has_demo = any(p.get("esempio") for p in PROJECTS if p["linea"] == key)
            s = page(shell, lang, path=c["path"], it=other["it"], en=other["en"], title=c["title"], desc=c["desc"],
                     og=src(c["cover"], 1024), kind="CollectionPage", nav_current=False, noindex=has_demo,
                     comment=[f"INFISSI GROUP, {LINES[key]['it']['name'].upper()} ({other['it']})", *TEMPLATE_LINES,
                              "Le foto della raccolta sono in archivio.json, i progetti della linea in progetti.json (campo linea).",
                              *([DEMO_LINE] if has_demo else [])],
                     crumbs_ld=[(t["home"], "Home"), (t["base"], t["section"]), (c["path"], c["crumb"])], main_html=line_page(lang, key))
            write(c["path"], s)
        for p in PROJECTS:
            title = tr(p["titolo"], lang)
            where = f" a {tr(p['luogo'], lang)}" if (lang == "it" and p["luogo"]) else (f" in {tr(p['luogo'], lang)}" if p["luogo"] else "")
            s = page(shells[lang], lang, path=url(p, lang), it=url(p, "it"), en=url(p, "en"),
                     title=t["p_title"].format(t=title), desc=t["p_desc"].format(t=title, where=where),
                     og=src(p["copertina"]["foto"], 1024), kind="WebPage", nav_current=False, noindex=bool(p.get("esempio")),
                     comment=[f"INFISSI GROUP, REALIZZAZIONE: {tr(p['titolo'], 'it').upper()} ({url(p, 'it')})", *TEMPLATE_LINES,
                              *([DEMO_LINE] if p.get("esempio") else []), f"DA VERIFICARE: {p.get('verifica') or '-'}"],
                     crumbs_ld=[(t["home"], "Home"), (t["base"], t["section"]), (url(p, lang), title)], main_html=project_page(p, lang))
            write(url(p, lang), s)
    print(f"generate: 2 pagine elenco, 4 pagine di linea e {2 * len(PROJECTS)} pagine progetto")
    if demo:
        print(f"ATTENZIONE: {len(demo)} progetti con dati inventati di esempio (pagine in noindex): " + ", ".join(demo))

if __name__ == "__main__":
    run()
