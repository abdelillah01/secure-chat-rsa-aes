import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from crypto_utils import encrypt_message, decrypt_message
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def handle_receive(sock, key):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            msg = decrypt_message(key, data)
            print(Fore.MAGENTA + f"\n[Server] {msg}\n" + Fore.GREEN + "[You] ", end="")
            if msg.lower().strip() == "exit":
                break
        except Exception as e:
            print(Fore.RED + f"\n[Error receiving] {e}")
            break

def handle_send(sock, key):
    while True:
        try:
            msg = input(Fore.GREEN + "[You] " + Style.RESET_ALL)
            encrypted = encrypt_message(key, msg)
            sock.send(encrypted)
            if msg.lower().strip() == "exit":
                break
        except Exception as e:
            print(Fore.RED + f"\n[Error sending] {e}")
            break

def client_program():
    host = "127.0.0.1"
    port = 12346

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(Fore.CYAN + f"[*] Connected to {host}:{port}")

    # Receive server's public key
    public_key = sock.recv(4096)
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))

    # Generate AES key
    symmetric_key = get_random_bytes(32)

    # Send encrypted AES key
    encrypted_key = cipher_rsa.encrypt(symmetric_key)
    sock.send(encrypted_key)
    print(Fore.YELLOW + "[System] Secure AES key exchange complete.")

    # Start threaded chat
    threading.Thread(target=handle_receive, args=(sock, symmetric_key), daemon=True).start()
    handle_send(sock, symmetric_key)

    sock.close()
    print(Fore.CYAN + "[*] Connection closed.")

if __name__ == "__main__":
    client_program()
