"""Lot 15 : construction du kit operationnel.

1. Genere les sources chiffrees : grille tarifaire (depuis les hypotheses), cahiers des charges et demandes de prix
   (francais et anglais) pour chaque equipement.
2. Genere deux classeurs a formules : grille de comparaison des offres, tableau de bord des indicateurs.
3. Convertit toutes les sources Markdown du kit, ainsi que les statuts, le pacte, la charte (lot 11) et la procedure
   d'acceptation des lots (lot 4 bis), en .docx selon la charte typographique, puis en .pdf par LibreOffice.

Usage : python 15_kit_operationnel/construire_kit.py [--sans-pdf]
"""
from pathlib import Path
import sys

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from commun.hypotheses import val  # noqa: E402
from commun.format import fcfa  # noqa: E402
from commun import docx_charte  # noqa: E402

KIT = Path(__file__).resolve().parent
SRC = KIT / "sources"
DATE = "2026-11-18"
PREFIXE = f"{DATE} Huiles usagees"

EQUIPEMENTS = [
    dict(code="E1", fr="Purificateur de gasoil portable", en="Portable diesel fuel conditioning cart",
         ref="Parker DFC14WS25VVX1 ou DFCC14WS10VVX1 (filtration plus fine), en version 50 Hz, ou équivalent (Donaldson Clean Diesel Cart, HYDAC LVU-CD)", qte="1",
         spec_fr=["débit d'au moins 60 L/min", "séparation de l'eau et filtration des particules (élément séparateur d'eau)",
                  "alimentation 220 V monophasé, 50 Hz", "indicateur de colmatage", "joints compatibles gasoil",
                  "flexibles d'aspiration et de refoulement d'au moins 5 m, canne d'aspiration de fond"],
         spec_en=["flow rate of at least 60 L/min", "water separation and particle filtration (water separator element)",
                  "220 V single phase, 50 Hz power supply", "clogging indicator", "diesel-compatible seals",
                  "suction and discharge hoses of at least 5 m, tank bottom suction wand"],
         options="achat, location ou crédit-bail ; prix d'un jeu de 12 cartouches de rechange ; offre séparée pour chacune des deux références Parker"),
    dict(code="E2", fr="Purificateur d'huile sous vide", en="Vacuum oil purifier",
         ref="série TYA ou équivalent", qte="1",
         spec_fr=["débit nominal de 10 L/min (600 L/h) au moins", "chauffage réglable de 40 à 80 °C",
                  "déshydratation sous vide, eau résiduelle garantie sur huile moteur usagée", "préfiltration grossière et filtration fine",
                  "sécurités : surchauffe, niveau, manque de vide", "essai sur échantillon réel fourni par l'acheteur avant commande"],
         spec_en=["nominal flow rate of at least 10 L/min (600 L/h)", "adjustable heating from 40 to 80 °C",
                  "vacuum dehydration, guaranteed residual water on used engine oil", "coarse prefiltration and fine filtration",
                  "safety devices: overheating, level, loss of vacuum", "test on a real sample supplied by the buyer before order"],
         options="achat uniquement après la porte de l'étape 4"),
    dict(code="E3", fr="Appareil de point éclair Pensky-Martens en vase clos", en="Pensky-Martens closed cup flash point tester",
         ref="conforme ASTM D93", qte="1",
         spec_fr=["méthode ASTM D93", "fonctionnement automatique", "détection de l'éclair automatique", "certificat d'étalonnage"],
         spec_en=["ASTM D93 method", "automatic operation", "automatic flash detection", "calibration certificate"],
         options="achat à l'étape 4 ; sous-traitance au laboratoire avant"),
    dict(code="E4", fr="Kits de dépistage des halogènes dans les huiles usagées", en="Halogen screening kits for used oils",
         ref="Dexsil Clor-D-Tect 1000 (ASTM D5384) ou équivalent", qte="20",
         spec_fr=["seuil de réponse à 1 000 ppm de chlore", "méthode ASTM D5384", "date de péremption d'au moins 12 mois à la livraison"],
         spec_en=["1,000 ppm chlorine response threshold", "ASTM D5384 method", "shelf life of at least 12 months at delivery"],
         options="achat"),
    dict(code="E5", fr="Matériel de prélèvement", en="Sampling equipment",
         ref="Koehler K27400 et échantillonneur COLIWASA ou équivalent", qte="1 lot",
         spec_fr=["canne de prélèvement de fût sur toute la hauteur", "échantillonneur COLIWASA", "50 flacons en verre ambré de 500 mL à bouchon à joint PTFE",
                  "étiquettes et scellés numérotés", "glacière"],
         spec_en=["full-height drum thief", "COLIWASA sampler", "50 amber glass 500 mL bottles with PTFE-lined caps",
                  "numbered labels and seals", "cool box"],
         options="achat"),
    dict(code="E6", fr="Camion hydrocureur ADR d'occasion pour huiles usagées", en="Used ADR vacuum tanker truck for used oils",
         ref="porteur de type IVECO Eurocargo, MAN ou DAF, citerne sous vide d'environ 13 000 L", qte="1",
         spec_fr=["citerne sous vide conforme ADR, compatible hydrocarbures", "pompe à vide (à palettes ou à anneau liquide) avec protection contre le débordement de la citerne",
                  "flexibles d'aspiration d'au moins 10 m et canne pour fûts de 200 L", "vidange par gravité et par mise en pression", "équipements de sécurité et signalisation",
                  "historique d'entretien de la pompe et du porteur", "visite technique valide", "garantie mécanique d'au moins 3 mois"],
         spec_en=["ADR-compliant vacuum tank, hydrocarbon-compatible", "vacuum pump (rotary vane or liquid ring) with tank overfill protection",
                  "suction hoses of at least 10 m and wand for 200 L drums", "gravity and pressure discharge", "safety equipment and placards",
                  "maintenance history of pump and chassis", "valid roadworthiness certificate", "mechanical warranty of at least 3 months"],
         options="achat à l'étape 3 seulement (D-10) ; location avec chauffeur en dépannage"),
    dict(code="E7", fr="Véhicule léger 4x4 pick-up", en="4x4 pick-up light vehicle",
         ref="Toyota Hilux 2.4 GD-6 ou équivalent", qte="1",
         spec_fr=["4x4, double cabine", "plateau avec arrimage pour le purificateur et des fûts vides", "réseau de pièces et d'entretien en Afrique centrale"],
         spec_en=["4x4, double cab", "load bed with tie-downs for the purifier and empty drums", "parts and service network in Central Africa"],
         options="location ou crédit-bail à l'étape 1, achat ou crédit-bail au passage en M1"),
]


