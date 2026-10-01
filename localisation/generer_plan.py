from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
import math
OUT="/home/user/petrosmart-tools/localisation/plan_localisation_RCCM.pdf"
W,H=A4
c=canvas.Canvas(OUT,pagesize=A4)
c.setTitle("Plan de localisation - Dossier RCCM"); c.setAuthor("")
ROAD=HexColor("#d9d9d9"); EDGE=HexColor("#555555"); BLD=HexColor("#f2e6c9"); RED=HexColor("#c0392b")
# Titre
c.setFont("Helvetica-Bold",18); c.drawCentredString(W/2,H-50,"PLAN DE LOCALISATION")
c.setFont("Helvetica",10.5); c.drawCentredString(W/2,H-66,"Pièce jointe au dossier d'immatriculation au Registre du Commerce et du Crédit Mobilier (RCCM)")
# Cadre carte
fx,fy,fw,fh=40,255,W-80,H-345
c.setLineWidth(1.2); c.setStrokeColor(black); c.rect(fx,fy,fw,fh)
c.saveState(); p=c.beginPath(); p.rect(fx,fy,fw,fh); c.clipPath(p,stroke=0,fill=0)
c.setFillColor(HexColor("#fbfbf7")); c.rect(fx,fy,fw,fh,fill=1,stroke=0)
def band(pts,w):
    c.setStrokeColor(EDGE); c.setLineWidth(w+2.5); c.setLineCap(0); c.setLineJoin(1)
    pa=c.beginPath(); pa.moveTo(*pts[0]); [pa.lineTo(*q) for q in pts[1:]]; c.drawPath(pa,stroke=1,fill=0)
def band_fill(pts,w):
    c.setStrokeColor(ROAD); c.setLineWidth(w); c.setLineJoin(1)
    pa=c.beginPath(); pa.moveTo(*pts[0]); [pa.lineTo(*q) for q in pts[1:]]; c.drawPath(pa,stroke=1,fill=0)
mx=165; rbx,rby=mx,330
roads=[([(mx,fy-10),(mx,fy+fh-110)],34),
       ([(mx,fy+fh-110),(mx-70,fy+fh+20)],28),
       ([(mx,fy+fh-110),(mx+45,fy+fh+20)],28),
       ([(rbx,rby),(fx+fw+20,rby+75)],30),
       ([(mx,650),(fx+fw+20,650)],26)]
for pts,w in roads: band(pts,w)
c.setFillColor(EDGE); c.circle(rbx,rby,40,fill=1,stroke=0)
for pts,w in roads: band_fill(pts,w)
c.setFillColor(ROAD); c.circle(rbx,rby,38.7,fill=1,stroke=0)
c.setFillColor(HexColor("#9fc89a")); c.setStrokeColor(EDGE); c.setLineWidth(1); c.circle(rbx,rby,14,fill=1,stroke=1)
# axe central pointillé
c.setDash(6,5); c.setStrokeColor(white); c.setLineWidth(1)
c.line(mx,fy,mx,rby-40); c.line(mx,rby+40,mx,fy+fh-112); c.line(mx+20,650,fx+fw,650)
ang=math.atan2(75,fx+fw+20-rbx); c.line(rbx+40*math.cos(ang),rby+40*math.sin(ang),fx+fw,rby+75*(fx+fw-rbx)/(fx+fw+20-rbx))
c.setDash()
# Bâtiments
c.setStrokeColor(black); c.setLineWidth(1.2); c.setFillColor(BLD)
c.rect(205,425,190,160,fill=1,stroke=1); c.rect(395,430,125,155,fill=1,stroke=1)
c.setFillColor(black); c.setFont("Helvetica-Bold",14); c.drawCentredString(300,508,"LYCÉE BILINGUE")
c.setFont("Helvetica",9); c.drawCentredString(457,505,"Bâtiment voisin")
# Repères triangles
c.setFillColor(HexColor("#7f8c8d")); c.setStrokeColor(black)
for tx in (232,295):
    pa=c.beginPath(); pa.moveTo(tx-18,630); pa.lineTo(tx+18,630); pa.lineTo(tx,600); pa.close(); c.drawPath(pa,fill=1,stroke=1)
