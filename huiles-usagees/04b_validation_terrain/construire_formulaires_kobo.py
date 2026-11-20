"""Formulaires de terrain au format XLSForm (KoboToolbox, ODK Collect), utilisables hors reseau sur telephone.

Sources : 04_marche/questionnaire_garages.md (enquete des 30 garages, saisie question par question)
et les fiches CSV de 04b_validation_terrain/formulaires/ (types deduits du nom de chaque colonne).
Sorties : 04b_validation_terrain/kobo/*.xlsx, chacun valide par pyxform (conversion en XForm).

Usage : python 04b_validation_terrain/construire_formulaires_kobo.py
"""
from pathlib import Path
import csv
import re

from openpyxl import Workbook

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
SORTIE = ICI / "kobo"

OUI_NON = [("oui", "Oui"), ("non", "Non")]
ECHELLE = [(str(i), str(i)) for i in range(1, 6)]

# --- enquete des garages : questions du questionnaire du lot 4 ---------------------------------
GARAGES = [
    ("note", "intro", "Présentation : objet de l'enquête, anonymat des réponses, aucune obligation d'achat.", None),
    ("date", "date_enquete", "Date de l'entretien", None),
    ("text", "enqueteur", "Enquêteur", None),
    ("select_one ville", "ville", "Ville", None),
    ("text", "arrondissement", "Arrondissement ou quartier", None),
    ("geopoint", "position", "Position de l'établissement", None),
    ("select_one strate", "strate", "1. Type d'établissement (strate)", None),
    ("text", "nom_etablissement", "Nom de l'établissement (confidentiel)", None),
    ("text", "interlocuteur_fonction", "Fonction de l'interlocuteur", None),
    ("integer", "q2_vehicules_mois", "2. Nombre de véhicules ou engins entretenus par mois", None),
    ("select_multiple types", "q3_types", "3. Types de véhicules ou engins", None),
    ("integer", "q4_vidanges_semaine", "4. Nombre de vidanges réalisées par semaine", None),
    ("decimal", "q5_volume_moyen_L", "5. Volume moyen d'huile retiré par vidange (L)", None),
    ("decimal", "q6_stock_L", "6. Volume d'huile usagée stocké aujourd'hui sur le site (L), observé si possible", None),
    ("select_one frequence", "q7_frequence_vidage", "7. Fréquence à laquelle le stock est vidé", None),
    ("select_one enleveur", "q8_enleveur", "8. Qui enlève aujourd'hui les huiles usagées ?", None),
    ("select_one flux", "q9_flux_financier", "9. Lors de l'enlèvement, le garage est-il payé, paie-t-il, ou est-ce gratuit ?", None),
    ("decimal", "q9_montant_FCFA_L", "9 bis. Montant par litre (FCFA)", "${q9_flux_financier} != 'gratuit'"),
    ("text", "q10_usage_aval", "10. À quoi servent les huiles selon vous, après l'enlèvement ?", None),
    ("select_multiple melanges", "q11_melanges", "11. Mélangez-vous d'autres liquides aux huiles ?", None),
    ("select_one oui_non", "q12_registre_bordereau", "12. Tenez-vous un registre ou recevez-vous un bordereau lors de l'enlèvement ?", None),
    ("select_one oui_non_nsp", "q13_controle_3ans", "13. Contrôle, remarque ou sanction sur les huiles ces trois dernières années ?", None),
    ("select_one oui_non", "q14_preuve_demandee", "14. Vos clients vous demandent-ils une preuve de gestion des huiles ?", None),
    ("decimal", "q15_prix_min_cession_FCFA_L", "15. Prix minimal pour céder vos huiles à un collecteur tracé (FCFA/L)", None),
    ("select_one cession", "q16_gratuit_payer", "16. Avec bordereau et certificat : céder gratuitement, payer, ou refuser ?", None),
    ("decimal", "q16_montant_FCFA_fut", "16 bis. Montant par fût (FCFA)", "${q16_gratuit_payer} = 'payer'"),
    ("select_one frequence", "q17_frequence_souhaitee", "17. Fréquence d'enlèvement souhaitée", None),
    ("select_one oui_non", "q18_futs_acceptes", "18. Accepteriez-vous des fûts étiquetés fournis par le collecteur ?", None),
    ("select_one oui_non", "q19_echantillon_accepte", "19. Accepteriez-vous un prélèvement d'échantillon pour analyse, sans frais ?", None),
    ("select_one oui_non", "q20_recontact", "20. Pouvons-nous vous recontacter ?", None),
    ("text", "q20_contact", "20 bis. Nom et fonction du contact", "${q20_recontact} = 'oui'"),
    ("note", "obs_intro", "Observations de l'enquêteur, sans question", None),
    ("select_one echelle", "observation_aire_vidange", "État de l'aire de vidange (1 très mauvais, 5 très bon)", None),
    ("select_one oui_non", "observation_retention", "Présence d'une rétention", None),
    ("select_one oui_non", "observation_sols", "Sols souillés", None),
    ("select_one oui_non", "observation_autres_futs", "Présence de fûts d'autres produits", None),
    ("image", "photo_stockage", "Photo du stockage (avec accord)", None),
    ("select_one oui_non", "refus_remplacement", "Établissement de remplacement après un refus ?", None),
]
CHOIX_GARAGES = {
    "ville": [("douala", "Douala"), ("yaounde", "Yaoundé")],
    "strate": [("garage", "Garage indépendant"), ("concession", "Concessionnaire ou atelier agréé"), ("flotte", "Flotte de transport"),
               ("btp_industrie", "BTP, industrie, groupes électrogènes")],
    "types": [("voitures", "Voitures"), ("camions", "Camions"), ("motos", "Motos"), ("engins", "Engins"), ("groupes", "Groupes électrogènes")],
    "frequence": [("semaine", "Chaque semaine"), ("mois", "Chaque mois"), ("trimestre", "Chaque trimestre"), ("plus", "Moins souvent"), ("nsp", "Ne sait pas")],
    "enleveur": [("collecteur_agree", "Collecteur agréé"), ("informel", "Acheteur informel"), ("reutilisation", "Réutilisation sur place"), ("autre", "Autre")],
    "flux": [("paye", "Le garage est payé"), ("paie", "Le garage paie"), ("gratuit", "Gratuit")],
    "melanges": [("aucun", "Aucun"), ("frein", "Liquide de frein"), ("refroidissement", "Liquide de refroidissement"), ("solvants", "Solvants"),
                 ("gasoil", "Gasoil de nettoyage"), ("nsp", "Ne sait pas")],
    "cession": [("gratuit", "Céder gratuitement"), ("payer", "Payer"), ("refus", "Refuser")],
    "oui_non": OUI_NON,
    "oui_non_nsp": OUI_NON + [("nsp", "Ne souhaite pas répondre")],
    "echelle": ECHELLE,
}

