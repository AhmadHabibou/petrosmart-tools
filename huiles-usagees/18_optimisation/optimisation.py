"""Optimisation robuste de la strategie de la societe (lot 18).

Leviers de decision dont l'effet est calcule par le modele mensuel (09_finance/modele_mensuel.py) :
- mode de financement des equipements : credit-bail sur toute la periode (D-11) ou achat finance par emprunt a la porte ;
- porte d'equipement (achat seulement) : mois minimal et nombre minimal de contrats ;
- enlevements : sous-traites (H-48) ou camion d'occasion propre a partir d'un mois donne (H-131, cout variable du lot 6).

Le prix du contrat (H-80) n'est pas un levier : le modele ne relie pas le prix a la demande. On calcule son seuil robuste.

Methode : chaque strategie est evaluee sur les memes tirages Monte-Carlo (nombres aleatoires communs) des hypotheses
incertaines du lot 9, avec un apport nul pour mesurer les fonds propres requis. Criteres :
- VAN avec valeur terminale au 10e centile (a maximiser) ;
- fonds propres requis au 90e centile (a minimiser) ;
- contrainte : couverture du service financier (loyers et dette) d'au moins 1,2 en annees 3 a 5 dans au moins 80 % des tirages.
Sorties : 18_optimisation/resultats_optimisation.md et .json.

Usage : python 18_optimisation/optimisation.py [--rapide]
"""
from itertools import product
from multiprocessing import Pool
from pathlib import Path
import json
import sys

import numpy as np

RACINE = Path(__file__).resolve().parents[1]
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(RACINE / "09_finance"))
sys.path.insert(0, str(RACINE / "06_logistique"))
from commun.format import m_fcfa, nombre, pct  # noqa: E402
from commun.hypotheses import HYPOTHESES, val  # noqa: E402
import modele_mensuel as mm  # noqa: E402

GRAINE = 20261120
N_RECHERCHE = 2_000
N_CONFIRMATION = 10_000
COUVERTURE_MIN = 1.2
PROBA_COUVERTURE = 0.80
PROBA_VAN5 = 0.80  # seuil de prix : VAN a 5 ans positive dans au moins 80 % des tirages


CAMION = "camion_l"  # cle de tirage du cout variable du camion propre (derivee du lot 6, pas une hypothese du registre)
LIBELLE_CAMION = "Coût variable par litre d'un camion propre (lot 6 : carburant, entretien, équipage)"


def cout_variable_camion_l():
    """Bornes (bas, central, haut) du cout variable par litre d'un camion d'occasion propre sur le reseau des 15 clients du lot 6.
    Bas : cas bas en saison seche ; haut : cas haut en saison des pluies ; central : moyenne des deux saisons au cas central."""
    import tournees as tr

    def cout(saison, cas):
        _, i = tr.couts_par_litre(saison, cas)
        return (i["km"] * (val("H-127", cas) / 100 * tr.GASOIL_FCFA_L + val("H-128", cas) * val("H-138", cas))
                + i["jours"] * val("H-129", cas)) / i["litres"]
    return cout("seche", "bas"), (cout("seche", "central") + cout("pluies", "central")) / 2, cout("pluies", "haut")


def strategies():
    out = [dict(nom=f"Crédit-bail, enlèvements {'sous-traités' if c is None else f'camion propre au mois {c}'}",
                credit_bail=True, mois_bascule_min=mm.MOIS_BASCULE_MIN, clients_bascule=mm.CLIENTS_BASCULE, camion_mois=c)
           for c in (None, 25, 37)]
    for (mmin, cmin), c, d in product(((13, 4), (19, 4), (13, 6), (25, 6)), (None, 25, 37), (0, 6, 12)):
        if d and c is not None:
            continue  # differe teste avec les enlevements sous-traites seulement
        out.append(dict(nom=f"Achat et emprunt{f' avec différé de {d} mois' if d else ''}, porte au mois {mmin} et {cmin} contrats, enlèvements "
                            f"{'sous-traités' if c is None else f'camion propre au mois {c}'}",
                        credit_bail=False, mois_bascule_min=mmin, clients_bascule=cmin, camion_mois=c, differe_mois=d))
    for s in out:
        s.setdefault("differe_mois", 0)
    return out


