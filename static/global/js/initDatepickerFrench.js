$(document).ready(function(){

    $('.datepicker').datepicker({
        format : "dd/mm/yyyy",
        i18n : {
            months : ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Octobre', 'Novembre', 'Décembre'],
            cancel : 'Annuler',
            clear : 'RaZ',
            monthsShort : ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jui', 'Jui', 'Aou', 'Oct', 'Nov', 'Déc'],
            weekdays : ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'],
            weekdaysShort : ['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'],
            weekdaysAbbrev : ['D','L','M','M','J','V','S']

        },
        minDate : new Date(),
        autoClose : true
    });
});