"""Documents PDF (bordereau de suivi, rapport annuel client) et QR codes des futs."""
import io

import segno
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ACCENT = colors.HexColor("#1F3864")
STYLE = ParagraphStyle("normal", fontName="Helvetica", fontSize=10, leading=13)
TITRE = ParagraphStyle("titre", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=ACCENT, spaceAfter=8)
SOUS = ParagraphStyle("sous", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=ACCENT, spaceBefore=8, spaceAfter=4)


def qr_svg(texte):
    buf = io.BytesIO()
    segno.make(texte, error="m").save(buf, kind="svg", scale=4, border=2)
    return buf.getvalue()


def _table(data, largeurs):
    t = Table(data, colWidths=largeurs, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), ACCENT), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                           ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9),
                           ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _pdf(elements, mention):
    buf = io.BytesIO()

    def pied(canvas, doc):
        canvas.setFont("Helvetica", 8)
        canvas.drawString(2 * cm, 1.2 * cm, mention)
        canvas.drawRightString(19 * cm, 1.2 * cm, f"Page {doc.page}")

    SimpleDocTemplate(buf, pagesize=A4, leftMargin=3 * cm, rightMargin=2 * cm, topMargin=2.5 * cm, bottomMargin=2.5 * cm).build(
        elements, onFirstPage=pied, onLaterPages=pied)
    return buf.getvalue()


def bordereau_pdf(enl, site, client, futs, societe="[Dénomination de la société]"):
    fictif = " (DONNÉES FICTIVES DE DÉMONSTRATION)" if client.get("fictif") else ""
    el = [Paragraph(f"Bordereau de suivi des déchets dangereux n° {enl['bordereau']}{fictif}", TITRE),
          Paragraph("Huiles usagées et déchets associés. Quatre exemplaires : producteur, transporteur, destinataire, société.", STYLE),
          Paragraph("Producteur", SOUS),
          _table([["Rubrique", "Renseignement"], ["Raison sociale", client["nom"]], ["Site", site["nom"]],
                  ["Coordonnées", f"{site.get('latitude') or ''} ; {site.get('longitude') or ''}"]], [5 * cm, 11 * cm]),
          Paragraph("Déchet", SOUS),
          _table([["Rubrique", "Renseignement"], ["Nature", "huiles moteur, hydrauliques et de transmission usagées"],
                  ["Volume", f"{enl['volume_l']:.0f} L"], ["Dépistage halogènes", enl["depistage"]],
                  ["Fûts", ", ".join(f["code"] for f in futs) or "vrac"]], [5 * cm, 11 * cm]),
          Paragraph("Transport et destination", SOUS),
          _table([["Rubrique", "Renseignement"], ["Transporteur", enl.get("transporteur") or ""],
                  ["Date de prise en charge", enl.get("date_realisee") or ""], ["Destinataire", ""], ["Opération", ""]], [5 * cm, 11 * cm]),
          Spacer(1, 12),
          _table([["Signature du producteur", "Signature du transporteur", "Signature du destinataire"], ["\n\n\n", "", ""]],
                 [5.3 * cm, 5.3 * cm, 5.4 * cm])]
    return _pdf(el, f"{societe} : bordereau {enl['bordereau']}")


def rapport_pdf(rapport, societe="[Dénomination de la société]"):
    c = rapport["client"]
    fictif = " (DONNÉES FICTIVES DE DÉMONSTRATION)" if c.get("fictif") else ""
    lignes = [["Date", "Site", "Bordereau", "Volume (L)", "Dépistage"]] + [
        [e["date_realisee"], e["site"], e["bordereau"], f"{e['volume_l']:.0f}", e["depistage"]] for e in rapport["enlevements"]]
    el = [Paragraph(f"Rapport annuel d'activité {rapport['annee']} : {c['nom']}{fictif}", TITRE),
          Paragraph("Rapport factuel des enlèvements d'huiles usagées réalisés pour le client, utilisable pour le suivi du PGES et les audits. "
                    "Il ne constitue ni un audit, ni un avis sur la conformité réglementaire du client.", STYLE),
          Paragraph("Synthèse", SOUS),
          _table([["Indicateur", "Valeur"], ["Enlèvements réalisés", str(len(rapport["enlevements"]))],
                  ["Volume total enlevé (L)", f"{rapport['volume_total_l']:.0f}"],
                  ["Lots positifs au dépistage", str(rapport["positifs"])]], [8 * cm, 8 * cm]),
          Paragraph("Détail des enlèvements", SOUS), _table(lignes, [2.5 * cm, 4.5 * cm, 3.5 * cm, 2.5 * cm, 3 * cm])]
    return _pdf(el, f"{societe} : rapport annuel {rapport['annee']}")
