"""Lot 0 : matrice multicritere des activites d'amorcage.

Methode : filtre eliminatoire (5 criteres), puis notation ponderee sur 3 criteres.
Le revenu net sur 12 mois est calcule a partir des hypotheses H-xx ;
les notes de temps et d'apport au projet sont des jugements d'expert
justifies dans `PISTES` (statut : supposé).

Sortie : 00b_amorcage/matrice_amorcage.md
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from commun.hypotheses import val  # noqa: E402
from commun.format import fcfa, m_fcfa, pct  # noqa: E402

PLAFOND_DEPENSES = 500_000  # FCFA, fixe par le cahier des charges [S-29]
POIDS = {"revenu": 0.35, "temps": 0.20, "apport": 0.45}
POIDS_EGAUX = {"revenu": 1 / 3, "temps": 1 / 3, "apport": 1 / 3}

# Depenses avant premier encaissement communes a toute activite
DEPENSES_COMMUNES = ["H-30", "H-31", "H-32"]


def _rev(volume, marge):
    return lambda cas: val(volume, cas) * val(marge, cas)


PISTES = [
    dict(id="A1", nom="Apporteur d'affaires d'un collecteur agréé",
         revenu=_rev("H-20", "H-21"), depenses_specifiques=0,
         criteres={"depenses": True, "delai": True, "legal": True, "conflit": True, "stock": True},
         remarques_legal="aucune manipulation de déchet ; statut à confirmer par écrit au MINEPDED (Q-03)",
         temps=4, temps_j="quelques rendez-vous par mois, le collecteur exécute",
         apport=5, apport_j="apprentissage du métier, données de gisement, relation avec un futur sous-traitant ou partenaire du pilote"),
    dict(id="A2", nom="Analyse d'huile en service (kits prépayés, laboratoire partenaire)",
         revenu=_rev("H-22", "H-23"), depenses_specifiques=0,
         criteres={"depenses": True, "delai": True, "legal": True, "conflit": True, "stock": True},
         remarques_legal="vente de prestation ; l'huile prélevée (100 à 200 mL) reste un échantillon d'analyse",
         temps=3, temps_j="prélèvement ou formation du client au prélèvement, interprétation des bulletins",
         apport=5, apport_j="accès aux intervalles de vidange et aux volumes de chaque engin : donnée directe du gisement forestier"),
    dict(id="A3", nom="Kits antipollution, absorbants, bacs, fûts sur commande",
         revenu=_rev("H-24", "H-25"), depenses_specifiques=0,
         criteres={"depenses": True, "delai": True, "legal": True, "conflit": True, "stock": True},
         remarques_legal="commerce général ; fournisseur à identifier (Q-06)",
         temps=3, temps_j="cotations, suivi de livraison",
         apport=4, apport_j="équipe les sites qui seront ensuite collectés ; prépare l'offre de conformité"),
    dict(id="A4", nom="Huile de chaîne biodégradable (agent ou dépôt-vente)",
         revenu=None, depenses_specifiques=None,
         criteres={"depenses": None, "delai": True, "legal": True, "conflit": True, "stock": None},
         remarques_legal="statut d'agent ou de dépôt-vente non confirmé par STIHL Cameroun [S-16] (Q-09)",
         temps=3, temps_j="", apport=2, apport_j="faible lien avec la collecte"),
    dict(id="A5", nom="Formation des mécaniciens et chefs d'atelier, chez le client",
         revenu=_rev("H-26", "H-27"), depenses_specifiques=0,
         criteres={"depenses": True, "delai": True, "legal": True, "conflit": True, "stock": True},
         remarques_legal="formation intra-entreprise ; besoin d'agrément MINEFOP à confirmer (Q-07) ; attestation de formation, pas certification",
         temps=2, temps_j="préparation des modules, 1 jour de session plus le trajet",
         apport=5, apport_j="crédibilité HSE, accès aux ateliers, mesure du besoin réel, premiers contrats"),
    dict(id="A6", nom="Abonnement à l'application de traçabilité seule",
         revenu=None, depenses_specifiques=None,
         criteres={"depenses": True, "delai": False, "legal": True, "conflit": True, "stock": True},
         remarques_legal="", temps=3, temps_j="",
         apport=4, apport_j="", motif_elimination="application non livrée (lot 16) : premier encaissement au-delà de 3 mois"),
    dict(id="A7", nom="Audit de la gestion du carburant",
         revenu=None, depenses_specifiques=None,
         criteres={"depenses": True, "delai": True, "legal": True, "conflit": False, "stock": True},
         remarques_legal="", temps=2, temps_j="", apport=3, apport_j="",
         motif_elimination="prestation d'audit concurrente de HIKMA auprès des mêmes clients ; demande non vérifiée"),
    dict(id="A8", nom="Contenu de formation en ligne",
         revenu=_rev("H-28", "H-29"), depenses_specifiques=0,
         criteres={"depenses": True, "delai": True, "legal": True, "conflit": True, "stock": True},
         remarques_legal="vente numérique", temps=4, temps_j="production unique, puis vente passive",
         apport=2, apport_j="notoriété ; peu de contact direct avec les producteurs d'huiles"),
    dict(id="A9", nom="Prix, concours, incubateurs, subventions",
         revenu=None, depenses_specifiques=None,
         criteres={"depenses": True, "delai": False, "legal": True, "conflit": True, "stock": True},
         remarques_legal="", temps=3, temps_j="", apport=3, apport_j="",
         motif_elimination="aucun appel ouvert et sourcé au 17/11/2026 [S-21][S-22] ; veille mensuelle maintenue"),
    dict(id="A10", nom="Courtage de lots d'huiles via la Bourse nationale des déchets",
         revenu=None, depenses_specifiques=None,
         criteres={"depenses": True, "delai": None, "legal": None, "conflit": True, "stock": True},
         remarques_legal="", temps=3, temps_j="", apport=4, apport_j="",
         motif_elimination="plateforme non opérationnelle confirmée [S-10][S-11] ; statut du courtier au regard du permis inconnu (Q-03)"),
    dict(id="A11", nom="Prestation de purification du gasoil avec unité louée",
         revenu=None, depenses_specifiques=None,
         criteres={"depenses": False, "delai": True, "legal": True, "conflit": True, "stock": True},
         remarques_legal="", temps=2, temps_j="", apport=5, apport_j="",
         motif_elimination="location d'unité estimée au-dessus du plafond (H-47) : traitée dans le pilote 4 bis n°1"),
]

CRITERES_ELIM = {
    "depenses": "dépenses avant encaissement <= 500 000 FCFA",
    "delai": "premier encaissement < 3 mois",
    "legal": "pas d'autorisation lourde",
    "conflit": "pas de conflit d'intérêts",
    "stock": "pas de stock payé d'avance",
}


def depenses_avant_encaissement(cas="central"):
    return sum(val(h, cas) for h in DEPENSES_COMMUNES)


def eligible(p):
    return all(v is True for v in p["criteres"].values())


def evaluer(poids=POIDS):
    retenues = [p for p in PISTES if eligible(p)]
    rev = {p["id"]: p["revenu"]("central") for p in retenues}
    rmax = max(rev.values())
    lignes = []
    for p in retenues:
        note_rev = 1 + 4 * rev[p["id"]] / rmax
        score = poids["revenu"] * note_rev + poids["temps"] * p["temps"] + poids["apport"] * p["apport"]
        lignes.append(dict(id=p["id"], nom=p["nom"], rev_bas=p["revenu"]("bas"),
                           rev_central=rev[p["id"]], rev_haut=p["revenu"]("haut"),
                           note_rev=note_rev, temps=p["temps"], apport=p["apport"], score=score))
    lignes.sort(key=lambda d: -d["score"])
    return lignes


def _sym(v):
    return {True: "oui", False: "NON", None: "à vérifier"}[v]


def rapport():
    dep = {c: depenses_avant_encaissement(c) for c in ("bas", "central", "haut")}
    out = ["# Matrice multicritère des activités d'amorçage", "",
           "Fichier généré par `00b_amorcage/matrice_amorcage.py` : ne pas éditer à la main.", "",
           "Méthode : matrice multicritère (filtre éliminatoire puis notation pondérée).", "",
           "## Filtre éliminatoire", "",
           "| Piste | " + " | ".join(CRITERES_ELIM.values()) + " | Résultat |",
           "|---" * (len(CRITERES_ELIM) + 2) + "|"]
    for p in PISTES:
        res = "retenue" if eligible(p) else "écartée : " + p.get("motif_elimination", p["remarques_legal"])
        out.append(f"| {p['id']} {p['nom']} | " + " | ".join(_sym(p["criteres"][k]) for k in CRITERES_ELIM) + f" | {res} |")
    out += ["", f"Dépenses communes avant premier encaissement (H-30, H-31, H-32) : {fcfa(dep['bas'])} "
            f"à {fcfa(dep['haut'])}, valeur centrale {fcfa(dep['central'])}, pour un plafond de "
            f"{fcfa(PLAFOND_DEPENSES)}. Statut : supposé.", "",
            "## Notation pondérée", "",
            f"Poids : revenu net 12 mois {pct(POIDS['revenu'])}, temps du promoteur {pct(POIDS['temps'])} "
            f"(5 = peu de temps), apport au projet principal {pct(POIDS['apport'])}. "
            "La note de revenu va de 1 à 5, proportionnelle au revenu central.", "",
            "| Rang | Piste | Revenu net 12 mois bas | central | haut | Note revenu | Note temps | Note apport | Score |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for i, d in enumerate(evaluer(), 1):
        out.append(f"| {i} | {d['id']} {d['nom']} | {m_fcfa(d['rev_bas'])} | {m_fcfa(d['rev_central'])} | "
                   f"{m_fcfa(d['rev_haut'])} | {d['note_rev']:.2f} | {d['temps']} | {d['apport']} | {d['score']:.2f} |".replace(".", ","))
    out += ["", "Revenus en M FCFA. Statut : supposé (hypothèses H-20 à H-29).", "",
            "## Test de robustesse : poids égaux", "",
            "| Rang | Piste | Score |", "|---|---|---:|"]
    for i, d in enumerate(evaluer(POIDS_EGAUX), 1):
        out.append(f"| {i} | {d['id']} {d['nom']} | {d['score']:.2f} |".replace(".", ","))
    top3 = evaluer()[:3]
    out += ["", "Revenu net cumulé des trois premières pistes sur 12 mois : "
            f"{m_fcfa(sum(d['rev_bas'] for d in top3))} M FCFA (cas bas) à "
            f"{m_fcfa(sum(d['rev_haut'] for d in top3))} M FCFA (cas haut), "
            f"{m_fcfa(sum(d['rev_central'] for d in top3))} M FCFA en cas central."]
    top_base = [d["id"] for d in evaluer()][:3]
    top_eg = [d["id"] for d in evaluer(POIDS_EGAUX)][:3]
    out += ["", "Les trois premières pistes sont identiques avec les deux jeux de poids : "
            + ("oui." if set(top_base) == set(top_eg) else "non : le classement dépend des poids, voir la synthèse du lot 0."), "",
            "## Justification des notes de temps et d'apport", ""]
    for p in PISTES:
        if eligible(p):
            out.append(f"- {p['id']} : temps {p['temps']} ({p['temps_j']}) ; apport {p['apport']} ({p['apport_j']}) ;")
    out[-1] = out[-1][:-2] + "."
    return "\n".join(out) + "\n", top_base


if __name__ == "__main__":
    texte, top = rapport()
    Path(__file__).with_name("matrice_amorcage.md").write_text(texte, encoding="utf-8")
    print("Lot 0 : trois premieres pistes", top)
