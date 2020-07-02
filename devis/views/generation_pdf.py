import io

from django.contrib.staticfiles.finders import find
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib import colors
from reportlab.lib.colors import red, black, white, green, grey
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from django.templatetags.static import static
from devis.models import Devis, PrestationCoutFixe, PrestationCoutVariableConcrete, PrestationPneumatique

from reportlab.lib.units import cm

largeur, hauteur = A4


def setDecoration(c):
    c.setFillColor(colors.HexColor("#212121"))
    c.rect(0, hauteur - 1.6 * cm, largeur - 3 * cm, 0.5 * cm, fill=1, stroke=0)

    c.setFillColor(red)
    c.rect(4 * cm, hauteur - 1.4 * cm, largeur - 3 * cm, 0.3 * cm, fill=1, stroke=0)


def setClient(c, devis):
    c.setFillColor(colors.HexColor("#212121"))
    c.rect(0, hauteur - 3.6 * cm, width=10 * cm, height=cm, fill=1, stroke=0)

    textobject = c.beginText()
    textobject.setTextOrigin(x=0.2 * cm, y=hauteur - 3.4 * cm)
    textobject.setFont(psfontname='Helvetica', size=20)
    textobject.setFillColor(white)
    textobject.textLine(str(devis.client)[0:34])
    c.drawText(textobject)


def setDevisId(c, devis):
    c.setFillColor(colors.HexColor("#212121"))
    c.rect(largeur - (7.5 * cm), hauteur - (4.6 * cm), width=7.5 * cm, height=2 * cm, fill=1, stroke=0)

    textobject = c.beginText()
    textobject.setTextOrigin(x=largeur - (7.3 * cm), y=hauteur - (4 * cm))
    textobject.setFont(psfontname="Helvetica", size=30)
    textobject.setFillColor(white)
    textobject.textLine("Devis n°{}".format(str(devis.id).zfill(5)))

    c.drawText(textobject)


def setLignesHeader(c):
    c.setStrokeColor(colors.HexColor("#212121"))
    c.setFillColor(colors.HexColor("#212121"))
    c.rect(0, 21 * cm, width=largeur * 1 / 2, height=1 * cm, fill=1)

    c.setFillColor(red)
    c.rect(largeur * 1 / 2, 21 * cm, width=largeur * 1 / 6, height=1 * cm, fill=1)
    c.setFillColor(red)
    c.rect(largeur * 1 / 2 + (largeur * 1 / 6), 21 * cm, width=largeur * 1 / 6, height=1 * cm, fill=1)
    c.setFillColor(red)
    c.rect(largeur * 1 / 2 + (largeur * 2 / 6), 21 * cm, width=largeur * 1 / 6, height=1 * cm, fill=1)

    textobject = c.beginText()
    textobject.setTextOrigin(x=3.5 * cm, y=21.25 * cm)
    textobject.setFont(psfontname="Helvetica", size=20)
    textobject.setFillColor(white)
    textobject.textLine("Prestation")
    c.drawText(textobject)

    textobject = c.beginText()
    textobject.setTextOrigin(x=10.8 * cm, y=21.25 * cm)
    textobject.setFont(psfontname="Helvetica", size=20)
    textobject.setFillColor(white)
    textobject.textLine("Prix unité")
    c.drawText(textobject)

    textobject = c.beginText()
    textobject.setTextOrigin(x=14.4 * cm, y=21.25 * cm)
    textobject.setFont(psfontname="Helvetica", size=20)
    textobject.setFillColor(white)
    textobject.textLine("Quantité")
    c.drawText(textobject)

    textobject = c.beginText()
    textobject.setTextOrigin(x=18.3 * cm, y=21.25 * cm)
    textobject.setFont(psfontname="Helvetica", size=20)
    textobject.setFillColor(white)
    textobject.textLine("Total")
    c.drawText(textobject)


