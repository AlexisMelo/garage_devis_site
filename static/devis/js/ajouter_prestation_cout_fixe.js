

$(document).ready(function(){
    $('input').on('input', function() {

        id = this.id.split('-')[0];

        console.log(id + " swag");

        prix_unitaire = parseFloat($('#'+id+'-prix_unitaire').text());
        console.log(prix_unitaire);
        quantite = parseInt($('#'+id+'-quantite').val());
        console.log(quantite);
        nouveauprix = prix_unitaire * quantite;
        console.log(nouveauprix);
        $('#'+id+'-prix_total').text(nouveauprix);
    })

    window.openmodal = function(id) {
        console.log(id);
        $('#'+id).modal('open');
    }

    window.incrementerValeurInput = function(input, valeur) {

    console.log(input);

    monInput = $('#'+input);

    newval = +monInput.val() + valeur;

    if (newval >= parseInt(monInput.attr('min'))) {

        $("label[for='"+input+"']").addClass("active");

        if (Number.isInteger(newval)) {
            monInput.val(newval).trigger("input");
        } else {
            monInput.val(newval.toFixed(2)).trigger("input");
        }

    }
}
});