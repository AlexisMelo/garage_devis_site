var TVA = 1.2;
var marge = 11.5;

function setValeurInput(input, valeur) {
    if (Object.prototype.toString.call(valeur) === "[object String]") {
        console.log("c un string");
        $('#'+input).val(valeur).trigger("input");
    }
    else {
        console.log("c autre chose");
        $('#'+input).val(valeur).trigger("input");
    }
    $("label[for='"+input+"']").addClass("active");
}

function reinitialiserFormulaire() {
    $('input').val('').trigger('input');
    $("label.active").removeClass("active");

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

        if (isNaN(prixttc)) {
            $('#valeur-prix-ttc').text("?");
        }else {
            $('#valeur-prix-ttc').text(prixttc.toFixed(2));
        }
    });
});