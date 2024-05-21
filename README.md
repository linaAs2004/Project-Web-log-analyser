# Project-Web-log-analyser

Ce projet vise à créer une application web Flask pour l'analyse des logs des services Internet, en mettant particulièrement l'accent sur les services web et d'authentification.

## Encadré par
- Lahmar Mohammed

## Réalisé par
- Asbagui Lina

## Table des matières
1. [Introduction](#introduction)
2. [Cheminement du projet](#cheminement-du-projet)
3. [Fonctionnalités](#fonctionnalités)
4. [Technologies utilisées](#technologies-utilisées)
5. [Configuration et déploiement](#configuration-et-déploiement)


## Introduction
Ce projet a pour objectif de développer une application web permettant d'analyser les logs des services Internet, en fournissant des graphes résultants des analyses éfféctuées.

## Cheminement du projet
1. **Création de la base de données :** Modélisation et mise en place d'une base de données MySQL adaptée pour stocker les logs.
   La base de données bdLog est composée des trois tables suivantes :
      - **ssh_logs :** cette table contient les données extraites des fichiers de logs SSH (fichier secure).
      - **apache_access_logs (web) :** cette table contient les données d'accès des utilisateurs extraites des fichiers de logs d'accès Apache.
      - **apache_error_logs (errors) :** cette table contient les données d'erreur des utilisateurs extraites des fichiers de logs d'erreur Apache.
   Ensemble, ces tables permettent de stocker et d'analyser les différents types de logs collectés, facilitant ainsi la génération de rapports et de tableaux de bord pour la visualisation des données

2. **Extraction et Chargement des Logs :** Processus d'extraction et de chargement des logs dans la base de données.
    La connexion à la base de données MySQL est établie via la bibliothèque mysql.connector. Une fonction dédiée get_db_connection est utilisée pour gérer cette connexion, en s'assurant de capturer et de journaliser toute erreur de connexion.
    Trois types de logs sont extraits : les logs SSH, les logs d'accès Apache et les logs d'erreur Apache. Chaque type de log a un format spécifique et nécessite une méthode d'extraction dédiée.
          - **Logs SSH :** Les logs SSH sont extraits à l'aide d'une expression régulière pour capturer les informations pertinentes telles que la date, l'heure, le PID, le message et l'adresse IP.
          - **Logs d'accès Apache :** Les logs d'accès Apache sont analysés pour extraire l'adresse IP, le timestamp, la ressource demandée, le code de statut et l'agent utilisateur.
          - **Logs d'erreur Apache :** Les logs d'erreur Apache sont traités pour extraire l'heure du log, le niveau de log, le PID et le message.
          
    **Chargement des Logs dans la Base de Données**
        Les données extraites sont ensuite chargées dans des tables dédiées dans la base de données MySQL. Avant d'insérer les données, nous vérifions l'existence des tables et les créons si nécessaire grâce à la fonction existe_table(table_name, cursor).

3. **Réalisation des requêtes MySQL pour le développement des services :** Définition des requêtes SQL nécessaires pour l'analyse des logs.
4. **Implémentation des services demandés :** Développement des fonctionnalités telles que l'analyse des visiteurs uniques, des requêtes analysées, des requêtes statiques, etc.
5. **Création du controller Flask :** Développement du contrôleur Flask contenant les routes vers les pages principales et les méthodes pour générer les graphiques correspondant à chaque service.
6. **Réalisation de la page HTML :** Création de la structure de la page web et de son contenu.
7. **Réalisation de la feuille de style :** Définition des styles CSS pour améliorer l'apparence de l'application.
8. **Visualisation des dashboards dans la page :**
     
![img8](https://github.com/linaAs2004/Project-Web-log-analyser/assets/163998352/0114bf98-045e-42cc-866b-d1e77bcfceac)
![img9](https://github.com/linaAs2004/Project-Web-log-analyser/assets/163998352/b22e824d-0ba2-4912-8e20-f28dfcd78c87)
![img10](https://github.com/linaAs2004/Project-Web-log-analyser/assets/163998352/ba66b9b0-bbdd-4029-9720-04f7ed4b0c34)
![img11](https://github.com/linaAs2004/Project-Web-log-analyser/assets/163998352/c8fb38ab-160c-44ab-b46e-9598477d511d)
![img12](https://github.com/linaAs2004/Project-Web-log-analyser/assets/163998352/791321bd-2893-417f-aba9-f8705c05a59e)
![img13](https://github.com/linaAs2004/Project-Web-log-analyser/assets/163998352/7e9b1ca9-0782-4b3d-821b-857383d3584b)
![img14](https://github.com/linaAs2004/Project-Web-log-analyser/assets/163998352/facaa2bf-40b8-4531-b9b1-babf0c45f0af)
![img15](https://github.com/linaAs2004/Project-Web-log-analyser/assets/163998352/81269785-9e6b-4272-bba2-9ca2006aec42)
![img16](https://github.com/linaAs2004/Project-Web-log-analyser/assets/163998352/cb08c245-0cea-4acf-9181-542c38a3cd73)
![img17](https://github.com/linaAs2004/Project-Web-log-analyser/assets/163998352/719635b4-1676-4918-8355-a3a17b878723)

## Fonctionnalités
- **Visiteurs uniques par jour**
- **Requêtes analysées dans l'ensemble**
- **Fichiers demandés (URLs)**
- **Requêtes statiques**
- **URLs non trouvées**
- **Noms d'hôtes et adresses IP des visiteurs**
- **Géolocalisation**
- **Codes de statut HTTP**
- **Systèmes d'exploitation**
- **Navigateurs**

## Technologies et language de programmation utilisées
- PTHON
- Flask
- MySQL 
- HTML/CSS
- geoip2
- folium
- os
- logging
- re

## Configuration et déploiement
- **Configuration de l'environnement :** Assurez-vous d'avoir Python et Flask installés sur votre machine.
- **Configuration de la base de données :** Créez une base de données MySQL ou MongoDB et mettez à jour les informations de connexion dans le fichier de configuration de l'application.
# Web Log Analyzer Deployment Guide
## Prérequis

- [Multipass](https://multipass.run) installé sur votre machine
- Un projet local contenant le code source de votre application

## Étapes de déploiement

### 1. Créer et monter le répertoire du projet

Créez une instance Multipass et montez le répertoire de votre projet :
     1. **multipass launch --name primary --mount C:/Users/HP/Desktop/Project-Web-log-analyser:/home/ubuntu/ProjetWebLogAnalyser**
  Création du répértoire portant le projet en le montant sur l'instance primary  
     2. **Multipass list**:   Pour checker si l'instance est créer.  
     3. **Multipass shell primary**:   Lancement de l'instance primary.  
     4. **ls**:   Pour checker si le dossier a bien été monter.   
     5. **cd ProjetWebLogAnalyser**:   Pour rentrer dans le repertoire.  
     6. **ls**:   Voila le resultat = Controller.py  Dao.py     Templates    etl.py    map.py  pays.py  services.py  DATA   README.md  __pycache__  fcai_c_map.html  secure  
     7. **python3 -m venv myenv**:   Pour créer un environnement virtuelle  
     8. **source myenv/bin/activate**:    Pour rentrer dans l'environnement virtuelle  
     9. **nano start_app.sh**:    Créez un script de démarrage contenant les commandes pour démarrer votre application =
        source /home/ubuntu/ProjetWebLogAnalyser/myenv/bin/activate
        python3 /home/ubuntu/ProjetWebLogAnalyser/Controller.py  
   10. **cd /etc/systemd/system** :   Pour naviguer ver ce repertoire  
   11. **sudo su**  ---> **touch /etc/systemd/system/flask_app.service**
                    ---> **nano /etc/systemd/system/flask_app.service**
       
                        [Unit]
                        Description=Web logs analyser app
                        After=network.target
                        [Service]
                        User=ubuntu
                        WorkingDirectory=/home/ubuntu/ProjetWebLogAnalyser
                        ExecStart=/home/ubuntu/ProjetWebLogAnalyser/myenv/bin/python3                                                /home/ubuntu/ProjetWebLogAnalyser/Controller.py
                        Restart=always
                        [Install]
                        WantedBy=multi-user.target
   12. **ctrl¨d** :   pour sortir  
   13. **sudo systemctl daemon-reload**  
   14. **sudo systemctl enable flask_app.service**  
   15. **sudo systemctl start flask_app.service**  
   16. **sudo systemctl status flask_app.service**  
   17. **cd /home/ubuntu/ProjetWebLogAnalyser**  
   18. **sudo apt update**  
   19. **sudo apt install python3-flask python3-mysql.connector python3-matplotlib python3-geoip2 python3-folium -y**  
   20. **ls** = Controller.py  Dao.py     Templates    etl.py           flask_app.log         map.py  pays.py  services.py DATA  README.md  __pycache__  fcai_c_map.html  flask_app_backup.log  myenv   secure   start_app.sh  
   21. **python3 Controller.py** :   Pour enfin lancer l'application sur le navigateur.  
           



