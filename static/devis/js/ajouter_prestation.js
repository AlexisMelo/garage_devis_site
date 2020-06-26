$(document).ready(function(){

    window.incrementerValeurInput = function(input, valeur) {

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