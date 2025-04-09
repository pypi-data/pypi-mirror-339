# 🔐 MiniSecret

[![PyPI version](https://img.shields.io/pypi/v/minisecret.svg)](https://pypi.org/project/minisecret/)
[![License](https://img.shields.io/github/license/Cognet-74/minisecret)](https://github.com/Cognet-74/minisecret)
[![Python](https://img.shields.io/pypi/pyversions/minisecret)](https://pypi.org/project/minisecret/)

**MiniSecret** is a minimal, secure secrets manager for Python projects and automation agents.  
It uses **AES-256-GCM encryption** and an environment-based master key to keep your secrets safe, simple, and offline.

---

## 📦 Features

- 🔒 AES-256-GCM authenticated encryption
- 🔐 Environment-based master key (`MINISECRET_KEY`)
- 🧊 Local encrypted file store (`secrets.enc.json`)
- ⚙️ Simple Python class + optional CLI tool
- 🧽 Secure memory auto-wipe for sensitive values
- 🚫 No cloud dependencies or runtime daemons

---

## 🧪 Summary Comparison

| Feature                   | MiniSecret     | python-keyring | python-decouple | hvac / AWS / GCP |
|---------------------------|----------------|----------------|------------------|------------------|
| 🔐 Encryption             | ✅ AES-256-GCM | ✅ OS-backed    | ❌ None           | ✅ Enterprise     |
| 📁 File-based             | ✅             | ❌              | ✅                | ❌                |
| 💻 Works offline          | ✅             | ✅              | ✅                | ⚠️ Limited        |
| 🧠 Simple to use          | ✅             | ✅              | ✅                | ❌                |
| 🛡️ Secrets in memory only | ✅ Optional     | ❌              | ❌                | ✅                |

---

## ⚙️ Installation

Install directly from [PyPI](https://pypi.org/project/minisecret/):

```bash
pip install minisecret
```

---

## 🔑 Setup: Master Key

### ✅ Step 1: Generate a Strong Key

```bash
python -c "import os, base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())"
```

---

### ✅ Step 2: Set the `MINISECRET_KEY` Environment Variable

#### 🔹 Linux/macOS (temporary)

```bash
export MINISECRET_KEY="your-generated-key"
```

To persist: add to `~/.bashrc`, `~/.zshrc`, or `.profile`.

#### 🔹 Windows PowerShell (temporary)

```powershell
$env:MINISECRET_KEY = "your-generated-key"
```

#### 🔹 Windows GUI (persistent)

1. Search for **"Environment Variables"**
2. Add a new **User variable**
   - Name: `MINISECRET_KEY`
   - Value: your-generated-key

---

## 🧪 Example: Store and Use Secrets

You want to store the following secret:

```
MySecretPassword
```

---

### ✅ CLI: Store the Secret

```bash
minisecret put my_password MySecretPassword
```

---

### ✅ CLI: Retrieve the Secret

```bash
minisecret get my_password
```

Secure retrieval (auto-wiped from memory):

```bash
minisecret get my_password --secure
```

List all stored keys:

```bash
minisecret list
```

---

### ✅ Python: Use the Stored Secret

```python
from minisecret import MiniSecret
import pyautogui
import time

secrets = MiniSecret()

# Secure version (wiped from memory immediately)
password = secrets.secure_get("my_password")

# Type the password into a GUI window
time.sleep(2)
pyautogui.write(password, interval=0.1)
```

---

## 🔐 Security Notes

- Secrets are encrypted with AES-256-GCM and stored in `secrets.enc.json`
- Secrets are decrypted only in memory when accessed
- Use `secure_get()` or `--secure` to clear secrets from memory after use
- Do **not** commit `secrets.enc.json` or your `MINISECRET_KEY` to version control

---

## ✅ CLI Summary

```bash
minisecret put <key> <value>
minisecret get <key> [--secure]
minisecret list
```

---

## 📚 License

[MIT](LICENSE)

---

## 💡 Ideas for the Future

- ⏳ Auto-expiring secrets
- 📦 Project-based secret stores
- 🔐 Password-prompt fallback for the master key
- 🧽 Clipboard auto-clear support

---

_Developed with ❤️ by [@Cognet-74](https://github.com/Cognet-74)_
```