def grille_tarifaire():
    marge = 0.20  # regle du lot 4 bis : prix couvrant le cout complet + 20 %
    lignes = [
        ("Forfait annuel de conformité par site forestier (fûts, kit, registre, formation, 4 enlèvements, dépistage, rapport)", fcfa(val("H-80")) + " HT par an", "H-80, à valider par le pilote"),
        ("Intervention de purification du gasoil et nettoyage de cuve hors forfait", fcfa(val("H-81")) + " HT par intervention", "H-81"),
        ("Session de formation d'une journée, jusqu'à 15 participants, hors frais de mission", fcfa(val("H-33")) + " HT", "H-33"),
        ("Analyse d'huile en service par engin", "coût du laboratoire + acheminement + " + fcfa(val("H-34")) + " HT", "H-34"),
        ("Enlèvement d'urgence hors calendrier", "coût réel du transport + 20 %", "règle du lot 4 bis"),
        ("Élimination d'un lot refusé (chlore, PCB)", "coût réel de l'élimination + 20 %", "contrat C1, article 6"),
        ("Collecte des filtres et absorbants souillés (après permis)", "sur devis", "extension E1"),
    ]
    out = ["# Grille tarifaire", "", f"Tarifs applicables au [date], valables jusqu'au [date].", "",
           "| Prestation | Prix |", "|---|---|"]
    out += [f"| {a} | {b} |" for a, b, _ in lignes]
    out += ["", "Facturation trimestrielle d'avance pour les forfaits. Paiement à 30 jours. Prix révisables chaque année.",
            f"Les majorations de {int(marge * 100)} % appliquées aux prestations au coût réel couvrent la gestion et le risque."]
    return "\n".join(out) + "\n", lignes