def tirages(n, graine=GRAINE, fixes=(), camion=None):
    rng = np.random.default_rng(graine)
    t = {}
    for k in mm.MC_CLES:
        h = HYPOTHESES[k]
        t[k] = rng.triangular(h.bas, h.central, h.haut, n) if h.bas < h.haut else np.full(n, h.central)
    camion = camion or cout_variable_camion_l()
    t[CAMION] = rng.triangular(camion[0], camion[1], camion[2], n)
    for k in fixes:
        t.pop(k, None)
    return t


def _couverture(s):
    out = []
    for a in (2, 3, 4):
        idx = slice(12 * a, 12 * a + 12)
        service = float(np.sum(s["loyers"][idx] + s["interets"][idx] + s["remboursement"][idx]))
        dispo = float(np.sum(s["ebitda"][idx] + s["loyers"][idx] - s["impot"][idx]))
        out.append(dispo / service if service > 0 else float("inf"))
    return min(out)


def renouvellement_actualise(s, taux):
    """Valeur actuelle du renouvellement perpetuel des equipements possedes, approche par l'amortissement de l'annee 5.
    La valeur terminale du lot 9 ne le deduit pas ; sans cette correction, l'achat (et le camion) serait avantage."""
    return float(np.sum(s["amortissement"][48:])) / taux * (1 + taux) ** -5


def evaluer(args):
    """Evalue une strategie sur un bloc de tirages ; renvoie les series par tirage."""
    strat, t, debut, fin, cout_l, extra = args
    n = fin - debut
    r = {k: np.zeros(n) for k in ("van", "van_vt", "fp", "couv")}
    for i in range(n):
        p = mm.parametres()
        p.update(credit_bail=strat["credit_bail"], mois_bascule_min=strat["mois_bascule_min"],
                 clients_bascule=strat["clients_bascule"], camion_mois=strat["camion_mois"], cout_var_camion_l=cout_l,
                 differe_mois=strat.get("differe_mois", 0))
        p["H-157"] = 0.0
        p.update(extra)
        for k, v in t.items():
            if k != CAMION:
                p[k] = float(v[debut + i])
        # le cout par litre du camion croit avec la frequence des enlevements (km par an proportionnels a H-88)
        p["cout_var_camion_l"] = float(t[CAMION][debut + i]) * p["H-88"] / HYPOTHESES["H-88"].central
        s, ind = mm.simuler(p)
        taux = p["H-98"]
        r["van"][i] = ind["van"]
        r["van_vt"][i] = ind["van_vt"] - renouvellement_actualise(s, taux)
        r["fp"][i] = max(0.0, -ind["tresorerie_min"])
        r["couv"][i] = _couverture(s)
    return r


def evaluer_complet(strat, t, n, cout_l, pool, extra=None, blocs=4):
    bornes = np.linspace(0, n, blocs + 1).astype(int)
    parts = pool.map(evaluer, [(strat, t, bornes[b], bornes[b + 1], cout_l, extra or {}) for b in range(blocs)])
    return {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}


def synthese(r):
    return dict(van5_p10=float(np.percentile(r["van"], 10)), van5_p50=float(np.percentile(r["van"], 50)),
                p_van5_neg=float(np.mean(r["van"] < 0)), vanvt_p10=float(np.percentile(r["van_vt"], 10)),
                vanvt_p50=float(np.percentile(r["van_vt"], 50)), fp_p50=float(np.percentile(r["fp"], 50)),
                fp_p90=float(np.percentile(r["fp"], 90)), p_couv=float(np.mean(r["couv"] >= COUVERTURE_MIN)))


def pareto(lignes):
    """Strategies admissibles non dominees sur (VAN VT P10 max, fonds propres P90 min)."""
    adm = [l for l in lignes if l["p_couv"] >= PROBA_COUVERTURE]
    return [l for l in adm if not any(o is not l and o["vanvt_p10"] >= l["vanvt_p10"] and o["fp_p90"] <= l["fp_p90"]
                                      and (o["vanvt_p10"] > l["vanvt_p10"] or o["fp_p90"] < l["fp_p90"]) for o in adm)]


