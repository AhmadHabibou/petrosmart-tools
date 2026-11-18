"""Lot 13 : registre des risques du projet (hors risques HSE operationnels, traites au lot 7), matrice
probabilite x gravite, mesures, declencheurs d'alerte et responsables.

Sortie : 13_risques/registre_risques.md
"""
from pathlib import Path
import importlib.util
import sys

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))

_spec = importlib.util.spec_from_file_location("hse", RACINE / "07_hse_eies" / "risques_hse.py")
hse = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hse)

# id, categorie, risque, cause, P, G, mesures, declencheur d'alerte (chiffre), responsable, P residuelle, G residuelle
RISQUES = [
    ("P01", "Réglementaire", "le MINEPDED juge que la valorisation ou la vente de combustible n'est pas couverte", "Q-01, Q-21 non tranchées", 3, 4,
     "aucun investissement de traitement avant réponse écrite (D-06) ; modèle de service d'abord", "absence de réponse écrite 90 jours après la demande", "gérant", 3, 2),
    ("P02", "Réglementaire", "le service de conformité est assimilé à une activité exigeant un permis", "Q-03", 2, 4,
     "demande écrite au MINEPDED en semaine 1 ; enlèvements toujours sous bordereau d'un collecteur titulaire", "remarque d'un inspecteur ou d'un client", "gérant", 1, 4),
    ("P03", "Réglementaire", "délai d'obtention du permis et de l'établissement classé supérieur à 18 mois", "enquête publique, catégorie d'évaluation", 3, 3,
     "dépôt dès le seuil de 320 000 L/an ; sous-traitance maintenue pendant l'instruction", "dossier non instruit 6 mois après le dépôt", "gérant", 3, 2),
    ("P04", "Marché", "les forestiers refusent le prix du contrat de conformité", "sanctions faibles ou non recouvrées", 3, 5,
     "pilote payant avec prix ferme testé ; relevé des sanctions ; offre modulaire", "moins de 1 contrat signé sur les 2 pilotes ; prix accepté inférieur à 4 M FCFA par an", "gérant", 2, 4),
    ("P05", "Marché", "la signature de nouveaux clients est deux fois plus lente que prévu", "cycle de décision des grands comptes", 3, 4,
     "plan de prospection des 50 cibles ; commercial au passage en M1 ; références des pilotes", "moins de 4 clients au mois 18", "commercial", 2, 3),
    ("P06", "Concurrence", "un collecteur agréé capte directement les clients forestiers", "révélation de la niche lors de la sous-traitance", 3, 4,
     "contrat de conformité signé avant sous-traitance ; clause de non-sollicitation de 2 ans", "démarche directe du sous-traitant chez un client", "gérant", 2, 3),
    ("P07", "Concurrence", "l'unité de Valtech Energy démarre et collecte gratuitement à Douala", "Q-11", 2, 3,
     "positionnement forestier ; proposition de partenariat d'approvisionnement", "annonce de mise en service ou offre de collecte gratuite", "gérant", 2, 2),
    ("P08", "Concurrence", "guerre des prix sur les contrats", "concurrent ou circuit informel", 2, 4,
     "valeur ajoutée documentaire (FSC, OLB, rapport annuel) ; contrats de 2 ans", "baisse de prix demandée par au moins 2 clients", "commercial", 2, 3),
    ("P09", "Approvisionnement", "aucun valorisateur titulaire n'accepte les huiles gratuitement", "absence de débouché en service", 3, 3,
     "accord écrit avant le premier enlèvement ; coût d'élimination refacturé dans le contrat", "valorisateur exigeant un paiement supérieur à 50 FCFA/L", "gérant", 2, 2),
    ("P10", "Approvisionnement", "lots contaminés (chlore, PCB) fréquents", "mélanges de solvants en atelier", 3, 3,
     "dépistage systématique ; formation au tri ; prix majoré des lots refusés", "plus de 10 % de lots positifs sur un trimestre", "technicien", 2, 2),
    ("P11", "Financier", "fonds propres et quasi-fonds propres insuffisants", "associés non trouvés", 3, 5,
     "comptes courants bloqués ; garantie CDEC et AGF ; facturation trimestrielle d'avance", "trésorerie prévisionnelle à 3 mois inférieure à 2 mois de charges", "gérant", 2, 4),
    ("P12", "Financier", "retards de paiement des grands comptes", "pratiques de paiement à 90 jours ou plus", 3, 3,
     "facturation d'avance ; suspension de service contractuelle ; affacturage à étudier", "encours clients supérieur à 90 jours de chiffre d'affaires", "assistant administratif", 2, 2),
    ("P13", "Financier", "hausse du coût du crédit ou refus bancaire", "profil sans historique", 3, 3,
     "crédit-bail plutôt qu'emprunt ; dossier bancaire avec les résultats du pilote", "deux refus de financement", "gérant", 2, 3),
    ("P14", "Opérationnel", "un client devient inaccessible en saison des pluies, avec débordement des fûts", "barrières de pluie, pistes", 3, 4,
     "stock tampon sur rétention pour un trimestre ; enlèvements calés en saison sèche", "taux de remplissage des fûts d'un client supérieur à 80 % à l'approche des pluies", "technicien", 2, 2),
    ("P15", "Opérationnel", "rupture de cartouches de rechange du purificateur", "approvisionnement hors CEMAC", 3, 2,
     "stock de sécurité de 3 mois ; deuxième fournisseur (Q-37)", "stock inférieur à 6 semaines de consommation", "technicien", 1, 2),
    ("P16", "Ressources humaines", "départ du technicien unique", "missions longues, salaire", 3, 4,
     "vivier formé ; prime de fidélité ; polyvalence du gérant", "absence non remplacée de plus de 2 semaines", "gérant", 2, 3),
    ("P17", "Gouvernance", "conflit d'intérêts avec HIKMA mis en cause par un client ou un tiers", "double fonction du promoteur", 3, 4,
     "charte signée ; lettre d'information aux clients communs ; registre des conflits", "réclamation écrite d'un client ou d'un concurrent", "gérant et associés", 1, 4),
    ("P18", "Gouvernance", "le promoteur ne peut pas dégager le temps nécessaire", "poste chez HIKMA", 4, 4,
     "gérant à temps plein au passage en M1 ; technicien autonome dès le pilote", "plus de 2 jalons du plan des 100 jours en retard de plus de 2 semaines", "associés", 2, 3),
    ("P19", "Réputation", "accident de transport d'un sous-traitant attribué à la société", "voir R01 du lot 7", 2, 5,
     "exigences HSE et assurance du sous-traitant ; GPS partagé ; assurance propre", "incident de transport chez un sous-traitant", "gérant", 1, 4),
    ("P20", "Technique", "rendement et qualité du prétraitement inférieurs aux hypothèses", "huiles très contaminées", 2, 3,
     "essai sur échantillon réel avant achat ; prétraitement seulement à l'étape 4", "rendement mesuré inférieur à 70 %", "responsable d'exploitation", 1, 2),
]


