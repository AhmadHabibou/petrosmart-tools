// Test de bout en bout : saisie hors ligne puis synchronisation (Chromium via Playwright).
// Usage : node e2e_navigateur.js http://127.0.0.1:PORT
const { chromium } = require("playwright");
(async () => {
  const url = process.argv[2];
  const nav = await chromium.launch();
  const ctx = await nav.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  await page.goto(url);
  await page.click("text=Réglages");
  await page.fill("input[name=jeton]", "secret");
  await page.click("text=Enregistrer le jeton");
  await page.waitForTimeout(500);
  await ctx.setOffline(true);
  await page.evaluate(() => window.dispatchEvent(new Event("offline")));
  await page.click("text=Clients et sites");
  await page.fill("#f-client input[name=nom]", "Client saisi en forêt");
  await page.click("text=Enregistrer le client");
  await page.waitForTimeout(300);
  const attente = await page.innerText("#attente");
  const visible = (await page.innerText("#contenu")).includes("Client saisi en forêt");
  await ctx.setOffline(false);
  await page.evaluate(() => window.dispatchEvent(new Event("online")));
  await page.waitForFunction(() => document.getElementById("attente").textContent === "0", null, { timeout: 5000 });
  const largeur = await page.evaluate(() => document.documentElement.scrollWidth);
  await page.click("text=Tableau de bord");
  await page.screenshot({ path: process.argv[3] || "capture.png" });
  await nav.close();
  console.log(JSON.stringify({ attente, visible, largeur }));
})().catch((e) => { console.error(e); process.exit(1); });
