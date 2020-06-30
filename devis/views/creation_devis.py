from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ValidationError
from django.db.models import Max
from django.shortcuts import render, redirect
from django.urls import reverse

from devis.models import Client, Categorie, PrestationCoutFixe, PrestationCoutVariableStandard, Devis, LigneDevis, \
    PrestationCoutVariableConcrete, PieceDetacheeStandard, PieceDetacheeAvecPrix, PrestationPneumatique, Marque


def ajouter_prestation_pneumatique(request):
    if request.META.get('HTTP_REFERER').endswith(reverse('devis_creation_ecrit')):
        ajout_au_devis_possible = True

    return render(request, 'devis/ajouter_prestation_pneumatique.html', locals())

def ajouter_prestation_mecanique(request):
    prestationsFixes = PrestationCoutFixe.objects.all()
    catPossiblePrestFixe = prestationsFixes.values('categorie').distinct()
    catFixes = Categorie.objects.filter(id__in=catPossiblePrestFixe)

    prestationsVar = PrestationCoutVariableStandard.objects.all()
    catPossiblePrestVar = prestationsVar.values('categorie').distinct()
    catVars = Categorie.objects.filter(id__in=catPossiblePrestVar)

    return render(request, 'devis/ajouter_prestation_mecanique.html', locals())

@login_required
def devis_creation_ecrit(request):
    if not 'devis_en_creation' in request.session:
        request.session['devis_en_creation'] = True

    allClients = Client.objects.all()
    jsonClients = serializers.serialize('json', allClients)

    if request.session['devis_en_creation']:

        tousMesDevis = Devis.objects.all()
        nbDevis = tousMesDevis.count()
        numeroSupposeDevis = 1
        if nbDevis != 0:
            numeroSupposeDevis = tousMesDevis.aggregate(Max('id'))['id__max'] + 1
        request.session['numeroProchainDevis'] = numeroSupposeDevis

        if 'mesPrestationsCoutFixe' in request.session:
            # afficher prestations
            mesPrestationsCoutFixe = request.session['mesPrestationsCoutFixe']

    return render(request, 'devis/devis_creation_ecrit.html', locals())

@login_required
def reset(request):
    nettoyer_devis_en_cours(request)
    messages.success(request, "Devis réinitialisé")
    return redirect('creer_devis')


def nettoyer_devis_en_cours(request):
    request.session.pop('mesPrestationsCoutFixe', None)
    request.session.pop('mesPrestationsCoutVariable', None)
    request.session.pop('mesPrestationsPneumatiques', None)
    request.session.pop('devis_en_creation', None)
    request.session.pop('prix_devis_total', None)
    request.session.pop('client', None)
    request.session.modified = True


@login_required
def sauvegarder_devis(request):
    if not 'client' in request.session or not request.session['client']:
        messages.error(request, 'Sélectionnez un client !')
        return redirect('devis_creation_ecrit')

    if not any(key in request.session for key in
               ['mesPrestationsCoutFixe', 'mesPrestationsCoutVariable', 'mesPrestationsPneumatiques']):
        messages.error(request, 'Ajoutez au moins une préstation au devis !')
        return redirect('devis_creation_ecrit')

    devis = Devis()

    clientFields = request.session.get('client').split(" ", maxsplit=2)

    client = None

    try:
        client = Client.objects.get(nom__iexact=clientFields[0])
    except Client.MultipleObjectsReturned:
        if len(clientFields) == 2:
            try:
                client = Client.objects.get(nom__iexact=clientFields[0], prenom__iexact=clientFields[1])
            except:
                try:
                    client = Client.objects.get(nom__iexact=clientFields[0],
                                                societe__iexact=clientFields[1].replace('(', '').replace(')',
                                                                                                         '').strip())
                except:
                    pass
        elif len(clientFields) == 3:
            try:
                client = Client.objects.get(nom__iexact=clientFields[0], prenom__iexact=clientFields[1],
                                            societe__iexact=clientFields[2].replace('(', '').replace(')', '').strip())
            except:
                pass
    except:
        pass

    if client is None:
        messages.error(request, "Impossible de faire le lien avec une fiche client, veuillez la renseigner")
    else:
        devis.client = client

    try:
        devis.full_clean()
        devis.save()
    except ValidationError as e:
        messages.error(request, "Echec lors de l'enregistrement du devis pour la raison suivante : {}".format(e))
        return redirect('devis_creation_ecrit')

    if 'mesPrestationsCoutFixe' in request.session:
        for prestationId in request.session['mesPrestationsCoutFixe']:
            prestation = PrestationCoutFixe.objects.get(id=prestationId)
            ligne, created = LigneDevis.objects.get_or_create(prestation=prestation, quantite=
            request.session['mesPrestationsCoutFixe'][prestationId]['quantite'])
            devis.lignes.add(ligne)

    if 'mesPrestationsCoutVariable' in request.session:
        for prestationId in request.session['mesPrestationsCoutVariable']:
            prestReference = PrestationCoutVariableStandard.objects.get(id=prestationId)
            nouvellePrestConcrete = PrestationCoutVariableConcrete(libelle=prestReference.libelle,
                                                                   categorie=prestReference.categorie)
            nouvellePrestConcrete.save()

            for pieceId in request.session['mesPrestationsCoutVariable'][prestationId]['pieces_detachees']:
                pieceReference = PieceDetacheeStandard.objects.get(id=pieceId)
                nouvellePieceConcrete = PieceDetacheeAvecPrix(libelle=pieceReference.libelle)
                nouvellePieceConcrete.prix = \
                request.session['mesPrestationsCoutVariable'][prestationId]['pieces_detachees'][pieceId]['prix_vente']
                nouvellePieceConcrete.save()
                nouvellePrestConcrete.pieces_detachees.add(nouvellePieceConcrete)

            nouvellePrestConcrete.save()
            ligne, created = LigneDevis.objects.get_or_create(prestation=nouvellePrestConcrete, quantite=
            request.session['mesPrestationsCoutVariable'][prestationId]['quantite'])
            devis.lignes.add(ligne)

    if 'mesPrestationsPneumatiques' in request.session:
        for prestation in request.session['mesPrestationsPneumatiques'].values():
            nouvellePrestPneu = PrestationPneumatique(prixAchat=prestation.get('prixAchat'),
                                                      dimensions=prestation.get('dimensions'),
                                                      marque=Marque.objects.get_or_create(libelle=prestation.get('marque'))[0])

            nouvellePrestPneu.save()
            ligne, created = LigneDevis.objects.get_or_create(prestation=nouvellePrestPneu, quantite=prestation.get('quantite'))
            devis.lignes.add(ligne)

    devis.save()
    nettoyer_devis_en_cours(request)
    messages.success(request, 'Devis ajouté avec succès')
    return redirect('devis_detail', pk=devis.id)
