$(document).ready(function(){
    $('input').on('input', function() {

        id = this.id.split('-')[0];

        prix_unitaire = parseFloat($('#'+id+'-prix_unitaire').text());
        quantite = parseInt($('#'+id+'-quantite').val());
        nouveauprix = prix_unitaire * quantite;
        $('#'+id+'-prix_total').text(nouveauprix);
    })
});