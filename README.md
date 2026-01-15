# Ransomware Pédagogique - Projet Python

## Description
[cite_start]Ce projet est un ransomware éducatif développé dans le cadre du module "Malware et sécurité offensive"[cite: 4]. [cite_start]Il illustre le fonctionnement d'un malware contrôlé à distance (C2) et les mécanismes de chiffrement de fichiers[cite: 5, 8].

## [cite_start]Fonctionnalités implémentées [cite: 129]
- [cite_start]**Identification unique** : Récupération de l'UUID via `/proc/sys/kernel/random/uuid`[cite: 49, 50].
- [cite_start]**Génération de clé** : Clé aléatoire (A-Z) générée via `os.urandom` (équivalent `/dev/urandom`)[cite: 41, 42].
- [cite_start]**Chiffrement XOR** : Algorithme symétrique et réversible appliqué récursivement[cite: 54, 55, 57].
- **C2 (Command & Control)** : 
    - [cite_start]Exécution de commandes système (Reverse Shell)[cite: 79].
    - [cite_start]Exfiltration de fichiers (Upload)[cite: 77].
    - [cite_start]Infiltration de fichiers (Download)[cite: 78].
    - [cite_start]Contrôle du chiffrement/déchiffrement à distance[cite: 78].

## [cite_start]Architecture [cite: 130]
Le projet repose sur une architecture **Client-Serveur** utilisant le protocole **TCP**. 
1. Le client se connecte au serveur et exfiltre immédiatement son ID et sa clé.
2. Le serveur maintient une session interactive pour envoyer des ordres.
3. Les transferts de fichiers utilisent un handshake (Taille -> READY -> Data) pour garantir l'intégrité des données binaires.



## [cite_start]Comment lancer le projet [cite: 131]
1. **Lancer le serveur** (sur la machine attaquante) :
   ```bash
   python3 src/c2_server.py