def grille_tarifaire_trace():
    _, lignes = grille_tarifaire()
    return "\n".join(["| Prestation | Prix d'appel | Hypothèse ou règle |", "|---|---|---|"] + [f"| {a} | {b} | {c} |" for a, b, c in lignes])


def cahiers_des_charges():
    out = ["# Cahiers des charges des équipements", "",
           "Spécifications minimales. Les offres doivent indiquer : prix départ usine et prix rendu Douala, délai de livraison, garantie, "
           "service après-vente et disponibilité des pièces et consommables en Afrique centrale, formation à la mise en service.", ""]
    for e in EQUIPEMENTS:
        out += [f"## {e['code']} {e['fr']}", "", f"Référence indicative : {e['ref']}. Quantité : {e['qte']}. Mode d'acquisition : {e['options']}.", ""]
        out += [f"- {s} ;" for s in e["spec_fr"][:-1]] + [f"- {e['spec_fr'][-1]}.", ""]
    return "\n".join(out) + "\n"


def rfq(e):
    fr = [f"# Demande de prix et request for quotation : {e['fr']}", "",
          "## Demande de prix (français)", "",
          "[Dénomination], [adresse], [téléphone], [courriel]", "",
          f"Objet : demande de prix n°{DATE[:4]}-{e['code']} pour : {e['fr']}.", "",
          f"Nous vous prions de nous adresser votre meilleure offre pour la fourniture de : {e['fr']} ({e['ref']}), quantité : {e['qte']}.", "",
          "Spécifications minimales :", ""]
    fr += [f"- {s} ;" for s in e["spec_fr"][:-1]] + [f"- {e['spec_fr'][-1]}.", ""]
    fr += ["Votre offre précisera : prix départ usine (incoterm EXW ou FOB) et prix rendu Douala (CIF Douala) ; délai de livraison ; garantie ; "
           "service après-vente et pièces de rechange en Afrique centrale ; prix des consommables pour un an d'utilisation ; "
           "conditions de paiement ; validité de l'offre ; documents techniques.", "",
           "Date limite de réponse : [date]. Contact : [nom, téléphone, courriel].", "",
           "## Request for quotation (English)", "",
           "[Company name], [address], [phone], [email]", "",
           f"Subject: request for quotation No. {DATE[:4]}-{e['code']} for: {e['en']}.", "",
           f"Please send us your best offer for the supply of: {e['en']} ({e['ref']}), quantity: {e['qte']}.", "",
           "Minimum specifications:", ""]
    fr += [f"- {s};" for s in e["spec_en"][:-1]] + [f"- {e['spec_en'][-1]}.", ""]
    fr += ["Your offer shall state: ex-works or FOB price and CIF Douala price; delivery time; warranty; after-sales service and spare parts "
           "availability in Central Africa; price of consumables for one year of operation; payment terms; offer validity; technical documents.", "",
           "Deadline for reply: [date]. Contact: [name, phone, email].", ""]
    return "\n".join(fr) + "\n"


