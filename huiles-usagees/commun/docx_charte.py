"""Conversion d'un Markdown simple en .docx selon la charte typographique retenue (D-02) :
A4, marges 2,5 / 2,5 / 3 / 2 cm, Arial 11 justifie, interligne 1,15, 6 pt apres ; titres en bleu marine 1F3864 ;
tableaux a en-tete colore repete ; champs [a completer] surlignes en jaune ; en-tete et pied de page.

Syntaxe reconnue : # titre du document, ## titre de niveau 1, ### niveau 2, #### niveau 3, paragraphes,
listes a puces (- ), listes numerotees (1. ), cases a cocher (- [ ] ), tableaux Markdown, citations (> ),
**gras**, `code`, saut de page (---page---).
"""
from pathlib import Path
import re
import subprocess

from docx import Document
from docx.enum.section import WD_ORIENT  # noqa: F401
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ACCENT = RGBColor(0x1F, 0x38, 0x64)
PROJET = "Collecte et valorisation des huiles usagées"


def _police(run, taille=11, gras=False, italique=False, couleur=None):
    run.font.name = "Arial"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    run.font.size = Pt(taille)
    run.bold = gras
    run.italic = italique
    if couleur is not None:
        run.font.color.rgb = couleur


def _inline(par, texte, taille=11, gras_defaut=False, couleur=None):
    """Gere **gras**, `code` et les champs [a completer] surlignes."""
    jetons = re.split(r"(\*\*[^*]+\*\*|\[[^\]]+\]|`[^`]+`)", texte)
    for j in jetons:
        if not j:
            continue
        if j.startswith("**") and j.endswith("**"):
            r = par.add_run(j[2:-2])
            _police(r, taille, True, couleur=couleur)
        elif j.startswith("[") and j.endswith("]") and not re.fullmatch(r"\[(S|H|Q|D)-\d+\]", j):
            r = par.add_run(j)
            _police(r, taille, gras_defaut, couleur=couleur)
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
        elif j.startswith("`") and j.endswith("`"):
            r = par.add_run(j[1:-1])
            _police(r, taille, gras_defaut, couleur=couleur)
        else:
            r = par.add_run(j)
            _police(r, taille, gras_defaut, couleur=couleur)


def _format_par(par, apres=6, justifie=True):
    pf = par.paragraph_format
    pf.space_after = Pt(apres)
    pf.space_before = Pt(0)
    pf.line_spacing = 1.15
    pf.widow_control = True
    if justifie:
        par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def _filet(par):
    p = par._p
    pPr = p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bas = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", "6"), ("w:space", "1"), ("w:color", "1F3864")):
        bas.set(qn(k), v)
    bdr.append(bas)
    pPr.append(bdr)


def _cellule_fond(cell, couleur="1F3864"):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), couleur)
    tcPr.append(shd)


def _bordures(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for cote in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{cote}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), "808080")
        b.append(e)
    tblPr.append(b)


def _repeter_entete(row):
    trPr = row._tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader")
    h.set(qn("w:val"), "true")
    trPr.append(h)
    cs = OxmlElement("w:cantSplit")
    trPr.append(cs)


def _champ(par, code):
    r = par.add_run()
    _police(r, 8)
    f1 = OxmlElement("w:fldChar")
    f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = code
    f2 = OxmlElement("w:fldChar")
    f2.set(qn("w:fldCharType"), "end")
    r._r.append(f1)
    r._r.append(it)
    r._r.append(f2)


def _entete_pied(doc, titre_court, reference):
    s = doc.sections[0]
    s.header_distance = Cm(1.25)
    s.footer_distance = Cm(1.25)
    h = s.header.paragraphs[0]
    h.text = ""
    r = h.add_run(PROJET + "\t\t" + titre_court)
    _police(r, 8)
    _filet(h)
    f = s.footer.paragraphs[0]
    f.text = ""
    r = f.add_run(reference + "\t\tPage ")
    _police(r, 8)
    _champ(f, "PAGE")
    r = f.add_run(" sur ")
    _police(r, 8)
    _champ(f, "NUMPAGES")


