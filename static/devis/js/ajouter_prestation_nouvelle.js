$(document).ready(function(){
    $('input[id^=nvelle]').on('input', function() {

        console.log("tu touches a nvelle")

        quantite = parseInt($('#nvelle-quantite').val())
        prixVente = parseFloat($('#nvelle-prix').val())

        if (!isNaN(quantite) && !isNaN(prixVente)) {

            total = quantite * prixVente
            $('#nvelle-prix_unitaire').text(prixVente.toFixed(2));
            $('#nvelle-prix_total').text(total.toFixed(2));
        }
        else {
            $('#nvelle-prix_unitaire').text("? ");
            $('#nvelle-prix_total').text("? ");
        }


    })
});