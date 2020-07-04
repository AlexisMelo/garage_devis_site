import io

from django.contrib.staticfiles.finders import find
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib import colors
from reportlab.lib.colors import red, black, white, green, grey, blue
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from django.templatetags.static import static
from devis.models import Devis, PrestationCoutFixe, PrestationCoutVariableConcrete, PrestationPneumatique

from reportlab.lib.units import cm

from devis.views.utilitaires import iterable

largeur, hauteur = A4


def setDecoration(c):
    c.setFillColor(colors.HexColor("#212121"))
    c.rect(0, hauteur - 1.6 * cm, largeur - 3 * cm, 0.5 * cm, fill=1, stroke=0)

    c.setFillColor(red)
    c.rect(4 * cm, hauteur - 1.4 * cm, largeur - 3 * cm, 0.3 * cm, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#212121"))
    c.rect(4 * cm, cm, largeur - 3 * cm, 0.5 * cm, fill=1, stroke=0)

    c.setFillColor(red)
    c.rect(0, cm, largeur - 3 * cm, 0.3 * cm, fill=1, stroke=0)


def setClient(c, devis):
    c.setFillColor(colors.HexColor("#212121"))
    c.rect(0, hauteur - 3.6 * cm, width=10 * cm, height=cm, fill=1, stroke=0)

    textobject = c.beginText()
    textobject.setTextOrigin(x=0.2 * cm, y=hauteur - 3.4 * cm)
    textobject.setFont(psfontname='Helvetica', size=20)
    textobject.setFillColor(white)
    textobject.textLine(str(devis.client)[0:34])
    c.drawText(textobject)

    textAdresse = c.beginText()
    textAdresse.setTextOrigin(x=0.1 * cm, y=hauteur - 4.5 * cm)
    textAdresse.setFont(psfontname='Helvetica', size=17)
    textAdresse.setFillColor(black)

    adresseList = devis.client.adresse.split()
    stringFinales = []
    currentSring = ""
    for string in adresseList:
        print(string)
        print("current : " + currentSring)
        if len(currentSring) + len(string) > 26 and currentSring:
            stringFinales.append(currentSring)
            currentSring = ""
        currentSring += " " + string[0:28]

    stringFinales.append(currentSring)
    for string in stringFinales:
        textAdresse.textLine(string)
    c.drawText(textAdresse)


def setDevisId(c, devis):
    c.setFillColor(colors.HexColor("#212121"))
    c.rect(largeur - (7.5 * cm), hauteur - (4.6 * cm), width=7.5 * cm, height=2 * cm, fill=1, stroke=0)

    textobject = c.beginText()
    textobject.setTextOrigin(x=largeur - (7.3 * cm), y=hauteur - (4 * cm))
    textobject.setFont(psfontname="Helvetica", size=30)
    textobject.setFillColor(white)
    textobject.textLine("Devis n°{}".format(str(devis.id).zfill(5)))

    c.drawText(textobject)


def setLignesHeader(c, y=21 * cm):
    c.setStrokeColor(colors.HexColor("#212121"))
    c.setFillColor(colors.HexColor("#212121"))
    c.rect(0, y, width=largeur * 1 / 2, height=1 * cm, fill=1)

    c.setStrokeColor(red)
    c.setFillColor(red)
    c.rect(largeur * 1 / 2, y, width=largeur * 1 / 6, height=1 * cm, fill=1)
    c.setFillColor(red)
    c.rect(largeur * 1 / 2 + (largeur * 1 / 6), y, width=largeur * 1 / 6, height=1 * cm, fill=1)
    c.setFillColor(red)
    c.rect(largeur * 1 / 2 + (largeur * 2 / 6), y, width=largeur * 1 / 6, height=1 * cm, fill=1)

    textobject = c.beginText()
    textobject.setTextOrigin(x=3.5 * cm, y=y + 0.25 * cm)
    textobject.setFont(psfontname="Helvetica", size=20)
    textobject.setFillColor(white)
    textobject.textLine("Prestation")
    c.drawText(textobject)

    textobject = c.beginText()
    textobject.setTextOrigin(x=10.8 * cm, y=y + 0.25 * cm)
    textobject.setFont(psfontname="Helvetica", size=20)
    textobject.setFillColor(white)
    textobject.textLine("Prix unité")
    c.drawText(textobject)

    textobject = c.beginText()
    textobject.setTextOrigin(x=14.4 * cm, y=y + 0.25 * cm)
    textobject.setFont(psfontname="Helvetica", size=20)
    textobject.setFillColor(white)
    textobject.textLine("Quantité")
    c.drawText(textobject)

    textobject = c.beginText()
    textobject.setTextOrigin(x=18.3 * cm, y=y + 0.25 * cm)
    textobject.setFont(psfontname="Helvetica", size=20)
    textobject.setFillColor(white)
    textobject.textLine("Total")
    c.drawText(textobject)

def getLigneValeursCalculeesTO(c, string, boxbeginX, boxsize, movingY):
    widthPrixUnit = stringWidth(string, "Helvetica", fontSize=14)
    prixUnitObject = c.beginText()
    prixUnitObject.setFont(psfontname="Helvetica", size=14)
    prixUnitObject.setFillColor(black)
    prixUnitObject.setTextOrigin(boxbeginX + (boxsize - widthPrixUnit - 0.2 * cm), movingY - cm)
    prixUnitObject.textLine(string)
    return prixUnitObject


def getSousLigneValeursCalculeesTO(c, string, boxbeginX, boxsize, movingY):
    widthPrixUnit = stringWidth(string, "Helvetica", fontSize=9)
    prixUnitObject = c.beginText()
    prixUnitObject.setFont(psfontname="Helvetica", size=9)
    prixUnitObject.setFillColor(colors.HexColor("#424242"))
    prixUnitObject.setTextOrigin(boxbeginX + (boxsize - widthPrixUnit - 0.2 * cm), movingY)
    prixUnitObject.textLine(string)
    return prixUnitObject


def getPrestationNameTO(c, name, movingY):
    textobject = c.beginText()
    textobject.setTextOrigin(x=0.5 * cm, y=movingY - cm)
    textobject.setFont(psfontname="Helvetica", size=14)
    textobject.setFillColor(black)
    textobject.textLine(name[0:30])
    return textobject


def getPieceTO(c, piece, movingY):
    textobject = c.beginText()
    textobject.setTextOrigin(x=1 * cm, y=movingY)
    textobject.setFont(psfontname="Helvetica", size=9)
    textobject.setFillColor(colors.HexColor("#424242"))
    textobject.textLine(("- " + piece.libelle)[0:30])
    return textobject


def getLigne(c, ligne, movingY):
    tailleOccupee = 0
    textObjects = []
    boxsize = largeur * 1 / 6

    if isinstance(ligne.prestation, PrestationCoutFixe):
        tailleOccupee = 1.5 * cm
        textObjects.append(getPrestationNameTO(c, ligne.prestation.libelle, movingY))

    elif isinstance(ligne.prestation, PrestationCoutVariableConcrete):
        tailleOccupee = 1.5 * cm
        textObjects.append(getPrestationNameTO(c, ligne.prestation.libelle, movingY))
        movingYCopie = movingY - cm
        for piece in ligne.prestation.pieces_detachees.all():
            movingYCopie -= cm
            textObjects.append(getPieceTO(c, piece, movingYCopie))

            prixUnitaire = str(piece.prix_total)
            textObjects.append(
                getSousLigneValeursCalculeesTO(c=c, string=prixUnitaire, boxbeginX=largeur * 1 / 2, boxsize=boxsize,
                                               movingY=movingYCopie))

            tailleOccupee += cm

    elif isinstance(ligne.prestation, PrestationPneumatique):
        tailleOccupee = 1.5 * cm
        textObjects.append(
            getPrestationNameTO(c, "{} {}\"".format(ligne.prestation.marque.libelle, ligne.prestation.dimensions),
                                movingY))

    prixUnitaire = str(ligne.prestation.prix_total)
    textObjects.append(getLigneValeursCalculeesTO(c=c, string=prixUnitaire, boxbeginX=largeur * 1 / 2, boxsize=boxsize,
                                                  movingY=movingY))

    quantite = str(ligne.quantite)
    textObjects.append(
        getLigneValeursCalculeesTO(c=c, string=quantite, boxbeginX=largeur * 1 / 2 + (largeur * 1 / 6), boxsize=boxsize,
                                   movingY=movingY))

    prixTotal = str(ligne.prix_total)
    textObjects.append(getLigneValeursCalculeesTO(c=c, string=prixTotal, boxbeginX=largeur * 1 / 2 + (largeur * 2 / 6),
                                                  boxsize=boxsize,
                                                  movingY=movingY))

    return tailleOccupee, textObjects


def setTextObjects(c, textObjects):
    if iterable(textObjects):
        for to in textObjects:
            c.drawText(to)
    else:
        c.drawText(textObjects)


def initNouvellePage(c, lignesHeader=True):
    c.showPage()
    setDecoration(c)
    topLeft = 26 * cm
    tailleAutorisee = topLeft - 2 * cm

    if lignesHeader:
        setLignesHeader(c, y=26 * cm)

    return topLeft, tailleAutorisee


def colorerLigne(c, movingY, tailleOccupee, numeroLigne):
    if numeroLigne % 2 == 0:
        c.setFillColor(colors.HexColor("#eeeeee"))
    else:
        c.setFillColor(white)

    c.rect(0, movingY, largeur, height=tailleOccupee, fill=1, stroke=0)


def getsetTotal(c, movingY, devis):
    c.setFillColor(colors.HexColor("#212121"))
    c.rect(11.5 * cm, movingY, width=3.5 * cm, height=1 * cm, fill=1, stroke=0)
    c.setFillColor(red)
    c.rect(11 * cm + 4 * cm, movingY, width=6 * cm, height=1 * cm, fill=1, stroke=0)

    textobjectTotal = c.beginText()
    textobjectTotal.setTextOrigin(x=12.3 * cm, y=movingY + 0.2 * cm)
    textobjectTotal.setFont(psfontname="Helvetica", size=25)
    textobjectTotal.setFillColor(white)
    textobjectTotal.textLine("Total")

    stringPrix = str(devis.prix_total) + " €"
    widthTotalPrix = stringWidth(stringPrix, "Helvetica", fontSize=25)
    widthPossible = 5 * cm
    textObjectPrix = c.beginText()
    textObjectPrix.setTextOrigin(11 * cm + 5 * cm + (widthPossible - widthTotalPrix - 0.2 * cm), movingY + 0.2 * cm)
    textObjectPrix.setFont(psfontname="Helvetica", size=25)
    textObjectPrix.setFillColor(white)
    textObjectPrix.textLine(stringPrix)

    return [textobjectTotal, textObjectPrix]



def setLignes(c, devis):
    topleftY = 21 * cm
    movingY = topleftY
    tailleAutorisee = topleftY - 2 * cm
    numeroLigne = 1

    for ligne in devis.lignes.all():
        tailleOccupee, textObjects = getLigne(c, ligne, movingY)

        yBotPrest = movingY - tailleOccupee
        yBotMin = topleftY - tailleAutorisee

        if yBotPrest < yBotMin:
            topleftY, tailleAutorisee = initNouvellePage(c)
            movingY = topleftY
            tailleOccupee, textObjects = getLigne(c, ligne, movingY)

        movingY -= tailleOccupee
        colorerLigne(c, movingY, tailleOccupee, numeroLigne)

        if numeroLigne == devis.lignes.all().count():
            nouveauY = movingY - 3 * cm
            if nouveauY < yBotMin:
                nouveauY, tailleAutorisee = initNouvellePage(c, lignesHeader=False)

            textObjects += getsetTotal(c, nouveauY, devis)

        else:
            numeroLigne += 1

        setTextObjects(c, textObjects)

def setDate(c, devis):
    dateString = devis.date_creation.strftime("%d/%m/%Y")
    print(dateString)
    textdate = c.beginText()
    textdate.setTextOrigin(x=13.7 * cm, y=hauteur - 5.5*cm)
    textdate.setFont(psfontname="Helvetica", size=18)
    textdate.setFillColor(black)
    textdate.textLine("Date : {}".format(dateString))
    c.drawText(textdate)


def generer_pdf(request, pk):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    devis = get_object_or_404(Devis, id=pk)

    setDevisId(c, devis)
    setClient(c, devis)
    setDecoration(c)
    setLignesHeader(c)
    setDate(c, devis)

    setLignes(c, devis)


    c.showPage()
    c.save()

    buffer.seek(0)

    # return FileResponse(buffer, as_attachment=True, filename="hello.pdf")
    return FileResponse(buffer, filename="hello.pdf")
