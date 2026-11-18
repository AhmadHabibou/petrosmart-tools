// Interface mobile de tracabilite. Les saisies passent par une file d'attente locale
// (localStorage), envoyee au serveur par /api/sync des que le reseau le permet.
"use strict";

const LS = {
  lire(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
  ecrire(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* stockage indisponible */ } },
};
const uuid = () => (crypto.randomUUID ? crypto.randomUUID() : "x" + Date.now() + Math.random().toString(16).slice(2));
const jeton = () => LS.lire("jeton", "");
const file = () => LS.lire("file", []);
const cache = () => LS.lire("cache", {});
let vue = "tdb";

async function api(chemin, options = {}) {
  const r = await fetch(chemin, { ...options, headers: { "Content-Type": "application/json", "X-Token": jeton(), ...(options.headers || {}) } });
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).erreur || r.statusText);
  return r.json();
}

function mettreEnFile(type, table, data) {
  const f = file();
  f.push({ op_id: uuid(), type, table, data });
  LS.ecrire("file", f);
  // reflet local immediat
  if (type === "creer") { const c = cache(); (c[table] = c[table] || []).push({ ...data, _attente: true }); LS.ecrire("cache", c); }
  majPied();
  afficher();
  synchroniser();
}

async function synchroniser() {
  const f = file();
  if (!navigator.onLine) { majEtat(); majPied(); return; }
  try {
    if (f.length) {
      const r = await api("/api/sync", { method: "POST", body: JSON.stringify({ operations: f }) });
      const erreurs = r.resultats.filter((x) => x.statut === "erreur");
      LS.ecrire("file", []);
      if (erreurs.length) alert("Saisies refusées par le serveur :\n" + erreurs.map((e) => e.resultat.erreur).join("\n"));
    }
    const c = {};
    for (const t of ["clients", "sites", "futs", "enlevements", "lots", "ventes", "analyses"]) c[t] = await api("/api/" + t);
    c.stock = await api("/api/stock");
    c.tdb = await api("/api/tableau_de_bord");
    LS.ecrire("cache", c);
  } catch (e) { console.warn(e); }
  majEtat(); majPied(); afficher();
}

function majEtat() { document.getElementById("etat").textContent = navigator.onLine ? "en ligne" : "hors ligne"; }
function majPied() { document.getElementById("attente").textContent = file().length; }

const LIBELLES = { planifie: "planifié", realise: "réalisé", annule: "annulé", chez_client: "chez le client", enleve: "enlevé",
  en_attente: "en quarantaine", accepte_provisoire: "accepté (provisoire)", accepte: "accepté", refuse: "refusé", traite: "traité" };
const lib = (s) => LIBELLES[s] || s;
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const nom = (t, id, champ = "nom") => (cache()[t] || []).find((x) => x.id === id)?.[champ] || "";
const tableau = (entetes, lignes) => `<table><tr>${entetes.map((h) => `<th>${h}</th>`).join("")}</tr>${lignes.join("")}</table>`;
const opt = (liste, champ = "nom") => liste.map((x) => `<option value="${x.id}">${esc(x[champ])}</option>`).join("");

function formulaire(id, champs, bouton) {
  return `<form id="${id}">${champs.join("")}<button class="principal">${bouton}</button></form>`;
}

