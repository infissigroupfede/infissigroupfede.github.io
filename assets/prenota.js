/* =====================================================================
   PRENOTAZIONE INCONTRI PER I PROFESSIONISTI
   Pagine: /contatti/professionisti/ e /en/contact/professionals/ (testi in base a <html lang>).

   MOCKUP, DA COLLEGARE PIÙ AVANTI:
   - Disponibilità generata nel browser: ogni giorno lavorativo ha 10 incontri da 45 minuti,
     di cui 5 risultano non disponibili. Quali siano dipende solo dalla data (generatore
     pseudo-casuale con la data come seme): tutti i visitatori vedono gli stessi orari e
     cambiano in modo naturale da un giorno all'altro. Sabato, domenica e festivi sono chiusi.
     Quando si collega Google Calendar, getBusy() va sostituita con gli orari occupati veri
     (API free/busy) o la sezione con una pagina di prenotazione di Google Calendar.
   - Invio simulato con DEMO_MODE come il preventivatore; endpoint previsto /api/appuntamento.php,
     che dovrà confermare l'appuntamento per email entro un giorno lavorativo.
   ===================================================================== */
(() => {
  "use strict";

  const DEMO_MODE = true;
  const ENDPOINT = "/api/appuntamento.php";
  const WEEKS = 4;                 // settimane prenotabili, a partire dal primo giorno utile
  const BUSY_PER_DAY = 5;          // orari non disponibili su 10
  const SLOTS = ["09:00", "09:45", "10:30", "11:15", "12:00", "14:00", "14:45", "15:30", "16:15", "17:00"];

  const form = document.getElementById("prenota");
  if (!form) return;

  const EN = document.documentElement.lang === "en";
  const LOCALE = EN ? "en-GB" : "it-IT";
  const T = EN ? {
    week: "Week",
    prev: "Previous week",
    next: "Next week",
    closed: "Closed",
    full: "Full",
    past: "–",
    slotsOf: (d) => `Times on ${d}`,
    unavailable: "unavailable",
    pickDay: "Choose a day to see the times.",
    none: "No times left on this day: try another one.",
    chosen: (d, t, s) => `You chose ${d} at ${t}, ${s}.`,
    when: (d, t, s) => `${d} at ${t}, ${s}`,
    noChoice: "No time chosen yet.",
    errSede: "Choose where you would like to meet.",
    errSlot: "Choose a day and a time.",
    sending: "Sending",
    submit: "Request the meeting",
    error: "We couldn't send your request. Please try again or call us on 051 781570.",
    time: (t) => t,
  } : {
    week: "Settimana",
    prev: "Settimana precedente",
    next: "Settimana successiva",
    closed: "Chiuso",
    full: "Completo",
    past: "–",
    slotsOf: (d) => `Orari di ${d}`,
    unavailable: "non disponibile",
    pickDay: "Scegli un giorno per vedere gli orari.",
    none: "In questo giorno non ci sono più orari: prova un altro giorno.",
    chosen: (d, t, s) => `Hai scelto ${d} alle ${t}, ${s}.`,
    when: (d, t, s) => `${d} alle ${t}, ${s}`,
    noChoice: "Nessun orario scelto.",
    errSede: "Scegli dove preferisci incontrarci.",
    errSlot: "Scegli un giorno e un orario.",
    sending: "Invio in corso",
    submit: "Richiedi l'appuntamento",
    error: "Non siamo riusciti a inviare la richiesta. Riprova o chiamaci allo 051 781570.",
    time: (t) => t.replace(/^0/, "").replace(":", "."),
  };

  const $ = (sel, ctx = form) => ctx.querySelector(sel);
  const fmt = (o) => new Intl.DateTimeFormat(LOCALE, o);
  const fDayLong = fmt({ weekday: "long", day: "numeric", month: "long" });
  const fWd = fmt({ weekday: "short" });
  const fMonth = fmt({ month: "short" });
  const fRangeDay = fmt({ day: "numeric", month: "long" });
  const fYear = fmt({ year: "numeric" });

  /* -------------------------------------------------------------------
     Date e festivi
     ------------------------------------------------------------------- */
  const atMidnight = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
  const key = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const monday = (d) => addDays(d, -((d.getDay() + 6) % 7));

  function easter(y) { // algoritmo anonimo gregoriano
    const a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4;
    const f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30;
    const i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451);
    const month = Math.floor((h + l - 7 * m + 114) / 31), day = ((h + l - 7 * m + 114) % 31) + 1;
    return new Date(y, month - 1, day);
  }
  // Festività nazionali, San Petronio (patrono di Bologna, 4 ottobre) e Lunedì dell'Angelo
  const FIXED = ["01-01", "01-06", "04-25", "05-01", "06-02", "08-15", "10-04", "11-01", "12-08", "12-25", "12-26"];
  const isHoliday = (d) => FIXED.includes(key(d).slice(5)) || key(d) === key(addDays(easter(d.getFullYear()), 1));
  const isWorkday = (d) => d.getDay() >= 1 && d.getDay() <= 5 && !isHoliday(d);

  /* -------------------------------------------------------------------
     Disponibilità (mockup): orari non disponibili stabili per data
     ------------------------------------------------------------------- */
  function seeded(str) {
    let h = 2166136261;
    for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
    return () => { // mulberry32
      h = (h + 0x6D2B79F5) | 0;
      let t = Math.imul(h ^ (h >>> 15), 1 | h);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function getBusy(d) {
    const rnd = seeded(`ig-${key(d)}`);
    const idx = SLOTS.map((_, i) => i);
    for (let i = idx.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [idx[i], idx[j]] = [idx[j], idx[i]]; }
    return new Set(idx.slice(0, BUSY_PER_DAY).map((i) => SLOTS[i]));
  }

  // Primo giorno prenotabile: il giorno lavorativo dopo oggi
  const today = atMidnight(new Date());
  let first = addDays(today, 1);
  while (!isWorkday(first)) first = addDays(first, 1);
  const firstWeek = monday(first);
  const isBookable = (d) => d >= first && isWorkday(d) && d < addDays(firstWeek, WEEKS * 7);

  /* -------------------------------------------------------------------
     Stato e disegno
     ------------------------------------------------------------------- */
  const elWeek = $("[data-book-week]");
  const elPrev = $("[data-book-prev]");
  const elNext = $("[data-book-next]");
  const elDays = $("[data-book-days]");
  const elSlots = $("[data-book-slots]");
  const elLegend = $("[data-book-slots-legend]");
  const elChosen = $("[data-book-chosen]");
  const elErrSede = $("[data-book-err-sede]");
  const elErrSlot = $("[data-book-err-slot]");
  const elAlert = $("[data-book-alert]");
  const btn = $("button[type=submit]");
  const done = document.getElementById("prenota-fatto");

  let week = 0;
  let day = null;

  elPrev.setAttribute("aria-label", T.prev);
  elNext.setAttribute("aria-label", T.next);

  function weekDays() { return [0, 1, 2, 3, 4].map((i) => addDays(firstWeek, week * 7 + i)); }

  function sedeLabel() {
    const r = form.querySelector('input[name="sede"]:checked');
    return r ? r.dataset.label : "";
  }

  function updateChosen() {
    const r = form.querySelector('input[name="orario"]:checked');
    elChosen.textContent = r && day ? T.chosen(fDayLong.format(day), T.time(r.value.slice(11)), sedeLabel() || "…") : T.noChoice;
  }

  function renderSlots() {
    elSlots.replaceChildren();
    if (!day) { elLegend.textContent = T.pickDay; updateChosen(); return; }
    elLegend.textContent = T.slotsOf(fDayLong.format(day));
    const busy = getBusy(day);
    const dk = key(day);
    SLOTS.forEach((t) => {
      const lab = document.createElement("label");
      lab.className = "book__slot";
      const inp = document.createElement("input");
      inp.type = "radio"; inp.name = "orario"; inp.value = `${dk} ${t}`;
      const off = busy.has(t);
      inp.disabled = off;
      const span = document.createElement("span");
      span.textContent = T.time(t);
      if (off) {
        const sr = document.createElement("span");
        sr.className = "sr-only"; sr.textContent = ` ${T.unavailable}`;
        span.append(sr);
      }
      lab.append(inp, span);
      elSlots.append(lab);
    });
    updateChosen();
  }

  function renderWeek() {
    const days = weekDays();
    elWeek.textContent = `${fRangeDay.format(days[0]).replace(/ \D+$/, (m) => (days[0].getMonth() === days[4].getMonth() ? "" : m))} – ${fRangeDay.format(days[4])} ${fYear.format(days[4])}`;
    elPrev.disabled = week === 0;
    elNext.disabled = week === WEEKS - 1;
    if (!day || !days.some((d) => key(d) === key(day))) day = days.find(isBookable) || null;
    elDays.replaceChildren();
    days.forEach((d) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "book__day";
      const ok = isBookable(d);
      b.disabled = !ok;
      b.setAttribute("aria-pressed", String(!!day && key(d) === key(day)));
      const note = !ok ? (d < first ? T.past : T.closed) : fMonth.format(d).replace(".", "");
      b.innerHTML = `<span class="book__day-wd">${fWd.format(d).replace(".", "")}</span><span class="book__day-n">${d.getDate()}</span><span class="book__day-m">${note}</span>`;
      b.setAttribute("aria-label", `${fDayLong.format(d)}${ok ? "" : `, ${d < first ? T.unavailable : T.closed.toLowerCase()}`}`);
      b.addEventListener("click", () => { day = d; elErrSlot.hidden = true; renderWeek(); });
      elDays.append(b);
    });
    renderSlots();
  }

  elPrev.addEventListener("click", () => { if (week > 0) { week--; day = null; renderWeek(); } });
  elNext.addEventListener("click", () => { if (week < WEEKS - 1) { week++; day = null; renderWeek(); } });
  form.addEventListener("change", (e) => {
    if (e.target.name === "sede") elErrSede.hidden = true;
    if (e.target.name === "orario") elErrSlot.hidden = true;
    if (e.target.name === "sede" || e.target.name === "orario") updateChosen();
  });

  /* -------------------------------------------------------------------
     Invio
     ------------------------------------------------------------------- */
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const sede = form.querySelector('input[name="sede"]:checked');
    const slot = form.querySelector('input[name="orario"]:checked');
    elErrSede.hidden = !!sede;
    elErrSlot.hidden = !!slot;
    if (!sede) { form.querySelector('input[name="sede"]').focus(); return; }
    if (!slot) { (form.querySelector('input[name="orario"]:not(:disabled)') || elDays).focus(); return; }
    if (!form.checkValidity()) { form.reportValidity(); return; }

    const fd = new FormData(form);
    btn.disabled = true;
    btn.textContent = T.sending;
    elAlert.textContent = "";
    try {
      if (!fd.get("sito")) { // campo esca vuoto: richiesta di una persona
        if (DEMO_MODE) await new Promise((r) => setTimeout(r, 900));
        else {
          const res = await fetch(ENDPOINT, { method: "POST", body: fd, headers: { Accept: "application/json" } });
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
        }
      }
      done.querySelector("[data-book-done-when]").textContent = T.when(fDayLong.format(day), T.time(slot.value.slice(11)), sede.dataset.label);
      done.querySelector("[data-book-done-email]").textContent = fd.get("email");
      form.hidden = true;
      done.hidden = false;
      done.querySelector("h3").focus();
    } catch (err) {
      elAlert.textContent = T.error;
    } finally {
      btn.disabled = false;
      btn.textContent = T.submit;
    }
  });

  done.querySelector("[data-book-again]").addEventListener("click", () => {
    form.reset();
    week = 0; day = null;
    renderWeek();
    done.hidden = true;
    form.hidden = false;
    form.querySelector('input[name="sede"]').focus();
  });

  renderWeek();
})();
