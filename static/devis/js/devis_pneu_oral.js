var TVA = 1.2;
var marge = 11.5;

function setValeurInput(input, valeur) {
    $('#'+input).val(valeur).trigger("input");
    $("label[for='"+input+"']").addClass("active");
}

$(document).ready(function(){

    $('input').bind('input', function() {

        quantite = parseInt($('#quantite_input').val());
        taille = parseInt($('#dimensions_input').val());
        prixachat = parseFloat($('#prixAchat_input').val());

        prixttc = prixachat;

        if ( taille < 19 ) {
            prixttc += taille - 3;
        }
        else {
            prixttc += taille;
        }

        prixttc *= TVA;
        prixttc += marge;
        prixttc *= quantite;

        console.log(prixttc);
        if (isNaN(prixttc)) {
            $('#valeur-prix-ttc').text("?");
        }else {
            $('#valeur-prix-ttc').text(prixttc.toFixed(2));
        }
    });
});