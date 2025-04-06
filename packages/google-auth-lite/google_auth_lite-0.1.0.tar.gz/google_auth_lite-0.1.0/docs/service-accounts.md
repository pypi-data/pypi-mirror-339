### ✅ `docs/service-accounts.md`


# 🔐 Service Accounts Guide

Google Cloud service accounts are **robot identities** used to authenticate securely with Google APIs — without manual login.

This guide shows how to create, download, and use a service account with `google-auth-rewired`.

---

## 1. 🧱 Create a Service Account

1. Go to [Google Cloud Console → IAM & Admin → Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts).
2. Click **Create Service Account**.
3. Give it a name like: `google-auth-lite`
4. Click **Create and Continue**.
5. Assign role: `Editor` or more specific (like `Storage Admin`, `Drive Viewer`, etc).
6. Click **Done**.

---

## 2. 📁 Create and Download `key.json`

1. Click your newly created service account.
2. Go to the **Keys** tab.
3. Click **Add Key → Create new key**.
4. Select **JSON**, then click **Create**.
5. A `.json` file will download — **rename it to**:

```
key.json
```

And place it in your project root directory.

> ✅ This file is sensitive. **Never commit it to version control.**  
> Be sure it’s in your `.gitignore`.

---

## 3. 🧪 Test It Locally

Once `key.json` is in your root, run:

```bash
python -m pytest -v
```

All tests should pass, including access token and live API calls (e.g., Drive, Sheets).

---

## 4. 📂 Enable APIs You Need

Go to [API & Services → Library](https://console.cloud.google.com/apis/library) and **enable** the APIs your service account needs:

- Google Drive API
- Gmail API
- Google Sheets API
- Google Cloud Storage API
- etc.

---

## 5. 🤝 Grant File Access (For Drive / Gmail)

For some APIs like **Google Drive**, you must **share the resource** (file or folder) with your service account email:

```
your-service-account@your-project-id.iam.gserviceaccount.com
```

---

## 6. 🔒 Best Practices

- Restrict API scopes via `scopes.py`
- Never commit `key.json`
- Use `GOOGLE_APPLICATION_CREDENTIALS` for secure runtime environments (Cloud Run, CI/CD, etc.)

---

💡 Once your `key.json` works locally, you’re fully wired to start calling APIs securely with `GoogleAuthLite`.

```
from google_auth_rewired import GoogleAuthLite

auth = GoogleAuthLite("key.json")
token = auth.get_access_token()
```

🔥 Execute with no overhead. You’re now in full control.
```

---