myData = {};

mesClients.forEach((client) => {

    maChaine = client.fields.intitule;

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