# --- fiches CSV : titres et libelles ------------------------------------------------------------
TITRES = {
    "chaine_tracabilite_echantillons": "Chaîne de traçabilité des échantillons",
    "essai_combustion_mesures": "Mesures d'essai de combustion",
    "fiche_incident": "Fiche d'incident",
    "fiche_prospect": "Fiche prospect",
    "pilote_journal_tournee": "Pilote : journal de tournée",
    "pilote_purification_gasoil": "Pilote : purification du gasoil",
    "releve_sanctions": "Relevé des sanctions",
    "resultats_analyses": "Résultats d'analyses de laboratoire",
}
MOTS = {"id": "identifiant", "nb": "nombre de", "coord": "coordonnées", "gps": "GPS", "pct": "%", "C": "°C", "L": "L", "h": "h",
        "FCFA": "FCFA", "mL": "mL", "ppm": "ppm", "km": "km", "kg": "kg", "n": "n°", "1a5": "(1 à 5)",
        "cSt": "cSt", "40C": "40 °C", "15C": "15 °C", "pct_m": "% massique", "pct_v": "% volumique", "mg": "mg", "O2": "O₂", "NOx": "NOx",
        "SO2": "SO₂", "CO": "CO", "PCB": "PCB"}
DECIMAL = re.compile(r"((_FCFA|_L|_L_h|_km|_h|_ppm|_pct|_C|_mL|_kg|_cSt|_mg_kg|_D\d+|_15C)$|^(km|volume|debit|duree|temps|cout|montant|prix|densite)_)")
ACCENTS = {"echantillon": "échantillon", "preleveur": "préleveur", "methode": "méthode", "prelevement": "prélèvement", "prelevee": "prélevée",
           "scelle": "scellé", "a": "à", "reception": "réception", "fumees": "fumées", "opacite": "opacité", "stabilite": "stabilité",
           "observe": "observé", "operateur": "opérateur", "etalonnage": "étalonnage", "activite": "activité", "immediate": "immédiate",
           "declare": "déclaré", "cloture": "clôture", "categorie": "catégorie", "frequence": "fréquence", "enlevement": "enlèvement",
           "proposee": "proposée", "soustraitant": "sous-traitant", "vehicule": "véhicule", "duree": "durée", "etat": "état", "futs": "fûts",
           "cout": "coût", "facture": "facturé", "traite": "traité", "retiree": "retirée", "sediments": "sédiments", "apres": "après",
           "utilisees": "utilisées", "autorite": "autorité", "vise": "visé", "numero": "numéro", "delai": "délai", "regularisation": "régularisation",
           "donnee": "donnée", "piece": "pièce", "ref": "référence", "resultat": "résultat", "eclair": "éclair", "viscosite": "viscosité",
           "densite": "densité", "decision": "décision", "paye": "payé", "confidentialite": "confidentialité", "deversement": "déversement",
           "quasi": "quasi-", "non": "non", "conformite": "conformité", "mise": "mise", "demeure": "demeure", "heure": "et heure",
           "accreditation": "accréditation", "tect": "Tect", "clor": "Clor", "crepitement": "crépitement", "remise": "remise", "temp": "température",
           "debit": "débit", "acheteur": "acheteur", "observation": "observation", "fumee": "fumée", "tournee": "tournée"}
