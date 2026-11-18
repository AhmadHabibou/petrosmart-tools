"""Lot 7 : matrice probabilite x gravite des risques HSE (site et transport) et bornes d'emissions de metaux.

Sorties : 07_hse_eies/matrice_risques_hse.md, 07_hse_eies/emissions.md
Les notes P et G (1 a 5) sont des jugements de l'expert HSE, a reevaluer apres le pilote.
"""
from pathlib import Path
import sys

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from commun.hypotheses import val  # noqa: E402
from commun.format import nombre  # noqa: E402

# (id, activite, danger, evenement, P, G, mesures principales, P residuelle, G residuelle)
RISQUES = [
    ("R01", "Transport routier", "huile usagée en citerne", "renversement ou collision avec déversement", 3, 4,
     "chauffeur formé, vitesse limitée, pas de conduite de nuit sur piste, GPS, kit antipollution à bord, plan d'intervention", 2, 4),
    ("R02", "Transport sur piste", "véhicule lourd en terrain dégradé", "enlisement, basculement en saison des pluies", 4, 3,
     "calendrier d'enlèvement en saison sèche, reconnaissance des pistes, treuil, communication satellite ou radio", 2, 3),
    ("R03", "Chargement chez le client", "pompage d'huile", "débordement, rupture de flexible", 3, 2,
     "flexibles contrôlés, bac de rétention sous les raccords, absorbants, présence permanente de l'opérateur", 2, 2),
    ("R04", "Chargement chez le client", "lot contaminé (solvants chlorés, PCB)", "contamination de la citerne et du lot entier", 3, 4,
     "dépistage Clor-D-Tect avant chaque pompage, refus et isolement, déclaration d'origine signée", 1, 4),
    ("R05", "Purification du gasoil", "gasoil, électricité, groupe de pompage", "incendie ou départ de feu sur fuite", 2, 4,
     "liaison équipotentielle, zone sans flamme ni téléphone, extincteurs, matériel adapté aux atmosphères explosives si l'étude le demande", 1, 4),
    ("R06", "Nettoyage de cuve", "espace confiné, vapeurs", "intoxication, asphyxie, explosion", 2, 5,
     "nettoyage depuis l'extérieur de préférence ; sinon permis d'entrée, détecteur 4 gaz, ventilation, surveillant, harnais", 1, 5),
    ("R07", "Centre de transit (étape 3)", "stockage d'huiles et de gasoil", "incendie de cuvette", 2, 5,
     "rétention, distances de sécurité, détection, moyens d'extinction, plan d'opération interne", 1, 4),
    ("R08", "Centre de transit (étape 3)", "fuite de cuve ou de rétention", "pollution du sol et de la nappe", 3, 4,
     "dalle étanche, séparateur, inspection hebdomadaire, piézomètre de contrôle", 1, 3),
    ("R09", "Prétraitement (étape 4)", "huile chaude sous vide, condensats légers", "inflammation des vapeurs, brûlure", 2, 4,
     "température maîtrisée, soupapes, condensats en récipient fermé, point éclair suivi", 1, 4),
    ("R10", "Toutes activités", "contact cutané avec l'huile usagée", "dermatoses, exposition aux HAP et aux métaux", 4, 3,
     "gants nitrile, vêtements à manches longues, lavage, interdiction de manger sur le poste, suivi médical", 2, 2),
    ("R11", "Toutes activités", "manutention de fûts", "troubles musculosquelettiques, écrasement", 4, 2,
     "diable et lève-fût, fûts de 200 L non soulevés à la main, chaussures de sécurité", 2, 2),
    ("R12", "Riverains et circuit informel", "vol de fûts ou d'huiles", "brûlage ou rejet sauvage, atteinte à la réputation", 3, 3,
     "fûts scellés et numérotés (QR code, lot 16), bordereau, stockage fermé chez le client", 2, 3),
]


def classe(c):
    return "inacceptable" if c >= 15 else ("à réduire" if c >= 8 else "acceptable sous surveillance")


def rapport_risques():
    out = ["# Matrice probabilité × gravité des risques HSE", "",
           "Fichier généré par `07_hse_eies/risques_hse.py`. Probabilité et gravité notées de 1 à 5 par l'expert HSE ; criticité = P × G. "
           "Classes : 15 et plus inacceptable, 8 à 14 à réduire, moins de 8 acceptable sous surveillance. Statut : supposé.", "",
           "| ID | Activité | Événement | P | G | Criticité initiale | Mesures | P résiduelle | G résiduelle | Criticité résiduelle |",
           "|---|---|---|---:|---:|---|---|---:|---:|---|"]
    for r in RISQUES:
        ci, cr = r[4] * r[5], r[7] * r[8]
        out.append(f"| {r[0]} | {r[1]} | {r[3]} ({r[2]}) | {r[4]} | {r[5]} | {ci} {classe(ci)} | {r[6]} | {r[7]} | {r[8]} | {cr} {classe(cr)} |")
    ini = [r[4] * r[5] for r in RISQUES]
    res = [r[7] * r[8] for r in RISQUES]
    out += ["", f"Risques à réduire ou inacceptables avant mesures : {sum(c >= 8 for c in ini)} sur {len(RISQUES)} ; "
            f"après mesures : {sum(c >= 8 for c in res)} sur {len(RISQUES)}.", ""]
    return "\n".join(out) + "\n", ini, res


def borne_emission_kg(concentration_mg_kg, volume_l):
    """Borne haute : tout le metal du combustible est emis a la cheminee (aucune retention dans les cendres)."""
    return concentration_mg_kg * 1e-6 * volume_l * val("H-60")


def rapport_emissions():
    v_ref = 1000.0
    out = ["# Émissions de métaux lors de la combustion : méthode de borne haute", "",
           "Fichier généré par `07_hse_eies/risques_hse.py`.", "",
           "Les facteurs d'émission de l'EPA pour la combustion des huiles usagées (AP-42, section 1.11 [S-77]) expriment le plomb émis "
           "en proportion de la teneur en plomb du combustible ; leurs valeurs n'ont pas pu être lues. En attendant, la borne haute suppose que tout le métal "
           "contenu dans le combustible sort à la cheminée. Elle se calcule sans hypothèse sur l'installation de l'acheteur, à partir des résultats de laboratoire du protocole 4 bis n°2.", "",
           f"Formule : émission (kg) = teneur (mg/kg) × 10⁻⁶ × volume brûlé (L) × masse volumique (H-60, {nombre(val('H-60'), 2)} kg/L).", "",
           "| Teneur du combustible en métal (mg/kg) | Émission maximale pour 1 000 L brûlés (g) | Pour 100 000 L brûlés (kg) |", "|---:|---:|---:|"]
    for c in (10, 50, 100, 500, 1000):
        out.append(f"| {nombre(c)} | {nombre(borne_emission_kg(c, v_ref) * 1000, 1)} | {nombre(borne_emission_kg(c, 100_000), 2)} |")
    out += ["", "Aucune teneur n'est supposée ici : la colonne de gauche est une échelle de lecture. Les teneurs réelles viendront des analyses ASTM D5185.", ""]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    t, ini, res = rapport_risques()
    Path(__file__).with_name("matrice_risques_hse.md").write_text(t, encoding="utf-8")
    Path(__file__).with_name("emissions.md").write_text(rapport_emissions(), encoding="utf-8")
    print("Lot 7 : risques >= 8 avant/apres", sum(c >= 8 for c in ini), sum(c >= 8 for c in res))
