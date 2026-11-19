"""Lot 17 (complement) : deux business plans generes depuis les modeles du depot.

1. Document de projet institutionnel (trame des documents de projet presentes aux administrations camerounaises).
2. Business plan bancaire (structure de financement demandee : fonds propres et credit-bail, decision D-11).

Tous les chiffres sont lus dans les modeles ; aucun n'est saisi a la main.
Sorties : 17_synthese/bp_institutionnel.md, 17_synthese/bp_banque.md et leurs versions .docx et .pdf dans livrables/.
"""
from pathlib import Path
import importlib.util
import subprocess
import sys

import numpy as np

RACINE = Path(__file__).resolve().parents[1]
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(RACINE / "09_finance"))
sys.path.insert(0, str(ICI))
from commun.format import m_fcfa, nombre, pct  # noqa: E402
from commun.hypotheses import HYPOTHESES, val  # noqa: E402
from commun import docx_charte  # noqa: E402
import modele_mensuel as mm  # noqa: E402
import construire_synthese as cs  # noqa: E402

DATE, DATE_TXT = cs.DATE, cs.DATE_TXT
PREF = f"{DATE} Huiles usagees"


def _module(rel, nom):
    spec = importlib.util.spec_from_file_location(nom, RACINE / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def structure_demandee():
    """Structure de financement demandee (D-11) : fonds propres et quasi-fonds propres au niveau haut de H-157,
    equipements en credit-bail sur toute la periode, aucun emprunt."""
    p = mm.parametres()
    p["credit_bail"] = True
    p["H-157"] = HYPOTHESES["H-157"].haut
    return p


def annuel(s):
    a = {}
    for k in ("ca", "ca_contrat", "ca_gasoil", "ca_commission_urbaine", "ca_amorcage", "ca_huiles", "charges", "ebitda", "amortissement",
              "interets", "impot", "resultat_net", "capex", "flux_disponible", "loyers", "salaires", "enlevements"):
        a[k] = [float(s[k][12 * i: 12 * i + 12].sum()) for i in range(5)]
    for k in ("tresorerie", "creances", "immobilisations_nettes", "capital_restant", "dettes_fournisseurs", "clients"):
        a[k + "_fin"] = [float(s[k][12 * i + 11]) for i in range(5)]
    a["capitaux_propres_fin"] = [float(np.cumsum(s["apport"])[12 * i + 11] + np.cumsum(s["resultat_net"])[12 * i + 11]) for i in range(5)]
    a["volume_huiles_l"] = [float(sum(s["clients"][12 * i + j] for j in range(12)) * val("H-01") / 12) for i in range(5)]
    a["interventions"] = [float(sum(s["clients"][12 * i + j] for j in range(12)) * val("H-82") / 12) for i in range(5)]
    return a


def donnees():
    c = cs.chiffres()
    p = structure_demandee()
    s, ind = mm.simuler(p)
    c["sd"] = dict(s=s, ind=ind, a=annuel(s), p=p, ecart_bilan=float(np.abs(mm.bilan_equilibre(s)).max()))
    sb, ib = mm.simuler(mm.parametres())
    c["base"] = dict(ind=ib, a=annuel(sb))
    c["tornado"] = mm.tornado(fabrique=structure_demandee)
    c["mc"] = mm.monte_carlo(fabrique=structure_demandee)
    reg = _module("13_risques/registre_risques.py", "reg")
    c["risques"] = sorted(reg.RISQUES, key=lambda r: -r[4] * r[5])
    c["cal"] = c["fins"]
    return c


def _ligne(lib, vals, f=lambda x: m_fcfa(x, 1)):
    return f"| {lib} | " + " | ".join(f(v) for v in vals) + " |"


ENTETE5 = "| M FCFA | Année 1 | Année 2 | Année 3 | Année 4 | Année 5 |\n|---|---:|---:|---:|---:|---:|"


def bp_institutionnel(c):
    a, ind = c["sd"]["a"], c["sd"]["ind"]
    vol5 = round(a["volume_huiles_l"][4], -3)
    L = ["# Document de projet : société de gestion des huiles usagées et de purification du gasoil", "",
         "## Fiche signalétique du projet", "",
         "| Rubrique | Contenu |", "|---|---|",
         "| Désignation | [Dénomination de la société] |",
         "| Forme juridique | société à responsabilité limitée au capital de 1 000 000 FCFA (en création) |",
         "| Promoteur | [Nom du promoteur], ingénieur mines et pétrole, spécialiste HSE et EIES, certifié NEBOSH IGC |",
         "| Siège social | [Ville, adresse] |",
         "| Zone d'intervention | régions de l'Est, du Centre et du Sud (chantiers forestiers et UTB) ; Douala et Yaoundé (garages, flottes, industries) |",
         "| Activités | gestion des huiles usagées pour le compte des producteurs (fûts, kits, registres, enlèvements tracés, rapport annuel) ; purification du gasoil et nettoyage de cuves ; formation ; à terme, collecte et prétraitement sous permis |",
         "| Clientèle principale | exploitants forestiers, unités de transformation du bois, flottes d'engins et de camions, industries |",
         "| Échéancier | mois 1 à 3 : création, activités d'amorçage, démarches administratives ; mois 4 à 6 : pilote chez deux clients ; année 2 : équipement en crédit-bail ; année 3 : permis environnemental propre |",
         f"| Objectifs opérationnels à 5 ans | {nombre(a['clients_fin'][4], 0)} clients forestiers sous contrat ; environ {nombre(vol5)} litres d'huiles usagées tracées par an ; environ {nombre(a['interventions'][4], 0)} interventions de purification du gasoil par an |",
         "| Objectifs stratégiques | mettre en conformité les producteurs d'huiles usagées ; supprimer les rejets et brûlages sauvages ; créer une filière tracée de la forêt à l'installation de valorisation |",
         f"| Besoin de financement | {m_fcfa(ind['besoin_financement'], 1)} M FCFA au maximum (flux cumulés), couvert par environ {m_fcfa(c['sd']['p']['H-157'], 1)} M FCFA de fonds propres et quasi-fonds propres ; équipements en crédit-bail (valeur d'environ {m_fcfa(val('H-92'), 1)} M FCFA) |",
         f"| Indicateurs (structure de financement retenue) | VAN à 5 ans : {m_fcfa(ind['van'], 1)} M FCFA ; TRI : {pct(ind['tri'], 1)} ; point mort d'exploitation : mois {ind['point_mort_mois']} |",
         "| Parties prenantes clés | MINEPDED, MINMIDT, MINFOF, MINT, MINEFOP, communes d'intervention, Bourse nationale des déchets, collecteurs titulaires d'un permis, exploitants forestiers |", "",
         "## Résumé du projet", "",
         "Le projet crée une société de services qui prend en charge, pour le compte des exploitants forestiers, des unités de transformation du bois et des flottes, "
         "la gestion des huiles usagées de leurs engins et la qualité de leur gasoil. Les huiles usagées sont des déchets dangereux dont la collecte, le transport, le stockage "
         "et la valorisation sont soumis à permis [S-02]. Les chantiers forestiers, éloignés des collecteurs installés à Douala [S-06][S-07], en sont les producteurs les moins bien desservis.", "",
         "La société démarre sans investissement lourd : matériel loué, enlèvements confiés à un collecteur titulaire, contrats annuels de conformité. Elle s'équipe ensuite par étapes, "
         "et ne demande son propre permis qu'au-delà d'un volume collecté suffisant. La fabrication de combustible n'est envisagée qu'après une position écrite de l'administration "
         "sur le statut du produit et l'engagement d'un acheteur.", "",
         f"À cinq ans, le projet vise {nombre(a['clients_fin'][4], 0)} clients forestiers sous contrat et environ {nombre(vol5)} litres d'huiles usagées tracées par an. "
         f"Son chiffre d'affaires atteint {m_fcfa(a['ca'][4], 1)} M FCFA en année 5 pour un résultat net de {m_fcfa(a['resultat_net'][4], 1)} M FCFA (structure de financement retenue). "
         "Le modèle financier rémunère trois postes (gérant, technicien, commercial à mi-temps) ; l'organigramme cible d'environ sept personnes suppose le permis propre et n'est pas chiffré ici (`10_organisation/lot10_organisation.md`).", "",
         "## Introduction", "",
         "### Contexte", "",
         "La Stratégie nationale de développement 2020-2030 (SND30) fait de la transformation structurelle de l'économie et de l'industrialisation un axe central [S-91]. "
         "La gestion des déchets dangereux relève de la loi n°96/12 du 5 août 1996 portant loi-cadre relative à la gestion de l'environnement [S-24] et du décret n°2012/2809/PM du 26 septembre 2012 "
         "sur le tri, la collecte, le transport, la récupération, le recyclage, le traitement et l'élimination des déchets [S-31]. L'État a créé en 2025 une Bourse nationale des déchets "
         "pour mettre en relation les producteurs de déchets et les structures de valorisation [S-10][S-11].", "",
         "### Problématique", "",
         "Les exploitants forestiers produisent des huiles usagées sur des chantiers isolés, loin des opérateurs de collecte, concentrés à Douala. "
         "Faute de filière tracée, les huiles sont stockées dans de mauvaises conditions, cédées au circuit informel ou brûlées ; un usage combustible informel existe [S-61]. "
         "Les entreprises concernées s'exposent à des sanctions et à des difficultés lors des audits de certification forestière [S-29].", "",
         "### Justification", "",
         "- alignement sur la réglementation des déchets dangereux et sur la SND30 ;",
         "- réponse à un besoin non couvert : aucun collecteur identifié n'intervient en forêt ;",
         "- démarrage à faible capital, porté par un promoteur qualifié en HSE et en évaluation environnementale ;",
         "- création d'emplois qualifiés et formation des mécaniciens des clients ;",
         "- traçabilité complète des huiles, utile aux contrôles de l'administration.", "",
         "### Objectifs", "",
         "**Objectif global :** créer une filière tracée de gestion des huiles usagées des chantiers forestiers et des ateliers, de la production à la valorisation.", "",
         "**Objectifs spécifiques :**", "",
         f"- équiper et former les sites de {nombre(a['clients_fin'][4], 0)} clients forestiers en 5 ans ;",
         f"- tracer environ {nombre(vol5)} litres d'huiles usagées par an en année 5 ;",
         "- remettre 100 % des huiles collectées à des installations titulaires d'un permis ;",
         "- fournir à chaque client un rapport annuel d'activité utilisable pour son plan de gestion environnementale et sociale ;",
         "- obtenir le permis environnemental de la société dès que la collecte atteint 320 000 L/an.", "",
         "## Généralités sur le projet", "",
         "### Genèse", "",
         "Le projet est né du constat, fait par le promoteur dans ses missions d'accompagnement environnemental, que les exploitants forestiers sont sanctionnés pour leur gestion des huiles usagées [S-29]. "
         "Une étude de faisabilité complète a été conduite en novembre 2026 : réglementation, comparaison de quinze filières étrangères, marché, technique, logistique, HSE, finance et juridique.", "",
         "### Promoteur", "",
         "Le promoteur est ingénieur en mines et pétrole, titulaire d'une licence de chimie organique, certifié NEBOSH IGC, spécialiste HSE et des études d'impact environnemental et social. "
         "Il maîtrise les outils de simulation de procédés et d'analyse de données. La société est indépendante du bureau d'études qui l'emploie : une charte écrite de prévention des conflits d'intérêts "
         "organise cette séparation.", "",
         "## Étude de marché", "",
         "### Services proposés", "",
         "- contrat annuel de conformité par site : fûts identifiés, kit antipollution, registre, formation, enlèvements tracés, dépistage des halogènes, rapport annuel ;",
         "- purification du gasoil et nettoyage de cuve ;",
         "- dossier de preuves pour les audits de certification forestière ;",
         "- formation des mécaniciens et chefs d'atelier ; analyse d'huile en service.", "",
         "### Demande", "",
         f"Le segment forestier est estimé à environ {m_fcfa(c['gis']['central']['foret'], 1)} M L/an d'huiles usagées, réparties entre quelque 70 titulaires de concessions [S-46] et 251 unités de transformation du bois [S-45]. "
         f"L'ensemble du parc national de véhicules et d'engins produirait environ {m_fcfa(c['gis']['central']['parc_total'], 1)} M L/an (estimation par le parc, `04_marche/gisement.md`).", "",
         "### Concurrence", "",
         "Bocom International et SECA collectent et transportent des déchets dangereux à Douala [S-06][S-07][S-08] ; aucune activité en forêt n'est documentée. "
         "Une unité de valorisation de déchets pétroliers a été acquise par Valtech Energy pour le port de Kribi [S-03][S-04] ; son démarrage n'est pas confirmé [S-60]. "
         "Ces acteurs sont des partenaires possibles autant que des concurrents.", "",
         "### Prix", "",
         f"Le contrat annuel de conformité est proposé à {m_fcfa(val('H-80'), 1)} M FCFA HT par site, prix d'appel à valider pendant le pilote. "
         f"La purification du gasoil est facturée {nombre(val('H-81'))} FCFA HT par intervention hors forfait.", "",
         "### Stratégie commerciale", "",
         "Prospection directe des 50 premières cibles, pilote payant chez deux clients forestiers, contrats de deux ans facturés trimestriellement d'avance, "
         "partenariat avec un collecteur titulaire pour la clientèle urbaine.", "",
         "## Localisation", "",
         "### Zone d'intervention", "",
         "Les clients forestiers sont répartis dans l'Est (Bertoua, Batouri, Abong-Mbang, Yokadouma), le Centre et le Sud. Les huiles sont acheminées vers Douala, "
         "où se trouvent les collecteurs et éliminateurs identifiés [S-06][S-07].", "",
         "### Base opérationnelle", "",
         "La société est basée à [ville]. Un centre de transit sous permis sera implanté à l'étape 3, sur un site choisi après évaluation environnementale.", "",
         "## Impacts économiques, sociaux et environnementaux", "",
         "### Impacts économiques", "",
         f"- chiffre d'affaires de {m_fcfa(a['ca'][4], 1)} M FCFA en année 5 ;",
         f"- impôts et taxes versés sur 5 ans : {m_fcfa(sum(a['impot']), 1)} M FCFA d'impôt sur les sociétés et minimum de perception ;",
         "- sous-traitance confiée à des collecteurs et transporteurs camerounais titulaires d'un permis.", "",
         "### Impacts sociaux", "",
         "- trois emplois directs qualifiés dans le scénario chiffré, environ sept si le permis propre est obtenu ;",
         "- formation des mécaniciens et chefs d'atelier des clients ;",
         "- réduction de l'exposition des travailleurs et des riverains aux huiles usagées.", "",
         "### Impacts environnementaux", "",
         f"- environ {nombre(vol5)} litres d'huiles usagées par an soustraits aux rejets et brûlages non contrôlés en année 5 ;",
         "- refus et élimination séparée des lots contaminés par des PCB ou des solvants chlorés ;",
         "- prévention des déversements sur les chantiers (fûts sur rétention, kits, procédures).", "",
         "| Impact négatif potentiel | Mesure |", "|---|---|",
         "| déversement lors du transport | sous-traitance à un collecteur titulaire, procédures écrites, suivi GPS, assurance |",
         "| accident lors du nettoyage de cuve | nettoyage depuis l'extérieur, entrée en cuve interdite sans permis de travail |",
         "| pollution d'un futur centre de transit | évaluation environnementale par un bureau indépendant, dalle étanche, rétention |", "",
         "## Étude technique", "",
         "### Organisation des opérations", "",
         f"Le solveur de tournées regroupe les sites forestiers en tournées d'environ une semaine ; collecter en forêt coûte de l'ordre de {nombre(c['cout_l_min'])} à {nombre(c['cout_l_max'])} FCFA par litre, "
         "selon l'option de flotte (`06_logistique/tournees.md`). La sous-traitance à un collecteur titulaire est retenue jusqu'à l'obtention du permis propre.", "",
         "### Équipements", "",
         "- purificateur de gasoil de 60 L/min ; matériel de prélèvement ; kits de dépistage des halogènes ; véhicule léger 4x4 (en location puis en crédit-bail) ;",
         "- à l'étape 3 : camion-citerne d'occasion et centre de transit ;",
         "- à l'étape 4 seulement : décanteur et purificateur d'huile sous vide.", "",
         "### Sécurité et environnement", "",
         "Huit procédures écrites encadrent la réception, l'analyse, le transport, l'intervention en cas de déversement, le nettoyage de cuve et la purification du gasoil. "
         "Une application de traçabilité, utilisable sans réseau, enregistre chaque fût, chaque enlèvement et chaque bordereau.", "",
         "### Ressources humaines", "",
         "Gérant, technicien de terrain, commercial ; puis, à l'étape 3, responsable d'exploitation et HSE, chauffeur-opérateur et assistant administratif.", "",
         "## Analyse financière", "",
         "### Coût et financement", "",
         f"Le besoin de financement maximal de la structure retenue est de {m_fcfa(ind['besoin_financement'], 1)} M FCFA. Il est couvert par environ {m_fcfa(c['sd']['p']['H-157'], 1)} M FCFA "
         "de fonds propres et de comptes courants d'associés bloqués ; les équipements sont pris en crédit-bail.", "",
         "### Comptes prévisionnels", "", ENTETE5,
         _ligne("Chiffre d'affaires", a["ca"]), _ligne("Excédent brut d'exploitation", a["ebitda"]), _ligne("Résultat net", a["resultat_net"]),
         _ligne("Trésorerie de fin d'année", a["tresorerie_fin"]), "",
         "### Rentabilité", "",
         f"VAN à 5 ans : {m_fcfa(ind['van'], 1)} M FCFA ; TRI : {pct(ind['tri'], 1)} ; point mort d'exploitation au mois {ind['point_mort_mois']}. "
         f"Le point mort est atteint avec environ {nombre(c['pm5'], 0)} clients forestiers sous contrat.", "",
         "## Cadre réglementaire et institutionnel", "",
         "### Textes applicables", "",
         "La loi n°96/12 du 5 août 1996 fixe le cadre de la gestion de l'environnement [S-24]. Le décret n°2012/2809/PM du 26 septembre 2012 encadre la gestion des déchets [S-31]. "
         "L'arrêté n°001/MINEPDED du 15 octobre 2012 fixe les conditions du permis environnemental en matière de gestion des déchets [S-02]. "
         "Le décret n°2013/0171/PM du 14 février 2013 encadre les évaluations environnementales [S-33]. La loi n°98/015 du 14 juillet 1998 régit les établissements classés [S-35].", "",
         "### Institutions", "",
         "Le MINEPDED délivre le permis et approuve l'évaluation environnementale ; le ministère chargé des établissements classés instruit l'autorisation du futur centre de transit [S-35] ; "
         "le MINT autorise le transport de marchandises dangereuses [S-37] ; le MINFOF contrôle les exploitants forestiers.", "",
         "## Mise en œuvre", "",
         "| Période | Étape | Résultat attendu |", "|---|---|---|",
         "| mois 1 à 3 | création, amorçage, démarches écrites | 2 clients pilotes engagés |",
         "| mois 4 à 6 | pilote chez 2 clients forestiers | premier contrat annuel signé |",
         "| mois 7 à 18 | développement du portefeuille | au moins 4 contrats annuels |",
         "| mois 19 à 30 | équipement en crédit-bail | au moins 9 clients |",
         f"| mois 31 à 36 | évaluation environnementale et permis propre | permis obtenu ; délai réglementaire estimé de {nombre(c['cal']['bas'] / 30.4, 0)} à {nombre(c['cal']['haut'] / 30.4, 0)} mois |", "",
         "## Appui attendu des pouvoirs publics", "",
         "- une position écrite du MINEPDED sur le régime d'un prestataire de conformité qui ne détient pas de déchets, et sur le statut d'une huile usagée traitée ;",
         "- la catégorie d'évaluation environnementale applicable au futur centre de transit ;",
         "- la mise en relation avec la Bourse nationale des déchets ;",
         "- l'appui des délégations régionales du MINFOF pour la sensibilisation des exploitants forestiers.", "",
         "## Questions en suspens", "",
         "1. Le prix du contrat de conformité et le rythme de signature restent à mesurer pendant le pilote.",
         "2. Les textes réglementaires n'ont été lus que par extraits ; les positions de l'administration sont attendues par écrit.",
         "3. Aucun devis d'équipement, de crédit-bail ou d'assurance n'a encore été obtenu."]
    return "\n".join(L) + "\n"


def bp_banque(c):
    sd, b = c["sd"], c["base"]
    a, ind = sd["a"], sd["ind"]
    mc = c["mc"]
    g = c["F"]["guerre_prix"]
    base_tor, tor = c["tornado"]
    couv = [(a["ebitda"][i] + a["loyers"][i]) / a["loyers"][i] if a["loyers"][i] else None for i in range(5)]
    besoin_ct = max(0.0, -ind["tresorerie_min"])
    L = ["# Business plan : dossier de financement", "",
         "## Résumé exécutif", "",
         f"**Demande : un crédit-bail d'équipements d'une valeur d'environ {m_fcfa(val('H-92'), 1)} M FCFA, une facilité de trésorerie d'au moins {m_fcfa(besoin_ct, 1)} M FCFA "
         "et l'accès à une garantie de portefeuille PME (dispositif de la CDEC et de l'African Guarantee Fund [S-79]).**", "",
         "**Recommandation : financer une société de services à faible intensité capitalistique, déjà engagée par ses associés, dont la croissance est conditionnée à des portes de décision chiffrées.**", "",
         "Trois raisons :", "",
         f"1. **Un besoin payant et mal servi.** Collecter les huiles usagées en forêt coûte {nombre(c['cout_l_min'])} à {nombre(c['cout_l_max'])} FCFA par litre ; seul le producteur peut le payer, "
         "et aucun collecteur identifié n'intervient sur les chantiers forestiers.",
         f"2. **Un modèle léger.** Les associés apportent {m_fcfa(sd['p']['H-157'], 1)} M FCFA ; les équipements sont en crédit-bail ; aucun emprunt bancaire n'est demandé. "
         f"Le point mort est d'environ {nombre(c['pm5'], 0)} clients sous contrat.",
         f"3. **Une rentabilité solide à terme, un démarrage fragile.** VAN à 5 ans de {m_fcfa(ind['van'], 1)} M FCFA et TRI de {pct(ind['tri'], 1)} ; "
         f"sur 10 000 tirages, la VAN avec valeur terminale n'est négative que dans {pct(mc['p_van_negative'], 1)} des cas, mais la VAN à 5 ans l'est dans {pct(mc['p_van5_negative'], 1)} des cas : "
         "le risque porte sur les deux premières années.", "",
         "| Chiffre clé | Valeur | Source |", "|---|---:|---|",
         f"| Chiffre d'affaires année 5 | {m_fcfa(a['ca'][4], 1)} M FCFA | modèle mensuel |",
         f"| EBITDA année 5 | {m_fcfa(a['ebitda'][4], 1)} M FCFA | modèle mensuel |",
         f"| Résultat net année 5 | {m_fcfa(a['resultat_net'][4], 1)} M FCFA | modèle mensuel |",
         f"| Besoin de financement maximal | {m_fcfa(ind['besoin_financement'], 1)} M FCFA | flux disponibles cumulés |",
         f"| Trésorerie minimale après apports | {m_fcfa(ind['tresorerie_min'], 1)} M FCFA | modèle mensuel |",
         f"| Point mort d'exploitation | mois {ind['point_mort_mois']} | modèle mensuel |",
         f"| Besoin au 90e centile (Monte-Carlo) | {m_fcfa(mc['besoin_p90'], 1)} M FCFA | 10 000 tirages |", "",
         "## Promoteur et équipe", "",
         "- **Gérant et associé majoritaire :** [Nom du promoteur], ingénieur mines et pétrole, licence de chimie organique, certifié NEBOSH IGC, spécialiste HSE et des études d'impact. "
         "Il assure la vente, la conformité réglementaire et la direction HSE.",
         "- **Technicien de terrain :** recruté au mois 3 ; purification du gasoil, prélèvements, accompagnement des enlèvements.",
         "- **Commercial :** à mi-temps au passage à l'étape 2.",
         f"- **Rémunérations :** le modèle retient {m_fcfa(val('H-150') * 12, 1)} M FCFA par an pour le gérant, sous le niveau du marché (`10_organisation/masse_salariale.md`) : le plan suppose que le promoteur accepte une rémunération réduite pendant cinq ans (à partir du mois 13).",
         "- **Associés minoritaires :** [à identifier], apporteurs des comptes courants bloqués.",
         "- **Gouvernance :** SARL, pacte d'associés, comité trimestriel ; charte de prévention des conflits d'intérêts avec le bureau d'études employeur du promoteur.", "",
         "## Besoin et marché", "",
         "Les huiles usagées sont des déchets dangereux soumis à permis [S-02]. Les exploitants forestiers sont sanctionnés pour leur gestion [S-29]. "
         f"Le segment forestier représente environ {m_fcfa(c['gis']['central']['foret'], 1)} M L/an chez environ 70 titulaires de concessions [S-46] et 251 UTB [S-45]. "
         "Les collecteurs de déchets dangereux identifiés travaillent à Douala [S-06][S-07]. Aucun acheteur de combustible n'étant confirmé, le modèle ne dépend d'aucune vente de combustible.", "",
         "## Offre et modèle économique", "",
         f"- contrat annuel de conformité : {m_fcfa(val('H-80'), 1)} M FCFA HT par site, facturé trimestriellement d'avance ;",
         f"- purification du gasoil : {nombre(val('H-81'))} FCFA par intervention, environ {nombre(val('H-82'), 0)} interventions par client et par an ;",
         "- commission sur les volumes urbains apportés à un collecteur partenaire ;",
         "- activités d'amorçage pendant 24 mois : formation, analyse d'huile, apport d'affaires.", "",
         f"Contribution annuelle d'un client forestier : environ {m_fcfa(c['contrib'], 2)} M FCFA, après enlèvements sous-traités et consommables.", "",
         ENTETE5,
         _ligne("Contrats de conformité", a["ca_contrat"]), _ligne("Purification du gasoil", a["ca_gasoil"]),
         _ligne("Commission urbaine", a["ca_commission_urbaine"]), _ligne("Activités d'amorçage (marge nette)", a["ca_amorcage"]),
         _ligne("**Chiffre d'affaires**", a["ca"]),
         _ligne("Clients forestiers en fin d'année", a["clients_fin"], lambda x: nombre(x, 1)), "",
         "## Opérations", "",
         "- enlèvements sous-traités à un collecteur titulaire d'un permis jusqu'à l'étape 3, sous contrat avec exigences HSE, suivi GPS et clause de non-sollicitation ;",
         "- huit procédures écrites, dépistage des halogènes avant chaque pompage, application de traçabilité hors ligne ;",
         "- purificateur de gasoil de 60 L/min, véhicule léger 4x4, matériel de prélèvement : en crédit-bail.", "",
         "## Cadre réglementaire, environnemental et social", "",
         f"Tant qu'elle ne détient ni ne transporte de déchets, la société n'a probablement pas besoin de permis ; une position écrite du MINEPDED est demandée. "
         f"Le permis propre (étape 3) suppose une évaluation environnementale par un bureau indépendant ; délai estimé de {nombre(c['cal']['bas'] / 30.4, 0)} à {nombre(c['cal']['haut'] / 30.4, 0)} mois. "
         "Risques environnementaux et sociaux principaux : déversement en transport, accident lors du nettoyage de cuve ; mesures : sous-traitance encadrée, procédures, assurance de responsabilité civile.", "",
         "## Hypothèses clés", "",
         "| ID | Hypothèse | Basse | Centrale | Haute | Statut | Vérification |", "|---|---|---:|---:|---:|---|---|"]
    for hid in ("H-80", "H-97", "H-48", "H-81", "H-82", "H-88", "H-83", "H-151", "H-150", "H-153", "H-155", "H-94"):
        h = HYPOTHESES[hid]
        L.append(f"| {hid} | {h.libelle} | {nombre(h.bas)} | {nombre(h.central)} | {nombre(h.haut)} | {h.statut} | {h.verification} |")
    L += ["", "Registre complet : `00_registres/hypotheses.md`.", "",
          "## Plan financier", "",
          "### Compte de résultat", "", ENTETE5,
          _ligne("Chiffre d'affaires", a["ca"]), _ligne("Charges d'exploitation (loyers de crédit-bail compris)", a["charges"]),
          _ligne("dont loyers de crédit-bail", a["loyers"]), _ligne("EBITDA", a["ebitda"]), _ligne("Amortissements", a["amortissement"]),
          _ligne("Impôt", a["impot"]), _ligne("**Résultat net**", a["resultat_net"]), "",
          "### Bilan simplifié en fin d'année", "", ENTETE5,
          _ligne("Immobilisations nettes", a["immobilisations_nettes_fin"]), _ligne("Créances clients", a["creances_fin"]),
          _ligne("Trésorerie (négative : découvert)", a["tresorerie_fin"]), _ligne("Capitaux propres et comptes courants", a["capitaux_propres_fin"]),
          _ligne("Dettes financières", a["capital_restant_fin"]), _ligne("Dettes fournisseurs", a["dettes_fournisseurs_fin"]), "",
          f"Écart maximal actif moins passif sur 60 mois : {nombre(sd['ecart_bilan'], 6)} FCFA.", "",
          "### Flux de trésorerie", "", ENTETE5,
          _ligne("Flux de trésorerie disponible", a["flux_disponible"]), _ligne("Investissements", a["capex"]), _ligne("Trésorerie de fin d'année", a["tresorerie_fin"]), "",
          "### Ratios", "",
          "| Ratio | Année 1 | Année 2 | Année 3 | Année 4 | Année 5 |", "|---|---:|---:|---:|---:|---:|",
          "| Couverture des loyers (EBITDA avant loyers / loyers) | " + " | ".join("s.o." if v is None else nombre(v, 2) for v in couv) + " |",
          "| Marge d'EBITDA | " + " | ".join(pct(a["ebitda"][i] / a["ca"][i], 1) if a["ca"][i] else "s.o." for i in range(5)) + " |", "",
          "La couverture des loyers est inférieure à 1 les deux premières années : les loyers sont alors payés par les fonds propres, ce qui justifie l'apport demandé aux associés et la facilité de trésorerie.", "",
          "## Scénarios et sensibilité", "",
          "| Indicateur | Structure demandée | Base (emprunt) | Guerre des prix (base) |", "|---|---:|---:|---:|",
          f"| VAN à 5 ans (M FCFA) | {m_fcfa(ind['van'], 1)} | {m_fcfa(b['ind']['van'], 1)} | {m_fcfa(g['van'], 1)} |",
          f"| VAN avec valeur terminale (M FCFA) | {m_fcfa(ind['van_vt'], 1)} | {m_fcfa(b['ind']['van_vt'], 1)} | {m_fcfa(g['van_vt'], 1)} |",
          f"| Besoin de financement maximal (M FCFA) | {m_fcfa(ind['besoin_financement'], 1)} | {m_fcfa(b['ind']['besoin_financement'], 1)} | {m_fcfa(g['besoin_financement'], 1)} |", "",
          "« Base (emprunt) » : variante d'origine du modèle, avec un emprunt au passage à l'étape 2 ; son DSCR est négatif en année 2, d'où la structure en crédit-bail demandée.", "",
          f"**Tornado (structure demandée, VAN avec valeur terminale, base {m_fcfa(base_tor, 1)} M FCFA).**", "",
          "| Hypothèse | VAN à la borne basse | VAN à la borne haute |", "|---|---:|---:|"]
    for k, lo, hi, _ in tor[:5]:
        L.append(f"| {k} {HYPOTHESES[k].libelle} | {m_fcfa(lo, 1)} | {m_fcfa(hi, 1)} |")
    L += ["", f"**Monte-Carlo (10 000 tirages triangulaires sur 18 hypothèses, structure demandée).** Probabilité de VAN à 5 ans négative : {pct(mc['p_van5_negative'], 1)} ; avec valeur terminale : {pct(mc['p_van_negative'], 1)} ; "
          f"VAN médiane avec valeur terminale : {m_fcfa(mc['van_p50'], 1)} M FCFA ; besoin au 90e centile : {m_fcfa(mc['besoin_p90'], 1)} M FCFA.", "",
          "## Financement demandé et garanties", "",
          "| Emplois | M FCFA | Ressources | M FCFA |", "|---|---:|---|---:|",
          f"| Besoin de financement maximal (pertes de démarrage, BFR, dépôts) | {m_fcfa(ind['besoin_financement'], 1)} | Fonds propres et comptes courants bloqués | {m_fcfa(sd['p']['H-157'], 1)} |",
          f"| Équipements (purificateur, véhicule, matériel) | {m_fcfa(val('H-92'), 1)} | Crédit-bail | {m_fcfa(val('H-92'), 1)} |",
          f"| Marge de sécurité de trésorerie | {m_fcfa(besoin_ct, 1)} | Facilité de trésorerie | {m_fcfa(besoin_ct, 1)} |", "",
          f"Au 90e centile des tirages, le besoin atteint {m_fcfa(mc['besoin_p90'], 1)} M FCFA (voir les points faibles).", "",
          "Garanties proposées : propriété du bailleur sur les équipements ; garantie de portefeuille PME (CDEC et African Guarantee Fund [S-79]) ; "
          "domiciliation des encaissements des contrats ; blocage des comptes courants d'associés pendant la durée du crédit-bail. Lignes de refinancement mobilisables par la banque : "
          "lignes PME vertes [S-80], lignes PME de bailleurs [S-81].", "",
          "## Risques et atténuation", "",
          "| ID | Risque | Criticité | Mesure | Déclencheur |", "|---|---|---:|---|---|"]
    for r in c["risques"][:8]:
        L.append(f"| {r[0]} | {r[2]} | {r[4] * r[5]} | {r[6]} | {r[7]} |")
    L += ["", "Registre complet : `13_risques/registre_risques.md`.", "",
          "## Plan de mise en œuvre et portes de décision", "",
          "| Période | Étape | Porte de sortie |", "|---|---|---|",
          "| mois 1 à 3 | amorçage | 2 clients pilotes, collecteur sous-traitant, charte signée |",
          "| mois 4 à 18 | pilote et développement | 4 contrats annuels, 3 mois d'EBITDA positif |",
          "| mois 19 à 30 | équipement en crédit-bail | 9 clients, 100 000 L/an enlevés |",
          "| mois 31 à 36 | permis propre | 320 000 L/an collectés |", "",
          "## Conditions préalables au décaissement", "",
          "- société immatriculée, statuts et pacte d'associés signés ;",
          f"- fonds propres et comptes courants versés ou engagés pour {m_fcfa(sd['p']['H-157'], 1)} M FCFA ;",
          "- charte de prévention des conflits d'intérêts signée ;",
          "- au moins un contrat annuel de conformité signé à l'issue du pilote ;",
          "- contrat de sous-traitance avec un collecteur titulaire d'un permis ;",
          "- attestation d'assurance de responsabilité civile.", "",
          "## Points faibles du dossier", "",
          "1. Le prix du contrat et le rythme de signature, qui expliquent l'essentiel de la valeur, ne sont pas encore mesurés.",
          f"2. Au 90e centile, le besoin de financement atteint {m_fcfa(mc['besoin_p90'], 1)} M FCFA, au-delà des {m_fcfa(sd['p']['H-157'] + besoin_ct, 1)} M FCFA demandés (fonds propres et facilité) : "
          "une seconde tranche de comptes courants est à prévoir dans le pacte d'associés, faute de quoi la porte du mois 18 sert de point d'arrêt.",
          f"3. Les loyers de crédit-bail ({m_fcfa(val('H-94'), 1)} M FCFA par an) ne viennent d'aucune offre, et aucune administration n'a encore répondu par écrit sur le régime applicable."]
    return "\n".join(L) + "\n"


# Pages du corps, mesurees sur le PDF (LibreOffice ne calcule pas SECTIONPAGES) ; controlees a chaque generation du PDF et par les tests.
PAGES_CORPS = {"Document de projet institutionnel": 15, "Business plan bancaire": 17}
MARQUEURS = {"Document de projet institutionnel": "FICHE SIGNALÉTIQUE", "Business plan bancaire": "RÉSUMÉ EXÉCUTIF"}


def pages_corps_pdf(pdf, marqueur):
    total = int(next(l.split()[-1] for l in subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout.splitlines() if l.startswith("Pages")))
    for page in range(1, total + 1):
        t = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), str(pdf), "-"], capture_output=True, text=True).stdout
        if marqueur in t and "SOMMAIRE" not in t:
            return total - page + 1
    return None


