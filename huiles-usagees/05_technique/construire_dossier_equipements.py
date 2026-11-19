"""Dossier technique des equipements (annexe des deux business plans).

Genere par le code a partir des donnees du kit (15_kit_operationnel/construire_kit.py, liste EQUIPEMENTS)
et des hypotheses chiffrees (commun/hypotheses.py) :
- trois schemas de principe dessines par le code (05_technique/figures/*.png) ;
- 05_technique/dossier_equipements.md ;
- le .docx et le .pdf au format officiel dans 17_synthese/livrables/.

La fonction plan_acquisition() est reprise par les business plans (17_synthese/construire_business_plans.py).
Usage : python 05_technique/construire_dossier_equipements.py [--sans-pdf]
"""
from pathlib import Path
import importlib.util
import sys

from PIL import Image, ImageDraw, ImageFont

RACINE = Path(__file__).resolve().parents[1]
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))
from commun.format import m_fcfa  # noqa: E402
from commun.hypotheses import val  # noqa: E402
from commun import docx_charte  # noqa: E402

DATE, DATE_TXT = "2026-11-18", "18 novembre 2026"
NOM = "Dossier technique des equipements"
PREF = f"{DATE} Huiles usagees"
PAGES_CORPS = 13  # mesure sur le PDF ; controle a chaque generation et par les tests
MARQUEUR = "OBJET ET PÉRIMÈTRE"
FIGURES = ICI / "figures"