const VUES = {
  tdb(c) {
    const t = c.tdb || {};
    const cartes = [["Clients", t.clients], ["Sites", t.sites], ["Fûts chez les clients", t.futs_chez_clients], ["Enlèvements planifiés", t.enlevements_planifies],
      ["Enlèvements réalisés", t.enlevements_realises], ["Volume enlevé (L)", Math.round(t.volume_enleve_l || 0)], ["Stock (L)", t.stock_total_l],
      ["Lots refusés", t.taux_lots_refuses == null ? "s.o." : Math.round(t.taux_lots_refuses * 100) + " %"]];
    const fictif = (c.clients || []).some((x) => x.fictif) ? `<div class="fictif">Base de démonstration : les données affichées sont fictives.</div>` : "";
    return `<h2>Tableau de bord</h2>${fictif}<div class="cartes">${cartes.map(([l, v]) => `<div class="carte">${l}<b>${v ?? "…"}</b></div>`).join("")}</div>`;
  },
  clients(c) {
    return `<h2>Nouveau client</h2>${formulaire("f-client", [`<input name="nom" placeholder="Raison sociale" required>`,
      `<select name="type"><option value="forestier">forestier ou UTB</option><option value="urbain">garage ou flotte</option><option value="industrie">industrie</option></select>`,
      `<input name="contact" placeholder="Contact">`, `<input name="telephone" placeholder="Téléphone">`], "Enregistrer le client")}
    <h2>Nouveau site</h2>${formulaire("f-site", [`<select name="client_id" required>${opt(c.clients || [])}</select>`, `<input name="nom" placeholder="Nom du site" required>`,
      `<input name="latitude" placeholder="Latitude" inputmode="decimal">`, `<input name="longitude" placeholder="Longitude" inputmode="decimal">`,
      `<input name="piste_km" placeholder="Distance de piste (km)" inputmode="decimal">`], "Enregistrer le site")}
    <h2>Clients</h2>${tableau(["Client", "Type", "Sites", "Rapport annuel"], (c.clients || []).map((x) => `<tr class="${x._attente ? "attente" : ""}"><td>${esc(x.nom)}${x.fictif ? " (fictif)" : ""}</td><td>${esc(x.type)}</td>
      <td>${(c.sites || []).filter((s) => s.client_id === x.id).map((s) => esc(s.nom)).join(", ")}</td>
      <td>${x._attente ? "" : `<a href="/api/clients/${x.id}/rapport/${new Date().getFullYear()}.pdf?token=${encodeURIComponent(jeton())}" target="_blank">PDF</a>`}</td></tr>`))}`;
  },
  futs(c) {
    return `<h2>Nouveau fût</h2>${formulaire("f-fut", [`<input name="code" placeholder="Code du fût (ex. F-0001)" required>`, `<select name="site_id">${opt(c.sites || [])}</select>`], "Enregistrer le fût")}
    <h2>Fûts</h2>${tableau(["Code", "Site", "Statut", "QR"], (c.futs || []).map((f) => `<tr><td>${esc(f.code)}</td><td>${esc(nom("sites", f.site_id))}</td><td>${esc(lib(f.statut))}</td>
      <td>${f._attente ? "" : `<a href="/api/futs/${f.id}/qr.svg?token=${encodeURIComponent(jeton())}" target="_blank">QR</a>`}</td></tr>`))}`;
  },
  enlevements(c) {
    const planifies = (c.enlevements || []).filter((e) => e.statut === "planifie" && !e._attente);
    return `<h2>Planifier un enlèvement</h2>${formulaire("f-enl", [`<select name="site_id" required>${opt(c.sites || [])}</select>`, `<input name="date_prevue" type="date" required>`,
      `<input name="transporteur" placeholder="Transporteur titulaire">`], "Planifier")}
    <h2>Réaliser un enlèvement</h2>${formulaire("f-real", [`<select name="id" required>${planifies.map((e) => `<option value="${e.id}">${esc(e.date_prevue)} : ${esc(nom("sites", e.site_id))}</option>`).join("")}</select>`,
      `<input name="volume_l" placeholder="Volume enlevé (L)" inputmode="decimal" required>`,
      `<select name="depistage"><option value="negatif">dépistage halogènes négatif</option><option value="positif">dépistage positif (quarantaine)</option></select>`,
      `<input name="date" type="date">`], "Valider l'enlèvement")}
    <h2>Enlèvements</h2>${tableau(["Date", "Site", "Statut", "Volume (L)", "Bordereau"], (c.enlevements || []).map((e) => `<tr class="${e._attente ? "attente" : ""}"><td>${esc(e.date_realisee || e.date_prevue)}</td>
      <td>${esc(nom("sites", e.site_id))}</td><td>${esc(lib(e.statut))}</td><td class="n">${e.volume_l ?? ""}</td>
      <td>${e.bordereau ? `<a href="/api/enlevements/${e.id}/bordereau.pdf?token=${encodeURIComponent(jeton())}" target="_blank">${esc(e.bordereau)}</a>` : ""}</td></tr>`))}`;
  },
  lots(c) {
    return `<h2>Saisir une analyse</h2>${formulaire("f-ana", [`<select name="lot_id" required>${opt(c.lots || [], "numero")}</select>`,
      `<input name="chlore_ppm" placeholder="Chlore total (ppm)" inputmode="decimal">`, `<select name="pcb_detecte"><option value="0">PCB non détectés</option><option value="1">PCB détectés</option></select>`,
      `<input name="eau_pct" placeholder="Eau (% m/m)" inputmode="decimal">`, `<input name="laboratoire" placeholder="Laboratoire">`], "Enregistrer l'analyse")}
    <h2>Stock par lot</h2>${tableau(["Lot", "Statut", "Stock (L)"], (c.stock || []).map((s) => `<tr><td>${esc(s.numero)}</td><td>${esc(lib(s.statut))}</td><td class="n">${Math.round(s.stock_l)}</td></tr>`))}`;
  },
  ventes(c) {
    const lots = (c.lots || []).filter((l) => l.statut === "accepte" || l.statut === "traite");
    return `<h2>Enregistrer une vente</h2><p>Réservé à l'étape 4 (décision D-06).</p>${formulaire("f-vente", [`<input name="date" type="date" required>`, `<input name="acheteur" placeholder="Acheteur" required>`,
      `<select name="lot_id">${opt(lots, "numero")}</select>`, `<input name="volume_l" placeholder="Volume (L)" inputmode="decimal" required>`,
      `<input name="prix_l" placeholder="Prix (FCFA/L)" inputmode="decimal" required>`], "Enregistrer la vente")}
    <h2>Ventes</h2>${tableau(["Date", "Acheteur", "Volume (L)", "Prix (FCFA/L)"], (c.ventes || []).map((v) => `<tr><td>${esc(v.date)}</td><td>${esc(v.acheteur)}</td><td class="n">${v.volume_l}</td><td class="n">${v.prix_l}</td></tr>`))}`;
  },
  reglages() {
    return `<h2>Réglages</h2>${formulaire("f-jeton", [`<input name="jeton" type="password" placeholder="Jeton d'accès" value="${esc(jeton())}">`], "Enregistrer le jeton")}`;
  },
};

