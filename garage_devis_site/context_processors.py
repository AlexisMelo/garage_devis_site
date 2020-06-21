from devis.models import Devis


def get_infos(request):
    devis = Devis()

    return {'devis_construction': devis}