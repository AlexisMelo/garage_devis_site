$(document).ready(function(){
    $('input').on('input', function() {

        id = this.id.split('-')[0];

        totalClientUnitaire = 0;
        totalBoutiqueUnitaire = 0;

        mesPrixInput = $("input[id^='"+id+"'][id$='prix']").each( function(index) {
            totalBoutiqueUnitaire += parseFloat(this.value);
            totalClientUnitaire += applicationMarge(parseFloat(this.value));
        });

        quantite = parseInt($('#'+id+'-quantite').val());

        totalClient = quantite * totalClientUnitaire;
        totalBoutique =  quantite * totalBoutiqueUnitaire;

        $('#'+id+'-prix_client').text(totalClient.toFixed(2));
        $('#'+id+'-prix_boutique').text(totalBoutique.toFixed(2));
    })
});

function applicationMarge(prix) {
    if (prix <= 5) {
        return prix*2.5;
    }
    else if (prix <= 10){
        return prix*2;
    }
    else if (prix <= 20) {
        return prix*1.75;
    }
    return prix*1.5;
}