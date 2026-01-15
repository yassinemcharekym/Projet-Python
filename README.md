Projet : Ransomware Pédagogique (C2 & Malware)
<img width="1600" height="1201" alt="unnamed" src="https://github.com/user-attachments/assets/e9634ab1-d1d4-4d76-9082-31d17ed0fbaa" />

1. Présentation du Projet

Ce projet a été réalisé dans le cadre du module Malware et sécurité offensive en Python. Il consiste en la conception d'un ransomware fonctionnel composé d'un serveur de contrôle (C2) et d'un agent malveillant (Client). L'objectif est de comprendre les mécanismes de manipulation du système de fichiers, le chiffrement symétrique et la communication réseau asynchrone.

2. Architecture Globale

Le système utilise une architecture Client-Serveur basée sur le protocole TCP.

    Le Serveur (C2) : Agit comme le centre de commandement. Il attend les connexions, stocke les informations de la victime (ID et Clé) et envoie des ordres interactifs.

Le Client (Malware) : Infecte la machine cible, s'identifie, et attend les instructions du serveur pour agir sur le système de fichiers.

3. Fonctionnalités Implémentées

Conformément au cahier des charges, les fonctionnalités suivantes sont opérationnelles:

Identification et Exfiltration

    UUID Unique : Le client récupère l'identifiant machine depuis /proc/sys/kernel/random/uuid pour une identification précise côté serveur.

Génération de Clé : Une clé de 16 caractères (A-Z) est générée via os.urandom (accès sécurisé à /dev/urandom).

Handshake Initial : Dès la connexion, le client transmet son UUID et sa clé de chiffrement au serveur.

Actions à Distance (C2)

    Chiffrement/Déchiffrement : Utilisation d'un algorithme XOR réversible. Le parcours du répertoire personnel est entièrement récursif.

Upload (Exfiltration) : Possibilité de transférer n'importe quel fichier de la victime vers le serveur.

Download (Infiltration) : Envoi de fichiers depuis le serveur vers la machine cible.

Reverse Shell : Exécution de commandes système (ls, whoami, pwd) sans privilèges administrateur avec retour de la sortie standard.

4. Protocole de Communication

Le protocole a été conçu pour être robuste et éviter la corruption des données lors des transferts binaires:

    Envoi de Commande : Le serveur envoie l'ordre en texte clair (ex: GET file.txt).

    Handshake de Taille : Pour les transferts, l'expéditeur envoie d'abord la taille totale en octets.

    Confirmation (READY) : Le destinataire confirme la réception de la taille, libérant le buffer.

    Transfert par Chunks : Les données sont transmises par blocs de 4096 octets pour ne pas saturer la mémoire.

5. Comment lancer le projet
Prérequis

    Une VM Linux (Debian/Ubuntu recommandée).

    Python 3 installé sur les deux machines.

Étapes

    Sur la machine Attaquant (Serveur) :
    Bash

python3 src/c2_server.py

Sur la machine Victime (Client) :
Bash

    python3 src/ransomware_client.py

    Utilisation : Suivez le menu d'aide qui s'affiche sur le serveur dès que la connexion est établie.

6. Limites et Faiblesses

Comme tout ransomware artisanal, ce projet présente des faiblesses analysées ci-dessous:

    Chiffrement XOR : Bien que réversible et rapide, le XOR est vulnérable à une analyse fréquentielle si la clé est courte ou si l'on possède un fichier original et sa version chiffrée.

Communication en Clair : Le flux TCP n'est pas encapsulé dans du TLS/SSL, ce qui rend les commandes et les fichiers exfiltrés visibles pour un IDS (Système de Détection d'Intrusion) ou un analyseur de paquets comme Wireshark.

Détection Statique : L'utilisation de bibliothèques standards comme os et subprocess rend le binaire facilement détectable par des solutions antivirus basées sur l'analyse comportementale.