def setLigneValeursCalculees(c, string, boxbeginX, boxsize, movingY, tailleOccupee):
    widthPrixUnit = stringWidth(string, "Helvetica", fontSize=14)
    prixUnitObject = c.beginText()
    prixUnitObject.setFont(psfontname="Helvetica", size=14)
    prixUnitObject.setFillColor(black)
    prixUnitObject.setTextOrigin(boxbeginX + (boxsize - widthPrixUnit - 0.2 * cm), movingY - cm)
    prixUnitObject.textLine(string)
    c.drawText(prixUnitObject)


def setPrestationName(c, name, movingY):
    textobject = c.beginText()
    textobject.setTextOrigin(x=0.5 * cm, y=movingY - cm)
    textobject.setFont(psfontname="Helvetica", size=14)
    textobject.setFillColor(black)
    textobject.textLine((name + "EJZ0FEJFEHZFIZHFHZFHZFHZFH9ZHF9")[0:30])
    c.drawText(textobject)


def setLigne(c, ligne, movingY):
    tailleOccupee = 0

    print(type(ligne.prestation))
    if isinstance(ligne.prestation, PrestationCoutFixe):
        tailleOccupee = 1.5 * cm
        setPrestationName(c, ligne.prestation.libelle, movingY)

    elif isinstance(ligne.prestation, PrestationCoutVariableConcrete):
        tailleOccupee = 1.5 * cm
        setPrestationName(c, ligne.prestation.libelle, movingY)

    elif isinstance(ligne.prestation, PrestationPneumatique):
        tailleOccupee = 1.5 * cm
        setPrestationName(c, "{} {}\"".format(ligne.prestation.marque.libelle, ligne.prestation.dimensions), movingY)

    boxsize = largeur * 1 / 6

    prixUnitaire = str(ligne.prestation.prix_total)
    setLigneValeursCalculees(c=c, string=prixUnitaire, boxbeginX=largeur * 1 / 2, boxsize=boxsize,
                             movingY=movingY, tailleOccupee=tailleOccupee)

    quantite = str(ligne.quantite)
    setLigneValeursCalculees(c=c, string=quantite, boxbeginX=largeur * 1 / 2 + (largeur * 1 / 6), boxsize=boxsize,
                             movingY=movingY, tailleOccupee=tailleOccupee)

    prixTotal = str(ligne.prix_total)
    setLigneValeursCalculees(c=c, string=prixTotal, boxbeginX=largeur * 1 / 2 + (largeur * 2 / 6), boxsize=boxsize,
                             movingY=movingY, tailleOccupee=tailleOccupee)

    c.setStrokeColor(colors.HexColor("#212121"))
    c.line(0, movingY - tailleOccupee, largeur, movingY - tailleOccupee)

    return tailleOccupee


def setLignes(c, devis):
    c.setFillColor(colors.HexColor("#e0e0e0"))
    c.rect(0, 2 * cm, width=largeur, height=19 * cm, fill=1, stroke=0)

    c.setStrokeColor(green)
    c.circle(0, 2 * cm, r=cm, stroke=1)
    c.circle(0, 21 * cm, r=cm, stroke=1)
    c.circle(largeur, 2 * cm, r=cm, stroke=1)
    c.circle(largeur, 21 * cm, r=cm, stroke=1)

    topleftY = 21 * cm
    movingY = topleftY

    for ligne in devis.lignes.all():
        tailleOcuppee = setLigne(c, ligne, movingY)
        movingY -= tailleOcuppee


def generer_pdf(request, pk):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    devis = get_object_or_404(Devis, id=pk)

    setDevisId(c, devis)
    setClient(c, devis)
    setDecoration(c)
    setLignesHeader(c)
    setLignes(c, devis)

    c.showPage()
    c.save()

    buffer.seek(0)

    # return FileResponse(buffer, as_attachment=True, filename="hello.pdf")
    return FileResponse(buffer, filename="hello.pdf")
