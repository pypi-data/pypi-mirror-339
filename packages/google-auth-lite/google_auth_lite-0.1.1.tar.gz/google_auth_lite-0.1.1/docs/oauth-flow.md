### ✅ `docs/oauth-flow.md`


# 🔐 OAuth 2.0 Flow (User Consent)

This guide covers how to authenticate **as a user** instead of a service account. This is helpful when:

- You need to access a user’s Gmail, Drive, or Calendar
- You're building a local CLI or web app with user login
- The API you're using doesn't support service accounts

---

## 🚀 When to Use OAuth2

✅ Use this if you need to:
- Send emails from a user's Gmail
- Access **their** Google Drive
- Read their Google Sheets, Calendar, etc.

❌ Not needed if you're using:
- Cloud services with service accounts
- Internal GCP infra (Cloud Run, GCS)

---

## ⚙️ Setup on Google Cloud Console

1. Go to your [Google Cloud Project](https://console.cloud.google.com/)
2. Navigate to:  
   **APIs & Services → Credentials**
3. Click **“Create Credentials” → “OAuth client ID”**
4. Choose:
   - **Desktop App** (for CLI tools)  
   - or **Web Application** (for web apps)
5. Download the `client_secret.json` file  
   (rename to `client_oauth.json` if you want)

---

## 🧪 Using in Code

```python
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_oauth.json",
    scopes=SCOPES,
)
credentials = flow.run_local_server(port=8080)

print("Access token:", credentials.token)
```

This launches a local browser tab to ask for user consent. After approval, it prints the access token.

---

## 🧠 Storing the Token

You can store the token to avoid repeated login:

```python
import pickle

# Save token
with open("token.pkl", "wb") as f:
    pickle.dump(credentials, f)

# Load token
with open("token.pkl", "rb") as f:
    credentials = pickle.load(f)
```

---

## 🔄 Refreshing the Token

Google's OAuth2 credentials auto-refresh when expired:

```python
from google.auth.transport.requests import Request

if credentials.expired and credentials.refresh_token:
    credentials.refresh(Request())
```

---

## ✅ Summary

| Step | Action |
|------|--------|
| 1 | Create OAuth Client ID (desktop or web) |
| 2 | Use `google-auth-oauthlib.flow` |
| 3 | Get user consent via browser |
| 4 | Store & refresh credentials securely |
| 5 | Use the access token in your requests |

---

## 💬 Coming Soon

We plan to include a full wrapper in:
```
google_auth_rewired/oauth_flow.py
```

Stay tuned. 😎
```

---