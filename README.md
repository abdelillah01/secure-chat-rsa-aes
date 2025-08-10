# 🔒 PySecureChat – RSA & AES Encrypted Messaging

This is a **secure client-server chat application** in Python, built using **RSA** for key exchange and **AES** for encrypted communication.  
I originally developed this project a while ago as a personal learning exercise in **cryptography** and **network programming**.  
Now, I’m publishing it here on GitHub to share it and keep it as part of my portfolio.

---

## ✨ Features

- **RSA 2048-bit** for secure key exchange
- **AES-256 (CBC mode)** for encrypted messages
- **HMAC-SHA256** for message integrity verification
- **Multi-threaded** send/receive communication
- **Colorized console output** (via `colorama`)
- **Graceful exit** with `"exit"` command
- Works on **localhost** by default


## 🛠 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/secure-chat.git
   cd secure-chat



2-Install dependencies

      pip install pycryptodome colorama

3-Run the server

      python server.py

4-Run the client (in another terminal)

      python client.py

## How It Works

   Server generates an RSA key pair and sends the public key to the client.

   Client generates a random 256-bit AES key, encrypts it with the server's public key, and sends it back.

   Both sides now share the same AES key for encrypting and decrypting messages.

  Messages are encrypted with AES-CBC and protected with HMAC-SHA256.

  Color output shows:

  🟣 Incoming messages (Fore.MAGENTA)

  🟢 Your messages (Fore.GREEN)

  🟡 System messages (Fore.YELLOW)

  🔴 Errors (Fore.RED)




## Author

Developed by abdelillah01
