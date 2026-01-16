Projet : Ransomware Pédagogique (C2 & Malware)
<img width="1600" height="1201" alt="unnamed" src="https://github.com/user-attachments/assets/e9634ab1-d1d4-4d76-9082-31d17ed0fbaa" />

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

    Deux machines (ou deux terminaux) sous Linux (Debian recommandé).

    Python 3 installé.

Étape 1 : Lancer le Serveur (Attaquant)

Ouvrez un terminal et placez-vous dans le dossier du serveur :
Bash

python3 /home/yassine/Documents/c2_server.py

Le serveur affichera : [*] SERVEUR C2 PRET - En attente de connexion...
Étape 2 : Lancer le Malware (Victime)

Ouvrez un second terminal et lancez l'agent :
Bash

python3 /home/yassine/Documents/ransomware_client.py

Étape 3 : Interaction

Une fois la connexion établie, le serveur affiche un menu d'aide. Vous pouvez alors taper :

    ls -a : Pour voir les fichiers de la victime.

    ENCRYPT : Pour lancer le chiffrement du HOME.

    cat ~/.system_trace.log : Pour voir les logs d'activité sur la victime.

    GET <fichier> : Pour voler un document.

6. Analyse des Limites

    Chiffrement : L'algorithme XOR est vulnérable à l'analyse de fréquence. Une amélioration serait l'utilisation de l'AES-256.

    Furtivité : Les communications circulent en clair sur le réseau. Dans un scénario réel, l'utilisation de TLS (SSL) serait nécessaire pour échapper aux systèmes de détection d'intrusion (IDS).