def demande_credit_bail():
    """Demande d'offre de credit-bail adressee aux etablissements de credit-bail et aux banques (decision D-11)."""
    eq = [e for e in EQUIPEMENTS if e["code"] in ("E1", "E5", "E7")]
    L = ["# Demande d'offre de crédit-bail d'équipements", "",
         "[Dénomination], société à responsabilité limitée en création, [adresse], [téléphone], [courriel]", "",
         "À l'attention de : [établissement de crédit-bail ou banque], [service crédit-bail], [adresse]", "",
         f"Objet : demande d'offre de crédit-bail n°{DATE[:4]}-CB pour l'équipement d'une société de gestion des huiles usagées et de purification du gasoil.", "",
         "Madame, Monsieur,", "",
         "Notre société, en création, propose aux exploitants forestiers et aux flottes un service annuel de gestion des huiles usagées et de purification du gasoil. "
         f"Son plan de financement prévoit un crédit-bail d'équipements d'une valeur d'environ {fcfa(val('H-92'))} HT, mis en place au passage à la deuxième étape de son développement. "
         "Nous vous prions de nous adresser une offre indicative pour les biens suivants :", "",
         "| Code | Équipement | Quantité | Référence indicative |", "|---|---|---:|---|"]
    L += [f"| {e['code']} | {e['fr']} | {e['qte']} | {e['ref']} |" for e in eq]
    L += ["", "Les spécifications détaillées figurent dans les cahiers des charges joints (document B1).", "",
          "Votre offre précisera :", "",
          "- les durées proposées (36 et 48 mois) et le montant des loyers mensuels ou trimestriels hors taxes ;",
          "- le premier loyer majoré ou l'apport initial demandé ;",
          "- la valeur résiduelle et les conditions de levée d'option ;",
          "- le taux de financement implicite et les frais de dossier ;",
          "- l'assurance exigée sur les biens et son coût, ou la possibilité de l'assurer auprès de notre assureur ;",
          "- les garanties demandées (caution des associés, dépôt de garantie, domiciliation des encaissements, garantie de portefeuille PME) ;",
          "- l'éligibilité d'un véhicule d'occasion et l'âge maximal accepté ;",
          "- les documents à fournir et le délai d'instruction ;",
          "- la durée de validité de l'offre.", "",
          "Nous joignons le business plan bancaire de la société. Nous restons à votre disposition pour une rencontre.", "",
          "Date limite de réponse : [date]. Contact : [nom, téléphone, courriel].", "",
          "Veuillez agréer, Madame, Monsieur, l'expression de nos salutations distinguées.", "",
          "[Nom du gérant], gérant", ""]
    return "\n".join(L) + "\n"


def demande_pret_garanti():
    """Demande de pret bancaire garanti, alternative au credit-bail (lot 18), avec differe de remboursement."""
    eq = [e for e in EQUIPEMENTS if e["code"] in ("E1", "E5", "E7")]
    L = ["# Demande de prêt d'équipement garanti", "",
         "[Dénomination], société à responsabilité limitée, [adresse], [téléphone], [courriel]", "",
         "À l'attention de : [banque], [direction des PME], [adresse]", "",
         f"Objet : demande de prêt à moyen terme n°{DATE[:4]}-PG pour l'équipement d'une société de gestion des huiles usagées et de purification du gasoil.", "",
         "Madame, Monsieur,", "",
         "Notre société propose aux exploitants forestiers et aux flottes un service annuel de gestion des huiles usagées et de purification du gasoil. "
         f"Pour son passage à la deuxième étape de son développement, nous sollicitons un prêt à moyen terme d'environ {fcfa(val('H-158'))}, "
         f"sur {int(val('H-160'))} mois, dont un différé de remboursement du capital de 12 mois, pour financer les biens suivants :", "",
         "| Code | Équipement | Quantité | Référence indicative |", "|---|---|---:|---|"]
    L += [f"| {e['code']} | {e['fr']} | {e['qte']} | {e['ref']} |" for e in eq]
    L += ["", "La demande sera présentée au franchissement de la porte de décision de l'étape 2 : au moins quatre contrats annuels signés et trois mois consécutifs d'excédent brut d'exploitation positif.", "",
          "Garanties proposées :", "",
          "- garantie de portefeuille PME mobilisable par votre établissement (dispositif de la CDEC et de l'African Guarantee Fund, ou ligne de garantie d'un bailleur dont vous bénéficiez) ;",
          "- nantissement des équipements financés ;",
          "- domiciliation des encaissements des contrats de conformité et cession des créances de ces contrats ;",
          "- blocage des comptes courants d'associés pendant la durée du prêt.", "",
          "Nous vous remercions de nous indiquer :", "",
          "- le taux d'intérêt, les frais de dossier et les commissions de garantie ;",
          "- la durée possible et la durée du différé de remboursement acceptée ;",
          "- l'apport personnel exigé et la quotité couverte par la garantie ;",
          "- les garanties complémentaires éventuelles, dont la caution des associés ;",
          "- l'éligibilité du projet à une ligne de crédit ou de garantie dédiée aux PME ou aux investissements verts ;",
          "- les documents à fournir et le délai d'instruction.", "",
          "Pièces jointes : business plan bancaire, dossier technique des équipements, devis des fournisseurs, statuts et extrait du registre du commerce, contrats signés.", "",
          "Date souhaitée de réponse : [date]. Contact : [nom, téléphone, courriel].", "",
          "Veuillez agréer, Madame, Monsieur, l'expression de nos salutations distinguées.", "",
          "[Nom du gérant], gérant", ""]
    return "\n".join(L) + "\n"


