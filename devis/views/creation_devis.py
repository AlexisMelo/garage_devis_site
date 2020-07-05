from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ValidationError
from django.db.models import Max
from django.shortcuts import render, redirect
from django.urls import reverse

from devis.models import Client, Categorie, PrestationCoutFixe, PrestationCoutVariableStandard, Devis, LigneDevis, \
    PrestationCoutVariableConcrete, PieceDetacheeStandard, PieceDetacheeAvecPrix, PrestationPneumatique, Marque, \
    PrestationMainOeuvre, PrestationNouvelle


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
    request.session.pop('mesPrestationsNouvelles', None)
    request.session.pop('devis_en_creation', None)
    request.session.pop('prix_devis_total', None)
    request.session.pop('client', None)
    request.session.pop('mo', None)
    request.session.modified = True


@login_required
def sauvegarder_devis(request):
    if not 'client' in request.session or not request.session['client']:
        messages.error(request, 'Sélectionnez un client !')
        return redirect('devis_creation_ecrit')

    if not any(key in request.session for key in
               ['mesPrestationsCoutFixe', 'mesPrestationsCoutVariable', 'mesPrestationsPneumatiques', 'mesPrestationsNouvelles']):
        messages.error(request, 'Ajoutez au moins une préstation au devis !')
        return redirect('devis_creation_ecrit')

    devis = Devis()

    try:
        client = Client.objects.get(intitule__iexact=request.session.get('client'))
        devis.client = client
    except Client.DoesNotExist:
        messages.error(request, "Impossible de faire le lien avec une fiche client, veuillez la renseigner")
        request.session["ajout_client_inconnu_pour_devis"] = True
        return redirect("ajout_client")
    except Client.MultipleObjectsReturned:
        messages.error(request, "Plusieurs clients avec le même nom trouvé, veuillez en sélectionner un : (c pas encore implémenté")
        return redirect("devis_creation_ecrit")

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
            nouvellePrestPneu = PrestationPneumatique(libelle="Prestation pneumatique",
                                                      prixAchat=prestation.get('prixAchat'),
                                                      dimensions=prestation.get('dimensions'),
                                                      marque=Marque.objects.get_or_create(libelle=prestation.get('marque'))[0])

            nouvellePrestPneu.save()
            ligne, created = LigneDevis.objects.get_or_create(prestation=nouvellePrestPneu, quantite=prestation.get('quantite'))
            devis.lignes.add(ligne)

    if 'mesPrestationsNouvelles' in request.session:
        for prestation in request.session['mesPrestationsNouvelles'].values():
            nouvellePrest = PrestationNouvelle(libelle=prestation.get('libelle'),
                                               prix=prestation.get('prix'))

            nouvellePrest.save()
            ligne, created = LigneDevis.objects.get_or_create(prestation=nouvellePrest, quantite=prestation.get('quantite'))
            devis.lignes.add(ligne)

    if 'mo' in request.session:
        p = PrestationMainOeuvre(libelle="Main d'oeuvre", tauxHoraire=request.session['mo']['tauxHoraire'])
        p.save()
        ligne, created = LigneDevis.objects.get_or_create(prestation=p, quantite=request.session['mo']['heures'])
        devis.lignes.add(ligne)
    else:
        p = PrestationMainOeuvre(libelle="Main d'oeuvre", tauxHoraire=55)
        p.save()
        ligne, created = LigneDevis.objects.get_or_create(prestation=p, quantite=1)
        devis.lignes.add(ligne)

    devis.save()
    nettoyer_devis_en_cours(request)
    messages.success(request, 'Devis ajouté avec succès')
    return redirect('devis_detail', pk=devis.id)
