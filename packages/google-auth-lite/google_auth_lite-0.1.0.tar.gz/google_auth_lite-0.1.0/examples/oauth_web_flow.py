# examples/oauth_web_flow.py

from flask import Flask, redirect, request, session, url_for
from google_auth_rewired.oauth_flow import GoogleOAuthFlow
import os
import json

# 🔐 ENV CONFIG (REPLACE with your own)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"
SCOPES = ["openid", "email", "profile"]

app = Flask(__name__)
app.secret_key = os.urandom(24)

flow = GoogleOAuthFlow(CLIENT_ID, CLIENT_SECRET, SCOPES, REDIRECT_URI)

@app.route("/")
def index():
    return '<a href="/login">Login with Google</a>'

@app.route("/login")
def login():
    auth_url = flow.auth_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    response_url = request.url
    token = flow.fetch_token(response_url)
    session["token"] = token
    return redirect(url_for("profile"))

@app.route("/profile")
def profile():
    token = session.get("token")
    if not token:
        return redirect(url_for("index"))
    
    import requests
    headers = {"Authorization": f"Bearer {token['access_token']}"}
    resp = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers=headers)

    if resp.status_code == 200:
        user_info = resp.json()
        return f"<h1>Logged in as {user_info['email']}</h1><pre>{json.dumps(user_info, indent=2)}</pre>"
    else:
        return "Failed to fetch user info", 400

if __name__ == "__main__":
    app.run(debug=True)

"""
🧪 How to Run:

# In your terminal:
export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="your-client-secret"
python examples/oauth_web_flow.py

Then visit:
👉 http://localhost:5000

You’ll:
1. Click login → redirected to Google
2. Consent
3. Come back to /callback
4. See your email & profile data on /profile
"""
