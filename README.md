<p align="center">
<img src="Litreview_P9.png">
</p>


# Développez une application Web en utilisant Django

## Le thème: 

L'application doit permettre de faire fonctionner un site de critiques de livres. Principalement lire,  publier ou demander, des articles ou critiques de livres. 

## Les fonctionnalités:

    • Se connecter ou s'inscrire - le site ne devra pas être accessible à un utilisateur non connecté.

    • Afficher un flux contenant les derniers billets et avis que l'utilisateur suit, classés par heure avec le plus récent en premier.

    • Créer de nouveaux tickets demandant une critique sur un livre/article.

    • Créez des avis en réponse aux tickets.

    • Créer ticket et sa critique en même temps.

    • Pouvoir afficher, modifier et supprimer ses propres tickets et avis,

    • Suivre les autres utilisateurs en saisissant leur nom d'utilisateur,

    • Voir ses abonnements et les supprimer s'il ne veut plus suivre les utilisateurs en question.

## Le cahier des charges

*Le site devra :*

    • Avoir une UI correspondant à celles des wireframes fournis.

    • Avoir une interface utilisateur propre et minimale.

    • Utilisez le rendu côté serveur pour afficher dynamiquement les informations de la base de données sur la page.

*La base de code devra :*

    • Utiliser le framework Django.

    • Utilisez le langage de modèle Django pour le rendu côté serveur.

    • Utilisez SQLite comme base de développement locale.

    • Avoir une conception de base de données qui correspond au schéma de la base de données. Avoir une syntaxe conforme aux directives PEP8.

----------


## Mise en place du projet:

Pré-requis: se placer depuis le terminal dans le dossier où l'on exécute le script:

Avant toute chose on clone le répository git:

    git clone https://github.com/LGD-P/P9_Open_C.git

Une fois le projet cloné on crée et on active l'environnement virtuel:

    python3 -m venv env

suivi de:

    source env/bin/activate

Puis on lance l'installation des modules nécessaires au fonctionnement du script:

    pip install -r requirements.txt

On se place dans le dossier de notre application: 

    cd litreview

Il n'y a plus qu'à lancer Django:

    python3 manage.py runserver


*En général c'est le port 8000 qui est ouvert il n'y a plus qu'a suivre le lien http://....... pour accéder à l'application.*


Le répository est fourni avec une base de données,  dans la page abonnement, vous pouvez suivre les deux utilisateurs Pierre et Marie déjà créés, pour avoir une idée de l'expérience utilisateur.