def _entete(ws, valeurs):
    ws.append(valeurs)
    for c in ws[1]:
        c.font = Font(name="Arial", bold=True, color="FFFFFF", size=9)
        c.fill = PatternFill("solid", fgColor="1F3864")


def grille_comparaison(chemin):
    wb = Workbook()
    ws = wb.active
    ws.title = "Comparaison"
    _entete(ws, ["Critère", "Poids", "Offre A : note (1 à 5)", "Offre B : note (1 à 5)", "Offre C : note (1 à 5)"])
    criteres = [("Prix rendu Douala", 0.30), ("Conformité aux spécifications", 0.25), ("Délai de livraison", 0.10),
                ("Service après-vente et pièces en Afrique centrale", 0.20), ("Coût des consommables sur un an", 0.10), ("Garantie", 0.05)]
    for c, p in criteres:
        ws.append([c, p, None, None, None])
    n = len(criteres) + 1
    ws.append(["Score pondéré", f"=SUM(B2:B{n})"] + [f"=SUMPRODUCT($B$2:$B${n},{col}2:{col}{n})" for col in "CDE"])
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5")
    ws.add_data_validation(dv)
    dv.add(f"C2:E{n}")
    ws.column_dimensions["A"].width = 48
    info = wb.create_sheet("Offres")
    _entete(info, ["Offre", "Fournisseur", "Équipement", "Prix départ (devise)", "Devise", "Cours FCFA", "Prix départ FCFA", "Fret et dédouanement FCFA", "Prix rendu Douala FCFA", "Délai (semaines)", "Garantie (mois)"])
    for i, o in enumerate("ABC", start=2):
        info.append([o, None, None, None, None, None, f"=D{i}*F{i}", None, f"=G{i}+H{i}", None, None])
    wb.save(chemin)


def tableau_de_bord(chemin):
    wb = Workbook()
    ws = wb.active
    ws.title = "Saisie mensuelle"
    _entete(ws, ["Mois", "Clients sous contrat", "Volume d'huiles déclaré par les clients (L)", "Volume enlevé (L)", "Lots refusés", "Lots contrôlés",
                 "Coût des enlèvements (FCFA)", "Chiffre d'affaires (FCFA)", "Charges totales (FCFA)", "Incidents avec déversement", "Quasi-accidents",
                 "Taux de récupération", "Coût par litre enlevé (FCFA/L)", "Marge (FCFA)", "Taux de lots refusés"])
    for i in range(2, 38):
        ws.append([f"Mois {i - 1}"] + [None] * 10 + [f'=IF(C{i}>0,D{i}/C{i},"")', f'=IF(D{i}>0,G{i}/D{i},"")', f"=H{i}-I{i}", f'=IF(F{i}>0,E{i}/F{i},"")'])
    ws.column_dimensions["A"].width = 12
    s = wb.create_sheet("Synthèse")
    _entete(s, ["Indicateur", "Valeur cumulée", "Cible", "Source de la cible"])
    s.append(["Volume enlevé (L)", "=SUM('Saisie mensuelle'!D2:D37)", 320000, "seuil de D-06, par an"])
    s.append(["Taux de récupération", "=IF(SUM('Saisie mensuelle'!C2:C37)>0,SUM('Saisie mensuelle'!D2:D37)/SUM('Saisie mensuelle'!C2:C37),\"\")", 0.9, "objectif de travail"])
    s.append(["Coût par litre enlevé (FCFA/L)", "=IF(SUM('Saisie mensuelle'!D2:D37)>0,SUM('Saisie mensuelle'!G2:G37)/SUM('Saisie mensuelle'!D2:D37),\"\")", 200, "ordre de grandeur du lot 6"])
    s.append(["Marge cumulée (FCFA)", "=SUM('Saisie mensuelle'!N2:N37)", None, "modèle financier, lot 9"])
    s.append(["Incidents avec déversement", "=SUM('Saisie mensuelle'!J2:J37)", 0, "critère du pilote"])
    s.append(["Taux de lots refusés", "=IF(SUM('Saisie mensuelle'!F2:F37)>0,SUM('Saisie mensuelle'!E2:E37)/SUM('Saisie mensuelle'!F2:F37),\"\")", 0.1, "déclencheur P10 du lot 13"])
    s.column_dimensions["A"].width = 36
    wb.save(chemin)