SIGLES = {
    "AGF": "African Guarantee Fund", "ASTM": "American Society for Testing and Materials", "BEAC": "Banque des États de l'Afrique centrale",
    "CA": "chiffre d'affaires", "CDEC": "Caisse des dépôts et consignations du Cameroun", "CEMAC": "Communauté économique et monétaire de l'Afrique centrale",
    "CFCE": "Centre de formalités de création d'entreprises", "DSCR": "ratio de couverture du service de la dette",
    "EBITDA": "excédent brut d'exploitation", "EIES": "étude d'impact environnemental et social", "FCFA": "franc de la Coopération financière en Afrique centrale",
    "FSC": "Forest Stewardship Council", "HSE": "hygiène, sécurité et environnement", "HT": "hors taxes",
    "MINEPDED": "ministère de l'Environnement, de la Protection de la Nature et du Développement durable", "MINEFOP": "ministère de l'Emploi et de la Formation professionnelle",
    "MINFOF": "ministère des Forêts et de la Faune", "MINMIDT": "ministère des Mines, de l'Industrie et du Développement technologique",
    "MINT": "ministère des Transports", "OHADA": "Organisation pour l'harmonisation en Afrique du droit des affaires", "OLB": "Origine et légalité des bois",
    "PCB": "polychlorobiphényles", "PGES": "plan de gestion environnementale et sociale", "PME": "petite et moyenne entreprise",
    "QR": "quick response (code-barres en deux dimensions)", "RCCM": "registre du commerce et du crédit mobilier", "SARL": "société à responsabilité limitée",
    "TRI": "taux de rentabilité interne", "UTB": "unité de transformation du bois", "VAN": "valeur actuelle nette",
}


def _num_pages(section, fmt, debut=None):
    sectPr = section._sectPr
    pg = OxmlElement("w:pgNumType")
    pg.set(qn("w:fmt"), fmt)
    if debut is not None:
        pg.set(qn("w:start"), str(debut))
    sectPr.append(pg)


def _pied(section, reference, total):
    section.footer.is_linked_to_previous = False
    f = section.footer.paragraphs[0]
    f.text = ""
    r = f.add_run(reference + "\t\tPage ")
    _police(r, 8)
    _champ(f, "PAGE")
    if total:
        r = f.add_run(" sur ")
        _police(r, 8)
        if str(total).isdigit():
            r = f.add_run(str(total))
            _police(r, 8)
        else:
            _champ(f, total)


