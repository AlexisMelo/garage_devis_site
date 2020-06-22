console.log(mesClients);

myData = {};

mesClients.forEach((client) => {
    myData[client.fields.nom + " " + client.fields.prenom] = "";
})

console.log(myData);
$(document).ready(function(){
    $('.autocomplete').autocomplete({
    data : myData
    });

    $('.autocomplete').
});
