### ✅ Here's a ready-to-commit version of `docs/scopes-reference.md`:


# 🔐 OAuth Scopes Reference

Google APIs require specific OAuth scopes to authorize access to data.  
This doc provides a clean, searchable list of scopes used across major Google APIs.

---

## 📁 Google Drive

| Scope | Purpose |
|-------|---------|
| `https://www.googleapis.com/auth/drive` | Full access to user's Drive |
| `https://www.googleapis.com/auth/drive.readonly` | View files in user's Drive |
| `https://www.googleapis.com/auth/drive.file` | Access only files created/opened by the app |

---

## 📧 Gmail

| Scope | Purpose |
|-------|---------|
| `https://www.googleapis.com/auth/gmail.send` | Send email as user |
| `https://www.googleapis.com/auth/gmail.readonly` | Read user's email |

---

## 📊 Google Sheets

| Scope | Purpose |
|-------|---------|
| `https://www.googleapis.com/auth/spreadsheets` | Full access to Sheets |
| `https://www.googleapis.com/auth/spreadsheets.readonly` | Read-only access to Sheets |

---

## ☁️ Google Cloud Storage (GCS)

| Scope | Purpose |
|-------|---------|
| `https://www.googleapis.com/auth/devstorage.full_control` | Full access to buckets & objects |
| `https://www.googleapis.com/auth/devstorage.read_only` | Read-only access to buckets & objects |

---

## 🔥 Firestore / Datastore

| Scope | Purpose |
|-------|---------|
| `https://www.googleapis.com/auth/datastore` | Read and write access to Firestore/Datastore |

---

## ☁️ Cloud Platform (Generic)

| Scope | Purpose |
|-------|---------|
| `https://www.googleapis.com/auth/cloud-platform` | Broad access to all Google Cloud services |

---

## 🔄 Identity & Impersonation

| Scope | Purpose |
|-------|---------|
| `https://www.googleapis.com/auth/iam` | Manage service accounts |
| `https://www.googleapis.com/auth/iam.credentials` | Sign blobs & tokens, impersonate |

---

## 🛠 How to Use

In code:

```python
from google_auth_rewired.scopes import DRIVE_READONLY

auth = GoogleAuthLite("key.json", scopes=[DRIVE_READONLY])
```

---

> ✅ Keep this file growing with real scopes from working projects.  
> Avoid listing unused enterprise-only scopes unless truly needed.

```

---