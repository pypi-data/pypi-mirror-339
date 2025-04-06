### 📄 `docs/getting-started.md` — **Google Auth Rewired: Getting Started**


# 🚀 Getting Started

Welcome to **Google Auth Rewired** — a lightweight Python auth toolkit designed to get you authenticated and calling Google APIs in seconds, not hours.

---

## 🔧 1. Setup & Install

Clone the repo and create a virtual environment:

```bash
git clone https://github.com/cureprotocols/google-auth-rewired.git
cd google-auth-rewired
python -m venv .venv
.venv\Scripts\activate     # On Windows
# Or
source .venv/bin/activate  # On macOS/Linux
```

Install dependencies:

```bash
pip install -e .[dev]
```

---

## 🔑 2. Service Account Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a **Service Account** and generate a key.
3. Save it as `key.json` in the project root.

> ✅ Add `key.json` to your `.gitignore`. Never commit secrets!

---

## ✅ 3. Run Tests

Quick sanity check:

```bash
python -m pytest -v
```

You should see:

```
3 passed in X.XXs
```

---

## 📦 4. Use an Example

Run the Drive API example:

```bash
python examples/drive_basic.py
```

Or Sheets, Gmail, GCS:

```bash
python examples/sheets_read.py
python examples/gmail_send.py
python examples/gcs_upload.py
```

---

## 📚 Want More?

Check out:

- [`docs/service-accounts.md`](service-accounts.md)
- [`docs/scopes-reference.md`](scopes-reference.md)
- [`docs/oauth-flow.md`](oauth-flow.md) (for user auth)
- [`examples/`](../examples)

---

## 🙌 You’re In

This is Python + Google auth with **zero bloat**, clean session management, token refresh, and readable code.

Let’s ship.

—
*Built for devs who want velocity, clarity, and control.*
```

---