LIBELLES = {"clor_d_tect_resultat": "Résultat du dépistage Clor-D-Tect", "eau_test_crepitement": "Test d'eau au crépitement",
            "texte_vise_numero_date": "Texte visé (numéro et date)", "type_acte": "Type d'acte", "type": "Type d'événement"}
FORCES = {
    "saison": ("select_one", "saison", [("seche", "Saison sèche"), ("pluies", "Saison des pluies")]),
    "decision_acceptation": ("select_one", "decision", [("accepte", "Lot accepté"), ("refuse", "Lot refusé"), ("attente", "En attente")]),
    "confidentialite": ("select_one", "oui_non", OUI_NON),
    "clor_d_tect_resultat": ("select_one", "clor", [("bleu", "Bleu : moins de 1 000 ppm"), ("jaune", "Jaune : plus de 1 000 ppm")]),
    "frequence_vidange_h": ("decimal", None, None),
}
INTEGER = re.compile(r"^(nb_|cartouches)", re.I)


def libelle(col):
    col = re.sub(r"\(.*\)", "", col)
    if col in LIBELLES:
        return LIBELLES[col]
    col = re.sub(r"_oui_non$", "", col)
    mots = [MOTS.get(m, ACCENTS.get(m, m)) for m in col.split("_")]
    t = " ".join(m for m in mots if m).strip().replace("nombre de e", "nombre d'e").replace("quasi- ", "quasi-").replace("Nombre de e", "Nombre d'e")
    return t[:1].upper() + t[1:]


def type_colonne(col):
    """(type XLSForm, nom de liste, choix) deduits du nom de la colonne."""
    m = re.search(r"\(([^)]*\|[^)]*)\)", col)
    nom = re.sub(r"\(.*\)", "", col)
    if nom in FORCES:
        return FORCES[nom]
    if m:
        return "select_one", nom, [(c, libelle(c)) for c in m.group(1).split("|")]
    if nom.endswith("oui_non"):
        return "select_one", "oui_non", OUI_NON
    if nom.endswith("1a5"):
        return "select_one", "echelle", ECHELLE
    if nom == "date" or nom.startswith("date_") and "heure" not in nom:
        return "date", None, None
    if nom == "date_heure":
        return "dateTime", None, None
    if nom.startswith("coord_gps"):
        return "geopoint", None, None
    if nom.startswith("signature"):
        return "image", None, None
    if INTEGER.search(nom):
        return "integer", None, None
    if DECIMAL.search(nom) or re.fullmatch(r"(O2|CO|NOx|SO2|PCB|Pb|Zn|Cd|Cr|Ni|Cu|eau|chlore|soufre|point_eclair|viscosite|charge|sediments)(_.*)?", nom) \
            and not nom.startswith(("eau_test",)):
        return "decimal", None, None
    return "text", None, None


def classeur(chemin, titre, form_id, lignes, choix):
    wb = Workbook()
    s = wb.active
    s.title = "survey"
    s.append(["type", "name", "label", "required", "relevant", "appearance"])
    for typ, nom, lab, rel in lignes:
        app = "signature" if typ == "image" and nom.startswith("signature") else ""
        req = "" if typ in ("note", "image", "geopoint") or rel else "yes"
        s.append([typ, nom, lab, req, rel or "", app])
    c = wb.create_sheet("choices")
    c.append(["list_name", "name", "label"])
    for liste, valeurs in choix.items():
        for v, l in valeurs:
            c.append([liste, v, l])
    st = wb.create_sheet("settings")
    st.append(["form_title", "form_id", "default_language"])
    st.append([titre, form_id, "Français (fr)"])
    wb.save(chemin)
    from commun.deterministe import figer
    figer(chemin)


def depuis_csv(chemin_csv):
    entetes = next(csv.reader(chemin_csv.open(encoding="utf-8"), delimiter=";"))
    lignes, choix = [], {}
    for col in entetes:
        typ, liste, valeurs = type_colonne(col)
        nom = re.sub(r"\(.*\)", "", col)
        if typ == "select_one":
            choix[liste] = valeurs
            typ = f"select_one {liste}"
        lignes.append((typ, nom, libelle(col), None))
    return lignes, choix


def valider(chemin):
    """Conversion XLSForm vers XForm par pyxform ; leve une exception si le formulaire est invalide."""
    from pyxform.xls2xform import convert
    return convert(xlsform=str(chemin), validate=False).xform


def construire():
    import sys
    sys.path.insert(0, str(RACINE))
    SORTIE.mkdir(exist_ok=True)
    produits = []
    g = SORTIE / "enquete_garages.xlsx"
    classeur(g, "Enquête des 30 garages et flottes", "enquete_garages", GARAGES, CHOIX_GARAGES)
    produits.append(g)
    for f in sorted((ICI / "formulaires").glob("*.csv")):
        lignes, choix = depuis_csv(f)
        x = SORTIE / f"{f.stem}.xlsx"
        classeur(x, TITRES.get(f.stem, f.stem), f.stem, lignes, choix)
        produits.append(x)
    for p in produits:
        valider(p)
    return produits


if __name__ == "__main__":
    p = construire()
    print(f"Formulaires KoboToolbox : {len(p)} classeurs XLSForm valides")