def _kit():
    spec = importlib.util.spec_from_file_location("kit", RACINE / "15_kit_operationnel" / "construire_kit.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return {e["code"]: e for e in m.EQUIPEMENTS}


# Choix par equipement : etape, mode d'acquisition, reference recommandee, alternatives, vigilance. Sources [S-xx] du registre.
CHOIX = {
    "E1": dict(etape="1", mode="location au pilote, puis crédit-bail",
               reco="Parker Racor DFC14WS25VVX1 [S-73] ou DFCC14WS10VVX1 [S-92] : 60 L/min, séparation de l'eau, élément FBO-14, pompe à engrenages",
               alt="Donaldson Clean Diesel Cart X011431 [S-93] ; HYDAC LowViscosity Unit LVU-CD [S-94]",
               vig="la fiche Parker indique 60 Hz : exiger la version 50 Hz ; l'élément absorbant Donaldson sature avec l'eau, prévoir un stock d'éléments"),
    "E2": dict(etape="4", mode="achat après la porte de l'étape 4 (D-06)",
               reco="Pall HNP022 ou HNP023 [S-95] : déshydratation sous vide, appareil portable",
               alt="HYDAC FluidAqua Mobile [S-94] ; série TYA chinoise (Chongqing TOP, Zhongneng, Rexon) [S-96], après essai sur notre huile",
               vig="le procédé retire l'eau et les particules, pas les additifs dégradés ni les métaux ; essai sur 20 L d'huile réelle et analyse indépendante avant toute commande"),
    "E3": dict(etape="4", mode="achat ; laboratoire sous-traitant avant",
               reco="Anton Paar PMA 500 [S-97] : ASTM D93, détection automatique, extincteur intégré",
               alt="Stanhope-Seta PM-93 [S-98] ; Koehler, appareil automatique",
               vig="la révision ASTM D93-25 impose une vérification par matériaux de référence certifiés [S-98] ; godet standard en laiton"),
    "E4": dict(etape="0", mode="achat, consommable",
               reco="Dexsil Clor-D-Tect 1000 [S-99] : seuil de 1 000 ppm de chlore, ASTM D5384, EPA 9077",
               alt="Dexsil Clor-D-Tect Q4000 [S-99] : mesure de 200 à 4 000 ppm",
               vig="biais positif au-delà de 3 % de soufre : tout lot positif est confirmé au laboratoire ; réactifs périssables"),
    "E5": dict(etape="0", mode="achat",
               reco="échantillonneur COLIWASA Nasco ou Wheaton [S-100], flacons ambrés à bouchon PTFE, scellés numérotés",
               alt="gamme Blackburn Sampling ; Koehler K27400 [S-28]",
               vig="un flacon par lot, scellé et étiqueté avant transport au laboratoire"),
    "E6": dict(etape="3", mode="achat d'occasion (D-10), location avec chauffeur en dépannage",
               reco="camion hydrocureur ADR à citerne sous vide d'environ 13 000 L, porteur IVECO, MAN ou DAF [S-101]",
               alt="porteur avec citerne compartimentée et pompe de transfert",
               vig="agrément ADR, état de la pompe à vide, inspection avant achat ; autorisation de transport du MINT [S-37] ; prix rendu Douala inconnu (Q-44)"),
    "E7": dict(etape="1", mode="location, puis crédit-bail",
               reco="Toyota Hilux double cabine, distribué par CAMI, groupe CFAO [S-102]",
               alt="pick-up 4x4 équivalent avec réseau de pièces en Afrique centrale",
               vig="plateau avec points d'arrimage et bac de rétention ; offre de crédit-bail à demander avec la lettre B4"),
}


def plan_acquisition():
    """Lignes (etape, contenu, mode, montant FCFA ou None, hypothese, etat du devis)."""
    return [
        ("0 et pilote", "matériel de prélèvement (E5) ; les kits de dépistage (E4) sont comptés dans les consommables", "achat", val("H-45"), "H-45", "aucun devis"),
        ("0 et pilote", "purificateur de gasoil (E1), 3 mois", "location", val("H-47"), "H-47", "aucun devis"),
        ("1", "dépôts de garantie, premiers loyers et petit matériel pour le purificateur (E1) et le véhicule (E7)", "location ou crédit-bail", val("H-93"), "H-93", "aucun devis"),
        ("1 à 5", "loyers de crédit-bail et de location, par an", "loyers", val("H-94"), "H-94", "demande B4 à envoyer"),
        ("2", "purificateur, matériel d'échantillonnage, véhicule, stock de fûts et kits", "crédit-bail", val("H-92"), "H-92", "demande B4 à envoyer"),
        ("3", "camion hydrocureur ADR d'occasion (E6)", "achat d'occasion", val("H-131"), "H-131", "aucun devis (Q-44)"),
        ("3 et 4", "centre de transit : cuves, décanteur, déshydrateur (E2), laboratoire de base (E3), permis", "achat", val("H-95"), "H-95", "aucun devis"),
    ]


# --- figures -----------------------------------------------------------------
ACCENT, EAU, NOIR, FOND = (31, 56, 100), (47, 111, 179), (20, 20, 20), (255, 255, 255)
_POLICE = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def _police(t):
    try:
        return ImageFont.truetype(_POLICE, t)
    except OSError:
        return ImageFont.load_default()


def _toile(l=1800, h=900):
    im = Image.new("RGB", (l, h), FOND)
    return im, ImageDraw.Draw(im)


def _boite(d, x, y, l, h, lignes, f, plein=None):
    d.rounded_rectangle([x, y, x + l, y + h], radius=14, outline=NOIR, width=4, fill=plein or FOND)
    hl = f.size + 8
    y0 = y + h / 2 - hl * len(lignes) / 2
    for k, t in enumerate(lignes):
        d.text((x + l / 2, y0 + k * hl + hl / 2), t, fill=NOIR, font=f, anchor="mm")


def _fleche(d, pts, coul=ACCENT, larg=8, tirets=False):
    for a, b in zip(pts, pts[1:]):
        if tirets:
            n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1])) // 24) or 1
            for k in range(0, n, 2):
                p = (a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n)
                q = (a[0] + (b[0] - a[0]) * (k + 1) / n, a[1] + (b[1] - a[1]) * (k + 1) / n)
                d.line([p, q], fill=coul, width=larg)
        else:
            d.line([a, b], fill=coul, width=larg)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    dx, dy = (x2 - x1), (y2 - y1)
    n = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / n, dy / n
    d.polygon([(x2, y2), (x2 - 30 * ux + 15 * uy, y2 - 30 * uy - 15 * ux), (x2 - 30 * ux - 15 * uy, y2 - 30 * uy + 15 * ux)], fill=coul)


