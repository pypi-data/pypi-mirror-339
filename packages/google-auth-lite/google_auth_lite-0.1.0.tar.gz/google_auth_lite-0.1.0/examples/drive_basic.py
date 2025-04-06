# examples/drive_basic.py

from google_auth_rewired.lite import GoogleAuthLite
from google_auth_rewired.scopes import DRIVE_READONLY

auth = GoogleAuthLite("key.json", scopes=[DRIVE_READONLY])

# Call the Drive API to list files
response = auth.get("https://www.googleapis.com/drive/v3/files")

if response.status_code == 200:
    files = response.json().get("files", [])
    print("✅ Files in Drive:")
    for file in files:
        print(f"📄 {file.get('name')} (ID: {file.get('id')})")
else:
    print("❌ Failed to retrieve files:", response.text)
