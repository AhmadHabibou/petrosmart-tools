"""Lot 12 : analyse des parties prenantes, carte interet x pouvoir, guides d'entretien et plan d'engagement MoSCoW.

Sorties : 12_parties_prenantes/fiches_parties_prenantes.md, 12_parties_prenantes/guides_entretien.md
Interet et pouvoir notes de 1 a 5 par le specialiste des parties prenantes (jugement, statut : suppose).
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

COMMUNES = {
    "administration": [
        "Quelles sont vos attentes envers un opérateur de gestion des huiles usagées ?",
        "Quels textes appliquez-vous à cette activité, et lesquels sont en vigueur aujourd'hui ?",
        "Quelles pièces exigez-vous, et quels délais constatez-vous réellement ?",
        "Quels manquements constatez-vous le plus souvent chez les producteurs d'huiles usagées ?",
        "Quels opérateurs détiennent aujourd'hui un titre pour cette activité ?",
        "Quelles évolutions réglementaires sont en préparation ?",
        "Comment se déroulent les contrôles et les sanctions dans votre domaine ?",
        "Qui suivra notre dossier, et sous quelle forme souhaitez-vous être tenu informé ?",
    ],
    "client": [
        "Combien d'engins et de groupes entretenez-vous, et à quelle fréquence vidangez-vous ?",
        "Quel volume d'huiles usagées produisez-vous par mois, et comment le mesurez-vous ?",
        "Où et comment stockez-vous ces huiles aujourd'hui ?",
        "Qui les enlève, à quel prix, et avec quel document ?",
        "Avez-vous reçu ces trois dernières années une observation, une mise en demeure ou une sanction sur ce point ?",
        "Vos auditeurs FSC, OLB ou vos bailleurs vous demandent-ils des preuves sur les huiles et le gasoil ?",
        "Rencontrez-vous des problèmes d'eau ou de pollution dans votre gasoil ?",
        "Qui décide d'un contrat de ce type chez vous, et avec quel budget annuel ?",
    ],
    "fournisseur": [
        "Combien de vidanges réalisez-vous par semaine, et quel volume d'huile retirez-vous ?",
        "Que deviennent aujourd'hui vos huiles usagées ?",
        "Êtes-vous payé pour ces huiles, ou payez-vous leur enlèvement ? Combien ?",
        "Mélangez-vous d'autres liquides aux huiles usagées ?",
        "Tenez-vous un registre ou recevez-vous un bordereau ?",
        "Vos clients vous demandent-ils une preuve de bonne gestion des huiles ?",
        "À quelles conditions confieriez-vous vos huiles à un collecteur tracé ?",
        "Quelle fréquence d'enlèvement vous conviendrait ?",
    ],
    "acheteur": [
        "Quel combustible utilisez-vous, en quelle quantité par mois et à quel prix ?",
        "Quel type de brûleur ou de four exploitez-vous, et quelles spécifications de combustible exige-t-il ?",
        "Avez-vous déjà brûlé des huiles usagées ou des combustibles de substitution ?",
        "Votre autorisation d'exploitation vous permet-elle de brûler un combustible issu de déchets ?",
        "Quels paramètres de qualité seraient éliminatoires pour vous ?",
        "Accepteriez-vous un essai de combustion encadré, avec mesure des gaz ?",
        "À quel prix, en pourcentage de votre combustible actuel, le produit vous intéresserait-il ?",
        "Quelles conditions contractuelles exigeriez-vous (volumes, régularité, analyses, responsabilité) ?",
    ],
    "partenaire": [
        "Quelle est votre activité actuelle dans les huiles usagées et les déchets dangereux ?",
        "Quels titres détenez-vous, et pour quelles opérations ?",
        "Quels volumes traitez-vous, et d'où viennent-ils ?",
        "Que faites-vous des huiles collectées ?",
        "Quelles zones géographiques couvrez-vous, et lesquelles refusez-vous ?",
        "Quels sont vos tarifs pour un enlèvement en ville et en forêt ?",
        "Quelles difficultés rencontrez-vous avec les producteurs et l'administration ?",
        "À quelles conditions envisageriez-vous un partenariat ou une sous-traitance avec nous ?",
    ],
    "financeur": [
        "Quels produits proposez-vous à une jeune société de services environnementaux ?",
        "Quels critères d'éligibilité et quelles garanties exigez-vous ?",
        "Quel taux, quelle durée et quel différé pouvez-vous proposer ?",
        "Pratiquez-vous le crédit-bail sur du matériel léger et des véhicules ?",
        "Disposez-vous de lignes vertes ou de garanties de partenaires pour ce type de projet ?",
        "Quels ratios regardez-vous (fonds propres, DSCR, trésorerie) ?",
        "Quels documents attendez-vous dans le dossier ?",
        "Quels délais d'instruction constatez-vous ?",
    ],
    "autre": [
        "Comment percevez-vous la gestion actuelle des huiles usagées dans votre domaine ?",
        "Quelles préoccupations un projet de ce type soulève-t-il pour vous ?",
        "Quelles informations souhaitez-vous recevoir, et à quelle fréquence ?",
        "Quelles conditions poseriez-vous à votre soutien ?",
        "Qui d'autre devrions-nous rencontrer ?",
        "Quelles expériences passées, positives ou négatives, avez-vous connues avec des projets comparables ?",
        "Quels engagements écrits attendez-vous de notre part ?",
        "Comment souhaitez-vous signaler un problème si vous en constatez un ?",
    ],
}

# nom, categorie, groupe, interet, pouvoir, position probable (avec source et certitude), a obtenir, moscow, questions specifiques
PP = [
    ("MINEPDED", "administration", "Administrations", 4, 5,
     "Délivre le permis environnemental déchets et approuve les évaluations environnementales [S-02][S-33]. Probablement favorable à un opérateur qui structure une filière, exigeant sur la valorisation. Certitude : probable.",
     "réponses écrites à Q-01, Q-03, Q-17, Q-21, Q-23 ; liste des titulaires de permis", "Must",
     ["Le permis de l'arrêté n°001/MINEPDED couvre-t-il la valorisation en combustible, et sous quelle mention ?",
      "Un apporteur d'affaires ou un prestataire de conformité qui ne détient aucun déchet doit-il un permis ?",
      "Quand une huile traitée cesse-t-elle d'être un déchet ? L'acheteur doit-il un titre ?",
      "Quelle catégorie d'évaluation environnementale pour un centre de transit, et pour une unité de prétraitement ?",
      "Un essai de combustion d'un lot de 200 L peut-il être autorisé avant le permis ?"]),
    ("Ministère chargé des établissements classés (MINMIDT)", "administration", "Administrations", 3, 4,
     "Le ministre des Mines est désigné comme destinataire des demandes d'autorisation des établissements classés [S-35] ; contrôle des agréments en 2026 [S-36]. Neutre, procédural. Certitude : probable.",
     "classe d'un centre de transit et d'une unité de prétraitement (Q-22) ; pièces de l'étude de dangers", "Should",
     ["Dans quelle classe de la nomenclature se range un centre de transit d'huiles usagées ?",
      "L'enquête publique est-elle requise, et combien de temps dure-t-elle en pratique ?",
      "Quels bureaux sont agréés pour les études de dangers et les plans d'urgence ?"]),
    ("MINFOF", "administration", "Administrations", 3, 4,
     "Contrôle les exploitants forestiers et les normes d'intervention en milieu forestier [S-29]. Probablement favorable si le projet aide les forestiers à respecter les normes. Certitude : supposé.",
     "constats fréquents sur les huiles en forêt ; calendrier des barrières de pluie (Q-38)", "Should",
     ["Quels constats faites-vous sur les huiles et le gasoil lors des contrôles de chantier ?",
      "Comment la décision n°0108/D/MINEF/CAB du 9 février 1998 est-elle appliquée aujourd'hui sur ce point ?",
      "Quels sont les calendriers de barrières de pluie dans l'Est ?"]),
    ("MINCOMMERCE", "administration", "Administrations", 2, 3,
     "Compétent pour le commerce et les prix ; intérêt limité pour un service. Certitude : supposé.",
     "règles applicables à la vente d'un combustible et aux importations de matériel", "Could",
     ["La vente d'un combustible de substitution relève-t-elle d'une homologation ou d'un prix encadré ?",
      "Quelles règles s'appliquent à l'importation de kits et de consommables ?"]),
    ("MINT", "administration", "Administrations", 2, 4,
     "Délivre l'autorisation de transport de marchandises dangereuses et impose le suivi GPS [S-37][S-38]. Neutre. Certitude : probable.",
     "pièces, coût réel et délai de l'autorisation de transport ; position sur l'ADR", "Should",
     ["L'autorisation de transport coûte-t-elle 100 000 ou 200 000 FCFA, et pour quelle durée ?",
      "Quelles règles techniques appliquez-vous aux citernes d'huiles usagées ?",
      "Quels organismes forment les chauffeurs au transport de matières dangereuses ?"]),
    ("Administration des douanes", "administration", "Administrations", 1, 3,
     "Applique le tarif extérieur commun de la CEMAC aux équipements. Neutre. Certitude : supposé.",
     "positions tarifaires et taxes des équipements (Q-28) ; règles pour l'expédition d'échantillons (Q-14)", "Could",
     ["Quelles positions tarifaires et quels droits pour un purificateur de gasoil et un purificateur sous vide ?",
      "Quelles formalités pour expédier des échantillons d'huile usagée vers un laboratoire étranger ?"]),
    ("DGI", "administration", "Administrations", 1, 4,
     "Applique l'impôt sur les sociétés, le minimum de perception et la TVA. Neutre. Certitude : supposé.",
     "taux effectif de l'IS, minimum de perception, régime de TVA (Q-31, Q-42)", "Should",
     ["Quel taux effectif d'impôt sur les sociétés, centimes additionnels compris, pour une PME en 2026 ?",
      "Comment s'applique le minimum de perception la première année ?",
      "Quel régime de TVA pour une société de services dont le chiffre d'affaires démarre sous 20 M FCFA ?"]),
    ("Commune d'implantation du centre de transit", "administration", "Administrations", 3, 3,
     "Intéressée par l'emploi, sensible aux nuisances ; consultée lors de l'enquête publique. Certitude : supposé.",
     "accord de principe sur un site, conditions d'urbanisme", "Could",
     ["Quelles zones de la commune accueillent des activités industrielles ?",
      "Quelles conditions poseriez-vous à l'implantation d'un centre de transit d'huiles usagées ?"]),
    ("Bourse nationale des déchets", "partenaire", "Administrations", 3, 2,
     "Société d'économie mixte créée en 2025 pour mettre en relation producteurs et valorisateurs [S-10][S-11]. Probablement favorable. Certitude : probable.",
     "date d'ouverture de la plateforme, conditions d'inscription et commissions", "Could",
     ["La plateforme est-elle ouverte, et à quelle date les transactions commencent-elles ?",
      "Quels frais et commissions s'appliquent ?"]),
    ("SCIEB", "client", "Clients forestiers et UTB", 4, 3,
     "Client de HIKMA, sanctionné pour la gestion des huiles selon le cahier des charges [S-29]. Probablement intéressé si le prix est inférieur au coût des sanctions. Certitude : supposé.",
     "accord pour le pilote ; données de sanctions (4 bis n°4)", "Must",
     ["Accepteriez-vous un pilote de trois mois, payant, avec un engagement de décision à la fin ?"]),
    ("BOISCAM", "client", "Clients forestiers et UTB", 4, 3, "Même situation que SCIEB [S-29]. Certitude : supposé.",
     "rendez-vous de présentation ; données de sanctions", "Must", ["Accepteriez-vous un pilote de trois mois, payant ?"]),
    ("SEXTRANSBOIS", "client", "Clients forestiers et UTB", 4, 3, "Même situation que SCIEB [S-29]. Certitude : supposé.",
     "rendez-vous de présentation ; données de sanctions", "Should", ["Accepteriez-vous un pilote de trois mois, payant ?"]),
    ("NCIEB", "client", "Clients forestiers et UTB", 4, 3, "Même situation que SCIEB [S-29]. Certitude : supposé.",
     "rendez-vous de présentation ; données de sanctions", "Should", ["Accepteriez-vous un pilote de trois mois, payant ?"]),
    ("SFSC", "client", "Clients forestiers et UTB", 4, 3, "Même situation que SCIEB [S-29]. Certitude : supposé.",
     "rendez-vous de présentation ; données de sanctions", "Should", ["Accepteriez-vous un pilote de trois mois, payant ?"]),
    ("Concessions certifiées (Wijma Cameroun, PALLISCO)", "client", "Clients forestiers et UTB", 4, 3,
     "Certifiées FSC, avec une gestion des déchets mise en avant [S-71]. Probablement intéressées par le dossier de preuves FSC (E2). Certitude : supposé.",
     "exigences de leurs auditeurs sur les huiles", "Should",
     ["Qu'exigent vos auditeurs FSC sur les huiles, le gasoil et les déchets dangereux ?",
      "Comment gérez-vous aujourd'hui ces preuves ?"]),
    ("Garages de Douala et Yaoundé", "fournisseur", "Fournisseurs d'huiles urbaines", 2, 2,
     "Vendent ou cèdent probablement leurs huiles au circuit informel ; aucune donnée publiée (Q-30). Certitude : supposé.",
     "volumes, prix pratiqués, conditions de cession (enquête du lot 4)", "Should",
     ["Accepteriez-vous un prélèvement d'échantillon gratuit pour analyse ?"]),
    ("Concessionnaires d'engins et de véhicules (Tractafric Equipment Cameroun)", "fournisseur", "Fournisseurs d'huiles urbaines", 3, 3,
     "Concessionnaire exclusif Caterpillar, plus de 6 500 machines suivies au Cameroun [S-18][S-19]. Peut être prescripteur ou concurrent pour l'analyse d'huile (Q-20). Certitude : probable.",
     "position sur l'analyse d'huile et sur les huiles de ses ateliers", "Should",
     ["Proposez-vous l'analyse d'huile à vos clients au Cameroun, avec quel délai ?",
      "Que deviennent les huiles vidangées dans vos ateliers ?"]),
    ("Transporteurs, entreprises de BTP et industries", "fournisseur", "Fournisseurs d'huiles urbaines", 3, 2,
     "Flottes soumises à des exigences de leurs clients et bailleurs ; position non documentée. Certitude : supposé.",
     "volumes et intérêt pour un enlèvement tracé payant", "Could",
     ["Vos clients ou bailleurs exigent-ils une traçabilité des déchets de vos ateliers ?"]),
    ("Producteurs d'électricité thermique (Socadel)", "acheteur", "Fournisseurs d'huiles urbaines et acheteurs", 2, 4,
     "Achète du fioul lourd HFO 3500 par appel d'offres pour quatre centrales du Littoral ; appel d'octobre 2026 annulé [S-62]. Producteur d'huiles moteur usagées et acheteur théorique de combustible. Certitude : probable.",
     "devenir des huiles usagées des centrales ; ouverture éventuelle à un combustible de substitution", "Could",
     ["Que deviennent les huiles usagées de vos moteurs ?",
      "Vos constructeurs autorisent-ils un combustible de substitution en mélange ?"]),
    ("Cimencam, usine de clinker de Figuil", "acheteur", "Acheteurs de combustible", 2, 4,
     "Four à clinker alimenté en coke de pétrole importé [S-27]. Débouché technique possible, éloigné du gisement. Certitude : probable.",
     "politique de combustibles de substitution", "Could",
     ["Avez-vous une politique de combustibles de substitution pour le four de Figuil ?",
      "Quelles quantités minimales et quelle logistique accepteriez-vous ?"]),
    ("Briqueteries, séchoirs à bois, chaudières industrielles", "acheteur", "Acheteurs de combustible", 3, 2,
     "Non identifiés nommément (Q-29). Position supposée : intéressés par un combustible moins cher que le fioul si l'installation le permet.",
     "liste nominative et consommations", "Should",
     ["Votre chaudière est-elle équipée d'un préchauffage du combustible ?"]),
    ("TotalEnergies Marketing Cameroun et autres distributeurs de lubrifiants", "partenaire", "Distributeurs de lubrifiants", 2, 4,
     "Marché décrit comme très concurrentiel, marqué par les indépendants, les importations et la contrebande [S-66]. Intérêt possible pour une offre de reprise des huiles de leurs grands comptes (E5). Certitude : supposé.",
     "intérêt pour un partenariat de reprise ; volumes vendus (Q-25)", "Could",
     ["Vos grands comptes vous demandent-ils de reprendre leurs huiles usagées ?",
      "Quels volumes de lubrifiants mettez-vous sur le marché par an ?"]),
    ("Bocom International", "partenaire", "Concurrents et acteurs existants", 3, 4,
     "Collecte, transport et élimination de déchets dangereux depuis Bonabéri ; marché de la Sonara [S-07][S-08]. Partenaire possible pour la sous-traitance, concurrent potentiel. Certitude : probable.",
     "accord de sous-traitance en forêt (Q-18) ; accord d'apporteur d'affaires (Q-04)", "Must",
     ["Accepteriez-vous des tournées d'une semaine dans l'Est, et à quel prix par enlèvement ?",
      "Accepteriez-vous un contrat d'apporteur d'affaires avec commission ?"]),
    ("SECA", "partenaire", "Concurrents et acteurs existants", 3, 4,
     "Collecte et transport de déchets industriels à Douala ; contrat du Port autonome de Douala [S-06]. Même position que Bocom. Certitude : probable.",
     "accord de sous-traitance (Q-18)", "Must",
     ["Accepteriez-vous des tournées d'une semaine dans l'Est, et à quel prix par enlèvement ?"]),
    ("Valtech Energy (groupe SCIN), Kribi", "partenaire", "Concurrents et acteurs existants", 4, 4,
     "Porteur de l'unité Scarabox d'Ecoslops à Kribi, en attente de démarrage dans la dernière source [S-03][S-60]. Débouché ou concurrent majeur. Certitude : probable.",
     "statut de l'unité, prix d'achat des huiles (Q-11)", "Must",
     ["L'unité Scarabox est-elle en service, et avec quelle capacité réelle ?",
      "Achetez-vous des huiles de vidange, à quel prix et avec quelles spécifications ?",
      "Envisagez-vous un réseau de collecteurs partenaires ?"]),
    ("Circuit informel", "fournisseur", "Concurrents et acteurs existants", 3, 3,
     "Usage combustible domestique et artisanal documenté [S-61] ; prix et volumes inconnus (Q-30). Hostile si la société capte ses volumes. Certitude : supposé.",
     "compréhension des prix et des usages, sans confrontation", "Should",
     ["À quoi servent les huiles que vous achetez, et à quel prix les revendez-vous ?"]),
    ("Banques et microfinance (Afriland First Bank, Attijariwafa bank, établissements de microfinance)", "financeur", "Financement et assurance", 2, 5,
     "Crédit aux PME à 11,85 % en moyenne, garanties exigées [S-78] ; lignes PME de la SFI et lignes vertes avec l'AFD [S-80][S-81]. Prudents face à une société sans historique. Certitude : probable.",
     "accord de principe sur le crédit-bail et sur un crédit d'équipement garanti", "Should",
     ["Votre ligne PME verte est-elle accessible à une société de gestion des déchets dangereux ?"]),
    ("CDEC et African Guarantee Fund", "financeur", "Financement et assurance", 3, 4,
     "Dispositif de 5 milliards de FCFA pour les PME et phase pilote de crédit long terme [S-79]. Probablement favorables à une PME formalisée. Certitude : probable.",
     "conditions de garantie et banques partenaires", "Should",
     ["Quelles banques partenaires distribuent votre garantie, et pour quelle quotité ?"]),
    ("Bailleurs et fonds (AFD, BID, SFI)", "financeur", "Financement et assurance", 2, 3,
     "Interviennent par des lignes de crédit bancaires plutôt qu'en direct pour une PME de cette taille [S-80][S-81]. Certitude : probable.",
     "accès à leurs lignes via les banques", "Could", ["Existe-t-il un accompagnement technique associé à vos lignes PME ?"]),
    ("Assureurs (membres de l'ASAC)", "financeur", "Financement et assurance", 2, 4,
     "La responsabilité civile reste un segment faible dans la sous-région [S-90] ; offre de RC environnementale non documentée. Certitude : supposé.",
     "devis de responsabilité civile environnementale, flotte et site", "Must",
     ["Proposez-vous une garantie des atteintes à l'environnement, avec quels plafonds et exclusions ?",
      "Couvrez-vous les interventions chez les clients et les marchandises transportées par un sous-traitant ?"]),
    ("Organismes de certification forestière (FSC, OLB)", "autre", "Autres", 2, 3,
     "Référentiel FSC camerounais de 2026 [S-70] ; exigences sur les huiles non lues (Q-32). Neutres.", "exigences d'audit", "Could",
     ["Quels indicateurs du référentiel portent sur les hydrocarbures et les déchets dangereux ?",
      "Quelles preuves les auditeurs acceptent-elles ?"]),
    ("Laboratoires (SGS Cameroun et autres)", "partenaire", "Autres", 3, 3,
     "SGS Cameroun propose l'analyse d'huile depuis Douala [S-12] ; lieu d'analyse inconnu (Q-05). Certitude : probable.",
     "devis, délais, accréditations", "Must",
     ["Quelles analyses réalisez-vous à Douala, et lesquelles partent à l'étranger ?",
      "Quels délais et quels prix pour un lot de 12 échantillons ?"]),
    ("Riverains du futur site", "autre", "Autres", 4, 2,
     "Sensibles aux odeurs, au trafic et au risque de pollution ; consultés pendant l'enquête publique. Certitude : supposé.",
     "acceptation du site et canal de dialogue", "Could",
     ["Quelles nuisances craindriez-vous le plus ?", "Utilisez-vous des puits ou des sources à proximité du site envisagé ?",
      "Qui, dans le quartier ou le village, devrait être associé au suivi du site ?"]),
    ("HIKMA Advisory and Coordination", "autre", "Autres", 4, 5,
     "Employeur du promoteur et conseiller des clients forestiers [S-29]. Position à obtenir par écrit (Q-10). Certitude : supposé.",
     "accord écrit sur la charte de prévention des conflits d'intérêts", "Must",
     ["Acceptez-vous de signer la charte de prévention des conflits d'intérêts ?",
      "Quelles conditions posez-vous à l'exercice de cette activité par votre directeur de projets ?"]),
]


def quadrant(i, p):
    if p >= 4 and i >= 3:
        return "Gérer étroitement"
    if p >= 4:
        return "Satisfaire"
    if i >= 3:
        return "Tenir informé"
    return "Surveiller"


def guide(pp):
    q = COMMUNES[pp[1]] + pp[8]
    reserve = COMMUNES["autre"] + ["Quels documents pourriez-vous nous communiquer pour approfondir ces points ?",
                                   "Pouvons-nous vous recontacter après le pilote pour vous en présenter les résultats ?"]
    if len(q) < 10:
        q = q + [x for x in reserve if x not in q][: 10 - len(q)]
    return q[:15]


def rapport_fiches():
    out = ["# Parties prenantes : fiches, carte et plan d'engagement", "",
           "Fichier généré par `12_parties_prenantes/parties_prenantes.py`. Intérêt et pouvoir notés de 1 à 5 (jugement, statut : supposé). "
           "Méthodes : carte intérêt × pouvoir, MoSCoW pour le plan d'engagement.", "",
           "## Carte intérêt × pouvoir", ""]
    for qd in ("Gérer étroitement", "Satisfaire", "Tenir informé", "Surveiller"):
        noms = [f"{x[0]} ({x[3]}, {x[4]})" for x in PP if quadrant(x[3], x[4]) == qd]
        out.append(f"- **{qd}** : " + " ; ".join(noms) + ".")
    out += ["", "Entre parenthèses : intérêt, pouvoir. Gérer étroitement : pouvoir au moins 4 et intérêt au moins 3 ; Satisfaire : pouvoir au moins 4 ; Tenir informé : intérêt au moins 3 ; Surveiller : les autres.", "",
            "## Plan d'engagement priorisé (MoSCoW)", "", "| Priorité | Partie prenante | Ce qu'il faut obtenir |", "|---|---|---|"]
    ordre = {"Must": 0, "Should": 1, "Could": 2, "Won't": 3}
    for x in sorted(PP, key=lambda x: (ordre[x[7]], -x[4])):
        out.append(f"| {x[7]} | {x[0]} | {x[6]} |")
    out += ["", "## Fiches", ""]
    groupe = None
    for x in PP:
        if x[2] != groupe:
            groupe = x[2]
            out += [f"### {groupe}", ""]
        out += [f"**{x[0]}.** Intérêt {x[3]}, pouvoir {x[4]}, quadrant « {quadrant(x[3], x[4])} », priorité {x[7]}. "
                f"Position probable : {x[5]} À obtenir : {x[6]}.", ""]
    return "\n".join(out) + "\n"


def rapport_guides():
    out = ["# Guides d'entretien", "",
           "Fichier généré par `12_parties_prenantes/parties_prenantes.py`. Chaque guide compte de 10 à 15 questions : un tronc commun par catégorie, puis des questions propres à l'interlocuteur. "
           "Avant chaque entretien : présentation, objet, durée (45 minutes), confidentialité. Après : compte rendu dans les 48 heures, mise à jour du registre des questions ouvertes.", ""]
    for x in PP:
        q = guide(x)
        out += [f"## {x[0]}", ""] + [f"{i}. {t}" for i, t in enumerate(q, 1)] + [""]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    d = Path(__file__).parent
    (d / "fiches_parties_prenantes.md").write_text(rapport_fiches(), encoding="utf-8")
    (d / "guides_entretien.md").write_text(rapport_guides(), encoding="utf-8")
    print("Lot 12 :", len(PP), "parties prenantes")
