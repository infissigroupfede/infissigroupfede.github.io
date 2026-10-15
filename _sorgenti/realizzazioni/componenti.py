"""Aggiunge a tutte le pagine (stile, icone e script sono identici in ogni pagina) i componenti
della sezione Realizzazioni: filtri, card, scheda tecnica, racconto, sequenza di foto, barra delle sezioni,
confronto prima/dopo e galleria a schermo intero. Si può rilanciare: non duplica nulla.
Le etichette delle categorie sono solo testo (ICONS è vuoto: toglie le vecchie icone dalle pagine).

Uso, dalla cartella del sito:  python _sorgenti/realizzazioni/componenti.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
MARK = "/* 13.x Realizzazioni"

CSS_ANCHOR = "\n</style>"
CSS = r"""
/* 13.x Realizzazioni. Impaginazione ispirata alle pagine progetti di Viabizzuno: griglia regolare di card con
   scheda tecnica apribile, barra dei filtri tra due filetti, pagina progetto con scheda "dettagli", testo stretto
   accanto a una foto grande, sequenza di foto a tutta larghezza e a coppie, barra delle sezioni in basso. */
.todo { display: inline-block; padding: 0 6px; border: 1px dashed var(--color-line-strong); border-radius: var(--radius); color: var(--color-ardesia); font-size: var(--fs-small); font-style: italic; font-weight: 400; }
.todo--block { display: block; padding: var(--space-16); }
.intro-cols { display: grid; gap: var(--space-16); color: var(--color-ardesia); }
.intro-cols .lead { color: var(--color-ink); }
/* Barra dei filtri: voci come testo, quella attiva sottolineata nel colore del logo */
.filters { display: flex; flex-wrap: wrap; align-items: center; column-gap: var(--space-32); margin-bottom: clamp(32px, 4vw, 56px); border-top: 1px solid var(--color-ink); border-bottom: 1px solid var(--color-line); }
.filters[hidden] { display: none; }
.filters__group { display: flex; flex-wrap: wrap; align-items: center; column-gap: var(--space-4); }
.filters__label { margin-right: var(--space-8); color: var(--color-ink); font-size: var(--fs-small); font-weight: 600; }
.chip { display: inline-flex; align-items: center; gap: 6px; min-height: 48px; padding: 0 var(--space-8); border: 0; background: none; color: var(--color-ardesia); font: inherit; font-size: var(--fs-small); text-underline-offset: 8px; cursor: pointer; }
.chip .icon { width: 16px; height: 16px; color: var(--color-brand); }
.chip:hover { color: var(--color-ink); }
.chip[aria-pressed="true"] { color: var(--color-ink); text-decoration: underline 2px var(--color-brand); }
.chip:focus-visible { outline: 2px solid var(--color-brand); outline-offset: -2px; }
.filters__status { display: flex; align-items: center; min-height: 48px; margin-left: auto; color: var(--color-ardesia); font-size: var(--fs-small); }
.filters__status:only-child { margin-left: 0; } /* nessun gruppo da filtrare: resta solo il conteggio */
@media (max-width: 767.98px) {
  .filters { display: grid; }
  .filters__group { flex-wrap: nowrap; overflow-x: auto; margin-inline: calc(-1 * var(--container-pad)); padding-inline: var(--container-pad); border-bottom: 1px solid var(--color-line); scrollbar-width: none; }
  .filters__group::-webkit-scrollbar { display: none; }
  .filters__label, .chip { flex: none; }
  .filters__status { min-height: 0; margin: 0; padding-block: var(--space-12); }
}
/* Griglia regolare di card: foto 4:3, titolo ed etichetta, "Dettagli" apribile */
.pgrid { display: grid; gap: clamp(40px, 5vw, 64px) var(--gutter); }
@media (min-width: 768px) { .pgrid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .pgrid:not(.pgrid--two) { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
.pcard { display: grid; align-content: start; }
.pcard[hidden] { display: none; }
.pcard__media { display: block; overflow: hidden; margin-bottom: var(--space-16); background: var(--color-calce); }
.pcard__media .media { aspect-ratio: 4 / 3; transition: transform var(--dur-slow) var(--ease); }
.pgrid--two .pcard__media .media { aspect-ratio: 3 / 2; }
@media (hover: hover) { .pcard__media:hover .media, .pcard:has(.pcard__title a:hover) .media { transform: scale(1.03); } }
.pcard__head { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--space-12); padding-bottom: var(--space-12); border-bottom: 1px solid var(--color-ink); }
.pcard__title { font: 600 1.0625rem/1.3 var(--font-display); }
.pcard__title a { color: var(--color-ink); text-decoration: none; text-decoration-thickness: 1px; text-underline-offset: 4px; }
.pcard__title a:hover { text-decoration-line: underline; }
.pcard__title a:focus-visible { outline: 2px solid var(--color-brand); outline-offset: 3px; }
.pcard__text { padding-top: var(--space-12); color: var(--color-ardesia); font-size: var(--fs-small); }
.ptag { display: inline-flex; flex: none; align-items: center; gap: 6px; padding: 3px 8px; border: 1px solid var(--color-line-strong); border-radius: var(--radius); background: var(--color-bg); color: var(--color-ink); font: 500 var(--fs-tag)/1.3 var(--font-text); white-space: nowrap; }
.ptag .icon { width: 16px; height: 16px; color: var(--color-brand); }
.pcard__details { border-bottom: 1px solid var(--color-line); }
.pcard__details summary { display: flex; align-items: center; justify-content: space-between; min-height: 44px; color: var(--color-ardesia); font-size: var(--fs-small); list-style: none; cursor: pointer; }
.pcard__details summary::-webkit-details-marker { display: none; }
.pcard__details summary:hover { color: var(--color-ink); }
.pcard__details summary:focus-visible { outline: 2px solid var(--color-brand); outline-offset: -2px; }
.pcard__details summary .icon { width: 18px; height: 18px; transition: transform var(--dur-ui) var(--ease); }
.pcard__details[open] summary .icon { transform: rotate(180deg); }
.specs { display: grid; margin: 0 0 var(--space-12); font-size: var(--fs-small); line-height: 1.45; }
.specs > div { display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 3fr); gap: var(--space-12); padding: 6px 0; border-top: 1px solid var(--color-line); }
.specs > div:first-child { border-top: 0; }
.specs dt { color: var(--color-ardesia); }
.specs dd { margin: 0; color: var(--color-ink); }
.specs a { color: var(--color-brand); text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 3px; }
.projects__more { display: flex; justify-content: center; margin-top: clamp(40px, 5vw, 64px); }
.projects__empty { display: grid; justify-items: start; gap: var(--space-16); padding: var(--space-32) 0; }
/* Pagina progetto: titolo ed etichette, foto d'apertura 16:9 */
.project-head__row { row-gap: var(--space-16); }
.project-head__tags { display: flex; flex-wrap: wrap; gap: var(--space-8); }
@media (min-width: 1024px) { .project-head__tags { grid-column: 8 / -1; align-self: end; justify-content: flex-end; } }
/* Scheda "dettagli": tabella su due colonne tra filetti */
.credits { row-gap: var(--space-16); }
.credits__title { font-size: var(--fs-h3); }
.specs--credits { margin: 0; border-bottom: 1px solid var(--color-line); font-size: var(--fs-body); }
.specs--credits > div { padding: var(--space-12) 0; }
.specs--credits > div:first-child { border-top: 1px solid var(--color-ink); }
@media (min-width: 1024px) {
  .credits__title { grid-column: 1 / span 4; }
  .specs--credits { grid-column: 5 / -1; }
  .specs--credits > div { grid-template-columns: minmax(0, 1fr) minmax(0, 2fr); }
}
/* Il progetto: testo stretto a sinistra, che resta in vista, e foto grande a destra */
.story-intro { row-gap: var(--space-32); align-items: start; }
.story-intro__text h2 { margin-bottom: var(--space-8); font-size: var(--fs-h3); }
.story-intro__text h3 { margin-top: var(--space-24); color: var(--color-ardesia); font-size: var(--fs-small); font-weight: 600; letter-spacing: 0.02em; }
.story-intro__media, .story-intro__before { display: grid; gap: var(--space-8); margin: 0; }
.story-intro__media .media { aspect-ratio: 4 / 5; }
@media (min-width: 1024px) {
  .story-intro__text { grid-column: 1 / span 4; position: sticky; top: calc(var(--header-h) + var(--space-24)); }
  .story-intro__media { grid-column: 6 / -1; }
}
/* Sequenza di foto: a tutta larghezza, a coppie, a metà destra. Ogni foto si apre a schermo intero. */
.sequence { display: grid; gap: clamp(32px, 5vw, 80px); }
.seq figure, .pgallery figure { display: grid; gap: var(--space-8); margin: 0; }
.seq a, .pgallery a { display: block; overflow: hidden; cursor: zoom-in; }
.seq a:focus-visible, .pgallery a:focus-visible { outline: 2px solid var(--color-brand); outline-offset: 3px; }
.seq .media, .pgallery .media { transition: transform var(--dur-slow) var(--ease); }
@media (hover: hover) { .seq a:hover .media, .pgallery a:hover .media { transform: scale(1.015); } }
.seq--full .media { aspect-ratio: 16 / 9; }
.seq--pair, .seq--half { display: grid; gap: var(--gutter); }
.seq--pair .media, .seq--half .media { aspect-ratio: 4 / 3; }
.seq--tall .media { aspect-ratio: 4 / 5; }
@media (min-width: 768px) {
  .seq--pair { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .seq--half { width: calc((100% - var(--gutter)) / 2); margin-left: auto; }
}
.seq figcaption, .pgallery figcaption, .story-intro figcaption { color: var(--color-ardesia); font-size: var(--fs-small); line-height: 1.4; }
.pgallery { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-24) var(--gutter); }
@media (min-width: 1024px) { .pgallery { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
.pgallery .media { aspect-ratio: 4 / 3; }
/* Barra delle sezioni del progetto, fissa in basso da 768px (sotto c'è già la barra mobile) */
.pnav { display: none; }
@media (min-width: 768px) {
  .pnav { position: fixed; right: 0; bottom: 0; left: 0; z-index: 30; display: block; border-top: 1px solid var(--color-line); background: rgba(255, 255, 255, 0.96); transition: transform var(--dur-ui) var(--ease); }
  .js .pnav:not(.is-visible) { transform: translateY(100%); }
  .pnav__inner { display: flex; align-items: center; justify-content: space-between; gap: var(--space-16); }
  .pnav__links { display: flex; }
  .pnav__links li + li { border-left: 1px solid var(--color-line); }
  .pnav__links a { display: inline-flex; align-items: center; min-height: 52px; padding: 0 var(--space-24); color: var(--color-ardesia); font-size: var(--fs-small); font-weight: 600; text-decoration: none; }
  .pnav__links li:first-child a { padding-left: 0; }
  .pnav__links a:hover, .pnav__links a[aria-current] { color: var(--color-ink); }
  .pnav__links a[aria-current] { box-shadow: inset 0 -2px var(--color-brand); }
  .pnav a:focus-visible { outline: 2px solid var(--color-brand); outline-offset: -2px; }
  body:has(.pnav) { padding-bottom: 52px; }
}
@media (prefers-reduced-motion: reduce) { .pnav { transition: none; } }
/* Confronto prima/dopo */
.compare { position: relative; overflow: hidden; aspect-ratio: 16 / 9; background: var(--color-calce); --pos: 50%; }
.compare > img, .compare__before > * { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.compare__before { position: absolute; inset: 0; clip-path: inset(0 calc(100% - var(--pos)) 0 0); }
.compare__before .todo { display: flex; align-items: flex-end; padding: var(--space-16); border: 0; border-radius: 0; background: var(--color-calce); }
.compare::after { content: ""; position: absolute; top: 0; bottom: 0; left: var(--pos); width: 2px; margin-left: -1px; background: #FFFFFF; pointer-events: none; }
.compare__handle { position: absolute; top: 50%; left: var(--pos); z-index: 1; display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; margin: -22px 0 0 -22px; border-radius: var(--radius); background: #FFFFFF; color: var(--color-ink); box-shadow: var(--shadow-overlay); pointer-events: none; }
.compare__handle .icon { width: 16px; height: 16px; margin: 0 -2px; }
.compare__range { position: absolute; inset: 0; z-index: 2; width: 100%; height: 100%; margin: 0; opacity: 0; cursor: ew-resize; }
.compare__range:focus-visible + .compare__handle { outline: 2px solid var(--color-brand); outline-offset: 2px; }
.compare__label { position: absolute; top: var(--space-12); z-index: 1; padding: 2px 8px; border-radius: var(--radius); background: rgba(17, 46, 46, 0.8); color: #FFFFFF; font: 500 var(--fs-tag)/1.3 var(--font-text); pointer-events: none; }
.compare__label--before { left: var(--space-12); }
.compare__label--after { right: var(--space-12); }
/* Risultato e testimonianza */
@media (min-width: 1024px) { .pillars--3 { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
.result__quote { max-width: 52rem; margin-top: clamp(32px, 4vw, 56px); }
.quote { margin: 0; padding-left: var(--space-24); border-left: 2px solid var(--color-brand); }
.quote p { font: 400 var(--fs-h4)/1.45 var(--font-display); }
.quote footer { margin-top: var(--space-12); color: var(--color-ardesia); font-size: var(--fs-small); }
/* Galleria a schermo intero */
.lightbox { width: 100%; max-width: none; height: 100%; max-height: none; margin: 0; padding: 0; border: 0; background: #0E1A1A; color: #FFFFFF; }
.lightbox[open] { display: grid; grid-template-rows: auto minmax(0, 1fr) auto; }
.lightbox::backdrop { background: #0E1A1A; }
.lightbox__bar, .lightbox__foot { display: flex; align-items: center; justify-content: space-between; gap: var(--space-16); padding: var(--space-12) var(--space-16); }
.lightbox__count { font-size: var(--fs-small); font-variant-numeric: tabular-nums; }
.lightbox__figure { display: grid; place-items: center; min-height: 0; margin: 0; padding: 0 var(--space-16); }
.lightbox__img { max-width: 100%; max-height: 100%; object-fit: contain; }
.lightbox__caption { flex: 1; color: rgba(255, 255, 255, 0.85); font-size: var(--fs-small); line-height: 1.4; text-align: center; }
.lightbox__btn { display: inline-grid; flex: none; place-items: center; width: 48px; height: 48px; border: 1px solid rgba(255, 255, 255, 0.4); border-radius: var(--radius); background: transparent; color: #FFFFFF; cursor: pointer; }
.lightbox__btn:hover { border-color: #FFFFFF; }
.lightbox__btn:focus-visible { outline: 2px solid #FFFFFF; outline-offset: 2px; }
"""

ICON_ANCHOR = '  <symbol id="i-alert"'
ICONS = """"""

JS_ANCHOR = """  /* -------------------------------------------------------------------
     6. Anno corrente nel footer"""
JS = """  /* -------------------------------------------------------------------
     7. Realizzazioni: filtri per tipo e prodotto e "Carica altre".
        Senza JS i filtri restano nascosti e si vedono tutte le card.
     ------------------------------------------------------------------- */
  $$("[data-projects]").forEach((box) => {
    const filters = $("[data-filters]", box);
    const cards = $$("[data-grid] > .pcard", box);
    const more = $("[data-more]", box);
    const empty = $("[data-empty]", box);
    const status = $("[data-status]", box);
    const page = Number(box.dataset.page || 9);
    const sel = { tipo: "", prodotto: "" };
    let shown = page;
    const match = (el) => Object.entries(sel).every(([k, v]) => !v || el.dataset[k].split(" ").includes(v));
    function render() {
      const hits = cards.filter(match);
      cards.forEach((el) => { el.hidden = true; });
      hits.slice(0, shown).forEach((el) => { el.hidden = false; });
      more.hidden = hits.length <= shown;
      empty.hidden = hits.length > 0;
      status.textContent = (hits.length === 1 ? status.dataset.one : status.dataset.many).replace("{n}", hits.length);
    }
    function pick(key, value) {
      sel[key] = value;
      $$(`[data-filter="${key}"]`, filters).forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.value === value)));
      shown = page;
      render();
    }
    filters.hidden = false;
    $$("[data-filter]", filters).forEach((b) => b.addEventListener("click", () => pick(b.dataset.filter, b.dataset.value)));
    $("[data-reset]", box).addEventListener("click", () => { pick("tipo", ""); pick("prodotto", ""); });
    more.addEventListener("click", () => {
      const next = cards.filter(match)[shown];
      shown += page;
      render();
      if (next) $(".pcard__title a", next).focus();
    });
    render();
  });

  /* -------------------------------------------------------------------
     8. Confronto prima/dopo: il cursore (input range) sposta il taglio tra le due foto
     ------------------------------------------------------------------- */
  $$(".compare").forEach((c) => {
    const range = $(".compare__range", c);
    const set = () => c.style.setProperty("--pos", `${range.value}%`);
    range.addEventListener("input", set);
    set();
  });

  /* -------------------------------------------------------------------
     9. Galleria a schermo intero: <dialog> nativo, frecce e tasti sinistra/destra.
        Senza JS ogni foto si apre da sola nella sua dimensione più grande.
        Alla chiusura il browser riporta il focus sulla foto da cui si è aperta.
     ------------------------------------------------------------------- */
  const lightbox = $("#lightbox");
  if (lightbox) {
    const links = $$("[data-lightbox]");
    const img = $(".lightbox__img", lightbox);
    const caption = $(".lightbox__caption", lightbox);
    const count = $(".lightbox__count", lightbox);
    let current = 0;
    const show = (n) => {
      current = (n + links.length) % links.length;
      const a = links[current];
      img.src = a.href;
      img.alt = $("img", a).alt;
      caption.textContent = a.dataset.caption || "";
      count.textContent = `${current + 1} / ${links.length}`;
    };
    const open = (n) => { show(n); lightbox.showModal(); };
    links.forEach((a, n) => a.addEventListener("click", (e) => { e.preventDefault(); open(n); }));
    $$("[data-lightbox-open]").forEach((b) => b.addEventListener("click", () => { if (links.length) open(0); }));
    $("[data-lb-prev]", lightbox).addEventListener("click", () => show(current - 1));
    $("[data-lb-next]", lightbox).addEventListener("click", () => show(current + 1));
    $("[data-lb-close]", lightbox).addEventListener("click", () => lightbox.close());
    lightbox.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });
    lightbox.addEventListener("click", (e) => { if (e.target === lightbox || e.target.classList.contains("lightbox__figure")) lightbox.close(); });
  }

  /* -------------------------------------------------------------------
     10. Barra delle sezioni del progetto: compare dopo la foto d'apertura
         e sottolinea la sezione che si sta leggendo.
     ------------------------------------------------------------------- */
  const pnav = $(".pnav");
  if (pnav && "IntersectionObserver" in window) {
    new IntersectionObserver(([e]) => {
      pnav.classList.toggle("is-visible", !e.isIntersecting && e.boundingClientRect.top < 0);
    }).observe($(".project-head"));
    const navLinks = $$(".pnav__links a", pnav);
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        navLinks.forEach((a) => {
          if (a.hash === `#${en.target.id}`) a.setAttribute("aria-current", "true");
          else a.removeAttribute("aria-current");
        });
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    navLinks.forEach((a) => { const s = document.getElementById(a.hash.slice(1)); if (s) spy.observe(s); });
  }

"""

JS_START = "  /* -------------------------------------------------------------------\n     7. Realizzazioni"

def replace_block(s, start, end, block):
    """Inserisce il blocco prima di `end`; se c'è già (da `start` a `end`) lo sostituisce."""
    if end not in s: return None
    i = s.find(start)
    if i != -1: s = s[:i] + s[s.index(end, i):]
    return s.replace(end, block + end, 1)

def main():
    n = 0
    for f in sorted(ROOT.rglob("index.html")):
        if ".git" in f.parts: continue
        s = o = f.read_bytes().decode("utf-8")
        if 'name="robots" content="noindex"' in s and "location.replace(" in s: continue
        for start, end, block, what in (("\n" + MARK, CSS_ANCHOR, "\n" + CSS.strip("\n"), "stile"),
                                        ('  <symbol id="i-cat-casa"', ICON_ANCHOR, ICONS, "icone"),
                                        (JS_START, JS_ANCHOR, JS, "script")):
            s = replace_block(s, start, end, block)
            if s is None: raise SystemExit(f"{f}: punto di inserimento ({what}) non trovato")
        if s != o:
            f.write_bytes(s.encode("utf-8")); n += 1
    print("pagine aggiornate:", n)

if __name__ == "__main__":
    main()