def produire(md_nom, nom, sous_titre, pdf=True):
    liv = ICI / "livrables"
    liv.mkdir(exist_ok=True)
    d = liv / f"{PREF} {nom}.docx"
    off = dict(sous_titre=sous_titre, date=DATE_TXT, sources=RACINE / "00_registres" / "sources.md", pages_corps=PAGES_CORPS[nom])
    docx_charte.convertir(ICI / md_nom, d, titre_court=nom, reference=f"{PREF} {nom}", officiel=off)
    if pdf:
        docx_charte.vers_pdf(d, liv)
        n = pages_corps_pdf(liv / f"{PREF} {nom}.pdf", MARQUEURS[nom])
        if n != PAGES_CORPS[nom]:
            print(f"ATTENTION : {nom} compte {n} pages de corps ; mettre PAGES_CORPS a jour et relancer")
    return d


if __name__ == "__main__":
    c = donnees()
    (ICI / "bp_institutionnel.md").write_text(bp_institutionnel(c), encoding="utf-8")
    (ICI / "bp_banque.md").write_text(bp_banque(c), encoding="utf-8")
    pdf = "--sans-pdf" not in sys.argv
    produire("bp_institutionnel.md", "Document de projet institutionnel", "Société de gestion des huiles usagées et de purification du gasoil", pdf)
    produire("bp_banque.md", "Business plan bancaire", "Dossier de financement : crédit-bail d'équipements et facilité de trésorerie", pdf)
    print("Business plans : institutionnel et bancaire generes")