def figure_purification_gasoil(chemin):
    im, d = _toile()
    f, fp = _police(40), _police(34)
    d.rounded_rectangle([60, 220, 480, 760], radius=18, outline=NOIR, width=4, fill=(230, 236, 245))
    d.rectangle([62, 640, 478, 758], fill=(205, 222, 240))
    d.text((270, 270), "Cuve du client", fill=NOIR, font=f, anchor="mm")
    d.text((270, 700), "eau et boues", fill=NOIR, font=fp, anchor="mm")
    _fleche(d, [(200, 690), (200, 110), (760, 110), (760, 230)])
    d.text((480, 70), "canne d'aspiration de fond", fill=NOIR, font=fp, anchor="mm")
    _boite(d, 640, 240, 240, 140, ["pompe"], f)
    _fleche(d, [(880, 310), (1010, 310)])
    _boite(d, 1020, 200, 300, 380, ["filtre", "séparateur", "d'eau"], f)
    d.ellipse([1135, 120, 1205, 190], outline=NOIR, width=4)
    d.text((1260, 155), "indicateur de colmatage", fill=NOIR, font=fp, anchor="lm")
    _fleche(d, [(1170, 580), (1170, 760)], EAU, 7, tirets=True)
    d.text((1200, 760), "purge de l'eau", fill=NOIR, font=fp, anchor="lm")
    _fleche(d, [(1320, 300), (1620, 300), (1620, 850), (380, 850), (380, 770)])
    d.text((1000, 820), "retour du gasoil filtré dans la cuve (boucle)", fill=NOIR, font=fp, anchor="mm")
    im.save(chemin, optimize=True)


def figure_deshydratation(chemin):
    im, d = _toile()
    f, fp = _police(38), _police(32)
    d.text((40, 420), "huile", fill=NOIR, font=fp)
    _fleche(d, [(40, 480), (150, 480)])
    _boite(d, 160, 400, 250, 160, ["préfiltre", "grossier"], f)
    _fleche(d, [(410, 480), (500, 480)])
    _boite(d, 510, 400, 280, 160, ["réchauffeur", "40 à 80 °C"], f)
    _fleche(d, [(790, 480), (880, 480)])
    _boite(d, 890, 230, 300, 520, ["colonne", "sous vide"], f, (230, 236, 245))
    _fleche(d, [(1040, 230), (1040, 120), (1300, 120)], EAU, 7, tirets=True)
    _boite(d, 1310, 60, 360, 130, ["pompe à vide"], f)
    d.text((1490, 240), "eau et gaz extraits", fill=NOIR, font=fp, anchor="mm")
    _fleche(d, [(1190, 650), (1310, 650)])
    _boite(d, 1320, 570, 300, 160, ["filtre fin"], f)
    _fleche(d, [(1470, 730), (1470, 840), (1100, 840)])
    d.text((900, 840), "huile déshydratée", fill=NOIR, font=fp, anchor="mm")
    im.save(chemin, optimize=True)


def figure_hydrocureur(chemin):
    im, d = _toile(1800, 800)
    f, fp = _police(38), _police(32)
    d.rounded_rectangle([600, 220, 1400, 520], radius=150, outline=NOIR, width=4, fill=(230, 236, 245))
    d.text((1000, 340), "citerne ADR", fill=NOIR, font=f, anchor="mm")
    d.text((1000, 400), "mise en dépression", fill=NOIR, font=fp, anchor="mm")
    _boite(d, 1420, 290, 200, 230, ["cabine"], f)
    d.rectangle([600, 520, 1620, 570], outline=NOIR, width=4, fill=FOND)
    for x in (720, 860, 1500):
        d.ellipse([x - 55, 545, x + 55, 655], outline=NOIR, width=4, fill=FOND)
    _boite(d, 820, 50, 360, 110, ["pompe à vide"], f)
    d.line([(1000, 160), (1000, 220)], fill=ACCENT, width=8)
    _boite(d, 80, 420, 160, 260, [], f)
    d.text((160, 720), "fût de 200 L", fill=NOIR, font=fp, anchor="mm")
    _fleche(d, [(160, 440), (160, 300), (480, 300), (590, 330)])
    d.text((330, 255), "flexible d'aspiration", fill=NOIR, font=fp, anchor="mm")
    im.save(chemin, optimize=True)