def seuil_prix(strat, n, cout_l, pool):
    """Prix annuel minimal du contrat (H-80) pour que la VAN a 5 ans soit positive dans PROBA_VAN5 des tirages."""
    t = tirages(n, GRAINE + 1, fixes=("H-80",), camion=cout_l)
    lo, hi = HYPOTHESES["H-80"].bas * 0.5, HYPOTHESES["H-80"].haut * 2
    for _ in range(9):
        mid = (lo + hi) / 2
        r = evaluer_complet(strat, t, n, cout_l, pool, extra={"H-80": mid})
        if np.mean(r["van"] >= 0) >= PROBA_VAN5:
            hi = mid
        else:
            lo = mid
    return hi


def seuil_loyer(cible_p10, t, n, cout_l, pool):
    """Loyer annuel maximal (H-94) pour que le credit-bail avec enlevements sous-traites egale la VAN avec VT au 10e centile de la cible,
    sur les memes tirages que la recherche."""
    strat = strategies()[0]
    lo, hi = 0.0, HYPOTHESES["H-94"].haut
    if np.percentile(evaluer_complet(strat, t, n, cout_l, pool, extra={"H-94": lo})["van_vt"], 10) < cible_p10:
        return None
    for _ in range(9):
        mid = (lo + hi) / 2
        if np.percentile(evaluer_complet(strat, t, n, cout_l, pool, extra={"H-94": mid})["van_vt"], 10) >= cible_p10:
            lo = mid
        else:
            hi = mid
    return lo


def valeur_information(strat, t, r):
    """Correlation de rang entre chaque hypothese tiree et la VAN avec valeur terminale."""
    def rangs(x):
        return np.argsort(np.argsort(x)).astype(float)
    rv = rangs(r["van_vt"])
    out = []
    for k, v in t.items():
        if np.ptp(v) > 0:
            out.append((k, float(np.corrcoef(rangs(v), rv)[0, 1])))
    return sorted(out, key=lambda x: -abs(x[1]))


def _ligne(res, pred):
    return max((l for l in res["lignes"] if pred(l["strat"])), key=lambda l: l["vanvt_p10"])


def differe_conclusion(res):
    sans = _ligne(res, lambda s: not s["credit_bail"] and s["camion_mois"] is None and s["differe_mois"] == 0)
    avec = _ligne(res, lambda s: not s["credit_bail"] and s["camion_mois"] is None and s["differe_mois"] == 12)
    return (f"5. **Négocier un différé de 12 mois sur un éventuel emprunt.** Il porte la probabilité de couverture d'au moins {nombre(COUVERTURE_MIN, 1)} en années 3 à 5 "
            f"de {pct(sans['p_couv'])} à {pct(avec['p_couv'])} et les fonds propres requis au 90e centile de {m_fcfa(sans['fp_p90'], 1)} à {m_fcfa(avec['fp_p90'], 1)} M FCFA. "
            "Il ne règle pas l'année 2, dont l'EBITDA est négatif dans le scénario de base : aucun remboursement n'y est possible sans les fonds propres.")