# Site
sx,sy=478,613
c.setFillColor(RED); c.setStrokeColor(black); c.setLineWidth(1.5); c.rect(sx-28,sy-14,56,28,fill=1,stroke=1)
c.setFillColor(white); c.setFont("Helvetica-Bold",11); c.drawCentredString(sx,sy-4,"SITE")
c.setStrokeColor(RED); c.setLineWidth(2); c.circle(sx,sy,42,fill=0,stroke=1)
c.setFillColor(RED); c.setFont("Helvetica-Bold",10); c.drawRightString(sx-48,sy-4,"NOUS SOMMES ICI  →")
# Libellés voies
c.setFillColor(black); c.setFont("Helvetica-Oblique",10)
c.saveState(); c.translate(rbx+150,rby+21); c.rotate(math.degrees(ang)); c.drawString(0,0,"Vers NKOLMESSENG  →"); c.restoreState()
c.saveState(); c.translate(mx-25,470); c.rotate(90); c.drawCentredString(0,0,"Route principale"); c.restoreState()
c.setFont("Helvetica",9); c.drawString(rbx+45,rby-48,"Carrefour / rond-point")
c.drawString(200,668,"Voie d'accès au site")
c.restoreState()
# Nord
nx,ny=fx+fw-35,fy+fh-55
c.setFillColor(black); pa=c.beginPath(); pa.moveTo(nx,ny+30); pa.lineTo(nx-11,ny-10); pa.lineTo(nx,ny); pa.close(); c.drawPath(pa,fill=1,stroke=0)
c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(1); pa=c.beginPath(); pa.moveTo(nx,ny+30); pa.lineTo(nx+11,ny-10); pa.lineTo(nx,ny); pa.close(); c.drawPath(pa,fill=1,stroke=1)
c.setFillColor(black); c.setFont("Helvetica-Bold",13); c.drawCentredString(nx,ny+35,"N")
c.setFont("Helvetica-Oblique",8); c.drawString(fx+6,fy+6,"Croquis non à l'échelle, orientation approximative")
# Légende
ly=fy-20; c.setFont("Helvetica-Bold",10); c.drawString(fx,ly,"LÉGENDE")
items=[("road","Voie"),("bld","Bâtiment / repère"),("tri","Repère existant"),("site","Emplacement de l'entreprise")]
x=fx; y=ly-20; c.setFont("Helvetica",9)
for k,t in items:
    if k=="road": c.setFillColor(ROAD); c.setStrokeColor(EDGE); c.rect(x,y-2,22,10,fill=1,stroke=1)
    if k=="bld": c.setFillColor(BLD); c.setStrokeColor(black); c.rect(x,y-2,22,10,fill=1,stroke=1)
    if k=="tri":
        c.setFillColor(HexColor("#7f8c8d")); pa=c.beginPath(); pa.moveTo(x+3,y+8); pa.lineTo(x+19,y+8); pa.lineTo(x+11,y-3); pa.close(); c.drawPath(pa,fill=1,stroke=1)
    if k=="site": c.setFillColor(RED); c.rect(x,y-2,22,10,fill=1,stroke=1)
    c.setFillColor(black); c.drawString(x+28,y,t); x+=118
# Cartouche avec champs remplissables
cy=22; ch=180; c.setLineWidth(1); c.rect(fx,cy,fw,ch)
c.setFont("Helvetica-Bold",10); c.drawString(fx+8,cy+ch-16,"IDENTIFICATION")
rows=[("Raison sociale / Nom commercial","raison"),("Nom du promoteur / gérant","promoteur"),("Activité","activite"),
      ("Adresse : quartier, ville","adresse"),("Téléphone","tel"),("Repère complémentaire","repere")]
form=c.acroForm; y=cy+ch-40
for lab,name in rows:
    c.setFont("Helvetica",9); c.drawString(fx+8,y+4,lab+" :")
    form.textfield(name=name,x=fx+175,y=y,width=fw-185,height=16,fontSize=9,borderWidth=0,fillColor=HexColor("#f4f7fb"),borderColor=white,forceBorder=False)
    c.setStrokeColor(HexColor("#999999")); c.setLineWidth(0.5); c.line(fx+175,y,fx+fw-10,y); y-=21
c.setStrokeColor(black); c.setFont("Helvetica",9)
c.drawString(fx+8,cy+12,"Fait à Yaoundé, le :"); form.textfield(name="date",x=fx+95,y=cy+8,width=120,height=16,fontSize=9,borderWidth=0,fillColor=HexColor("#f4f7fb"))
c.drawString(fx+fw-200,cy+12,"Signature :")
c.showPage(); c.save(); print(OUT)
