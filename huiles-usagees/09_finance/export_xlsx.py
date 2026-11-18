"""Lot 9 : export du modele mensuel en .xlsx avec formules visibles.

Les lignes de chiffre d'affaires, de charges, d'EBITDA, de BFR, de flux et de tresorerie sont des formules
qui renvoient a la feuille Hypotheses. Les lignes d'amortissement, d'interets, de remboursement, d'impot,
d'investissement et de financement sont des valeurs calculees par le modele Python, signalees en italique.
Une ligne de controle compare la tresorerie de la formule et celle de Python.
"""
from pathlib import Path
import sys

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun.hypotheses import HYPOTHESES  # noqa: E402
import modele_mensuel as mm  # noqa: E402

ACCENT = "1F3864"
ENTETE = Font(name="Arial", bold=True, color="FFFFFF", size=9)
NORMAL = Font(name="Arial", size=9)
CALCULE = Font(name="Arial", size=9, italic=True)
FOND = PatternFill("solid", fgColor=ACCENT)
FICHIER = Path(__file__).with_name("modele_financier.xlsx")


def construire(chemin=FICHIER):
    p = mm.parametres()
    s, ind = mm.simuler(p)
    wb = Workbook()
    hy = wb.active
    hy.title = "Hypotheses"
    hy.append(["ID", "Libellé", "Bas", "Central", "Haut", "Unité", "Valeur retenue", "Statut", "Justification"])
    ref = {}
    for r, k in enumerate(mm.CLES, start=2):
        h = HYPOTHESES[k]
        hy.append([h.id, h.libelle, h.bas, h.central, h.haut, h.unite, f"=D{r}", h.statut, h.justification])
        ref[k] = f"Hypotheses!$G${r}"
    r_bascule = len(mm.CLES) + 3
    hy.cell(row=r_bascule, column=1, value="Mois de bascule en M1 (calculé par Python)").font = CALCULE
    hy.cell(row=r_bascule, column=7, value=ind["mois_bascule"]).font = CALCULE
    ref["bascule"] = f"Hypotheses!$G${r_bascule}"
    for c in range(1, 10):
        hy.cell(row=1, column=c).font = ENTETE
        hy.cell(row=1, column=c).fill = FOND
    hy.column_dimensions["B"].width = 60
    hy.column_dimensions["I"].width = 60

    ws = wb.create_sheet("Mensuel")
    ws.cell(row=1, column=1, value="Ligne (FCFA)")
    for m in range(1, mm.MOIS + 1):
        ws.cell(row=1, column=m + 1, value=m)
    lignes = {}

    def ligne(nom, formule=None, valeurs=None):
        r = len(lignes) + 2
        lignes[nom] = r
        ws.cell(row=r, column=1, value=nom).font = NORMAL
        for m in range(1, mm.MOIS + 1):
            col = get_column_letter(m + 1)
            prev = get_column_letter(m) if m > 1 else None
            if formule is not None:
                ws.cell(row=r, column=m + 1, value="=" + formule(m, col, prev)).font = NORMAL
            else:
                c = ws.cell(row=r, column=m + 1, value=float(valeurs[m - 1]))
                c.font = CALCULE
        return r

    R = lambda n, col: f"{col}{lignes[n]}"  # noqa: E731
    H = ref
    ligne("Mois", lambda m, c, p_: f"{c}$1")
    ligne("Clients forestiers", lambda m, c, p_: f"IF({c}$1<4,0,IF({c}$1<=12,2,2+({H['H-97']}-2)*({c}$1-12)/48))")
    ligne("CA contrats de conformité", lambda m, c, p_: f"{R('Clients forestiers', c)}*{H['H-80']}/12")
    ligne("CA purification du gasoil", lambda m, c, p_: f"{R('Clients forestiers', c)}*{H['H-82']}/12*{H['H-81']}")
    ligne("CA valeur des huiles remises", lambda m, c, p_: f"{R('Clients forestiers', c)}*{H['H-01']}/12*{H['H-83']}")
    ligne("CA commission urbaine (partenariat)", lambda m, c, p_: f"IF({c}$1<=12,0,{H['H-96']}*MIN(({c}$1-12)/48,1)/12*{H['H-21']})")
    ligne("CA activités d'amorçage (net)", lambda m, c, p_: f"IF({c}$1<=24,{H['H-161']},0)")
    ligne("Chiffre d'affaires", lambda m, c, p_: f"SUM({c}{lignes['CA contrats de conformité']}:{c}{lignes['CA activités d’amorçage (net)'.replace('’', chr(39))]})")
    ligne("Enlèvements sous-traités", lambda m, c, p_: f"{R('Clients forestiers', c)}*{H['H-88']}/12*{H['H-48']}")
    ligne("Consommables de purification", lambda m, c, p_: f"{R('Clients forestiers', c)}*{H['H-82']}/12*{H['H-87']}")
    ligne("Salaires chargés", lambda m, c, p_: f"IF({c}$1>=4,{H['H-151']},0)+IF({c}$1>=13,{H['H-150']}+{H['H-152']},0)")
    ligne("Frais généraux", lambda m, c, p_: f"IF({c}$1>=4,{H['H-153']},0)")
    ligne("Assurances", lambda m, c, p_: f"IF({c}$1>=4,{H['H-154']}/12,0)")
    ligne("Loyers de crédit-bail et location", lambda m, c, p_: f"IF({c}$1>={H['bascule']},0,IF({c}$1>=4,{H['H-94']}/12,0))")
    ligne("Charges d'exploitation", lambda m, c, p_: f"SUM({c}{lignes['Enlèvements sous-traités']}:{c}{lignes['Loyers de crédit-bail et location']})")
    ligne("EBITDA", lambda m, c, p_: f"{R(chr(67) + 'hiffre d' + chr(39) + 'affaires', c)}-{R('Charges d' + chr(39) + 'exploitation', c)}")
    ligne("Amortissements (Python)", valeurs=s["amortissement"])
    ligne("Intérêts (Python)", valeurs=s["interets"])
    ligne("Impôt (Python)", valeurs=s["impot"])
    ligne("Résultat net", lambda m, c, p_: f"{R('EBITDA', c)}-{R('Amortissements (Python)', c)}-{R('Intérêts (Python)', c)}-{R('Impôt (Python)', c)}")
    ligne("BFR", lambda m, c, p_: f"{R(chr(67) + 'hiffre d' + chr(39) + 'affaires', c)}*{H['H-155']}/30-({R('Enlèvements sous-traités', c)}+{R('Consommables de purification', c)})*{H['H-156']}/30")
    ligne("Variation du BFR", lambda m, c, p_: f"{R('BFR', c)}" + (f"-{R('BFR', p_)}" if p_ else ""))
    ligne("Investissements (Python)", valeurs=s["capex"])
    ligne("Flux de trésorerie disponible", lambda m, c, p_: f"{R('EBITDA', c)}-{R('Impôt (Python)', c)}-{R('Variation du BFR', c)}-{R('Investissements (Python)', c)}")
    ligne("Apport en capital (Python)", valeurs=s["apport"])
    ligne("Emprunt débloqué (Python)", valeurs=s["emprunt"])
    ligne("Remboursement d'emprunt (Python)", valeurs=s["remboursement"])
    ligne("Trésorerie de fin de mois", lambda m, c, p_: (f"{R('Trésorerie de fin de mois', p_)}+" if p_ else "")
          + f"{R('Flux de trésorerie disponible', c)}+{R('Apport en capital (Python)', c)}+{R('Emprunt débloqué (Python)', c)}-{R('Intérêts (Python)', c)}-{R('Remboursement d' + chr(39) + 'emprunt (Python)', c)}")
    ligne("Trésorerie selon Python", valeurs=s["tresorerie"])
    ligne("Contrôle : écart formule moins Python", lambda m, c, p_: f"{R('Trésorerie de fin de mois', c)}-{R('Trésorerie selon Python', c)}")
    for c in range(1, mm.MOIS + 2):
        ws.cell(row=1, column=c).font = ENTETE
        ws.cell(row=1, column=c).fill = FOND
    ws.column_dimensions["A"].width = 42
    ws.freeze_panes = "B2"

    an = wb.create_sheet("Annuel")
    an.append(["Ligne (FCFA)", "Année 1", "Année 2", "Année 3", "Année 4", "Année 5"])
    for nom, r in lignes.items():
        if nom in ("Mois", "Clients forestiers", "BFR", "Trésorerie de fin de mois", "Trésorerie selon Python", "Contrôle : écart formule moins Python"):
            continue
        row = [nom]
        for a in range(5):
            c1, c2 = get_column_letter(2 + 12 * a), get_column_letter(13 + 12 * a)
            row.append(f"=SUM(Mensuel!{c1}{r}:{c2}{r})")
        an.append(row)
    for c in range(1, 7):
        an.cell(row=1, column=c).font = ENTETE
        an.cell(row=1, column=c).fill = FOND
    an.column_dimensions["A"].width = 42

    ind_ws = wb.create_sheet("Indicateurs")
    ind_ws.append(["Indicateur (scénario de base, calculé par Python)", "Valeur"])
    for k, v in ind.items():
        ind_ws.append([k, str(v) if isinstance(v, dict) else v])
    for c in range(1, 3):
        ind_ws.cell(row=1, column=c).font = ENTETE
        ind_ws.cell(row=1, column=c).fill = FOND
    ind_ws.column_dimensions["A"].width = 50
    wb.save(chemin)
    return chemin, lignes


if __name__ == "__main__":
    print("Export :", construire()[0].name)
