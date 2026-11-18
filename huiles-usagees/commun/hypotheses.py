"""Registre unique des hypotheses [H-xx].

Toute valeur chiffree utilisee par un script du depot vient d'ici.
Le fichier 00_registres/hypotheses.md est genere a partir de ce module
par `python run_all.py` : ne pas l'editer a la main.

Statuts possibles : "supposé" (aucune donnee terrain), "probable" (indice
documentaire indirect), "vérifié" (source primaire lue).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Hypothese:
    id: str
    libelle: str
    bas: float
    central: float
    haut: float
    unite: str
    justification: str
    impact: str
    verification: str
    statut: str = "supposé"
    lot: str = "commun"


_H = [
    # Business plan initial (desk study du 17/11/2026, fourni par le promoteur [S-29])
    Hypothese("H-01", "Huiles usagees par client forestier", 10_000, 10_000, 10_000, "L/an",
              "valeur du business plan initial [S-29], sans mesure", "critique pour le modele foret",
              "pilote 4 bis n°1 et releve des achats de lubrifiants des clients", lot="BP initial"),
    Hypothese("H-02", "Huiles urbaines collectees en annee 5", 1_200_000, 1_200_000, 1_200_000, "L/an",
              "valeur du business plan initial [S-29], non verifiee", "critique : seuil de VAN nulle a 320 000 L/an",
              "enquete 30 garages et flottes (lot 4), pilote", lot="BP initial"),
    Hypothese("H-03", "Prix d'achat des huiles urbaines", 50, 50, 50, "FCFA/L",
              "valeur du business plan initial [S-29]", "critique : le circuit informel fixe ce prix",
              "enquete garages (lot 4)", lot="BP initial"),
    Hypothese("H-04", "Prix de vente du combustible", 400, 400, 400, "FCFA/L",
              "valeur du business plan initial [S-29] ; gasoil pompe 828 FCFA/L [S-09]",
              "critique : seuil de VAN nulle a 250 FCFA/L", "lettre d'intention apres essai de combustion (4 bis n°3)",
              lot="BP initial"),
    Hypothese("H-05", "Rendement en combustible", 0.80, 0.80, 0.80, "fraction",
              "valeur du business plan initial [S-29]", "fort", "bilan matiere sur 10 a 15 echantillons (4 bis n°2)",
              lot="BP initial"),

    # Lot 0 : economie des activites d'amorcage (fourchettes larges, a tester en prospection)
    Hypothese("H-20", "Lot 0, apporteur d'affaires : volume apporte sur 12 mois", 20_000, 50_000, 100_000, "L",
              "ordre de grandeur : 2 a 10 clients de taille H-01", "moyen",
              "accord de commission signe avec un collecteur agree", lot="00b"),
    Hypothese("H-21", "Lot 0, apporteur d'affaires : commission", 10, 20, 30, "FCFA/L",
              "aucune reference publiee ; base a negocier (Q-04)", "moyen",
              "proposition ecrite du collecteur", lot="00b"),
    Hypothese("H-22", "Lot 0, analyse d'huile : analyses vendues sur 12 mois", 60, 120, 240, "analyses",
              "5 clients x 4 engins suivis x 3 a 12 prelevements par an", "moyen",
              "bons de commande prepayes", lot="00b"),
    Hypothese("H-23", "Lot 0, analyse d'huile : marge nette par analyse", 10_000, 15_000, 25_000, "FCFA",
              "prix de vente moins cout laboratoire (inconnu, Q-05) et acheminement", "fort",
              "devis SGS Cameroun et d'un second laboratoire", lot="00b"),
    Hypothese("H-24", "Lot 0, kits antipollution : commandes sur 12 mois", 5, 10, 20, "commandes",
              "achats ponctuels de chantiers et d'ateliers", "moyen",
              "bons de commande avec acompte", lot="00b"),
    Hypothese("H-25", "Lot 0, kits antipollution : marge par commande", 50_000, 90_000, 150_000, "FCFA",
              "marge d'agent sur prix fournisseur (fournisseur a identifier, Q-06)", "moyen",
              "contrat d'agent ou de depot-vente", lot="00b"),
    Hypothese("H-26", "Lot 0, formation : sessions vendues sur 12 mois", 4, 8, 12, "sessions",
              "une session par client cible et par semestre", "fort",
              "conventions de formation signees et payees", lot="00b"),
    Hypothese("H-27", "Lot 0, formation : marge nette par session (1 jour, chez le client)", 400_000, 600_000, 1_000_000, "FCFA",
              "prix de session moins deplacement et supports ; aucun prix de marche publie trouve (Q-07)", "fort",
              "test de prix aupres des 5 premiers prospects", lot="00b"),
    Hypothese("H-28", "Lot 0, contenu en ligne : ventes sur 12 mois", 10, 25, 50, "ventes",
              "audience de la plateforme du promoteur non mesuree", "faible",
              "statistiques de la plateforme", lot="00b"),
    Hypothese("H-29", "Lot 0, contenu en ligne : revenu net par vente", 15_000, 20_000, 30_000, "FCFA",
              "prix d'un module court", "faible", "test de prix", lot="00b"),
    Hypothese("H-33", "Lot 0, formation : prix d'appel d'une session d'1 jour, jusqu'a 15 participants, hors frais de mission", 600_000, 800_000, 1_200_000, "FCFA HT",
              "prix a tester ; aucun prix de marche publie trouve (Q-07)", "fort",
              "reaction des 5 premiers prospects", lot="00b"),
    Hypothese("H-34", "Lot 0, analyse d'huile : majoration appliquee au cout laboratoire", 10_000, 15_000, 25_000, "FCFA/analyse",
              "egale a la marge nette visee H-23 ; prix client = cout laboratoire + majoration + acheminement", "fort",
              "devis laboratoire (Q-05)", lot="00b"),
    # Lot 2 : delais reels des autorisations (jours calendaires)
    Hypothese("H-70", "Delai reel de creation de la societe au CFCE", 3, 7, 30, "jours",
              "aucun bareme consulte (Q-08)", "faible", "depot au CFCE", lot="02"),
    Hypothese("H-71", "Delai reel de l'evaluation environnementale (NIE ou EIES sommaire, TDR compris)", 90, 180, 365, "jours",
              "categorie a confirmer selon l'arrete n°00001/MINEPDED du 8 fevrier 2016 [S-34] (Q-23)", "fort",
              "echange avec le MINEPDED et un bureau d'etudes agree autre que HIKMA", lot="02"),
    Hypothese("H-72", "Delai reel du permis environnemental dechets apres depot complet", 60, 120, 240, "jours",
              "60 jours d'instruction selon le cahier des charges [S-29], texte non lu (Q-01)", "fort",
              "texte officiel et retour d'operateurs titulaires", lot="02"),
    Hypothese("H-73", "Delai reel de l'autorisation d'etablissement classe (enquete publique comprise)", 90, 180, 365, "jours",
              "premiere classe soumise a enquete publique [S-35] ; classe de l'installation inconnue (Q-22)", "fort",
              "MINMIDT, delegation regionale", lot="02"),
    Hypothese("H-74", "Delai reel de l'autorisation de transport de marchandises dangereuses", 30, 60, 90, "jours",
              "cout publie 100 000 ou 200 000 FCFA selon la source [S-37] ; delai non publie", "moyen", "MINT", lot="02"),

    # Lot 4 : gisement
    Hypothese("H-60", "Masse volumique de l'huile usagee", 0.88, 0.90, 0.92, "kg/L",
              "ordre de grandeur des huiles moteur ; a mesurer (ASTM D4052) dans le protocole 4 bis n°2", "faible",
              "resultats de laboratoire", lot="04"),
    Hypothese("H-61", "Huile usagee recuperable par vehicule routier et par an", 6, 10, 15, "L/vehicule/an",
              "2 a 3 vidanges de 3 a 5 L, pertes deduites ; parc vieillissant [S-44]", "fort",
              "enquete 30 garages et flottes", lot="04"),
    Hypothese("H-62", "Huile usagee recuperable par engin lourd et par an", 200, 400, 800, "L/engin/an",
              "vidanges moteur, transmission et hydraulique ; aucune donnee publiee", "fort",
              "pilote 4 bis n°1, carnets d'entretien", lot="04"),
    Hypothese("H-63", "Evolution du parc routier entre 2014 et 2026", 1.0, 1.3, 1.6, "facteur",
              "derniere estimation trouvee : 675 000 vehicules en 2014 [S-43]", "moyen",
              "INS, MINT", lot="04"),
    Hypothese("H-64", "Nombre d'etablissements forestiers clients adressables (titulaires de concessions et UTB, doublons retires)", 70, 150, 300, "clients",
              "environ 70 titulaires de concessions [S-46] et 251 UTB [S-45], avec recoupements", "fort",
              "liste MINFOF des titres et des UTB", lot="04"),
    Hypothese("H-65", "Part du gisement urbain situee a Douala et Yaounde", 0.40, 0.50, 0.60, "fraction",
              "concentration du parc et des industries dans les deux villes, non mesuree", "moyen",
              "immatriculations par region (INS)", lot="04"),
    Hypothese("H-66", "Masse volumique moyenne des carburants et lubrifiants importes (conversion du prix a la tonne)", 0.80, 0.85, 0.95, "kg/L",
              "melange de produits (essence, gasoil, fioul, lubrifiants) dont la repartition est inconnue", "faible",
              "statistiques INS par produit", lot="04"),
    # Lot 8 : comparaison des modeles d'entreprise (valeurs annuelles, HT)
    Hypothese("H-80", "Prix annuel du contrat de conformite par client forestier (futs, kits, registre, formation, 4 enlevements, rapport PGES)", 4_000_000, 6_000_000, 9_000_000, "FCFA/an",
              "doit couvrir 4 enlevements sous-traites (H-48) et les fournitures ; consentement a payer non mesure", "critique",
              "pilote 4 bis n°1, releve des sanctions 4 bis n°4", lot="08"),
    Hypothese("H-81", "Prix d'une intervention de purification du gasoil et nettoyage de cuve", 150_000, 250_000, 400_000, "FCFA/intervention",
              "aucun prix de marche trouve", "fort", "pilote 4 bis n°1", lot="08"),
    Hypothese("H-82", "Interventions de purification du gasoil par client forestier et par an", 4, 6, 12, "interventions/an",
              "une intervention par livraison importante ou par trimestre a mensuelle", "moyen", "pilote", lot="08"),
    Hypothese("H-83", "Valeur nette des huiles remises a un valorisateur titulaire (negatif : la societe paie)", -50, 0, 50, "FCFA/L",
              "aucun valorisateur en activite confirme (Q-11) ; cas central : remise gratuite", "fort",
              "offre ecrite d'un valorisateur", lot="08"),
    Hypothese("H-84", "Supplement de valeur des huiles pretraitees (decantees et deshydratees) remises au valorisateur", 20, 50, 100, "FCFA/L",
              "huile seche et sans sediments plus facile a valoriser ; aucun prix publie", "fort", "offre ecrite", lot="08"),
    Hypothese("H-85", "Cout de collecte urbaine par litre (camion, chauffeur, carburant, futs), hors achat des huiles", 20, 40, 60, "FCFA/L",
              "a remplacer par le modele de tournees du lot 6", "fort", "lot 6", lot="08"),
    Hypothese("H-86", "Part de marge reversee par un partenaire collecteur ou valorisateur (modele 4), en fraction du contrat de conformite", 0.15, 0.25, 0.35, "fraction",
              "repartition a negocier : la societe vend et gere la relation, le partenaire collecte", "fort", "accord de partenariat", lot="08"),
    Hypothese("H-87", "Cout des consommables par intervention de purification (cartouches, filtres, absorbants)", 30_000, 60_000, 100_000, "FCFA/intervention",
              "disponibilite et prix des cartouches Parker inconnus (Q-16)", "moyen", "devis", lot="08"),
    Hypothese("H-88", "Enlevements d'huiles par client forestier et par an", 3, 4, 6, "enlevements/an",
              "trimestriel ; plus frequent pour les UTB proches", "moyen", "pilote", lot="08"),
    Hypothese("H-89", "Charges fixes annuelles d'une structure legere (promoteur, technicien, commercial a mi-temps, bureau, assurances)", 25_000_000, 40_000_000, 60_000_000, "FCFA/an",
              "a remplacer par les salaires sources du lot 10", "fort", "lot 10", lot="08"),
    Hypothese("H-90", "Charges fixes supplementaires d'un centre de transit et de pretraitement (operateurs, laboratoire, site, permis)", 20_000_000, 30_000_000, 45_000_000, "FCFA/an",
              "a remplacer par le lot 5", "fort", "lot 5", lot="08"),
    Hypothese("H-91", "Charges fixes supplementaires d'une unite de traitement propre", 50_000_000, 70_000_000, 100_000_000, "FCFA/an",
              "structure du premier business plan, non detaillee [S-29]", "fort", "lot 5", lot="08"),
    Hypothese("H-92", "Investissement du modele 1 (purificateur, materiel d'echantillonnage, vehicule leger d'occasion, stock de futs et kits)", 10_000_000, 15_000_000, 25_000_000, "FCFA",
              "prix des equipements non consultes (Q-16)", "moyen", "devis du lot 5", lot="08"),
    Hypothese("H-93", "Investissement du modele 5 (purificateur en location ou credit-bail, vehicule loue)", 2_000_000, 4_000_000, 7_000_000, "FCFA",
              "depots de garantie et premiers loyers ; loyers comptes en charges fixes (H-94)", "moyen", "offres de credit-bail", lot="08"),
    Hypothese("H-94", "Loyers annuels de credit-bail et location du modele 5", 4_000_000, 6_000_000, 9_000_000, "FCFA/an",
              "aucune offre consultee", "moyen", "offres de credit-bail", lot="08"),
    Hypothese("H-95", "Investissement du modele 2 (centre de transit, cuves, decanteur, deshydrateur, laboratoire de base, permis)", 30_000_000, 45_000_000, 70_000_000, "FCFA",
              "a remplacer par le lot 5", "fort", "lot 5", lot="08"),
    Hypothese("H-96", "Volume urbain collecte, annee 5, modeles avec permis (2 et 3)", 300_000, 500_000, 800_000, "L/an",
              "plafonne a moins de 20 % du gisement routier de Douala et Yaounde en cas central (gisement.md)", "critique",
              "enquete garages, lot 6", lot="08"),
    Hypothese("H-97", "Clients forestiers sous contrat en annee 5", 8, 15, 25, "clients",
              "progression lineaire depuis 2 clients en annee 1 ; 10 % des clients adressables H-64 en cas central", "critique",
              "pilote et prospection", lot="08"),
    Hypothese("H-98", "Taux d'actualisation", 0.15, 0.15, 0.15, "fraction",
              "taux du premier business plan [S-29]", "moyen", "cout du capital du lot 9", lot="08"),
    Hypothese("H-99", "Taux d'impot sur les societes applique au benefice (minimum de perception de 2,2 % du CA en sus)", 0.25, 0.25, 0.30, "fraction",
              "25 % pour les PME selon le cahier des charges [S-29], centimes additionnels non integres (Q-31)", "moyen", "DGI, lot 9", lot="08"),
    Hypothese("H-30", "Lot 0 : frais de creation d'une structure juridique pour facturer", 50_000, 100_000, 200_000, "FCFA",
              "montant a confirmer au CFCE (Q-08)", "moyen", "bareme du CFCE", lot="00b"),
    Hypothese("H-31", "Lot 0 : supports commerciaux (impression, cartes, plaquette)", 50_000, 75_000, 100_000, "FCFA",
              "devis d'imprimerie a Yaounde a obtenir", "faible", "deux devis", lot="00b"),
    Hypothese("H-32", "Lot 0 : deplacements de prospection avant premier encaissement", 100_000, 150_000, 200_000, "FCFA",
              "4 a 8 deplacements Yaounde-Douala ou vers les UTB", "moyen", "releve des depenses", lot="00b"),

    # Lot 4 bis : budgets des protocoles de terrain (devis a obtenir)
    Hypothese("H-40", "Kit Dexsil Clor-D-Tect 1000, prix unitaire hors port", 22, 22, 30, "USD",
              "prix catalogue Hazmat Resource [S-14] ; commande minimale 10 kits [S-15]", "faible",
              "devis rendu Douala", statut="probable", lot="04b"),
    Hypothese("H-41", "Cours du dollar retenu pour les budgets", 560, 600, 650, "FCFA/USD",
              "fourchette de travail ; le cours du jour doit etre releve et source a chaque devis (Q-13)", "faible",
              "cours BEAC du jour de la commande", lot="04b"),
    Hypothese("H-42", "Fret et dedouanement des petits consommables importes", 0.30, 0.40, 0.60, "fraction du prix",
              "coefficient de travail, aucun bareme consulte", "moyen", "devis transitaire", lot="04b"),
    Hypothese("H-43", "Analyse complete en laboratoire externe (PCB, metaux, chlore, soufre, eau)", 150_000, 250_000, 400_000, "FCFA/echantillon",
              "aucun tarif publie trouve (Q-05)", "fort", "trois devis de laboratoires", lot="04b"),
    Hypothese("H-44", "Envoi international d'un echantillon (emballage et transport de marchandise dangereuse)", 50_000, 100_000, 200_000, "FCFA/envoi",
              "a confirmer aupres d'un transitaire agree pour les matieres dangereuses (Q-14)", "moyen",
              "devis transitaire", lot="04b"),
    Hypothese("H-45", "Materiel de prelevement (echantillonneur, flacons, glaciere, etiquettes)", 150_000, 250_000, 400_000, "FCFA",
              "Koehler K27400 et consommables, prix rendu Douala inconnu", "faible", "devis", lot="04b"),
    Hypothese("H-46", "Location d'un analyseur de gaz de combustion pour 1 semaine, ou prestataire", 500_000, 900_000, 1_500_000, "FCFA",
              "location Testo signalee par le promoteur, aucun loueur en Afrique centrale identifie (Q-15)", "moyen",
              "devis loueur ou prestataire", lot="04b"),
    Hypothese("H-47", "Pilote : location ou mise a disposition d'une unite de purification du gasoil (3 mois)", 600_000, 1_200_000, 2_500_000, "FCFA",
              "prix d'achat et de location du Parker DFC14WS25VVX1 non consultes (Q-16)", "fort",
              "devis distributeur Parker ou loueur", lot="04b"),
    Hypothese("H-48", "Pilote : cout d'une tournee d'enlevement sous-traitee a un collecteur agree", 300_000, 500_000, 900_000, "FCFA/tournee",
              "aucun tarif publie ; depend de la distance et de l'etat des pistes", "fort",
              "devis Bocom International, SECA ou autre collecteur agree", lot="04b"),
    Hypothese("H-49", "Pilote : nombre de tournees d'enlevement en 3 mois (2 clients)", 2, 3, 4, "tournees",
              "un enlevement par client et par trimestre, plus un enlevement d'urgence", "moyen",
              "planning du pilote", lot="04b"),
    Hypothese("H-50", "Pilote : frais de mission du promoteur et d'un technicien (3 mois)", 600_000, 900_000, 1_500_000, "FCFA",
              "6 a 10 sejours de 2 a 3 jours sur chantier", "moyen", "releve reel", lot="04b"),
    Hypothese("H-51", "Releve des sanctions : frais de deplacement et de reproduction", 50_000, 100_000, 150_000, "FCFA",
              "visites aux services des clients", "faible", "releve reel", lot="04b"),
    Hypothese("H-52", "Essai de combustion : fabrication d'un lot de 200 L par un partenaire autorise", 100_000, 200_000, 400_000, "FCFA",
              "a negocier ; la fabrication par la societe sans permis est exclue (Q-17)", "fort",
              "accord ecrit du partenaire", lot="04b"),
]

HYPOTHESES = {h.id: h for h in _H}


def val(hid: str, cas: str = "central") -> float:
    """Valeur d'une hypothese : cas = 'bas', 'central' ou 'haut'."""
    h = HYPOTHESES[hid]
    return {"bas": h.bas, "central": h.central, "haut": h.haut}[cas]
