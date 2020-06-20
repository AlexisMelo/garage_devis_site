var TVA = 1.2;
var marge = 11.5;

function changerValeurInput(input, valeur) {

    monInput = $('#'+input);

    newval = +monInput.val() + valeur;

    if (newval <= parseInt(monInput.attr('min'))) {
        $("label[for='"+input+"']").removeClass("active");
        monInput.val('').trigger("input");
    }
    else {
        $("label[for='"+input+"']").addClass("active");

        if (Number.isInteger(newval)) {
            monInput.val(newval).trigger("input");
        } else {
            monInput.val(newval.toFixed(2)).trigger("input");
        }

    }
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