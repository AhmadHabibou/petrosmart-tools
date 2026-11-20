"""Lot 9 : modele financier mensuel sur 60 mois de la trajectoire retenue (D-09) : M5 puis M1.

Contenu : compte de resultat, tresorerie, bilan simplifie, BFR, amortissements, impot (taux et minimum
de perception), emprunt, VAN, TRI, point mort, DSCR, delai de recuperation ; scenarios ; tornado ;
Monte-Carlo ; guerre des prix. Export .xlsx avec formules visibles dans export_xlsx.py.

Toutes les valeurs viennent de commun/hypotheses.py (H-xx) ; les constantes sourcees portent [S-xx].
"""
from pathlib import Path
import math
import sys

import numpy as np

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from commun.hypotheses import HYPOTHESES  # noqa: E402

MOIS = 60
MINIMUM_PERCEPTION = 0.022  # fraction du CA [S-29] (Q-31)
REPORT_DEFICITAIRE_ANS = 4  # regle de travail, a confirmer (Q-31)
DUREE_AMORT_MOIS = 60
MOIS_BASCULE_MIN = 13       # passage en M1 au plus tot (porte de l'etape 1, lot 8)
CLIENTS_BASCULE = 4         # au moins 4 contrats annuels (porte de l'etape 1, lot 8)

CLES = ["H-01", "H-21", "H-48", "H-80", "H-81", "H-82", "H-83", "H-87", "H-88", "H-92", "H-93", "H-94", "H-96", "H-97",
        "H-98", "H-99", "H-150", "H-151", "H-152", "H-153", "H-154", "H-155", "H-156", "H-157", "H-158", "H-159",
        "H-160", "H-161", "H-162"]

# +1 : valeur haute favorable ; -1 : defavorable (pour les scenarios pessimiste et optimiste)
SENS = {"H-01": 1, "H-21": 1, "H-48": -1, "H-80": 1, "H-81": 1, "H-82": 1, "H-83": 1, "H-87": -1, "H-88": -1,
        "H-92": -1, "H-93": -1, "H-94": -1, "H-96": 1, "H-97": 1, "H-98": -1, "H-99": -1, "H-150": -1, "H-151": -1,
        "H-152": -1, "H-153": -1, "H-154": -1, "H-155": -1, "H-156": 1, "H-157": 1, "H-158": 1, "H-159": -1,
        "H-160": 1, "H-161": 1, "H-162": -1}


def parametres(scenario="base"):
    p = {}
    for k in CLES:
        h = HYPOTHESES[k]
        if scenario == "base":
            p[k] = h.central
        else:
            fav = scenario == "optimiste"
            p[k] = h.haut if (SENS[k] > 0) == fav else h.bas
    p["guerre_prix"] = False
    p["credit_bail"] = False  # True : equipements en credit-bail sur toute la periode (decision D-11), ni achat ni emprunt
    # leviers de decision (optimisation, 18_optimisation) ; valeurs par defaut = trajectoire D-09
    p["mois_bascule_min"] = MOIS_BASCULE_MIN
    p["clients_bascule"] = CLIENTS_BASCULE
    p["camion_mois"] = None        # mois d'achat d'un camion d'occasion propre (None : enlevements sous-traites)
    p["cout_var_camion_l"] = 0.0   # cout variable par litre collecte avec le camion propre (lot 6), FCFA/L
    for k in ("H-01", "H-131", "H-132", "H-133"):
        p.setdefault(k, HYPOTHESES[k].central)
    return p


def clients(m, p):
    if m < 4:
        return 0
    if m <= 12:
        return 2
    return 2 + (p["H-97"] - 2) * (m - 12) / 48


