import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from crypto_utils import encrypt_message, decrypt_message
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def handle_receive(conn, key):
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break
            msg = decrypt_message(key, data)
            print(Fore.MAGENTA + f"\n[Client] {msg}\n" + Fore.GREEN + "[You] ", end="")
            if msg.lower().strip() == "exit":
                break
        except Exception as e:
            print(Fore.RED + f"\n[Error receiving] {e}")
            break

def handle_send(conn, key):
    while True:
        try:
            msg = input(Fore.GREEN + "[You] " + Style.RESET_ALL)
            encrypted = encrypt_message(key, msg)
            conn.send(encrypted)
            if msg.lower().strip() == "exit":
                break
        except Exception as e:
            print(Fore.RED + f"\n[Error sending] {e}")
            break

def server_program():
    host = "127.0.0.1"
    port = 12346

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(Fore.CYAN + f"[*] Server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(Fore.CYAN + f"[*] Connected to {addr}")

    # RSA key exchange
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    conn.send(public_key)

    encrypted_key = conn.recv(4096)
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
    symmetric_key = cipher_rsa.decrypt(encrypted_key)

    print(Fore.YELLOW + "[System] Secure AES key exchange complete.")

    # Start threaded chat
    threading.Thread(target=handle_receive, args=(conn, symmetric_key), daemon=True).start()
    handle_send(conn, symmetric_key)

    conn.close()
    server_socket.close()
    print(Fore.CYAN + "[*] Server closed.")

if __name__ == "__main__":
    server_program()