def _references(texte, sources_md):
    ids = sorted(set(re.findall(r"\[(S-\d+)\]", texte)), key=lambda x: int(x[2:]))
    table = {}
    for l in Path(sources_md).read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| (S-\d+) \| ([^|]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|", l)
        if m:
            table[m.group(1)] = [x.strip() for x in m.groups()[1:]]
    return [f"[{i}] {table[i][0]}, {table[i][1]}, {table[i][2]}, {table[i][3]}." for i in ids if i in table]


def _prelim(doc, off, titre, texte):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(200)
    _inline(p, titre, 24, True, ACCENT)
    _filet(p)
    for t, taille in ((off.get("sous_titre", ""), 14), (off.get("date", ""), 12)):
        q = doc.add_paragraph()
        _inline(q, t, taille)
        _format_par(q, apres=6, justifie=False)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def titre_prelim(t):
        q = doc.add_paragraph()
        _inline(q, t.upper(), 14, True, ACCENT)
        _format_par(q, apres=6, justifie=False)
        _filet(q)

    def tab(lignes):
        t = doc.add_table(rows=len(lignes), cols=len(lignes[0]))
        _bordures(t)
        for ri, row in enumerate(lignes):
            for ci, v in enumerate(row):
                c = t.cell(ri, ci)
                pp = c.paragraphs[0]
                _format_par(pp, apres=0, justifie=False)
                if ri == 0:
                    _cellule_fond(c)
                    _inline(pp, v, 9, True, RGBColor(0xFF, 0xFF, 0xFF))
                else:
                    _inline(pp, v, 9)
        _repeter_entete(t.rows[0])
        doc.add_paragraph()

    titre_prelim("Fiche de contrôle")
    tab([["", "Préparé", "Vérifié", "Approuvé"], ["Fonction", "chef de projet", "[contre-expert ou relecteur]", "[promoteur]"],
         ["Nom", "[ ]", "[ ]", "[ ]"], ["Date", off.get("date", ""), "[ ]", "[ ]"], ["Visa", "", "", ""]])
    titre_prelim("Sommaire")
    n = 0
    for l in texte.splitlines():
        if l.startswith("## "):
            h = l[3:].strip()
            q = doc.add_paragraph()
            if h in NON_NUMEROTES:
                _inline(q, h)
            else:
                n += 1
                _inline(q, f"{n}  {h}")
            _format_par(q, apres=2, justifie=False)
    q = doc.add_paragraph()
    _inline(q, "Références")
    titre_prelim("Liste des sigles")
    presents = [k for k in sorted(SIGLES) if re.search(r"(?<![\w-])" + re.escape(k) + r"(?![\w-])", texte)]
    tab([["Sigle", "Signification"]] + [[k, SIGLES[k]] for k in presents])


NON_NUMEROTES = {"Résumé exécutif", "Fiche signalétique du projet", "Résumé du projet"}


def convertir(md_path, docx_path, titre_court=None, reference=None, officiel=None):
    texte = Path(md_path).read_text(encoding="utf-8")
    doc = Document()
    s = doc.sections[0]
    s.page_height, s.page_width = Cm(29.7), Cm(21.0)
    s.top_margin, s.bottom_margin, s.left_margin, s.right_margin = Cm(2.5), Cm(2.5), Cm(3), Cm(2)
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(11)
    lignes = texte.splitlines()
    titre = next((l[2:].strip() for l in lignes if l.startswith("# ")), Path(md_path).stem)
    _entete_pied(doc, titre_court or titre[:60], reference or Path(md_path).stem)
    num_chap = 0
    if officiel:
        s.different_first_page_header_footer = True
        _num_pages(s, "lowerRoman", 1)
        _pied(s, reference or Path(md_path).stem, None)
        _prelim(doc, officiel, titre, texte)
        corps = doc.add_section()
        _num_pages(corps, "decimal", 1)
        corps.different_first_page_header_footer = False
        _pied(corps, reference or Path(md_path).stem, officiel.get("pages_corps") or "SECTIONPAGES")
        refs = _references(texte, officiel["sources"])
        lignes = [l for l in lignes if not l.startswith("# ")] + ["", "## Références", ""] + refs
    i = 0
    while i < len(lignes):
        l = lignes[i].rstrip()
        if not l.strip():
            i += 1
            continue
        if l.strip() == "---page---":
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            i += 1
            continue
        if l.startswith("|"):
            bloc = []
            while i < len(lignes) and lignes[i].startswith("|"):
                bloc.append(lignes[i])
                i += 1
            rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in bloc if not re.fullmatch(r"\|[\s:|-]+\|?", r.strip())]
            ncol = max(len(r) for r in rows)
            t = doc.add_table(rows=len(rows), cols=ncol)
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            _bordures(t)
            for ri, row in enumerate(rows):
                for ci in range(ncol):
                    val = row[ci] if ci < len(row) else ""
                    cell = t.cell(ri, ci)
                    p = cell.paragraphs[0]
                    _format_par(p, apres=0, justifie=False)
                    num = re.fullmatch(r"[-\d\s ,%.]+", val.replace("**", "")) is not None and val.strip() != ""
                    if num:
                        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    if ri == 0:
                        _cellule_fond(cell)
                        _inline(p, val.replace("**", ""), 9, True, RGBColor(0xFF, 0xFF, 0xFF))
                    else:
                        _inline(p, val, 9)
                if ri == 0:
                    _repeter_entete(t.rows[0])
                else:
                    trPr = t.rows[ri]._tr.get_or_add_trPr()
                    trPr.append(OxmlElement("w:cantSplit"))
            doc.add_paragraph()
            continue
        if l.startswith("# "):
            p = doc.add_paragraph()
            _inline(p, l[2:].strip(), 16, True, ACCENT)
            _format_par(p, apres=12, justifie=False)
            _filet(p)
        elif l.startswith("## "):
            h = l[3:].strip()
            if officiel and h not in NON_NUMEROTES and h != "Références":
                num_chap += 1
                h = f"{num_chap}  {h}"
            p = doc.add_paragraph()
            if officiel and (num_chap >= 1 or h == "Références"):
                p.paragraph_format.page_break_before = True
            _inline(p, h.upper(), 14, True, ACCENT)
            _format_par(p, apres=6, justifie=False)
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.keep_with_next = True
            _filet(p)
        elif l.startswith("### "):
            p = doc.add_paragraph()
            _inline(p, l[4:].strip(), 12, True, ACCENT)
            _format_par(p, apres=6, justifie=False)
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.keep_with_next = True
        elif l.startswith("#### "):
            p = doc.add_paragraph()
            _inline(p, l[5:].strip(), 11, True)
            _format_par(p, apres=6, justifie=False)
            p.paragraph_format.keep_with_next = True
        elif re.match(r"^\s*- \[ \] ", l):
            p = doc.add_paragraph()
            _inline(p, "☐ " + re.sub(r"^\s*- \[ \] ", "", l))
            _format_par(p, apres=3)
        elif re.match(r"^\s*- ", l):
            niveau = 1 if l.startswith("  ") else 0
            p = doc.add_paragraph(style="List Bullet 2" if niveau else "List Bullet")
            _inline(p, re.sub(r"^\s*- ", "", l))
            _format_par(p, apres=3)
        elif re.match(r"^\d+\. ", l):
            p = doc.add_paragraph(style="List Number")
            _inline(p, re.sub(r"^\d+\. ", "", l))
            _format_par(p, apres=3)
        elif l.startswith(">"):
            p = doc.add_paragraph()
            _inline(p, l.lstrip("> ").strip())
            _format_par(p)
            p.paragraph_format.left_indent = Cm(1)
        else:
            p = doc.add_paragraph()
            _inline(p, l.strip())
            _format_par(p)
        i += 1
    doc.save(docx_path)
    from commun.deterministe import figer
    figer(docx_path)
    return docx_path


def vers_pdf(docx_path, dossier):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(dossier), str(docx_path)],
                   check=True, capture_output=True, timeout=180)