const ACTIONS = {
  "f-client": (d) => mettreEnFile("creer", "clients", { id: uuid(), ...d }),
  "f-site": (d) => mettreEnFile("creer", "sites", { id: uuid(), ...d }),
  "f-fut": (d) => mettreEnFile("creer", "futs", { id: uuid(), ...d }),
  "f-enl": (d) => mettreEnFile("creer", "enlevements", { id: uuid(), ...d }),
  "f-real": (d) => mettreEnFile("realiser", "enlevements", { ...d, volume_l: parseFloat(d.volume_l), date: d.date || undefined }),
  "f-ana": (d) => mettreEnFile("analyse", "analyses", { id: uuid(), ...d, chlore_ppm: d.chlore_ppm ? parseFloat(d.chlore_ppm) : null, pcb_detecte: d.pcb_detecte === "1", eau_pct: d.eau_pct ? parseFloat(d.eau_pct) : null }),
  "f-vente": (d) => mettreEnFile("creer", "ventes", { id: uuid(), ...d, volume_l: parseFloat(d.volume_l), prix_l: parseFloat(d.prix_l) }),
  "f-jeton": (d) => { LS.ecrire("jeton", d.jeton); synchroniser(); },
};

function afficher() {
  document.getElementById("contenu").innerHTML = VUES[vue](cache());
  document.querySelectorAll("#contenu form").forEach((f) => f.addEventListener("submit", (e) => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(f).entries());
    ACTIONS[f.id](d);
    f.reset();
  }));
}

document.querySelectorAll("nav button").forEach((b) => b.addEventListener("click", () => {
  document.querySelectorAll("nav button").forEach((x) => x.classList.remove("actif"));
  b.classList.add("actif");
  vue = b.dataset.vue;
  afficher();
}));
document.getElementById("sync").addEventListener("click", synchroniser);
window.addEventListener("online", synchroniser);
window.addEventListener("offline", majEtat);
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
majEtat(); majPied(); afficher(); synchroniser();
