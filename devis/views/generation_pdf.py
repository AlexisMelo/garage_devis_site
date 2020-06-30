import io

from django.contrib.staticfiles.finders import find
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.colors import red, black, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from django.templatetags.static import static
from devis.models import Devis

from reportlab.lib.units import cm

largeur, hauteur = A4

def setDecoration(c):
    c.setFillColor(black)
    c.rect(0, hauteur-1.6*cm, largeur-3*cm, 0.5*cm, fill=1, stroke=0)

    c.setFillColor(red)
    c.rect(4*cm, hauteur-1.4*cm, largeur-3*cm, 0.3*cm, fill=1, stroke=0)

def setClient(c, devis):
    c.setFillColor(black)
    c.rect(0, hauteur-3.6*cm, width=10*cm, height=cm, fill=1, stroke=0)

    textobject = c.beginText()
    textobject.setTextOrigin(x=0.2*cm, y=hauteur-3.4*cm)
    textobject.setFont(psfontname='Helvetica', size=20)
    textobject.setFillColor(white)
    textobject.textLine(str(devis.client)[0:34])
    c.drawText(textobject)

def setDevisId(c, devis):

    c.setFillColor(black)
    c.rect(largeur-(7.5*cm), hauteur-(4.6*cm), width=7.5*cm, height=2*cm, fill=1, stroke=0)

    textobject = c.beginText()
    textobject.setTextOrigin(x=largeur-(7.3*cm), y=hauteur-(4*cm))
    textobject.setFont(psfontname="Helvetica", size=30)
    textobject.setFillColor(white)
    textobject.textLine("Devis n°{}".format(str(devis.id).zfill(5)))

    c.drawText(textobject)

def generer_pdf(request, pk):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    devis = get_object_or_404(Devis, id=pk)

    setDevisId(c, devis)
    setClient(c, devis)
    setDecoration(c)

    c.showPage()
    c.save()

    buffer.seek(0)

    # return FileResponse(buffer, as_attachment=True, filename="hello.pdf")
    return FileResponse(buffer, filename="hello.pdf")