def construire(pdf=True):
    (SRC / "2_achats").mkdir(parents=True, exist_ok=True)
    (SRC / "6_commercial" / "K1 Grille tarifaire.md").write_text(grille_tarifaire()[0], encoding="utf-8")
    (KIT / "grille_tarifaire_tracabilite.md").write_text("# Traçabilité de la grille tarifaire\n\nFichier généré par `construire_kit.py`. Prix d'appel à valider pendant le pilote ; aucun prix de marché publié n'a été trouvé.\n\n" + grille_tarifaire_trace() + "\n", encoding="utf-8")
    (SRC / "2_achats" / "B1 Cahiers des charges des equipements.md").write_text(cahiers_des_charges(), encoding="utf-8")
    for e in EQUIPEMENTS:
        (SRC / "2_achats" / f"B2 Demande de prix {e['code']} {e['fr']}.md").write_text(rfq(e), encoding="utf-8")
    (SRC / "2_achats" / "B4 Demande d'offre de credit-bail.md").write_text(demande_credit_bail(), encoding="utf-8")
    (SRC / "2_achats" / "B5 Demande de pret garanti.md").write_text(demande_pret_garanti(), encoding="utf-8")
    sorties = KIT / "docx"
    pdfs = KIT / "pdf"
    sorties.mkdir(exist_ok=True)
    pdfs.mkdir(exist_ok=True)
    grille_comparaison(sorties / f"{PREFIXE} B3 Grille de comparaison des offres.xlsx")
    tableau_de_bord(sorties / f"{PREFIXE} T1 Tableau de bord des indicateurs.xlsx")
    from commun.deterministe import figer
    for x in sorties.glob("*.xlsx"):
        figer(x)
    sources = sorted(SRC.rglob("*.md")) + [RACINE / "11_juridique" / n for n in ("statuts_sarl.md", "pacte_associes.md", "charte_conflits_interets.md")] \
        + [RACINE / "04b_validation_terrain" / n for n in ("procedure_acceptation_lots.md", "lettre_acces_sanctions.md")]
    noms = {"statuts_sarl": "J1 Projet de statuts SARL", "pacte_associes": "J2 Projet de pacte d'associes",
            "charte_conflits_interets": "J3 Charte de prevention des conflits d'interets",
            "procedure_acceptation_lots": "P0 Procedure d'acceptation et de refus des lots",
            "lettre_acces_sanctions": "A4 Lettre de demande d'acces aux donnees de sanctions"}
    produits = []
    for md in sources:
        nom = noms.get(md.stem, md.stem)
        docx = sorties / f"{PREFIXE} {nom}.docx"
        docx_charte.convertir(md, docx, titre_court=nom[3:] if nom[2] == " " else nom, reference=f"{PREFIXE} {nom[:2]}")
        produits.append(docx)
    if pdf:
        for d in produits:
            docx_charte.vers_pdf(d, pdfs)
    return produits


if __name__ == "__main__":
    p = construire(pdf="--sans-pdf" not in sys.argv)
    print("Lot 15 :", len(p), "documents .docx (et .pdf)")
