from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
import math
OUT="/home/user/petrosmart-tools/localisation/plan_localisation_Boubakari_Oumarou.pdf"
W,H=A4
c=canvas.Canvas(OUT,pagesize=A4)
c.setTitle("Plan de localisation - M. Boubakari Oumarou")
ROAD=HexColor("#d9d9d9"); EDGE=HexColor("#555555"); BLD=HexColor("#f2e6c9"); RED=HexColor("#c0392b"); GREEN=HexColor("#9fc89a")
c.setFont("Helvetica-Bold",20); c.drawCentredString(W/2,H-52,"PLAN DE LOCALISATION")
c.setFont("Helvetica-Bold",13); c.drawCentredString(W/2,H-74,"M. BOUBAKARI OUMAROU")
c.setFont("Helvetica",10); c.drawCentredString(W/2,H-90,"Yaoundé, secteur Omnisport / Lycée Bilingue / Nkolmesseng")
fx,fy,fw,fh=40,175,W-80,H-285
c.setLineWidth(1.2); c.rect(fx,fy,fw,fh)
c.saveState(); p=c.beginPath(); p.rect(fx,fy,fw,fh); c.clipPath(p,stroke=0,fill=0)
c.setFillColor(HexColor("#fbfbf7")); c.rect(fx,fy,fw,fh,fill=1,stroke=0)
# géométrie
A=(140,672)   # Carrefour Mobil Omnisport
B=(255,280)   # Carrefour Lycée Bilingue
def main(pa):
    pa.moveTo(*A); pa.curveTo(215,582,240,540,240,450); pa.curveTo(240,360,250,320,B[0],B[1]); pa.lineTo(260,fy-20)
def lin(pts):
    def f(pa):
        pa.moveTo(*pts[0]); [pa.lineTo(*q) for q in pts[1:]]
    return f
def side(pa):
    pa.moveTo(240,505); pa.lineTo(400,510); pa.curveTo(470,512,520,490,fx+fw+30,440)
roads=[(main,36),(lin([A,(fx+fw+30,720)]),30),
       (lin([B,(fx+fw+30,375)]),32),(side,26)]
def stroke(fn,w,col):
    c.setStrokeColor(col); c.setLineWidth(w); c.setLineJoin(1); c.setLineCap(0)
    pa=c.beginPath(); fn(pa); c.drawPath(pa,stroke=1,fill=0)
for fn,w in roads: stroke(fn,w+2.5,EDGE)
for (x,y),r in ((A,46),(B,42)): c.setFillColor(EDGE); c.circle(x,y,r+1.3,fill=1,stroke=0)
for fn,w in roads: stroke(fn,w,ROAD)
for (x,y),r in ((A,46),(B,42)):
    c.setFillColor(ROAD); c.circle(x,y,r,fill=1,stroke=0)
    c.setFillColor(GREEN); c.setStrokeColor(EDGE); c.setLineWidth(1); c.circle(x,y,15,fill=1,stroke=1)
# Lycée (îlot entre route principale, voie latérale et route de Nkolmesseng)
sl=(375-B[1])/(fx+fw+30-B[0])
yb=lambda x: B[1]+sl*(x-B[0])+30
c.setFillColor(BLD); c.setStrokeColor(black); c.setLineWidth(1.2)
pa=c.beginPath(); pa.moveTo(272,yb(272)); pa.lineTo(520,yb(520)); pa.lineTo(520,450); pa.lineTo(272,450); pa.close(); c.drawPath(pa,fill=1,stroke=1)
c.setFillColor(black); c.setFont("Helvetica-Bold",14); c.drawCentredString(395,405,"LYCÉE BILINGUE")
c.drawCentredString(395,388,"DE YAOUNDÉ")
# Site
sx,sy=420,474
c.setFillColor(RED); c.setStrokeColor(black); c.setLineWidth(1.5); c.rect(sx-26,sy-11,52,22,fill=1,stroke=1)
c.setFillColor(white); c.setFont("Helvetica-Bold",11); c.drawCentredString(sx,sy-4,"ICI")
c.setStrokeColor(RED); c.setLineWidth(2); c.circle(sx,sy,36,fill=0,stroke=1)
# Libellés
c.setFillColor(black)
def lab(x,y,a,t,font="Helvetica-Bold",s=10):
    c.saveState(); c.translate(x,y); c.rotate(a); c.setFont(font,s); c.drawCentredString(0,0,t); c.restoreState()
c.setFont("Helvetica-Bold",9.5)
c.drawString(A[0]+52,A[1]-48,"CARREFOUR MOBIL OMNISPORT")
c.drawString(B[0]+48,B[1]-38,"CARREFOUR LYCÉE BILINGUE")
lab(380,692,math.degrees(math.atan2(720-A[1],fx+fw+30-A[0])),"Vers NGOUSSO  →","Helvetica-Oblique")
lab(236,430,90,"Vers OMNISPORT  →","Helvetica-Oblique")
lab(440,330,math.degrees(math.atan(sl)),"Vers NKOLMESSENG  →","Helvetica-Oblique")
c.setFont("Helvetica",8.5); c.setFillColor(RED); c.setFont("Helvetica-Bold",10); c.drawRightString(sx-42,sy-4,"DOMICILE")
c.restoreState()
c.setFont("Helvetica-Oblique",8); c.drawString(fx+6,fy+6,"Croquis non à l'échelle")
# Légende
ly=fy-18; c.setFont("Helvetica-Bold",10); c.drawString(fx,ly,"LÉGENDE")
x=fx+58; c.setFont("Helvetica",9); y=ly
def sw(col,t,w=22):
    global x
    c.setFillColor(col); c.setStrokeColor(EDGE); c.rect(x,y-2,w,10,fill=1,stroke=1)
    c.setFillColor(black); c.drawString(x+w+6,y,t); x+=w+6+c.stringWidth(t,"Helvetica",9)+12
sw(ROAD,"Voie"); sw(GREEN,"Carrefour"); sw(BLD,"Établissement scolaire"); sw(RED,"Emplacement")
# Contacts
cy=40; ch=95; c.setStrokeColor(black); c.setLineWidth(1); c.rect(fx,cy,fw,ch)
c.setFont("Helvetica-Bold",11); c.drawString(fx+12,cy+ch-20,"CONTACTS")
c.setFont("Helvetica",11)
c.drawString(fx+12,cy+ch-45,"M. Boubakari Oumarou"); c.drawRightString(fx+fw-12,cy+ch-45,"Tél. : 699 23 36 64")
c.drawString(fx+12,cy+ch-70,"Personne à contacter : M. Bouba Sanda"); c.drawRightString(fx+fw-12,cy+ch-70,"Tél. : 695 29 39 79")
c.showPage(); c.save(); print(OUT)
