myData = {};

mesClients.forEach((client) => {

    maChaine = client.fields.nom;

    if (client.fields.prenom != null) {
        maChaine += " " + client.fields.prenom;
    }

    if (client.fields.societe != null) {
        maChaine += " ( " + client.fields.societe + " ) ";
    }
    myData[maChaine] = "";
})

$(document).ready(function(){
    $('.autocomplete').autocomplete({
    data : myData,
    limit : 7
    });
    $('.modal').modal();
    $('.tooltipped').tooltip();


});