def classe(c):
    return hse.classe(c)


def rapport():
    out = ["# Registre des risques du projet", "",
           "Fichier généré par `13_risques/registre_risques.py`. Méthode : matrice probabilité × gravité, notes de 1 à 5 (jugements, statut : supposé). "
           "Les risques HSE opérationnels sont dans `07_hse_eies/matrice_risques_hse.md` et rappelés en fin de fichier.", "",
           "| ID | Catégorie | Risque | Cause | P | G | Criticité | Mesures | Déclencheur d'alerte | Responsable | Criticité résiduelle |",
           "|---|---|---|---|---:|---:|---|---|---|---|---|"]
    for r in RISQUES:
        c, cr = r[4] * r[5], r[9] * r[10]
        out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {c} {classe(c)} | {r[6]} | {r[7]} | {r[8]} | {cr} {classe(cr)} |")
    out += ["", "## Matrice probabilité × gravité (criticité initiale)", "",
            "| Probabilité \\ Gravité | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|"]
    for p in range(5, 0, -1):
        cells = []
        for g in range(1, 6):
            ids = [r[0] for r in RISQUES if r[4] == p and r[5] == g]
            cells.append(", ".join(ids))
        out.append(f"| {p} | " + " | ".join(cells) + " |")
    ini = [r[4] * r[5] for r in RISQUES]
    res = [r[9] * r[10] for r in RISQUES]
    out += ["", f"Risques à réduire ou inacceptables : {sum(c >= 8 for c in ini)} sur {len(RISQUES)} avant mesures, {sum(c >= 8 for c in res)} après mesures. "
            f"Risques inacceptables (criticité de 15 ou plus) avant mesures : {', '.join(r[0] for r in RISQUES if r[4] * r[5] >= 15)}.", "",
            "## Rappel des risques HSE opérationnels (lot 7)", ""]
    for r in hse.RISQUES:
        out.append(f"- {r[0]} : {r[3]}, criticité {r[4] * r[5]} avant mesures, {r[7] * r[8]} après.")
    out.append("")
    return "\n".join(out) + "\n", ini, res


if __name__ == "__main__":
    t, ini, res = rapport()
    Path(__file__).with_name("registre_risques.md").write_text(t, encoding="utf-8")
    print("Lot 13 : >= 8 avant/apres", sum(c >= 8 for c in ini), sum(c >= 8 for c in res))
