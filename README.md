# 🔐 VAULT — File Encryptor

A web application for encrypting and decrypting files using **AES-256-GCM**, one of the strongest authenticated encryption algorithms available. Built with Python/Flask and containerized with Docker.

<p align="center">
  <img width="49%" alt="screenshot-encrypt" src="https://github.com/user-attachments/assets/6df3a044-414d-4305-9585-9bebce30afb8" />
  <img width="49%" alt="screenshot-decrypt" src="https://github.com/user-attachments/assets/1d49ed72-e624-4e1e-84a7-e4ca7fe3fd79" />
</p>
---

## ✨ Features

- **AES-256-GCM encryption** — authenticated encryption that guarantees both confidentiality and integrity
- **Auto key generation** — generates a cryptographically secure random key if none is provided
- **Key file support** — save and load `.key` files for convenience
- **Drag & drop interface** — clean, modern UI with real-time feedback
- **Zero dependencies on the client** — all processing happens on the server

---

## 🚀 Getting Started

### Requirements

- [Docker](https://www.docker.com/) installed

### Run with Docker

```bash
# Build the image
docker build -t vault-encryptor .

# Run the container
docker run -p 5000:5000 vault-encryptor
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🛠️ Tech Stack

| Layer     | Technology          |
|-----------|---------------------|
| Backend   | Python 3.11 + Flask |
| Crypto    | PyCryptodome (AES-256-GCM) |
| Frontend  | Vanilla HTML/CSS/JS |
| Container | Docker              |

---

## 🔒 How It Works

### Encryption
1. A 256-bit key is generated (or provided by the user)
2. A random 128-bit nonce is generated per encryption
3. The file is encrypted using AES-GCM, producing a ciphertext and a 128-bit authentication tag
4. The output file is structured as: `nonce (16B) + tag (16B) + ciphertext`

### Decryption
1. The nonce and tag are extracted from the file header
2. AES-GCM decrypts and **verifies the tag** — any tampering is detected
3. The original file is restored

---

## ⚠️ Security Notes

- **Save your key.** There is no key recovery — losing the key means losing the file permanently.
- The encryption key is returned via the `X-Key` response header after encryption. In a production scenario with stronger security requirements, encryption would be performed entirely on the client side using the [Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API), so the key never leaves the browser.
- File size is limited to **100MB** per upload.

---

## 📁 Project Structure

```
vault/
├── app.py              # Flask application and API routes
├── requirements.txt    # Python dependencies (pinned versions)
├── Dockerfile          # Container definition
├── .dockerignore       # Docker build exclusions
└── templates/
    └── index.html      # Frontend UI
```

---

## 📄 License

MIT — feel free to use, modify, and distribute.
