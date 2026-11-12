/* =====================================================================
   INVITO ALLA NEWSLETTER
   Alla prima visita, dopo la scelta sui cookie, compare una finestra che invita a iscriversi.
   Arriva dopo 12 secondi sulla pagina oppure quando si è letta quasi metà pagina (non prima di
   4 secondi), mai sopra un'altra finestra aperta, il menu o il pannello dell'accessibilità.
   Si vede una volta sola: se la chiudi ricompare dopo 6 mesi, se ti iscrivi mai più.
   La scelta resta nel browser (localStorage "ig-newsletter", elencato nell'informativa cookie).
   Non compare in area riservata, privacy e cookie. Per rivederla: aggiungere ?newsletter all'indirizzo.
   Stile in /assets/newsletter.css, caricato da qui solo quando serve.

   INVIO: con DEMO_MODE = true l'iscrizione è simulata. Per la messa online collegare ENDPOINT al
   servizio scelto (Brevo, Mailchimp o simili) con doppia conferma via email; il servizio deve
   rispondere 2xx se va a buon fine. Campi inviati: email, consenso, lingua, pagina, website (esca antispam).
   ===================================================================== */
(() => {
  "use strict";

  const DEMO_MODE = true;
  const ENDPOINT = "/api/newsletter.php";
  const KEY = "ig-newsletter";
  const AGAIN_AFTER = 180 * 864e5; // se chiusa senza iscriversi, ricompare dopo 6 mesi
  const DELAY = 12000;             // tempo sulla pagina prima di comparire
  const MIN_DELAY = 4000;          // minimo, anche se si scorre subito
  const SCROLL_SHARE = 0.4;        // quota di pagina letta che la fa comparire prima
  const CSS = "/assets/newsletter.css?v=3";

  const root = document.documentElement;
  const force = /[?&]newsletter\b/.test(location.search);
  if (/^\/(en\/)?(area-riservata|privacy|cookie|cookies)(\/|$)/.test(location.pathname)) return;
  if (!("HTMLDialogElement" in window)) return;

  const read = () => { try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; } };
  const save = (stato) => { try { localStorage.setItem(KEY, JSON.stringify({ stato, data: Date.now() })); } catch (e) { /* storage non disponibile */ } };
  const prev = read();
  if (!force && prev && (prev.stato === "iscritto" || Date.now() - prev.data < AGAIN_AFTER)) return;

  const EN = (root.lang || "").toLowerCase().startsWith("en");
  const T = EN ? {
    title: "Ideas and news for your home",
    text: "New projects, guides to materials and updates on tax incentives, straight to your inbox.",
    label: "Your email",
    placeholder: "name@example.com",
    submit: "Subscribe",
    sending: "Sending",
    consent: 'I would like to receive the newsletter and I have read the <a href="/en/privacy/">privacy notice</a>.',
    later: "No, thanks",
    close: "Close",
    errEmail: "Enter a valid email address.",
    errConsent: "To subscribe, please tick the consent box.",
    errSend: "We could not complete your subscription. Please try again in a moment.",
    doneTitle: "Thank you!",
    doneText: "Check your inbox: we have sent you an email to confirm your subscription.",
    dialog: "Newsletter",
  } : {
    title: "Idee e novità per la tua casa",
    text: "Nuove realizzazioni, guide ai materiali e aggiornamenti sulle detrazioni, direttamente nella tua casella email.",
    label: "La tua email",
    placeholder: "nome@esempio.it",
    submit: "Iscriviti",
    sending: "Invio in corso",
    consent: 'Voglio ricevere la newsletter e ho letto l\'<a href="/privacy/">informativa privacy</a>.',
    later: "No, grazie",
    close: "Chiudi",
    errEmail: "Scrivi un indirizzo email valido.",
    errConsent: "Per iscriverti spunta la casella del consenso.",
    errSend: "Non siamo riusciti a completare l'iscrizione. Riprova tra qualche istante.",
    doneTitle: "Grazie!",
    doneText: "Controlla la tua casella: ti abbiamo scritto per confermare l'iscrizione.",
    dialog: "Newsletter",
  };

  let dlg, cssReady, opened = false, closing = false, lastFocus = null;

  /* ---------- Costruzione (quando la pagina è pronta: foto e stile arrivano prima di mostrarla) ---------- */
  function build() {
    cssReady = new Promise((resolve) => {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = CSS;
      link.onload = resolve;
      link.onerror = resolve;
      document.head.appendChild(link);
    });
    dlg = document.createElement("dialog");
    dlg.className = "nl";
    dlg.setAttribute("aria-labelledby", "nl-title");
    dlg.setAttribute("aria-describedby", "nl-text");
    dlg.innerHTML = `
      <div class="nl__scrim" data-nl-close></div>
      <div class="nl__card">
        <div class="nl__media"><img src="/assets/img/home/hero-linvisibile-atrio-768.jpg" srcset="/assets/img/home/hero-linvisibile-atrio-768.jpg 768w, /assets/img/home/hero-linvisibile-atrio-1024.jpg 1024w" sizes="(min-width: 768px) 370px, 100vw" width="768" height="512" alt="" decoding="async"></div>
        <div class="nl__body">
          <h2 class="nl__title attach" id="nl-title" tabindex="-1">${T.title}</h2>
          <p class="nl__text" id="nl-text">${T.text}</p>
          <form class="nl__form" novalidate>
            <label class="nl__label" for="nl-email">${T.label}</label>
            <div class="nl__row">
              <input class="input" id="nl-email" name="email" type="email" inputmode="email" autocomplete="email" autocapitalize="off" spellcheck="false" required placeholder="${T.placeholder}">
              <button class="btn btn--primary" type="submit">${T.submit}</button>
            </div>
            <div class="check-field">
              <input id="nl-consenso" name="consenso" type="checkbox" value="si" required>
              <label for="nl-consenso">${T.consent}</label>
            </div>
            <div class="nl__hp" aria-hidden="true"><label for="nl-website">Website</label><input id="nl-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
            <p class="field__error nl__alert" role="alert"></p>
          </form>
          <button class="link nl__later" type="button" data-nl-close>${T.later}</button>
          <div class="nl__done" hidden>
            <h2 class="nl__title attach" id="nl-done-title" tabindex="-1">${T.doneTitle}</h2>
            <p class="nl__text">${T.doneText}</p>
            <button class="btn btn--secondary" type="button" data-nl-close>${T.close}</button>
          </div>
        </div>
        <button class="nl__close" type="button" data-nl-close aria-label="${T.close}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
      </div>`;
    document.body.appendChild(dlg);

    const form = dlg.querySelector(".nl__form");
    const email = form.elements.email;
    const consent = form.elements.consenso;
    const alertBox = dlg.querySelector(".nl__alert");
    const submit = form.querySelector('[type="submit"]');

    dlg.addEventListener("click", (e) => { if (e.target.closest("[data-nl-close]")) hide(); });
    dlg.addEventListener("cancel", (e) => { e.preventDefault(); hide(); }); // Esc: chiusura animata
    [email, consent].forEach((el) => el.addEventListener("input", () => {
      el.removeAttribute("aria-invalid");
      if (!form.querySelector('[aria-invalid="true"]')) alertBox.textContent = "";
    }));

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      email.value = email.value.trim();
      const okEmail = email.value !== "" && email.checkValidity();
      const mark = (el, bad) => (bad ? el.setAttribute("aria-invalid", "true") : el.removeAttribute("aria-invalid"));
      mark(email, !okEmail);
      mark(consent, !consent.checked);
      if (!okEmail || !consent.checked) {
        alertBox.textContent = !okEmail ? T.errEmail : T.errConsent;
        (!okEmail ? email : consent).focus();
        return;
      }
      const fd = new FormData(form);
      fd.append("lingua", EN ? "en" : "it");
      fd.append("pagina", location.pathname);
      submit.disabled = true;
      submit.textContent = T.sending;
      alertBox.textContent = "";
      try {
        if (!fd.get("website")) { // esca vuota: richiesta di una persona
          if (DEMO_MODE) await new Promise((r) => setTimeout(r, 900));
          else {
            const res = await fetch(ENDPOINT, { method: "POST", body: fd, headers: { Accept: "application/json" } });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
          }
        }
        save("iscritto");
        form.hidden = true;
        dlg.querySelector(".nl__later").hidden = true;
        dlg.querySelector(".nl__body > .nl__title").hidden = true;
        dlg.querySelector("#nl-text").hidden = true;
        dlg.querySelector(".nl__done").hidden = false;
        dlg.setAttribute("aria-labelledby", "nl-done-title");
        dlg.querySelector("#nl-done-title").focus({ preventScroll: true });
      } catch (err) {
        alertBox.textContent = T.errSend;
        submit.textContent = T.submit;
      } finally {
        submit.disabled = false;
      }
    });
  }

  /* ---------- Apertura e chiusura ---------- */
  const busy = () => root.classList.contains("menu-open") || document.hidden ||
    Array.from(document.querySelectorAll("dialog[open]")).some((d) => d !== dlg) ||
    Boolean(document.querySelector("#cookie:not([hidden])"));

  async function show() {
    if (opened) return;
    if (busy()) { setTimeout(show, 3000); return; }
    opened = true;
    await cssReady;
    save("visto");
    lastFocus = document.activeElement;
    dlg.showModal();
    root.classList.add("nl-open");
    dlg.querySelector("#nl-title").focus({ preventScroll: true });
    // il browser registra lo stato iniziale, poi parte la transizione (timer e non requestAnimationFrame,
    // che con la scheda in secondo piano può restare fermo e lasciare la finestra invisibile)
    dlg.getBoundingClientRect();
    setTimeout(() => dlg.classList.add("is-in"), 30);
  }

  function hide() {
    if (closing || !dlg.open) return;
    closing = true;
    if ((read() || {}).stato !== "iscritto") save("chiuso");
    dlg.classList.remove("is-in");
    dlg.classList.add("is-out");
    setTimeout(() => {
      dlg.close();
      dlg.classList.remove("is-out");
      root.classList.remove("nl-open");
      closing = false;
      if (lastFocus && lastFocus.isConnected && lastFocus !== document.body) lastFocus.focus({ preventScroll: true });
    }, 320);
  }

  /* ---------- Quando: dopo la scelta sui cookie, poi tempo o lettura ---------- */
  function arm() {
    build();
    const t0 = Date.now();
    if (force) { setTimeout(show, 800); return; }
    const timer = setTimeout(show, DELAY);
    const onScroll = () => {
      const max = root.scrollHeight - innerHeight;
      if (max > 0 && scrollY / max >= SCROLL_SHARE && Date.now() - t0 >= MIN_DELAY) {
        removeEventListener("scroll", onScroll);
        clearTimeout(timer);
        show();
      }
    };
    addEventListener("scroll", onScroll, { passive: true });
  }

  function start() {
    const banner = document.getElementById("cookie");
    if (banner && !banner.hidden) document.addEventListener("ig:consent", arm, { once: true });
    else arm();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