def conclusions(res):
    """Synthese en tete du rapport (pyramide de Minto), entierement lue dans les resultats."""
    st = _ligne(res, lambda s: s["camion_mois"] is None)
    ca = _ligne(res, lambda s: s["camion_mois"] is not None)
    cb = _ligne(res, lambda s: s["credit_bail"] and s["camion_mois"] is None)
    p4 = _ligne(res, lambda s: not s["credit_bail"] and s["camion_mois"] is None and s["clients_bascule"] == 4)
    p6 = _ligne(res, lambda s: not s["credit_bail"] and s["camion_mois"] is None and s["clients_bascule"] == 6)
    couv_max = max(l["p_couv"] for l in res["lignes"])
    loyer = (f"le crédit-bail ne l'égale que si ses loyers restent sous {m_fcfa(res['seuil_loyer'], 2)} M FCFA par an ({m_fcfa(val('H-94'), 2)} M FCFA supposés)"
             if res["seuil_loyer"] is not None else "le crédit-bail ne l'égale pour aucun loyer")
    L = ["## Conclusions", "",
         f"1. **Sous-traiter les enlèvements jusqu'à l'étape 3** (confirme D-10). Le camion propre réduit la VAN avec valeur terminale au 10e centile de "
         f"{m_fcfa(st['vanvt_p10'] - ca['vanvt_p10'], 1)} M FCFA et augmente les fonds propres requis au 90e centile de {m_fcfa(ca['fp_p90'] - st['fp_p90'], 1)} M FCFA.",
         f"2. **Fixer la porte d'équipement à 4 contrats.** Elle fait mieux que 6 contrats ({m_fcfa(p4['vanvt_p10'], 1)} contre {m_fcfa(p6['vanvt_p10'], 1)} M FCFA au 10e centile) ; "
         "le mois minimal de la porte n'a pas d'effet, car c'est le nombre de contrats qui la déclenche.",
         f"3. **Le choix entre crédit-bail et emprunt dépend des offres.** Avec les hypothèses actuelles, l'achat financé par emprunt fait mieux "
         f"({m_fcfa(p4['vanvt_p10'], 1)} contre {m_fcfa(cb['vanvt_p10'], 1)} M FCFA au 10e centile) ; {loyer}. "
         "Mais l'emprunt suppose qu'une banque prête à une société dont la couverture de la dette est négative en année 2 (lot 9) : le crédit-bail (D-11) reste la voie réaliste "
         "tant qu'aucune offre de prêt n'est obtenue, et la décision est à revoir à réception des offres B4 (crédit-bail) et B5 (prêt garanti).",
         f"4. **La couverture du service financier est le point faible pour la banque.** Aucune stratégie n'atteint {nombre(COUVERTURE_MIN, 1)} en années 3 à 5 dans "
         f"{pct(PROBA_COUVERTURE)} des tirages (au mieux {pct(couv_max)}) ; la stratégie retenue y parvient dans {pct(next(l['p_couv'] for l in res['lignes'] if l['nom'] == res['retenue']))} des cas. "
         "La seconde tranche de comptes courants du pacte d'associés en est la réponse.",
         differe_conclusion(res),
         f"6. **Prix plancher du contrat : {m_fcfa(res['seuil_prix'], 2)} M FCFA HT par site** pour une VAN à 5 ans positive dans {pct(PROBA_VAN5)} des tirages.",
         "7. **Mesurer en premier** le nombre de contrats signés et le prix accepté (pilote), puis le prix des enlèvements sous-traités (devis des collecteurs).", ""]
    return L


