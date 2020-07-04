from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from devis.models import PieceDetacheeStandard
from devis.views.utilitaires import application_marge


@login_required
def ajouter_client_en_session(request):
    if request.POST.get('client', None):
        request.session['client'] = request.POST.get('client')
    else:
        request.session['client'] = False

    return redirect('devis_creation_ecrit')

@login_required
def ajouter_mo_session(request):
    if request.POST.get('heures', None) and request.POST.get('tauxHoraire', None):
        request.session['mo'] = {
            "heures" : request.POST.get('heures', None),
            "tauxHoraire" : request.POST.get('tauxHoraire', None)
        }

    request.session.modified = True
    update_prix_total_session(request)
    return redirect('devis_creation_ecrit')

@login_required
def update_prix_total_session(request):
    prix_total = 0.00

    if 'mesPrestationsCoutFixe' in request.session:
        liste_couts = [p['prix_total'] for p in request.session['mesPrestationsCoutFixe'].values() if p]
        sommeCoutPrestations = sum(liste_couts)
        prix_total += sommeCoutPrestations

    if 'mesPrestationsCoutVariable' in request.session:
        liste_couts = [p['prix_total'] for p in request.session['mesPrestationsCoutVariable'].values() if p]
        sommeCoutPrestations = sum(liste_couts)
        prix_total += sommeCoutPrestations

    if 'mesPrestationsPneumatiques' in request.session:
        liste_couts = [p['prix_total'] for p in request.session['mesPrestationsPneumatiques'].values() if p]
        sommeCoutPrestations = sum(liste_couts)
        prix_total += sommeCoutPrestations

    if 'mo' in  request.session:
        prix_total += float(request.session['mo']['tauxHoraire']) * float(request.session['mo']['heures'])

    request.session['prix_devis_total'] = round(prix_total,2)
    request.session.modified = True


@login_required
def ajouter_prestation_fixe_en_session(request):
    if not 'mesPrestationsCoutFixe' in request.session:
        request.session['mesPrestationsCoutFixe'] = {}

    quantite = request.POST.get('quantite')
    libelle = request.POST.get('libelle')
    prix_unit = request.POST.get('prix_unit')
    prix_total = float(prix_unit.replace(',', '.')) * float(quantite)

    request.session['mesPrestationsCoutFixe'][request.POST.get('id_prestation')] = {'quantite': quantite,
                                                                                    'libelle': libelle,
                                                                                    'prix_total': prix_total}
    request.session.modified = True
    update_prix_total_session(request)

    return redirect('ajouter_prestation_mecanique')


@login_required
def ajouter_prestation_pneumatique_en_session(request):
    if not 'mesPrestationsPneumatiques' in request.session:
        request.session['mesPrestationsPneumatiques'] = {}

    nouvelId = len(request.session['mesPrestationsPneumatiques']) + 1

    quantite = request.POST.get('quantite')
    dimensions = request.POST.get('dimensions')
    prixAchat = request.POST.get('prixAchat')
    marque = request.POST.get('marque')

    prixttc = float(prixAchat)
    TVA = 1.2
    marge = 11.5

    if int(dimensions) < 19:
        prixttc += int(dimensions) - 3
    else:
        prixttc += int(dimensions)

    prixttc *= TVA
    prixttc += marge
    prixttc *= int(quantite)

    request.session['mesPrestationsPneumatiques'][str(nouvelId)] = {'quantite': quantite,
                                                                    'dimensions': dimensions,
                                                                    'prixAchat': prixAchat,
                                                                    'marque': marque,
                                                                    'prix_total': round(prixttc, 2)}

    request.session.modified = True
    update_prix_total_session(request)
    return redirect('devis_creation_ecrit')


@login_required
def ajouter_prestation_variable_en_session(request):
    if not 'mesPrestationsCoutVariable' in request.session:
        request.session['mesPrestationsCoutVariable'] = {}

    quantite = int(request.POST.get('quantite'))
    libelle = request.POST.get('libelle')

    request.session['mesPrestationsCoutVariable'][request.POST.get('id_prestation')] = {'quantite': quantite,
                                                                                        'libelle': libelle,
                                                                                        'pieces_detachees': {}}

    for key in request.POST:
        if key.endswith('prix'):
            piece_detachee_id = key.split("-")[0]
            piece_detachee_object = PieceDetacheeStandard.objects.get(id=piece_detachee_id)

            piece_detachee = {}
            piece_detachee['libelle'] = piece_detachee_object.libelle
            piece_detachee['prix_achat'] = round(float(request.POST.get(key).replace(',', '.')), 2)
            piece_detachee['prix_vente'] = round(application_marge(float(request.POST.get(key).replace(',', '.'))), 2)

            request.session['mesPrestationsCoutVariable'][request.POST.get('id_prestation')]['pieces_detachees'][
                piece_detachee_id] = piece_detachee

    prixtotal = 0
    for piece in request.session['mesPrestationsCoutVariable'][request.POST.get('id_prestation')][
        'pieces_detachees'].values():
        prixtotal += piece['prix_vente']

    request.session['mesPrestationsCoutVariable'][request.POST.get('id_prestation')][
        'prix_total'] = round(prixtotal * quantite, 2)

    request.session.modified = True
    update_prix_total_session(request)

    return redirect('ajouter_prestation_mecanique')

@login_required
def supprimer_prestation_en_session(request, type_prestation, prestation_id):
    request.session[type_prestation].pop(prestation_id, None)
    if not request.session[type_prestation]:
        del request.session[type_prestation]

    update_prix_total_session(request)
    request.session.modified = True

    return redirect(request.META.get('HTTP_REFERER'))