def simuler(p):
    """Renvoie un dictionnaire de series mensuelles (indices 0 a 59 pour les mois 1 a 60) et les indicateurs."""
    s = {k: np.zeros(MOIS) for k in (
        "clients", "ca_contrat", "ca_gasoil", "ca_huiles", "ca_commission_urbaine", "ca_amorcage", "ca",
        "enlevements", "consommables", "salaires", "frais_generaux", "assurances", "loyers", "charges", "ebitda",
        "capex", "amortissement", "interets", "remboursement", "resultat_avant_impot", "impot", "resultat_net",
        "creances", "dettes_fournisseurs", "variation_bfr", "flux_exploitation", "flux_disponible", "emprunt",
        "apport", "tresorerie", "capital_restant", "immobilisations_nettes")}
    bascule = None
    capex_hist = []
    capital_restant = 0.0
    mensualite = 0.0
    for i in range(MOIS):
        m = i + 1
        n = clients(m, p)
        if bascule is None and m >= p.get("mois_bascule_min", MOIS_BASCULE_MIN) and n >= p.get("clients_bascule", CLIENTS_BASCULE):
            bascule = m
        en_m1 = bascule is not None and m >= bascule
        prix = p["H-80"] * ((1 - p["H-162"]) if (p["guerre_prix"] and m >= 25) else 1)
        s["clients"][i] = n
        s["ca_contrat"][i] = n * prix / 12
        nb_int = n * p["H-82"] / 12
        s["ca_gasoil"][i] = nb_int * p["H-81"]
        s["ca_huiles"][i] = n * p["H-01"] / 12 * p["H-83"]
        vol_urb = 0 if m <= 12 else p["H-96"] * min((m - 12) / 48, 1) / 12
        s["ca_commission_urbaine"][i] = 0 if p["guerre_prix"] and m >= 25 else vol_urb * p["H-21"]
        s["ca_amorcage"][i] = p["H-161"] if m <= 24 else 0
        s["ca"][i] = s["ca_contrat"][i] + s["ca_gasoil"][i] + s["ca_huiles"][i] + s["ca_commission_urbaine"][i] + s["ca_amorcage"][i]
        camion = p.get("camion_mois") is not None and m >= p["camion_mois"]
        if camion:
            s["enlevements"][i] = n * p["H-01"] / 12 * p["cout_var_camion_l"] + p["H-133"] / 12
        else:
            s["enlevements"][i] = n * p["H-88"] / 12 * p["H-48"]
        s["consommables"][i] = nb_int * p["H-87"]
        s["salaires"][i] = (p["H-151"] if m >= 4 else 0) + (p["H-150"] + p["H-152"] if m >= 13 else 0)
        s["frais_generaux"][i] = p["H-153"] if m >= 4 else 0
        s["assurances"][i] = p["H-154"] / 12 if m >= 4 else 0
        s["loyers"][i] = (p["H-94"] / 12 if m >= 4 else 0) if (p["credit_bail"] or not en_m1) else 0
        s["charges"][i] = sum(s[k][i] for k in ("enlevements", "consommables", "salaires", "frais_generaux", "assurances", "loyers"))
        s["ebitda"][i] = s["ca"][i] - s["charges"][i]
        # investissements et financement
        cap = 0.0
        if m == 3:
            cap += p["H-93"]
        if bascule == m and not p["credit_bail"]:
            cap += p["H-92"]
            s["emprunt"][i] = p["H-158"]
            capital_restant = p["H-158"]
            r = p["H-159"] / 12
            mensualite = capital_restant * r / (1 - (1 + r) ** -p["H-160"])
        duree = DUREE_AMORT_MOIS
        if p.get("camion_mois") == m:
            cap_camion = p["H-131"]
            duree_camion = int(round(p["H-132"] / 2 * 12))  # occasion : moitie de la duree (H-132)
        else:
            cap_camion, duree_camion = 0.0, 1
        s["capex"][i] = cap + cap_camion
        capex_hist.append((cap, duree))
        capex_hist.append((cap_camion, duree_camion))
        # amortissement lineaire a partir du mois suivant l'investissement
        s["amortissement"][i] = sum(c / d for j, (c, d) in enumerate(capex_hist) if j // 2 < i and i - j // 2 <= d)
        if capital_restant > 0:
            interet = capital_restant * p["H-159"] / 12
            amort_dette = min(mensualite - interet, capital_restant) if bascule is not None and m > bascule else 0
            if bascule == m:
                interet = 0
            s["interets"][i] = interet
            s["remboursement"][i] = amort_dette
            capital_restant -= amort_dette
        s["capital_restant"][i] = capital_restant
        s["resultat_avant_impot"][i] = s["ebitda"][i] - s["amortissement"][i] - s["interets"][i]
        s["apport"][i] = p["H-157"] if m == 1 else 0
    # impot annuel, verse au dernier mois de l'exercice, avec report deficitaire limite
    deficits = []
    for a in range(5):
        idx = slice(12 * a, 12 * a + 12)
        res = s["resultat_avant_impot"][idx].sum()
        ca = s["ca"][idx].sum()
        base = res
        if base > 0:
            for d in deficits:
                if d["reste"] > 0 and a - d["annee"] <= REPORT_DEFICITAIRE_ANS:
                    u = min(d["reste"], base)
                    d["reste"] -= u
                    base -= u
        else:
            deficits.append(dict(annee=a, reste=-base))
        impot = max(p["H-99"] * max(base, 0), MINIMUM_PERCEPTION * ca)
        s["impot"][12 * a + 11] = impot
    s["resultat_net"] = s["resultat_avant_impot"] - s["impot"]
    # BFR, tresorerie
    for i in range(MOIS):
        s["creances"][i] = s["ca"][i] * p["H-155"] / 30
        s["dettes_fournisseurs"][i] = (s["enlevements"][i] + s["consommables"][i]) * p["H-156"] / 30
        bfr = s["creances"][i] - s["dettes_fournisseurs"][i]
        bfr_prec = 0 if i == 0 else s["creances"][i - 1] - s["dettes_fournisseurs"][i - 1]
        s["variation_bfr"][i] = bfr - bfr_prec
        s["flux_exploitation"][i] = s["ebitda"][i] - s["impot"][i] - s["variation_bfr"][i]
        s["flux_disponible"][i] = s["flux_exploitation"][i] - s["capex"][i]
        flux_fin = s["apport"][i] + s["emprunt"][i] - s["interets"][i] - s["remboursement"][i]
        s["tresorerie"][i] = (s["tresorerie"][i - 1] if i else 0) + s["flux_disponible"][i] + flux_fin
        s["immobilisations_nettes"][i] = np.sum(s["capex"][: i + 1]) - np.sum(s["amortissement"][: i + 1])
    return s, indicateurs(s, p, bascule)


def _tri(flux):
    """TRI annuel d'une serie mensuelle, par dichotomie ; None si pas de changement de signe."""
    def van(r):
        return sum(f / (1 + r) ** (t / 12) for t, f in enumerate(flux, 1))
    lo, hi = -0.99, 10.0
    if van(lo) * van(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if van(lo) * van(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def indicateurs(s, p, bascule):
    t = p["H-98"]
    fcf = s["flux_disponible"]
    actu = np.array([(1 + t) ** (-(k + 1) / 12) for k in range(MOIS)])
    van = float(np.sum(fcf * actu))
    flux_an5 = float(np.sum(s["ebitda"][48:] - s["impot"][48:]))
    vt = flux_an5 / t * (1 + t) ** -5
    cumul = np.cumsum(fcf)
    besoin = float(max(0.0, -cumul.min()))
    recup = next((k + 1 for k in range(MOIS) if all(cumul[j] >= 0 for j in range(k, MOIS))), None)
    if recup == 1 and cumul.min() >= 0:
        recup = 1
    pm = next((k + 1 for k in range(MOIS) if all(s["ebitda"][j] > 0 for j in range(k, MOIS))), None)
    dscr = {}
    for a in range(5):
        idx = slice(12 * a, 12 * a + 12)
        service = float(np.sum(s["interets"][idx] + s["remboursement"][idx]))
        if service > 0:
            dscr[a + 1] = float(np.sum(s["ebitda"][idx] - s["impot"][idx])) / service
    tresorerie_min = float(s["tresorerie"].min())
    return dict(van=van, van_vt=van + vt, tri=_tri(list(fcf)), besoin_financement=besoin, recuperation_mois=recup,
                point_mort_mois=pm, dscr=dscr, dscr_min=min(dscr.values()) if dscr else None, mois_bascule=bascule,
                tresorerie_min=tresorerie_min, ca_an5=float(np.sum(s["ca"][48:])), rn_an5=float(np.sum(s["resultat_net"][48:])),
                ebitda_an5=float(np.sum(s["ebitda"][48:])))


def bilan_equilibre(s):
    """Ecart actif moins passif, mois par mois (doit etre nul)."""
    actif = s["immobilisations_nettes"] + s["creances"] + s["tresorerie"]
    passif = (np.cumsum(s["apport"]) + np.cumsum(s["resultat_net"]) + s["capital_restant"] + s["dettes_fournisseurs"])
    return actif - passif


def tornado(cles=("H-80", "H-97", "H-48", "H-81", "H-82", "H-88", "H-150", "H-153", "H-83", "H-87", "H-161", "H-155"), fabrique=None):
    fabrique = fabrique or parametres
    base = simuler(fabrique())[1]["van_vt"]
    lignes = []
    for k in cles:
        vals = []
        for borne in ("bas", "haut"):
            p = fabrique()
            p[k] = getattr(HYPOTHESES[k], borne)
            vals.append(simuler(p)[1]["van_vt"])
        lignes.append((k, vals[0], vals[1], abs(vals[1] - vals[0])))
    lignes.sort(key=lambda x: -x[3])
    return base, lignes


MC_CLES = ["H-01", "H-21", "H-48", "H-80", "H-81", "H-82", "H-83", "H-87", "H-88", "H-96", "H-97", "H-150", "H-151",
           "H-152", "H-153", "H-154", "H-155", "H-161"]


def monte_carlo(n=10_000, graine=20261118, fabrique=None):
    fabrique = fabrique or parametres
    rng = np.random.default_rng(graine)
    tirages = {k: rng.triangular(HYPOTHESES[k].bas, HYPOTHESES[k].central, HYPOTHESES[k].haut, n)
               if HYPOTHESES[k].bas < HYPOTHESES[k].haut else np.full(n, HYPOTHESES[k].central) for k in MC_CLES}
    van = np.zeros(n)
    van5 = np.zeros(n)
    besoin = np.zeros(n)
    for i in range(n):
        p = fabrique()
        for k in MC_CLES:
            p[k] = float(tirages[k][i])
        ind = simuler(p)[1]
        van[i] = ind["van_vt"]
        van5[i] = ind["van"]
        besoin[i] = ind["besoin_financement"]
    return dict(van=van, besoin=besoin, p_van_negative=float(np.mean(van < 0)), p_van5_negative=float(np.mean(van5 < 0)),
                besoin_p90=float(np.percentile(besoin, 90)), van_p10=float(np.percentile(van, 10)),
                van_p50=float(np.percentile(van, 50)), van_p90=float(np.percentile(van, 90)))
