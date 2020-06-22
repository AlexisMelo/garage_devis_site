console.log(mesClients);

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

console.log(myData);
$(document).ready(function(){
    $('.autocomplete').autocomplete({
    data : myData
    });
    $('.modal').modal();


});