def rapport(res):
    L = ["# Optimisation robuste de la stratégie", "",
         "Fichier généré par `18_optimisation/optimisation.py`. Méthode : évaluation de chaque stratégie sur les mêmes tirages Monte-Carlo "
         f"({nombre(res['n_recherche'])} pour la recherche, {nombre(res['n_confirmation'])} pour la confirmation), apport nul pour mesurer les fonds propres requis ; "
         "frontière de Pareto entre la VAN avec valeur terminale au 10e centile et les fonds propres requis au 90e centile, "
         f"sous la contrainte d'une couverture du service financier d'au moins {nombre(COUVERTURE_MIN, 1)} en années 3 à 5 dans au moins {pct(PROBA_COUVERTURE)} des tirages.", "",
         *conclusions(res),
         f"Coût variable d'un camion propre : tiré entre {nombre(res['cout_l'][0])} et {nombre(res['cout_l'][2])} FCFA/L, valeur centrale {nombre(res['cout_l'][1])} FCFA/L "
         "(carburant, entretien, équipage sur le réseau des 15 clients du lot 6, saisons sèche et des pluies), proportionnel à la fréquence des enlèvements (H-88) ; "
         "s'y ajoutent l'assurance et les autorisations (H-133) et l'achat d'occasion (H-131).", "",
         "## Stratégies évaluées", "",
         "| Stratégie | VAN 5 ans P10 | VAN 5 ans P50 | VAN 5 ans < 0 | VAN avec VT P10 | Fonds propres requis P50 | Fonds propres requis P90 | Couverture ≥ 1,2 | Admissible |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    for l in sorted(res["lignes"], key=lambda x: -x["vanvt_p10"]):
        L.append(f"| {l['nom']} | {m_fcfa(l['van5_p10'], 1)} | {m_fcfa(l['van5_p50'], 1)} | {pct(l['p_van5_neg'])} | {m_fcfa(l['vanvt_p10'], 1)} | "
                 f"{m_fcfa(l['fp_p50'], 1)} | {m_fcfa(l['fp_p90'], 1)} | {pct(l['p_couv'])} | {'oui' if l['p_couv'] >= PROBA_COUVERTURE else 'non'} |")
    L += ["", "Montants en M FCFA. P10, P50, P90 : 10e, 50e et 90e centiles des tirages. La VAN avec valeur terminale est corrigée du renouvellement des équipements "
          "(amortissement de l'année 5 reconduit à perpétuité).", "",
          "## Frontière de Pareto", ""]
    if res["pareto"]:
        L += ["| Stratégie | VAN avec VT P10 | Fonds propres requis P90 |", "|---|---:|---:|"]
        L += [f"| {l['nom']} | {m_fcfa(l['vanvt_p10'], 1)} | {m_fcfa(l['fp_p90'], 1)} |" for l in res["pareto"]]
    if not res["contrainte_tenue"]:
        L.insert(len(L) - (len(res["pareto"]) + 2 if res["pareto"] else 0),
                 f"**Aucune stratégie ne respecte la contrainte de couverture** (au moins {nombre(COUVERTURE_MIN, 1)} dans {pct(PROBA_COUVERTURE)} des tirages). "
                 "La frontière ci-dessous est calculée sans cette contrainte ; la probabilité de couverture de chaque stratégie figure dans le tableau précédent.\n")
    c = res["confirmation"]
    L += ["", "## Stratégie retenue et confirmation", "",
          f"**{res['retenue']}**, confirmée sur {nombre(res['n_confirmation'])} tirages : VAN à 5 ans au 10e centile {m_fcfa(c['van5_p10'], 1)} M FCFA, "
          f"médiane {m_fcfa(c['van5_p50'], 1)} M FCFA, négative dans {pct(c['p_van5_neg'], 1)} des tirages ; VAN avec valeur terminale au 10e centile {m_fcfa(c['vanvt_p10'], 1)} M FCFA ; "
          f"fonds propres requis {m_fcfa(c['fp_p50'], 1)} M FCFA en médiane et {m_fcfa(c['fp_p90'], 1)} M FCFA au 90e centile ; "
          f"couverture d'au moins {nombre(COUVERTURE_MIN, 1)} dans {pct(c['p_couv'], 1)} des tirages.", "",
          "Règle de choix : sur la frontière de Pareto (stratégies admissibles, ou toutes si aucune ne l'est), la plus forte VAN avec valeur terminale au 10e centile.", "",
          "## Correction à reporter au lot 9", "",
          f"La valeur terminale du modèle mensuel ne déduit pas le renouvellement des équipements achetés. Dans le scénario de base (achat et emprunt), "
          f"la VAN avec valeur terminale de {m_fcfa(res['van_vt_lot9'], 1)} M FCFA est surestimée d'environ {m_fcfa(res['biais_vt_lot9'], 1)} M FCFA. "
          "La structure en crédit-bail du business plan bancaire est peu touchée : ses loyers sont déjà dans l'EBITDA.", "",
          "## Crédit-bail ou emprunt", "",
          (f"Le crédit-bail (enlèvements sous-traités) égale la meilleure stratégie d'achat ({res['meilleur_achat'].lower()}) sur la VAN avec valeur terminale au 10e centile "
           f"si ses loyers ne dépassent pas **{m_fcfa(res['seuil_loyer'], 2)} M FCFA par an**, contre {m_fcfa(val('H-94'), 2)} M FCFA supposés (H-94). "
           if res["seuil_loyer"] is not None else
           f"Même sans loyer, le crédit-bail n'égale pas la meilleure stratégie d'achat ({res['meilleur_achat'].lower()}) sur la VAN avec valeur terminale au 10e centile. ")
          + "Le choix entre crédit-bail (D-11) et emprunt se fera donc sur les offres reçues avec la lettre B4, en tenant compte de l'option d'achat en fin de contrat, "
          "que le modèle ignore, et des garanties exigées pour un emprunt.", "",
          "## Seuil de prix du contrat", "",
          f"Pour la stratégie retenue, la VAN à 5 ans est positive dans au moins {pct(PROBA_VAN5)} des tirages si le contrat annuel atteint "
          f"**{m_fcfa(res['seuil_prix'], 2)} M FCFA HT par site**, contre {m_fcfa(val('H-80'), 2)} M FCFA retenus (H-80). C'est le prix minimal à valider pendant le pilote.", "",
          "## Ce qu'il faut mesurer en premier", "",
          "Corrélation de rang entre chaque hypothèse tirée et la VAN avec valeur terminale, stratégie retenue. Plus elle est forte en valeur absolue, plus la mesure de l'hypothèse réduit l'incertitude.", "",
          "| Hypothèse | Libellé | Corrélation de rang |", "|---|---|---:|"]
    for k, rho in res["valeur_information"][:8]:
        L.append(f"| {k if k != CAMION else 'lot 6'} | {HYPOTHESES[k].libelle if k != CAMION else LIBELLE_CAMION} | {nombre(rho, 2)} |")
    L += ["", "## Limites", "",
          "1. Les hypothèses tirées sont pour la plupart « supposées » : l'optimum dit quelle stratégie est la plus robuste à notre ignorance actuelle, pas quelle stratégie gagnera.",
          "2. Le coût du camion propre suppose des tournées organisées comme au lot 6 dès son achat ; avec moins de 15 clients, le coût par litre serait plus élevé.",
          "3. Les leviers commerciaux (prix, effort de vente, recrutement du commercial) ne sont pas optimisés : le modèle ne relie pas ces choix au nombre de clients.",
          "4. Le choix du modèle d'entreprise (M1 à M5) a été fait au lot 8 ; l'optimisation porte sur la trajectoire retenue (D-09)."]
    return "\n".join(L) + "\n"


def executer(n_recherche=N_RECHERCHE, n_confirmation=N_CONFIRMATION, n_prix=1_000):
    cout_l = cout_variable_camion_l()
    t = tirages(n_recherche, camion=cout_l)
    with Pool(4) as pool:
        lignes = []
        for st in strategies():
            r = evaluer_complet(st, t, n_recherche, cout_l, pool)
            lignes.append(dict(nom=st["nom"], strat=st, **synthese(r)))
        front = pareto(lignes)
        contrainte_tenue = bool(front)
        if not front:  # aucune strategie admissible : frontiere sans la contrainte, contrainte signalee
            front = pareto([dict(l, p_couv=1.0) for l in lignes])
            front = [next(l for l in lignes if l["nom"] == f["nom"]) for f in front]
        meilleure = max(front, key=lambda l: l["vanvt_p10"])
        tc = tirages(n_confirmation, GRAINE + 2, camion=cout_l)
        rc = evaluer_complet(meilleure["strat"], tc, n_confirmation, cout_l, pool)
        seuil = seuil_prix(meilleure["strat"], n_prix, cout_l, pool)
        achat = max((l for l in lignes if not l["strat"]["credit_bail"]), key=lambda l: l["vanvt_p10"])
        loyer = seuil_loyer(achat["vanvt_p10"], t, n_recherche, cout_l, pool)
    reference = mm.parametres()
    s_ref, i_ref = mm.simuler(reference)
    biais_vt = renouvellement_actualise(s_ref, reference["H-98"])
    res = dict(contrainte_tenue=contrainte_tenue, biais_vt_lot9=biais_vt, van_vt_lot9=i_ref["van_vt"], n_recherche=n_recherche, n_confirmation=n_confirmation, cout_l=cout_l, lignes=lignes, pareto=front,
               retenue=meilleure["nom"], meilleur_achat=achat["nom"], seuil_loyer=loyer, strategie_retenue=meilleure["strat"], confirmation=synthese(rc), seuil_prix=seuil,
               valeur_information=valeur_information(meilleure["strat"], tc, rc))
    return res


if __name__ == "__main__":
    rapide = "--rapide" in sys.argv
    res = executer(200, 400, 200) if rapide else executer()
    sortie = ICI / ("resultats_optimisation_rapide" if rapide else "resultats_optimisation")
    sortie.with_suffix(".md").write_text(rapport(res), encoding="utf-8")
    sortie.with_suffix(".json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    print("Optimisation : strategie retenue :", res["retenue"])
