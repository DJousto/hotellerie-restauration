pré-requis
- disponibilité de python >= 3.7
- python.exe doit être disponible dans le path

pour installer le script :
- créer un répertoire dédié
- copier tous les fichiers dans ce répertoire
- installer les modules python nécessaires :
    - dans le répertoire où sont les fichiers, lancer la commande : pip install -r requirements.txt

pour lancer le script :
- python  ./scrap.py

le script va
- lire le fichier annonces.xls s'il existe pour éviter de récupérer une 2e fois les mêmes annonces
- ensuite parcourir toutes les pages du site internet pour récupérer les annonces et en particulier les coordonnées des annonceurs
- enregistrer les nouvelles annonces dans "nouvelles_annonces.xls"
- enregistrer l'ensemble des annonces  dans "annonces.xls"

