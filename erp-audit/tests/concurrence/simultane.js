// Moteur de sessions simultanees : N utilisateurs, chacun dans son contexte navigateur isole,
// declenchent la meme action au meme instant (barriere), puis on compare les resultats.
// Usage : node simultane.js <scenario.js>   (le scenario exporte connexion, preparer, agir, verifier)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function main() {
  const scenario = require(path.resolve(process.argv[2]));
  const base = process.env.ERP_URL;
  if (!base) throw new Error('ERP_URL non defini');
  const sortie = path.resolve(__dirname, '../../resultats', path.basename(process.argv[2], '.js'));
  fs.mkdirSync(sortie, { recursive: true });

  const navigateur = await chromium.launch();
  const sessions = await Promise.all(scenario.profils.map(async (profil, i) => {
    const ctx = await navigateur.newContext();
    const page = await ctx.newPage();
    await scenario.connexion(page, base, profil);
    await scenario.preparer(page, base, profil, i);
    return { profil, page, ctx };
  }));

  // Barriere : toutes les sessions sont pretes, on declenche l'action ensemble.
  const t0 = Date.now();
  const resultats = await Promise.allSettled(sessions.map((s, i) => scenario.agir(s.page, base, s.profil, i)));
  const duree = Date.now() - t0;

  for (const [i, s] of sessions.entries()) await s.page.screenshot({ path: path.join(sortie, `session-${i}.png`), fullPage: true });
  const bilan = await scenario.verifier(resultats, sessions, base);
  fs.writeFileSync(path.join(sortie, 'bilan.json'), JSON.stringify({ duree_ms: duree, resultats: resultats.map(r => r.status === 'fulfilled' ? r.value : String(r.reason)), bilan }, null, 2));
  console.log(JSON.stringify(bilan, null, 2));
  await navigateur.close();
}
main().catch(e => { console.error(e); process.exit(1); });
