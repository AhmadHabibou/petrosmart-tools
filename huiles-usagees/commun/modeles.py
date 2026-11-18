"""Comparateur annuel des cinq modeles d'entreprise (lot 8), reutilise par le modele mensuel du lot 9.

Flux annuels hors financement (non endettes), annees 0 a 5, sans valeur terminale.
Scenarios : 'pessimiste', 'base', 'optimiste'. Chaque hypothese prend sa borne
defavorable en pessimiste et favorable en optimiste, selon SENS.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from commun.hypotheses import val  # noqa: E402

ANNEES = range(0, 6)

# +1 : une valeur haute est favorable a la societe ; -1 : defavorable
SENS = {
    "H-01": +1, "H-03": -1, "H-04": +1, "H-05": +1, "H-48": -1,
    "H-80": +1, "H-81": +1, "H-82": +1, "H-83": +1, "H-84": +1, "H-85": -1, "H-86": +1,
    "H-87": -1, "H-88": -1, "H-89": -1, "H-90": -1, "H-91": -1, "H-92": -1, "H-93": -1,
    "H-94": -1, "H-95": -1, "H-96": +1, "H-97": +1, "H-98": -1, "H-99": -1,
}

# Investissement du premier business plan, en FCFA, par annee [S-29]
CAPEX_BP = {0: 72e6, 2: 69e6, 3: 25e6}
MINIMUM_PERCEPTION = 0.022  # fraction du CA [S-29], a verifier (Q-31)

MODELES = {
    "M1": "Prestataire de conformité et de collecte pur (enlèvement sous-traité, huiles remises à un valorisateur)",
    "M2": "Collecte avec prétraitement léger (centre de transit, décantation, déshydratation), vente à un valorisateur",
    "M3": "Unité de traitement propre et vente de combustible (premier business plan)",
    "M4": "Partenariat avec un collecteur ou valorisateur existant (la société vend et gère, le partenaire collecte)",
    "M5": "Faible capital : M1 avec équipements en location ou crédit-bail et transport sous-traité",
}


def h(hid, scenario):
    if scenario == "base":
        return val(hid, "central")
    favorable = scenario == "optimiste"
    haut = (SENS.get(hid, +1) > 0) == favorable
    return val(hid, "haut" if haut else "bas")


def clients(annee, sc):
    """Progression lineaire de 2 clients en annee 1 a H-97 en annee 5."""
    if annee == 0:
        return 0
    fin = h("H-97", sc)
    return 2 + (fin - 2) * (annee - 1) / 4


def volume_urbain(annee, sc):
    if annee < 2:
        return 0
    return h("H-96", sc) * (annee - 1) / 4


def flux(modele, sc="base"):
    """Renvoie une liste de dictionnaires annuels."""
    lignes = []
    for a in ANNEES:
        n = clients(a, sc)
        vf = n * h("H-01", sc)
        vu = volume_urbain(a, sc) if modele in ("M2", "M3") else 0
        ca = {}
        ch = {}
        # service de conformite
        if modele == "M4":
            ca["commission conformité"] = n * h("H-80", sc) * h("H-86", sc)
        else:
            ca["contrats de conformité"] = n * h("H-80", sc)
            ch["enlèvements forestiers sous-traités"] = n * h("H-88", sc) * h("H-48", sc)
        # purification du gasoil (tous modeles)
        nb_int = n * h("H-82", sc)
        ca["purification du gasoil"] = nb_int * h("H-81", sc)
        ch["consommables de purification"] = nb_int * h("H-87", sc)
        # devenir des huiles
        if modele in ("M1", "M5"):
            ca["valeur nette des huiles remises"] = vf * h("H-83", sc)
        elif modele == "M2":
            ca["huiles prétraitées remises"] = (vf + vu) * (h("H-83", sc) + (h("H-84", sc) if a >= 2 else 0))
            ch["achat des huiles urbaines"] = vu * h("H-03", sc)
            ch["collecte urbaine"] = vu * h("H-85", sc)
        elif modele == "M3":
            prod = (vf + vu) * h("H-05", sc) if a >= 2 else 0
            ca["vente de combustible"] = prod * h("H-04", sc)
            ca["valeur nette des huiles remises"] = (vf + vu) * h("H-83", sc) if a < 2 else 0
            ch["achat des huiles urbaines"] = vu * h("H-03", sc)
            ch["collecte urbaine"] = vu * h("H-85", sc)
        # charges fixes
        if a >= 1:
            ch["charges fixes de structure"] = h("H-89", sc)
            if modele == "M5":
                ch["loyers de crédit-bail et location"] = h("H-94", sc)
            if modele == "M2" and a >= 2:
                ch["charges fixes du centre de transit"] = h("H-90", sc)
            if modele == "M3" and a >= 2:
                ch["charges fixes de l'unité"] = h("H-91", sc)
        # investissements
        capex = 0.0
        if a == 0:
            capex = {"M1": h("H-92", sc), "M2": h("H-92", sc), "M3": h("H-92", sc),
                     "M4": h("H-93", sc), "M5": h("H-93", sc)}[modele]
        if modele == "M2" and a == 1:
            capex += h("H-95", sc)
        if modele == "M3":
            capex += CAPEX_BP.get(a, 0)
        lignes.append(dict(annee=a, clients=n, volume_foret=vf, volume_urbain=vu,
                           ca=ca, charges=ch, capex=capex))
    # amortissements lineaires sur 5 ans, impot, flux
    for i, l in enumerate(lignes):
        amort = sum(lignes[j]["capex"] / 5 for j in range(0, i) if i - j <= 5)
        ca_tot = sum(l["ca"].values())
        ebitda = ca_tot - sum(l["charges"].values())
        resultat_avant_impot = ebitda - amort
        impot = max(h("H-99", sc) * max(resultat_avant_impot, 0), MINIMUM_PERCEPTION * ca_tot) if l["annee"] >= 1 else 0
        l.update(ca_total=ca_tot, ebitda=ebitda, amortissement=amort, impot=impot,
                 resultat_net=resultat_avant_impot - impot, flux=ebitda - impot - l["capex"])
    return lignes


def indicateurs(modele, sc="base"):
    lignes = flux(modele, sc)
    t = h("H-98", sc)
    van = sum(l["flux"] / (1 + t) ** l["annee"] for l in lignes)
    cumul, mini = 0.0, 0.0
    for l in lignes:
        cumul += l["flux"]
        mini = min(mini, cumul)
    l5 = lignes[5]
    vt = (l5["ebitda"] - l5["impot"]) / t / (1 + t) ** 5  # rente perpetuelle sans croissance, sans reinvestissement
    return dict(van=van, van_vt=van + vt, besoin_financement=-mini, capex_total=sum(l["capex"] for l in lignes),
                ca_an5=lignes[5]["ca_total"], rn_an5=lignes[5]["resultat_net"],
                ebitda_an5=lignes[5]["ebitda"], lignes=lignes)


def marge_par_client(modele, sc="base"):
    """Contribution annuelle d'un client forestier en regime de croisiere (FCFA)."""
    pur = h("H-82", sc) * (h("H-81", sc) - h("H-87", sc))
    if modele == "M4":
        return h("H-80", sc) * h("H-86", sc) + pur
    huiles = h("H-01", sc) * h("H-83", sc)
    return h("H-80", sc) - h("H-88", sc) * h("H-48", sc) + pur + huiles


def point_mort_clients(modele, sc="base"):
    fixes = h("H-89", sc) + (h("H-94", sc) if modele == "M5" else 0)
    m = marge_par_client(modele, sc)
    return fixes / m if m > 0 else float("inf")