def figures():
    FIGURES.mkdir(exist_ok=True)
    figure_purification_gasoil(FIGURES / "purification_gasoil.png")
    figure_deshydratation(FIGURES / "deshydratation_sous_vide.png")
    figure_hydrocureur(FIGURES / "hydrocureur.png")


# --- dossier -----------------------------------------------------------------
def dossier():
    eq = _kit()
    plan = plan_acquisition()
    L = ["# Dossier technique des équipements", "",
         "## Objet et périmètre", "",
         "Le dossier décrit les équipements de la société de gestion des huiles usagées et de purification du gasoil, rangés par étape de sa trajectoire (décision D-09). "
         "Il accompagne en annexe le document de projet institutionnel et le business plan bancaire. Il sert de base aux demandes de prix, à la demande d'offre de crédit-bail "
         "et, à l'étape 3, à la description des installations dans l'évaluation environnementale.", "",
         "Les caractéristiques citées sont celles publiées par les fabricants et leurs revendeurs : ce sont des déclarations commerciales, à confirmer par devis. "
         "Aucun devis n'a encore été reçu ; aucun distributeur au Cameroun n'a été identifié pour les marques citées, sauf Toyota.", "",
         "| Code | Équipement | Étape | Mode d'acquisition |", "|---|---|---|---|"]
    for c, e in eq.items():
        L.append(f"| {c} | {e['fr']} | étape {CHOIX[c]['etape']} | {CHOIX[c]['mode']} |")
    L += ["", "Étapes : 0 amorçage et pilote ; 1 matériel loué, enlèvements sous-traités ; 2 équipement en crédit-bail ; 3 permis propre et camion ; 4 traitement, sous les conditions de la décision D-06.", "",
          "## Principe de fonctionnement", "",
          "### Purification du gasoil", "",
          "Le gasoil est aspiré au fond de la cuve du client, traverse un élément qui retient les particules et sépare l'eau, puis revient dans la cuve. "
          "L'opération se fait à froid, en boucle, sans entrée en cuve. L'eau purgée et les éléments usagés sont des déchets gérés comme les huiles usagées.", "",
          "![Figure 1 : principe de la purification du gasoil en boucle sur la cuve](figures/purification_gasoil.png)",
          "Source : schéma de principe établi pour le projet d'après les fiches Parker et Donaldson [S-92][S-93].", "",
          "### Déshydratation sous vide", "",
          "L'huile préfiltrée est chauffée, puis passe dans une colonne sous vide où l'eau et les fractions légères s'évaporent à basse température ; une filtration fine termine le traitement. "
          "Le procédé ne retire ni les additifs dégradés, ni les métaux dissous : il ne transforme pas une huile moteur usagée en huile neuve ni en carburant.", "",
          "![Figure 2 : principe de la déshydratation sous vide](figures/deshydratation_sous_vide.png)",
          "Source : schéma de principe établi pour le projet d'après la fiche Pall HNP [S-95] et le bilan matière du lot 5.", "",
          "### Collecte par citerne sous vide", "",
          "La pompe met la citerne en dépression ; l'huile est aspirée depuis le fût sans passer par la pompe, ce qui tolère l'eau, les boues et les débris des fûts forestiers.", "",
          "![Figure 3 : principe de la collecte par camion hydrocureur](figures/hydrocureur.png)",
          "Source : schéma de principe établi pour le projet d'après les annonces de camions hydrocureurs [S-101].", "",
          "## Fiches équipements", ""]
    for c, e in eq.items():
        ch = CHOIX[c]
        L += [f"### {c} {e['fr']}", "",
              "| Rubrique | Contenu |", "|---|---|",
              f"| Fonction | {e['fr']}, quantité : {e['qte']} |",
              f"| Spécifications minimales | {' ; '.join(e['spec_fr'])} |",
              f"| Référence recommandée | {ch['reco']} |",
              f"| Alternatives | {ch['alt']} |",
              f"| Étape et mode d'acquisition | étape {ch['etape']} ; {ch['mode']} |",
              f"| Points de vigilance | {ch['vig']} |", ""]
    L += ["## Matériel de terrain", "",
          "| Matériel | Référence recommandée | Caractéristique publiée |", "|---|---|---|",
          "| Bac de rétention pour 4 fûts | DENIOS base-line en polyéthylène [S-103] | 255 L de rétention |",
          "| Kit antipollution | DENIOS DENSORB, version hydrocarbures [S-103] | absorbants hydrophobes, version mobile sur chariot |",
          "| Pompe de transfert | Graco Husky 1050, pneumatique à membrane [S-104] | version UL décrite pour le gasoil et les huiles ; certification ATEX du modèle exact à confirmer |", "",
          "Chaque site client reçoit des fûts identifiés sur bac de rétention et un kit antipollution ; ces fournitures sont comprises dans le contrat annuel de conformité.", "",
          "## Exigences HSE et réglementaires", "",
          "| Domaine | Exigence | Équipements concernés |", "|---|---|---|",
          "| Transport de marchandises dangereuses | agrément ADR de la citerne, licence de transport du MINT [S-37], suivi GPS [S-38] | E6 |",
          "| Atmosphères explosives | matériel électrique adapté au gasoil près des cuves ; pompe à certification ATEX à vérifier | E1, pompe de transfert |",
          "| Métrologie | vérification par matériaux de référence certifiés selon ASTM D93-25 [S-98] | E3 |",
          "| Déchets | huiles contaminées par des halogènes refusées et éliminées séparément ; éléments filtrants usagés gérés comme déchets dangereux [S-02] | E1, E2, E4 |",
          "| Installation | évaluation environnementale du centre de transit par un bureau indépendant [S-33] ; autorisation d'établissement classé [S-35] | E2, E3, E6 |", "",
          "## Plan d'acquisition", "",
          "| Étape | Contenu | Mode | Montant prévu (M FCFA) | Hypothèse | État du devis |", "|---|---|---|---:|---|---|"]
    for et, contenu, mode, mt, hid, devis in plan:
        L.append(f"| {et} | {contenu} | {mode} | {m_fcfa(mt, 1)} | {hid} | {devis} |")
    L += ["", "Source : registre des hypothèses du projet ; les montants sont des hypothèses centrales, sans devis.", "",
          "Les montants des étapes 3 et 4 ne sont engagés qu'au franchissement des portes de décision ; ils ne font pas partie du financement demandé à la banque.", "",
          "## Points à confirmer", "",
          "1. Existence et prix d'une version 50 Hz des chariots Parker (Q-16).",
          "2. Prix rendu Douala d'un camion hydrocureur ADR d'occasion et coût de sa mise en conformité (Q-44).",
          "3. Distributeurs en Afrique centrale de Parker, Donaldson, Pall, HYDAC, Anton Paar et Dexsil, avec délais et service après-vente.",
          "4. Résultat d'un essai de déshydratation sur 20 L d'huile usagée locale, analysé par un laboratoire indépendant, avant tout achat d'un appareil de l'étape 4.",
          "5. Certification ATEX du modèle exact de pompe de transfert."]
    return "\n".join(L) + "\n"


def construire(pdf=True):
    figures()
    md = ICI / "dossier_equipements.md"
    md.write_text(dossier(), encoding="utf-8")
    liv = RACINE / "17_synthese" / "livrables"
    liv.mkdir(exist_ok=True)
    d = liv / f"{PREF} {NOM}.docx"
    off = dict(sous_titre="Société de gestion des huiles usagées et de purification du gasoil : annexe aux business plans",
               date=DATE_TXT, sources=RACINE / "00_registres" / "sources.md", pages_corps=PAGES_CORPS)
    docx_charte.convertir(md, d, titre_court="Dossier technique des équipements", reference=f"{PREF} {NOM}", officiel=off)
    if pdf:
        docx_charte.vers_pdf(d, liv)
        sys.path.insert(0, str(RACINE / "17_synthese"))
        from construire_business_plans import pages_corps_pdf
        n = pages_corps_pdf(liv / f"{PREF} {NOM}.pdf", MARQUEUR)
        if n != PAGES_CORPS:
            print(f"ATTENTION : le dossier compte {n} pages de corps ; mettre PAGES_CORPS a jour et relancer")
    return d


if __name__ == "__main__":
    construire(pdf="--sans-pdf" not in sys.argv)
    print("Dossier technique des equipements genere")
