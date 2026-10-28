/*
  AREA RISERVATA: moduli di accesso, registrazione e password, pagina dei documenti.
  Il server sta in /api/area/ (PHP e MySQL su Hostinger, istruzioni in _sorgenti/area-riservata/LEGGIMI.md).
  Senza server (anteprima GitHub Pages, server locale) le API non rispondono in JSON:
  le pagine lo riconoscono e mostrano l'avviso "area non ancora attiva".
*/
(() => {
  const API = "/api/area/";
  const DOCUMENTI = "/area-riservata/documenti/";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  class NonAttiva extends Error {}

  /* GET senza dati, POST con dati in JSON. Ritorna { stato, ok, ... } oppure lancia NonAttiva */
  async function api(nome, dati) {
    const opts = { credentials: "same-origin", headers: { Accept: "application/json" } };
    if (dati !== undefined) {
      opts.method = "POST";
      opts.headers["Content-Type"] = "application/json";
      opts.headers["X-Requested-With"] = "fetch";
      opts.body = JSON.stringify(dati);
    }
    let res;
    try { res = await fetch(API + nome + ".php", opts); } catch (e) { throw new NonAttiva(); }
    const json = (res.headers.get("content-type") || "").includes("application/json") ? await res.json().catch(() => null) : null;
    if (!json || json.errore === "non_configurato") throw new NonAttiva();
    return { stato: res.status, ...json };
  }

  const avviso = $("[data-area-off]");
  const spento = () => {
    if (avviso) avviso.hidden = false;
    $$("[data-area-form] button[type=submit]").forEach((b) => { b.disabled = true; });
  };

  /* Dopo l'accesso torna alla pagina richiesta, ma solo dentro l'area riservata */
  const destinazione = () => {
    const t = new URLSearchParams(location.search).get("torna") || "";
    return t.startsWith("/area-riservata/") && !t.startsWith("//") ? t : DOCUMENTI;
  };

  /* -------------------------------------------------------------------
     Validazione: stessi messaggi e stessa grafica del preventivatore
     ------------------------------------------------------------------- */
  function setError(el, msg) {
    const box = el.closest(".field, .check-field");
    let err = $(".field__error", box);
    if (msg) {
      if (!err) {
        err = document.createElement("p");
        err.className = "field__error";
        err.id = el.id + "-err";
        err.innerHTML = '<svg class="icon" aria-hidden="true"><use href="#i-alert"/></svg><span></span>';
        box.append(err);
      }
      $("span", err).textContent = msg;
      el.setAttribute("aria-invalid", "true");
      el.setAttribute("aria-describedby", [el.dataset.hint, err.id].filter(Boolean).join(" "));
    } else {
      if (err) err.remove();
      el.removeAttribute("aria-invalid");
      if (el.dataset.hint) el.setAttribute("aria-describedby", el.dataset.hint);
      else el.removeAttribute("aria-describedby");
    }
  }
  // minlength a mano: il browser lo controlla solo sui valori digitati, non su quelli inseriti dall'autocompletamento
  const valido = (el) => el.type === "checkbox" ? el.checked : el.checkValidity() && el.value.trim() !== "" && el.value.length >= Math.max(0, el.minLength);
  const check = (el) => valido(el) || !el.required ? "" : el.dataset.error;
  function valida(form) {
    let first = null;
    $$("input[required]", form).forEach((el) => {
      const msg = check(el);
      setError(el, msg);
      if (msg && !first) first = el;
    });
    if (first) first.focus();
    return !first;
  }

  function messaggio(form, testo) {
    const box = $(".riservata-alert", form);
    box.textContent = testo || "";
    box.hidden = !testo;
  }

  /* Mostra o nasconde la password */
  $$("[data-pw-toggle]").forEach((b) => b.addEventListener("click", () => {
    const input = $("input", b.closest(".pw"));
    const show = input.type === "password";
    input.type = show ? "text" : "password";
    b.setAttribute("aria-pressed", String(show));
    b.textContent = show ? "Nascondi" : "Mostra";
  }));

  /* -------------------------------------------------------------------
     Moduli: ognuno ha data-area-form col nome dell'endpoint
     ------------------------------------------------------------------- */
  const dopo = {
    accedi: () => location.assign(destinazione()),
    registrati: () => location.assign(destinazione()),
    "password-nuova": () => location.assign(DOCUMENTI),
    "password-richiesta": (form) => {
      form.hidden = true;
      const ok = $("[data-area-sent]");
      ok.hidden = false;
      $("h2", ok).focus();
    },
  };

  $$("[data-area-form]").forEach((form) => {
    form.addEventListener("input", (e) => { if (e.target.hasAttribute("aria-invalid") && !check(e.target)) setError(e.target, ""); });
    form.addEventListener("change", (e) => { if (e.target.hasAttribute("aria-invalid") && !check(e.target)) setError(e.target, ""); });
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      messaggio(form, "");
      if (!valida(form)) return;
      const dati = {};
      $$("input[name]", form).forEach((el) => { dati[el.name] = el.type === "checkbox" ? el.checked : el.value; });
      const btn = $("button[type=submit]", form);
      btn.disabled = true;
      try {
        const r = await api(form.dataset.areaForm, dati);
        if (r.ok) return dopo[form.dataset.areaForm](form);
        const campo = r.errore && $(`input[name="${r.errore}"]`, form);
        if (campo) { setError(campo, r.messaggio); campo.focus(); }
        else messaggio(form, r.messaggio || "Qualcosa non ha funzionato. Riprova tra poco.");
      } catch (err) {
        if (err instanceof NonAttiva) spento();
        else messaggio(form, "Qualcosa non ha funzionato. Riprova tra poco.");
      }
      btn.disabled = false;
    });
  });

  /* Pagina della password: con ?t= nel link mostra il modulo per la nuova password */
  const token = new URLSearchParams(location.search).get("t");
  const nuova = $('[data-area-form="password-nuova"]');
  if (nuova && token) {
    $('[data-area-form="password-richiesta"]').hidden = true;
    nuova.hidden = false;
    $('input[name="token"]', nuova).value = token;
  }

  /* -------------------------------------------------------------------
     Accesso e registrazione: chi è già collegato va subito ai documenti
     ------------------------------------------------------------------- */
  if ($('[data-area-form="accedi"]')) {
    api("utente").then((r) => { if (r.ok) location.replace(destinazione()); }).catch((err) => { if (err instanceof NonAttiva) spento(); });
  }

  /* -------------------------------------------------------------------
     Documenti: senza sessione torna all'accesso
     ------------------------------------------------------------------- */
  const lista = $("[data-area-docs]");
  if (lista) {
    const num = new Intl.NumberFormat("it-IT", { maximumFractionDigits: 1 });
    const data = new Intl.DateTimeFormat("it-IT", { day: "numeric", month: "long", year: "numeric" });
    const peso = (b) => (b < 1024 * 1024 ? `${num.format(Math.max(1, b / 1024))} KB` : `${num.format(b / 1024 / 1024)} MB`);
    const el = (tag, cls, testo) => { const n = document.createElement(tag); if (cls) n.className = cls; if (testo) n.textContent = testo; return n; };

    (async () => {
      try {
        const u = await api("utente");
        if (!u.ok) return location.replace("/area-riservata/?torna=" + encodeURIComponent(location.pathname));
        $("[data-area-name]").textContent = u.utente.nome;
        $("[data-area-user]").hidden = false;
        const r = await api("documenti");
        lista.replaceChildren();
        if (!r.sezioni || !r.sezioni.length) { $("[data-area-empty]").hidden = false; return; }
        r.sezioni.forEach((s, i) => {
          const sec = el("section", "docs__section");
          const h = el("h2", "docs__title", s.titolo);
          h.id = "docs-" + i;
          sec.setAttribute("aria-labelledby", h.id);
          const ul = el("ul", "docs__list");
          s.file.forEach((f) => {
            const li = el("li", "doc");
            const a = el("a", "doc__link");
            a.href = API + "scarica.php?f=" + encodeURIComponent(f.file);
            a.setAttribute("download", "");
            const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            icon.setAttribute("class", "icon doc__icon");
            icon.setAttribute("aria-hidden", "true");
            icon.innerHTML = '<use href="#i-file"/>';
            const body = el("span", "doc__body");
            body.append(el("span", "doc__name", f.titolo), el("span", "doc__meta", `${f.tipo} · ${peso(f.byte)} · ${data.format(new Date(f.data))}`));
            const cta = el("span", "doc__cta", "Scarica");
            a.append(icon, body, cta);
            li.append(a);
            ul.append(li);
          });
          sec.append(h, ul);
          lista.append(sec);
        });
      } catch (err) {
        lista.replaceChildren();
        if (err instanceof NonAttiva) spento();
        else $("[data-area-error]").hidden = false;
      }
    })();

    $("[data-area-logout]").addEventListener("click", async () => {
      try { await api("esci", {}); } catch (e) { /* in ogni caso torna all'accesso */ }
      location.assign("/area-riservata/");
    });
  }
})();
