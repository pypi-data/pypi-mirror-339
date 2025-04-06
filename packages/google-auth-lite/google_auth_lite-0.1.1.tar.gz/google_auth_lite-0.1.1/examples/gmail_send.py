# examples/gmail_send.py

from google_auth_rewired.lite import GoogleAuthLite
from google_auth_rewired.scopes import GMAIL_SEND

import base64
from email.mime.text import MIMEText

# Initialize with Gmail scope
auth = GoogleAuthLite("key.json", scopes=[GMAIL_SEND])

def create_message(sender, to, subject, body_text):
    """Create a MIMEText email and encode in base64url."""
    message = MIMEText(body_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": encoded_message}

# 🔁 Replace these with actual values
sender = "your-email@gmail.com"
to = "recipient@example.com"
subject = "Test Email"
body_text = "Hello from GoogleAuthLite!"

message = create_message(sender, to, subject, body_text)

# Send via Gmail API
res = auth.post("https://gmail.googleapis.com/gmail/v1/users/me/messages/send", json=message)
print("Status:", res.status_code)
print("Response:", res.json())
