/* =====================================================================
   WIDGET ACCESSIBILITÀ
   Pulsante fisso in basso a sinistra (su telefono sopra la barra dei contatti) che apre
   un pannello <dialog> con le regolazioni di lettura. Ogni regolazione è una classe su <html>
   (a11y-...), con lo stile in /assets/accessibilita.css. Le scelte sono salvate in
   localStorage ("ig-a11y") come elenco di classi, che lo script in <head> rimette subito.
   Testi in italiano o in inglese secondo il lang della pagina.
   ===================================================================== */
(() => {
  "use strict";
  const KEY = "ig-a11y";
  const root = document.documentElement;
  const en = root.lang.toLowerCase().startsWith("en");

  const T = en ? {
    open: "Accessibility options",
    title: "Accessibility",
    close: "Close",
    size: "Text size",
    smaller: "Decrease text size",
    bigger: "Increase text size",
    reset: "Reset",
    note: "Your choices are saved on this device.",
    contrasto: "High contrast",
    link: "Highlight links",
    carattere: "Readable font",
    spazi: "Text spacing",
    fermo: "Stop animations",
    grigi: "Greyscale",
    cursore: "Large cursor",
    guida: "Reading guide",
  } : {
    open: "Opzioni di accessibilità",
    title: "Accessibilità",
    close: "Chiudi",
    size: "Dimensione del testo",
    smaller: "Riduci il testo",
    bigger: "Ingrandisci il testo",
    reset: "Ripristina",
    note: "Le scelte restano salvate su questo dispositivo.",
    contrasto: "Contrasto elevato",
    link: "Evidenzia i link",
    carattere: "Carattere leggibile",
    spazi: "Spaziatura del testo",
    fermo: "Ferma le animazioni",
    grigi: "Scala di grigi",
    cursore: "Cursore grande",
    guida: "Guida di lettura",
  };

  const SIZES = [100, 115, 130, 150];
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  // Cursore e guida servono solo con il mouse: sui touch non si mostrano
  const TOGGLES = ["contrasto", "link", "carattere", "spazi", "fermo", "grigi"].concat(fine ? ["cursore", "guida"] : []);

  const ICONS = {
    access: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="6.9" r="1.3" fill="currentColor" stroke="none"/><path d="M7 9.6l5 1.1 5-1.1M12 10.7v3.6l-2.6 4.4M12 14.3l2.6 4.4"/></svg>',
    close: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    reset: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.4-5.7L4 8.5"/><path d="M4 4v4.5h4.5"/></svg>',
    contrasto: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg>',
    link: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>',
    carattere: '<span class="a11y-toggle__icon" aria-hidden="true">Aa</span>',
    spazi: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 5h11M10 12h11M10 19h11M4 4v16M2 6l2-2 2 2M2 18l2 2 2-2"/></svg>',
    fermo: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M10 9v6M14 9v6"/></svg>',
    grigi: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/><path d="M12 8v12" /></svg>',
    cursore: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3l14 7.5-6.2 1.6L10 18z"/><path d="M13 12.5l5 6"/></svg>',
    guida: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18M3 19h18"/><rect x="3" y="9" width="18" height="6" rx="1"/></svg>',
  };

  // Stato attuale, letto dalle classi già messe dallo script in <head>
  let size = Math.max(0, SIZES.findIndex((_, i) => i && root.classList.contains(`a11y-testo-${i}`)));
  const on = Object.fromEntries(TOGGLES.map((id) => [id, root.classList.contains(`a11y-${id}`)]));

  /* ---------- Pulsante e pannello ---------- */
  const fab = document.createElement("button");
  fab.type = "button";
  fab.className = "a11y-ui a11y-fab";
  fab.setAttribute("aria-label", T.open);
  fab.setAttribute("aria-haspopup", "dialog");
  fab.setAttribute("aria-controls", "a11y-panel");
  fab.innerHTML = ICONS.access;

  const panel = document.createElement("dialog");
  panel.className = "a11y-ui a11y-panel";
  panel.id = "a11y-panel";
  panel.setAttribute("aria-labelledby", "a11y-title");
  panel.innerHTML = `
    <div class="a11y-panel__inner">
      <div class="a11y-panel__head">
        <h2 class="a11y-panel__title" id="a11y-title">${T.title}</h2>
        <button class="a11y-icon-btn" type="button" data-a11y-close aria-label="${T.close}">${ICONS.close}</button>
      </div>
      <div class="a11y-size" role="group" aria-labelledby="a11y-size-label">
        <span class="a11y-label" id="a11y-size-label">${T.size}</span>
        <div class="a11y-size__row">
          <button class="a11y-size__btn" type="button" data-a11y-size="-1" aria-label="${T.smaller}">A&minus;</button>
          <output class="a11y-size__value" aria-live="polite"></output>
          <button class="a11y-size__btn" type="button" data-a11y-size="1" aria-label="${T.bigger}">A+</button>
        </div>
      </div>
      <ul class="a11y-grid">
        ${TOGGLES.map((id) => `<li><button class="a11y-toggle" type="button" data-a11y="${id}" aria-pressed="false">${ICONS[id]}<span>${T[id]}</span></button></li>`).join("")}
      </ul>
      <div class="a11y-foot">
        <p class="a11y-note">${T.note}</p>
        <button class="a11y-reset" type="button" data-a11y-reset>${ICONS.reset}${T.reset}</button>
      </div>
    </div>`;

  // Dopo il link "Salta al contenuto", così da tastiera si raggiunge subito
  const skip = document.querySelector(".skip-link");
  if (skip) skip.after(fab); else document.body.prepend(fab);
  document.body.append(panel);

  const $ = (s) => panel.querySelector(s);
  const output = $(".a11y-size__value");
  const [smaller, bigger] = panel.querySelectorAll("[data-a11y-size]");

  /* ---------- Guida di lettura ---------- */
  let guide = null;
  const moveGuide = (e) => {
    guide.style.transform = `translateY(${e.clientY - 48}px)`;
    guide.classList.add("is-visible");
  };
  function setGuide(active) {
    if (active && !guide) {
      guide = document.createElement("div");
      guide.className = "a11y-ui a11y-fascia";
      guide.setAttribute("aria-hidden", "true");
      document.body.append(guide);
      addEventListener("pointermove", moveGuide, { passive: true });
    } else if (!active && guide) {
      removeEventListener("pointermove", moveGuide);
      guide.remove();
      guide = null;
    }
  }

  /* ---------- Applica e salva ---------- */
  function apply() {
    const classes = [];
    if (size) classes.push(`a11y-testo-${size}`);
    TOGGLES.forEach((id) => { if (on[id]) classes.push(`a11y-${id}`); });
    const wasStill = root.classList.contains("a11y-fermo");
    [...root.classList].filter((c) => c.startsWith("a11y-")).forEach((c) => root.classList.remove(c));
    root.classList.add(...classes);
    try {
      if (classes.length) localStorage.setItem(KEY, classes.join(" "));
      else localStorage.removeItem(KEY);
    } catch (e) { /* archiviazione non disponibile: le scelte valgono solo per questa pagina */ }

    output.textContent = `${SIZES[size]}%`;
    smaller.disabled = size === 0;
    bigger.disabled = size === SIZES.length - 1;
    panel.querySelectorAll("[data-a11y]").forEach((b) => b.setAttribute("aria-pressed", String(on[b.dataset.a11y])));
    fab.toggleAttribute("data-active", classes.length > 0);
    setGuide(on.guida);
    // Il carosello dell'hero riprogramma il cambio foto a ogni visibilitychange e legge a11y-fermo
    if (wasStill !== Boolean(on.fermo)) document.dispatchEvent(new Event("visibilitychange"));
  }

  panel.querySelectorAll("[data-a11y-size]").forEach((b) => b.addEventListener("click", () => {
    size = Math.min(SIZES.length - 1, Math.max(0, size + Number(b.dataset.a11ySize)));
    apply();
  }));
  panel.querySelectorAll("[data-a11y]").forEach((b) => b.addEventListener("click", () => {
    on[b.dataset.a11y] = !on[b.dataset.a11y];
    apply();
  }));
  $("[data-a11y-reset]").addEventListener("click", () => {
    size = 0;
    TOGGLES.forEach((id) => { on[id] = false; });
    apply();
  });

  /* ---------- Apertura e chiusura ---------- */
  fab.addEventListener("click", () => {
    panel.showModal();
    $("[data-a11y-close]").focus();
  });
  $("[data-a11y-close]").addEventListener("click", () => panel.close());
  // Clic sul fondo scuro fuori dal pannello
  panel.addEventListener("click", (e) => { if (e.target === panel) panel.close(); });
  panel.addEventListener("close", () => fab.focus());

  apply();
})();
