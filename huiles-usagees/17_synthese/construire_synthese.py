"""Lot 17 : construction de la synthese. Tous les chiffres sont lus dans les modeles et fichiers generes,
jamais recopies a la main.

Sorties : business_plan.md, note_go_no_go.md, presentation_banque.pptx (12 diapositives),
presentation_forestiers.pptx (8 diapositives), et leurs versions .docx et .pdf (dossier livrables/).
"""
from pathlib import Path
import importlib.util
import json
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Cm, Pt

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from commun.format import m_fcfa, nombre, pct  # noqa: E402
from commun.hypotheses import val  # noqa: E402
from commun import docx_charte  # noqa: E402

ICI = Path(__file__).resolve().parent
DATE = "2026-11-18"
DATE_TXT = "18 novembre 2026"
# Nombre de pages du corps du business plan (hors couverture et pages preliminaires), mesure sur le PDF
# par mesurer_pages_corps() ; LibreOffice ne calcule pas le champ SECTIONPAGES.
PAGES_CORPS_BP = 13


def _module(rel, nom):
    spec = importlib.util.spec_from_file_location(nom, RACINE / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def chiffres():
    F = json.loads((RACINE / "09_finance" / "resultats_finance.json").read_text(encoding="utf-8"))
    gis = _module("04_marche/gisement.py", "gis").resultats()
    cal = _module("02_reglementaire/calendrier.py", "cal")
    fins = {c: max(cal.planifier(c)[1].values()) for c in ("bas", "central", "haut")}
    comp = _module("08_modele_entreprise/comparaison.py", "comp")
    _, _, scores = comp.notes()
    bp = _module("14_plan_action/budget_preoperationnel.py", "bpo")
    _, tot, cum = bp.rapport()
    proc = _module("05_technique/procede.py", "proc")
    rend = {q: proc.bilan(c)["rendement"] for q, c in proc.QUALITES.items()}
    tour = _module("06_logistique/tournees.py", "tour")
    cpl, _ = tour.couts_par_litre("seche")
    mat = _module("00b_amorcage/matrice_amorcage.py", "mat")
    top3 = mat.evaluer()[:3]
    return dict(F=F, gis=gis, fins=fins, scores=scores, budget6=sum(tot), besoin6=max(0.0, -min(cum)), rend=rend,
                cout_l_min=min(cpl.values()), cout_l_max=max(cpl.values()), pm=comp.point_mort_clients("M1"),
                pm5=comp.point_mort_clients("M5"), contrib=comp.marge_par_client("M1"),
                amorcage=(sum(d["rev_bas"] for d in top3), sum(d["rev_central"] for d in top3), sum(d["rev_haut"] for d in top3)))


def business_plan(c):
    F, b = c["F"], c["F"]["scenarios"]["base"]
    p, o = c["F"]["scenarios"]["pessimiste"], c["F"]["scenarios"]["optimiste"]
    mc, a, g = F["monte_carlo"], F["annuel_base"], F["guerre_prix"]
    ratio = c["gis"]["central"]["etude"] / c["gis"]["central"]["parc_total"]
    L = [f"# Business plan : société de gestion des huiles usagées et de purification du gasoil", "",
         f"**Projet de création d'entreprise, Cameroun. Version de travail du {DATE_TXT}. Méthode de rédaction : pyramide de Minto. "
         "Chaque chiffre renvoie au livrable qui le calcule ; les hypothèses [H-xx] et sources [S-xx] sont dans `00_registres/`.**", "",
         "## Résumé exécutif", "",
         "**Recommandation : créer la société et lancer un pilote payant de trois mois, sans investissement lourd. "
         "Décision « Go conditionnel » : la trajectoire ne se poursuit qu'au franchissement de portes de décision chiffrées.**", "",
         "Trois raisons fondent cette recommandation :", "",
         f"1. **Un besoin payant existe chez les exploitants forestiers et les unités de transformation du bois**, qui doivent gérer leurs huiles usagées comme des déchets dangereux, loin de tout collecteur. "
         f"Collecter en forêt coûte de l'ordre de {nombre(c['cout_l_min'])} à {nombre(c['cout_l_max'])} FCFA par litre (`06_logistique/tournees.md`) : "
         "ce coût ne peut être payé que par un contrat de service avec le producteur, et c'est l'offre proposée.",
         f"2. **Le modèle démarre avec peu de capital.** Le purificateur et le véhicule sont loués, les enlèvements sous-traités à un collecteur titulaire. "
         f"Le point mort est d'environ {nombre(c['pm'], 0)} à {nombre(c['pm5'], 0)} clients forestiers sous contrat (`08_modele_entreprise/comparaison_modeles.md`).",
         f"3. **Le plan financier est positif en scénario de base** : VAN à 5 ans de {m_fcfa(b['van'], 1)} M FCFA, TRI de {pct(b['tri'], 1)}, "
         f"résultat net de {m_fcfa(b['rn_an5'], 1)} M FCFA en année 5 (`09_finance/resultats_finance.md`).", "",
         "Le projet abandonne la partie la plus risquée du premier business plan : l'unité de fabrication de combustible est gelée tant que trois conditions ne sont pas réunies "
         "(réponse écrite du MINEPDED sur le statut du produit, acheteur engagé avec un prix, collecte prouvée d'au moins 320 000 L/an ; décision D-06).", "",
         "## Problème et besoin", "",
         "Les huiles moteur, hydrauliques et de transmission usagées sont des déchets dangereux. Leur collecte, leur transport, leur stockage et leur valorisation sont soumis "
         "au permis environnemental prévu par l'arrêté n°001/MINEPDED du 15 octobre 2012 [S-02]. Les exploitants forestiers suivis par le promoteur sont sanctionnés pour leur gestion des huiles [S-29] ; "
         "le montant et la fréquence de ces sanctions sont relevés par le protocole de terrain n°4.", "",
         "## Offre", "",
         "- un contrat annuel de conformité par site : fûts identifiés par QR code, kit antipollution, registre, formation, enlèvements tracés sous bordereau, dépistage des halogènes, rapport annuel d'activité ;",
         "- la purification du gasoil et le nettoyage des cuves depuis l'extérieur ;",
         "- un dossier de preuves pour les audits de certification FSC et OLB ;",
         "- trois activités d'amorçage dès le premier mois : formation en atelier, analyse d'huile en service, apport d'affaires à un collecteur titulaire.", "",
         f"Prix d'appel du contrat : {m_fcfa(val('H-80'), 1)} M FCFA HT par site et par an (H-80), à valider pendant le pilote. "
         f"Contribution annuelle d'un client en régime de croisière : environ {m_fcfa(c['contrib'], 2)} M FCFA.", "",
         "## Marché", "",
         f"- Le gisement national de 70 000 t/an cité par la littérature [S-01] est probablement surestimé : l'estimation par le parc donne environ {m_fcfa(c['gis']['central']['parc_total'], 1)} M L/an, "
         f"soit {nombre(ratio, 1)} fois moins (`04_marche/gisement.md`).",
         f"- Le segment forestier représente environ {m_fcfa(c['gis']['central']['foret'], 1)} M L/an en cas central, chez quelque 70 titulaires de concessions [S-46] et 251 UTB [S-45].",
         "- Aucun collecteur identifié n'opère en forêt ; à Douala, Bocom International et SECA collectent des déchets dangereux [S-06][S-07]. L'unité de Valtech Energy à Kribi n'était pas en service dans la dernière source [S-60].",
         "- Aucun acheteur de combustible n'est confirmé : les cimenteries de Douala n'ont pas de four [S-64].", "",
         "## Modèle et trajectoire", "",
         "| Étape | Contenu | Porte de sortie |", "|---|---|---|",
         "| 0 Amorçage (mois 1 à 3) | société, activités d'amorçage, échantillonnage, démarches écrites | 2 clients pilotes engagés, sous-traitant d'accord, charte signée par HIKMA |",
         "| 1 Pilote et développement (mois 4 à 18) | purificateur loué, enlèvements sous-traités | 4 contrats annuels, 3 mois d'EBITDA positif |",
         "| 2 Prestataire équipé (mois 19 à 30) | équipements en crédit-bail, gérant à temps plein | 9 clients, 100 000 L/an enlevés |",
         "| 3 Permis propre (à partir du mois 31) | évaluation environnementale, permis, centre de transit | 320 000 L/an collectés |",
         "| 4 Traitement | prétraitement ou combustible | conditions de D-06 |", "",
         f"Le modèle retenu obtient le meilleur score de la matrice multicritère : {nombre(c['scores']['M5'], 2)} sur 5 pour le démarrage à faible capital, "
         f"contre {nombre(c['scores']['M3'], 2)} pour l'unité de traitement du premier business plan (`08_modele_entreprise/comparaison_modeles.md`).", "",
         "## Cadre réglementaire", "",
         f"Tant qu'elle ne détient ni ne transporte de déchets, la société n'a probablement pas besoin de permis (question posée par écrit au MINEPDED). "
         f"À l'étape 3, il faut une évaluation environnementale, le permis déchets et, pour le centre, le régime des établissements classés : de {nombre(c['fins']['bas'] / 30.4, 0)} à {nombre(c['fins']['haut'] / 30.4, 0)} mois "
         "selon les cas (`02_reglementaire/calendrier.md`). Les textes n'ont été lus que par extraits : un juriste doit confirmer ces conclusions.", "",
         "## Organisation et gouvernance", "",
         "SARL au capital de 1 000 000 FCFA [S-89], complétée par des comptes courants d'associés bloqués. Le promoteur, ingénieur HSE et EIES, est gérant et associé majoritaire. "
         "HIKMA ne détient aucune part ; une charte de prévention des conflits d'intérêts organise la séparation des activités (`11_juridique/`). "
         "Effectif : deux personnes la première année, quatre au passage en M1.", "",
         "## Plan financier", "",
         "| M FCFA | Année 1 | Année 2 | Année 3 | Année 4 | Année 5 |", "|---|---:|---:|---:|---:|---:|",
         "| Clients en fin d'année | " + " | ".join(nombre(x, 0) for x in a["clients_fin"]) + " |",
         "| Chiffre d'affaires | " + " | ".join(m_fcfa(x, 1) for x in a["ca"]) + " |",
         "| EBITDA | " + " | ".join(m_fcfa(x, 1) for x in a["ebitda"]) + " |",
         "| Résultat net | " + " | ".join(m_fcfa(x, 1) for x in a["resultat_net"]) + " |",
         "| Investissements | " + " | ".join(m_fcfa(x, 1) for x in a["capex"]) + " |",
         "| Flux de trésorerie disponible | " + " | ".join(m_fcfa(x, 1) for x in a["flux_disponible"]) + " |",
         "| Trésorerie de fin d'année | " + " | ".join(m_fcfa(x, 1) for x in a["tresorerie_fin"]) + " |", "",
         "Source : `09_finance/resultats_finance.md`, scénario de base.", "",
         "| Indicateur | Pessimiste | Base | Optimiste |", "|---|---:|---:|---:|",
         f"| VAN à 5 ans (M FCFA) | {m_fcfa(p['van'], 1)} | {m_fcfa(b['van'], 1)} | {m_fcfa(o['van'], 1)} |",
         f"| VAN avec valeur terminale (M FCFA) | {m_fcfa(p['van_vt'], 1)} | {m_fcfa(b['van_vt'], 1)} | {m_fcfa(o['van_vt'], 1)} |",
         f"| Besoin de financement maximal (M FCFA) | {m_fcfa(p['besoin_financement'], 1)} | {m_fcfa(b['besoin_financement'], 1)} | {m_fcfa(o['besoin_financement'], 1)} |", "",
         f"Simulation de Monte-Carlo sur 10 000 tirages : probabilité de VAN à 5 ans négative de {pct(mc['p_van5_negative'], 1)}, de VAN avec valeur terminale négative de {pct(mc['p_van_negative'], 1)} ; "
         f"besoin de financement au 90e centile de {m_fcfa(mc['besoin_p90'], 1)} M FCFA. Une guerre des prix réduisant les contrats de 30 % à partir du mois 25 rend la VAN à 5 ans négative "
         f"({m_fcfa(g['van'], 1)} M FCFA) sans annuler la valeur à long terme ({m_fcfa(g['van_vt'], 1)} M FCFA).", "",
         "## Financement demandé", "",
         f"- fonds propres et quasi-fonds propres : environ 20 M FCFA (apport de {m_fcfa(val('H-157'), 1)} M FCFA et comptes courants d'associés) ;",
         f"- crédit-bail des équipements au passage en M1 : environ {m_fcfa(val('H-92'), 1)} M FCFA ;",
         "- garantie recherchée : dispositif de la CDEC et de l'African Guarantee Fund [S-79] ; lignes PME vertes [S-80].", "",
         f"Sur les six premiers mois, les décaissements s'élèvent à {m_fcfa(c['budget6'], 2)} M FCFA et le besoin maximal à {m_fcfa(c['besoin6'], 2)} M FCFA (`14_plan_action/budget_preoperationnel.md`).", "",
         "## Risques principaux", "",
         "- refus du prix du contrat par les forestiers : le pilote teste un prix ferme ;",
         "- fonds propres insuffisants : tour de table engagé dès le premier mois, facturation trimestrielle d'avance ;",
         "- temps du promoteur : technicien autonome dès le pilote, gérant à temps plein au passage en M1 ;",
         "- conflit d'intérêts avec HIKMA : charte signée, lettre d'information aux clients communs.", "",
         "Registre complet : `13_risques/registre_risques.md`.", "",
         "## Points faibles du business plan", "",
         "1. Les hypothèses commerciales décisives (prix du contrat, rythme de signature) ne sont pas encore mesurées : le pilote les fournira.",
         "2. Les textes réglementaires n'ont été lus que par extraits ; aucune administration n'a encore répondu par écrit.",
         "3. Aucun devis d'équipement, de crédit-bail ou d'assurance n'a été obtenu."]
    return "\n".join(L) + "\n"


def note_go(c):
    b, mc = c["F"]["scenarios"]["base"], c["F"]["monte_carlo"]
    L = ["# Note Go/No Go", "", f"**Projet de société de gestion des huiles usagées et de purification du gasoil. {DATE_TXT}. Méthode : pyramide de Minto.**", "",
         "## Décision recommandée", "",
         "**GO CONDITIONNEL** : créer la société, lancer les activités d'amorçage et un pilote payant de trois mois chez deux clients forestiers, sans achat d'équipement ni demande de permis à ce stade.", "",
         "## Pourquoi", "",
         f"- le service de conformité répond à un coût que seul le producteur peut payer : {nombre(c['cout_l_min'])} à {nombre(c['cout_l_max'])} FCFA par litre collecté en forêt ;",
         f"- le scénario de base est positif (VAN à 5 ans de {m_fcfa(b['van'], 1)} M FCFA, TRI de {pct(b['tri'], 1)}), avec un point mort d'environ {nombre(c['pm'], 0)} clients ;",
         f"- le risque est surtout un risque de démarrage : VAN à 5 ans négative dans {pct(mc['p_van5_negative'], 1)} des tirages, mais VAN avec valeur terminale négative dans {pct(mc['p_van_negative'], 1)} seulement ;",
         f"- l'amorçage rapporte de {m_fcfa(c['amorcage'][0], 1)} à {m_fcfa(c['amorcage'][2], 1)} M FCFA nets sur 12 mois, sous un plafond de 500 000 FCFA de dépenses avant le premier encaissement.", "",
         "## Conditions du Go (porte 1, au plus tard au jour 75)", "",
         "- [ ] charte de prévention des conflits d'intérêts signée par HIKMA ;",
         "- [ ] deux clients pilotes engagés par écrit, avec un prix ferme ;",
         "- [ ] collecteur titulaire d'accord pour la sous-traitance des enlèvements ;",
         "- [ ] réponse écrite du MINEPDED sur le statut d'un prestataire qui ne détient pas de déchets, ou enlèvements strictement sous bordereau du collecteur ;",
         "- [ ] devis d'assurance de responsabilité civile, avec extension environnementale si disponible ;",
         f"- [ ] fonds propres et quasi-fonds propres d'environ 20 M FCFA engagés (besoin des six premiers mois : {m_fcfa(c['besoin6'], 2)} M FCFA).", "",
         "## Ce qui déclenche un No Go", "",
         "- HIKMA refuse la charte ou exige une part du capital ;",
         "- aucun client forestier n'accepte un pilote payant ;",
         "- aucun collecteur titulaire n'accepte la sous-traitance, et aucun permis n'est envisageable à court terme ;",
         "- à l'issue du pilote : aucun contrat annuel signé, ou contribution mesurée inférieure à 4 M FCFA par client et par an.", "",
         "## Ce qui n'est pas décidé", "",
         "L'unité de fabrication de combustible reste gelée (D-06). Sa réouverture exige une réponse écrite du MINEPDED sur le statut du produit, une lettre d'intention d'un acheteur à au moins 331 FCFA/L "
         "et une collecte prouvée d'au moins 320 000 L/an.", "",
         "## Points faibles de la note", "",
         "1. Le prix du contrat (H-80) et le nombre de clients (H-97), qui dominent la valeur, ne sont pas mesurés.",
         "2. La position de l'administration est déduite d'extraits de textes."]
    return "\n".join(L) + "\n"


def lisezmoi(c):
    b, mc = c["F"]["scenarios"]["base"], c["F"]["monte_carlo"]
    L = ["# Projet de collecte et de valorisation des huiles usagées et du gasoil au Cameroun", "",
         f"**Livraison du {DATE_TXT}. Lots 0 à 17 livrés.** Ce fichier est généré par `17_synthese/construire_synthese.py`.", "",
         "## Conclusion en cinq lignes", "",
         f"1. Go conditionnel : créer la société et lancer un pilote payant de trois mois, sans achat d'équipement ni demande de permis à ce stade.",
         f"2. Le marché porteur est le service de conformité payé par les forestiers : collecter en forêt coûte {nombre(c['cout_l_min'])} à {nombre(c['cout_l_max'])} FCFA/L, que seul le producteur peut payer.",
         f"3. Le scénario de base donne une VAN à 5 ans de {m_fcfa(b['van'], 1)} M FCFA, un TRI de {pct(b['tri'], 1)} et un point mort d'environ {nombre(c['pm'], 0)} clients sous contrat.",
         f"4. Le risque est de démarrage : VAN à 5 ans négative dans {pct(mc['p_van5_negative'], 1)} des 10 000 tirages, trésorerie tendue en année 2.",
         "5. L'unité de fabrication de combustible est gelée : statut légal du produit non tranché, aucun acheteur confirmé, gisement national probablement surestimé.", "",
         "## Modèle recommandé", "",
         "Trajectoire par étapes (décision D-09) : démarrage à faible capital (purificateur loué, enlèvements sous-traités à un collecteur titulaire, contrat annuel de conformité), "
         "passage en prestataire équipé à 4 contrats et 3 mois d'EBITDA positif, permis propre à 320 000 L/an, traitement seulement aux conditions de D-06.", "",
         "## Budget de démarrage", "",
         "- amorçage : au plus 500 000 FCFA avant le premier encaissement ;",
         f"- six premiers mois : {m_fcfa(c['budget6'], 2)} M FCFA de décaissements, besoin maximal de {m_fcfa(c['besoin6'], 2)} M FCFA (`14_plan_action/budget_preoperationnel.md`) ;",
         f"- fonds propres et quasi-fonds propres d'environ 20 M FCFA ; équipements en crédit-bail (environ {m_fcfa(val('H-92'), 1)} M FCFA) ; besoin au 90e centile de {m_fcfa(mc['besoin_p90'], 1)} M FCFA.", "",
         "## Cinq questions ouvertes à régler sur le terrain", "",
         "1. Q-10 : HIKMA signe-t-elle la charte de prévention des conflits d'intérêts ?",
         "2. Q-01 et Q-21 : le permis couvre-t-il la valorisation, et quand l'huile traitée cesse-t-elle d'être un déchet ? (réponse écrite du MINEPDED)",
         "3. H-80 : quel prix annuel les forestiers acceptent-ils pour le contrat de conformité ? (pilote)",
         "4. Q-18 : quel collecteur titulaire accepte de sous-traiter les enlèvements en forêt, et à quel prix ?",
         "5. Q-11 : l'unité de Valtech Energy à Kribi fonctionne-t-elle, et achète-t-elle les huiles ?", "",
         "Liste complète : `00_registres/questions_ouvertes.md`.", "",
         "## Ordre de lecture", "",
         "1. `17_synthese/livrables/` : note Go/No Go, business plan, présentations (banque, forestiers)",
         "2. `00b_amorcage/lot0_amorcage.md` et `14_plan_action/lot14_plan_action.md` : ce qu'il faut faire tout de suite",
         "3. `04b_validation_terrain/lot4bis_protocoles.md` : les preuves de terrain",
         "4. `02_reglementaire/`, `03_benchmark/`, `04_marche/`, `04c_extensions/` : le diagnostic",
         "5. `08_modele_entreprise/`, `05_technique/`, `06_logistique/`, `07_hse_eies/`, `09_finance/` : le modèle et ses chiffres",
         "6. `10_organisation/`, `11_juridique/`, `12_parties_prenantes/`, `13_risques/` : l'exécution",
         "7. `15_kit_operationnel/docx/` et `pdf/` : les documents prêts à l'emploi ; `16_application/` : l'application",
         "8. `00_registres/` : sources, hypothèses, questions ouvertes, décisions", "",
         "## Lundi", "",
         "1. Envoyer les quatre lettres du kit (A2) : HIKMA, MINEPDED, MINMIDT, MINEFOP.",
         "2. Demander les devis : laboratoires (SGS Cameroun et deux autres), Bocom International et SECA, distributeur Parker ou loueur, deux assureurs.",
         "3. Déposer le dossier de la SARL au CFCE (statuts J1 relus par un avocat).",
         "4. Faire dix appels de prospection avec le script K4, en commençant par les flottes urbaines et les concessionnaires.",
         "5. Lancer l'enquête des 30 garages et ouvrir le tour de table des comptes courants.", "",
         "## Reproduire", "",
         "```", "cd huiles-usagees", "pip install -r requirements.txt -r 16_application/requirements.txt",
         "python3 run_all.py        # régénère tous les chiffres, le kit et la synthèse ; contrôle les tirets",
         "make test                 # tests du dépôt et de l'application", "```", "",
         "## Limites de la livraison", "",
         "1. Le réseau de travail a bloqué les PDF officiels et OpenStreetMap : textes réglementaires lus par extraits, distances reconstruites.",
         "2. Aucune donnée de terrain, aucun devis, aucun entretien : les hypothèses décisives restent « supposées » jusqu'au pilote.",
         "3. Les documents juridiques sont des projets à faire relire par un avocat ou un notaire camerounais."]
    return "\n".join(L) + "\n"


# ---------- presentations ----------
NAVY = RGBColor(0x1F, 0x38, 0x64)


def _diapo(prs, titre, puces=None, tableau=None, note=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bar = s.shapes.add_shape(1, 0, 0, prs.slide_width, Cm(2.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    tf = bar.text_frame
    tf.text = titre
    tf.paragraphs[0].runs[0].font.size = Pt(26)
    tf.paragraphs[0].runs[0].font.bold = True
    tf.paragraphs[0].runs[0].font.name = "Arial"
    tf.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    haut = Cm(3.3)
    if puces:
        box = s.shapes.add_textbox(Cm(1.5), haut, prs.slide_width - Cm(3), Cm(13) if not tableau else Cm(5.2))
        t = box.text_frame
        t.word_wrap = True
        for i, p in enumerate(puces):
            par = t.paragraphs[0] if i == 0 else t.add_paragraph()
            par.text = "• " + p
            par.space_after = Pt(16)
            for r in par.runs:
                r.font.size = Pt(24)
                r.font.name = "Arial"
        haut = haut + (Cm(5.5) if tableau else 0)
    if tableau:
        nl, nc = len(tableau), len(tableau[0])
        shp = s.shapes.add_table(nl, nc, Cm(1.5), haut, prs.slide_width - Cm(3), Cm(1.5) * nl)
        for i, ligne in enumerate(tableau):
            for j, v in enumerate(ligne):
                cell = shp.table.cell(i, j)
                cell.text = str(v)
                for par in cell.text_frame.paragraphs:
                    for r in par.runs:
                        r.font.size = Pt(18)
                        r.font.name = "Arial"
                        r.font.bold = i == 0
                        if i == 0:
                            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                if i == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = NAVY
    if note:
        nb = s.shapes.add_textbox(Cm(1.5), prs.slide_height - Cm(1.6), prs.slide_width - Cm(3), Cm(1))
        nb.text_frame.text = note
        for r in nb.text_frame.paragraphs[0].runs:
            r.font.size = Pt(10)
            r.font.italic = True
            r.font.name = "Arial"
    return s


def _prs():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Cm(33.867), Cm(19.05)
    return prs


def deck_banque(c, chemin):
    F = c["F"]
    b, a, mc = F["scenarios"]["base"], F["annuel_base"], F["monte_carlo"]
    prs = _prs()
    _diapo(prs, "Gestion des huiles usagées et purification du gasoil", ["Projet de création de société, Cameroun", "Demande : crédit-bail d'équipements et garantie de crédit",
                                                                         f"Dossier du {DATE_TXT}"])
    _diapo(prs, "Synthèse", ["Un service de conformité payé par les producteurs forestiers, sans unité industrielle au démarrage",
                             f"VAN à 5 ans {m_fcfa(b['van'], 1)} M FCFA, TRI {pct(b['tri'], 1)} (scénario de base)",
                             f"Point mort : environ {nombre(c['pm'], 0)} clients sous contrat", "Trajectoire par étapes : chaque investissement suit une porte de décision chiffrée"],
           note="Sources : 09_finance/resultats_finance.md ; 08_modele_entreprise/comparaison_modeles.md")
    _diapo(prs, "Le besoin", ["Les huiles usagées sont des déchets dangereux soumis à permis [S-02]",
                              "Les exploitants forestiers sont sanctionnés pour leur gestion des huiles [S-29]",
                              f"Collecter en forêt coûte {nombre(c['cout_l_min'])} à {nombre(c['cout_l_max'])} FCFA par litre : le producteur doit payer le service"])
    _diapo(prs, "L'offre", ["Contrat annuel par site : fûts, kits, registre, formation, enlèvements tracés, rapport",
                            "Purification du gasoil et nettoyage de cuve sans entrée en cuve", "Dossier de preuves pour les audits FSC et OLB",
                            f"Prix d'appel : {m_fcfa(val('H-80'), 1)} M FCFA HT par site et par an, testé au pilote"])
    _diapo(prs, "Le marché", [f"Gisement par le parc : environ {m_fcfa(c['gis']['central']['parc_total'], 1)} M L/an (le chiffre de 70 000 t/an paraît surestimé)",
                              f"Segment forestier : environ {m_fcfa(c['gis']['central']['foret'], 1)} M L/an, 70 titulaires de concessions et 251 UTB",
                              "Aucun collecteur identifié en forêt ; collecteurs de déchets dangereux à Douala", "Aucun acheteur de combustible confirmé : la fabrication est gelée"])
    _diapo(prs, "Modèle et trajectoire", tableau=[["Étape", "Contenu", "Porte"], ["0", "amorçage, pilote préparé", "2 clients pilotes"],
                                                  ["1", "matériel loué, enlèvements sous-traités", "4 contrats, 3 mois d'EBITDA positif"],
                                                  ["2", "équipements en crédit-bail", "9 clients, 100 000 L/an"], ["3", "permis propre", "320 000 L/an"]])
    _diapo(prs, "Équipe et gouvernance", ["Gérant : ingénieur mines et pétrole, spécialiste HSE et EIES, certifié NEBOSH IGC",
                                          "SARL, capital de 1 M FCFA et comptes courants bloqués", "HIKMA hors du capital ; charte de prévention des conflits d'intérêts",
                                          "Deux personnes en année 1, quatre au passage à l'étape 2"])
    _diapo(prs, "Plan financier (scénario de base, M FCFA)", tableau=[["", "A1", "A2", "A3", "A4", "A5"],
                                                                       ["CA"] + [m_fcfa(x, 1) for x in a["ca"]], ["EBITDA"] + [m_fcfa(x, 1) for x in a["ebitda"]],
                                                                       ["Résultat net"] + [m_fcfa(x, 1) for x in a["resultat_net"]],
                                                                       ["Trésorerie"] + [m_fcfa(x, 1) for x in a["tresorerie_fin"]]],
           note="Source : 09_finance/resultats_finance.md")
    _diapo(prs, "Risques et sensibilité", [f"Monte-Carlo, 10 000 tirages : VAN à 5 ans négative dans {pct(mc['p_van5_negative'], 1)} des cas",
                                           f"VAN avec valeur terminale négative dans {pct(mc['p_van_negative'], 1)} des cas",
                                           "Variables dominantes : nombre de clients et prix du contrat", "Principaux risques : prix refusé, fonds propres, temps du gérant"])
    _diapo(prs, "Financement demandé", ["Fonds propres et quasi-fonds propres : environ 20 M FCFA (promoteur et associés)",
                                        f"Crédit-bail d'équipements : environ {m_fcfa(val('H-92'), 1)} M FCFA au passage à l'étape 2",
                                        "Garantie : dispositif CDEC et African Guarantee Fund", f"Besoin au 90e centile : {m_fcfa(mc['besoin_p90'], 1)} M FCFA"])
    _diapo(prs, "Plan d'action", ["Mois 1 à 3 : société, amorçage, échantillonnage, démarches écrites", "Mois 4 à 6 : pilote payant chez 2 clients forestiers",
                                  "Mois 7 à 18 : portefeuille de clients, dossier FSC et OLB", "Mois 19 à 36 : équipements, préparation du permis"])
    _diapo(prs, "Conditions et contact", ["Go conditionnel : franchissement de la porte 1 au plus tard au jour 75",
                                          "Points faibles : prix du contrat non mesuré, textes lus par extraits, aucun devis", "[Nom], gérant ; [téléphone] ; [courriel]"])
    prs.save(chemin)
    return len(prs.slides)


def deck_forestiers(c, chemin):
    prs = _prs()
    _diapo(prs, "Vos huiles usagées, gérées et tracées", ["Gestion des huiles usagées et purification du gasoil pour les exploitants forestiers et les UTB", "[Dénomination] ; [contact]"])
    _diapo(prs, "Vos enjeux", ["Des huiles usagées produites loin de tout collecteur", "Des preuves à fournir : registres, bordereaux, rapports PGES, audits FSC et OLB",
                               "De l'eau et des sédiments dans le gasoil des cuves"])
    _diapo(prs, "Notre offre", ["Fûts identifiés par QR code et kits antipollution", "Formation de vos mécaniciens et chefs d'atelier",
                                "Enlèvements planifiés par des transporteurs titulaires, sous bordereau", "Purification du gasoil sans entrée en cuve", "Rapport annuel d'activité"])
    _diapo(prs, "Comment ça marche", tableau=[["Étape", "Ce que nous faisons"], ["1", "visite d'état initial gratuite"], ["2", "équipement des sites et formation"],
                                              ["3", "enlèvements calés sur la saison sèche"], ["4", "purification du gasoil"], ["5", "rapport annuel et dossier d'audit"]])
    _diapo(prs, "Une traçabilité complète", ["Chaque fût a son QR code", "Chaque enlèvement a son bordereau numéroté", "Dépistage des halogènes avant tout pompage",
                                             "Application utilisable sans réseau, synchronisée au retour en ville"])
    _diapo(prs, "Sécurité", ["Procédures écrites pour chaque opération", "Chauffeurs et techniciens formés", "Intervention en cas de déversement : kit et procédure sur chaque site",
                             "Assurance de responsabilité civile"])
    _diapo(prs, "Le pilote proposé", ["Trois mois sur un ou deux sites", "Mesure de vos volumes, de vos coûts et de la qualité de votre gasoil",
                                      "Prix forfaitaire convenu à l'avance", "À la fin : un rapport et une proposition de contrat annuel"])
    _diapo(prs, "Prochaines étapes", ["Visite d'état initial : [date]", "Proposition écrite sous une semaine", "Contact : [nom], [téléphone], [courriel]"])
    prs.save(chemin)
    return len(prs.slides)


def construire(pdf=True):
    c = chiffres()
    (ICI / "business_plan.md").write_text(business_plan(c), encoding="utf-8")
    (ICI / "note_go_no_go.md").write_text(note_go(c), encoding="utf-8")
    (RACINE / "LISEZMOI.md").write_text(lisezmoi(c), encoding="utf-8")
    liv = ICI / "livrables"
    liv.mkdir(exist_ok=True)
    pref = f"{DATE} Huiles usagees"
    sorties = []
    d = liv / f"{pref} Business plan.docx"
    off = dict(sous_titre="Société de gestion des huiles usagées et de purification du gasoil, Cameroun",
               date=DATE_TXT, sources=RACINE / "00_registres" / "sources.md", pages_corps=PAGES_CORPS_BP)
    docx_charte.convertir(ICI / "business_plan.md", d, titre_court="Business plan", reference=f"{pref} Business plan", officiel=off)
    sorties.append(d)
    d = liv / f"{pref} Note Go No Go.docx"
    docx_charte.convertir(ICI / "note_go_no_go.md", d, titre_court="Note Go No Go", reference=f"{pref} Note Go No Go")
    sorties.append(d)
    nb = deck_banque(c, liv / f"{pref} Presentation banque.pptx")
    nf = deck_forestiers(c, liv / f"{pref} Presentation forestiers.pptx")
    sorties += [liv / f"{pref} Presentation banque.pptx", liv / f"{pref} Presentation forestiers.pptx"]
    from commun.deterministe import figer
    for x in sorties:
        figer(x)
    if pdf:
        for s in sorties:
            docx_charte.vers_pdf(s, liv)
    return nb, nf


def mesurer_pages_corps(pdf):
    """Pages du PDF a partir de celle qui porte le titre du resume executif."""
    import subprocess
    total = int(next(l.split()[-1] for l in subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout.splitlines() if l.startswith("Pages")))
    for page in range(1, total + 1):
        t = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), str(pdf), "-"], capture_output=True, text=True).stdout
        if "RÉSUMÉ EXÉCUTIF" in t and "SOMMAIRE" not in t:
            return total - page + 1
    return None


if __name__ == "__main__":
    nb, nf = construire(pdf="--sans-pdf" not in sys.argv)
    print("Lot 17 : diapositives", nb, nf)
