# garage_devis_site

Projet réalisé en autodidacte à la demande d'un ami gérant d'un garage automobile. Le principe était de faciliter la tâche du client pour qu'il puisse
saisir ses PDF plus rapidement, que le tout soit formalisé et enregistré.

Objectif : réaliser un site web permettant de saisir des devis et des les sortir au format pdf.

Le site permet plusieurs choses :
- Enregistrer un devis grâce à des menus permettant d'ajouter des "préstations" dans une liste (chaque préstation correspond en fait à une ligne du devis)
- Page de gestion des devis déjà créés (suppression/visionnage)
- Page de gestion des préstations enregistrées (type forfaits proposés par le garage, historique des préstations vendues...)
- Affichage détaillé du devis
- Possibilité de sortir un devis sous le format d'un PDF prêt à être donné au client
- La gestion des clients avec une partie d'ajout du client, liste de clients...

Technologies utilisées :
- Django (framework python) appris pour l'occasion
- HTML/CSS
- DB SQlite classique intégrée de base par Django
- Javascript / Jquery
- Materialize (Framework CSS)

Le site est uniquement accessible en localhost, il n'est actuellement pas déployé ni utilisé (bien qu'il soit largement fonctionnel, les raisons sont autres).
Il a été temporairement accessible sur un serveur Alwaysdata (fournisseur qui propose de l'aide pour le déploiement d'une application Django), mais j'ai préféré arrêter l'abonnement.

Ai suivi le tutoriel suivant : https://openclassrooms.com/fr/courses/1871271-developpez-votre-site-web-avec-le-framework-django
Terminé à 81% (manque partie test unitaire, et déploiement)
