from google_auth_rewired.lite import GoogleAuthLite
from google_auth_rewired.scopes import SHEETS_READONLY

# Replace with your actual spreadsheet ID
SPREADSHEET_ID = "your-sheet-id-here"
RANGE = "Sheet1!A1:D5"  # Modify as needed

auth = GoogleAuthLite("key.json", scopes=[SHEETS_READONLY])

url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{RANGE}"

resp = auth.get(url)
data = resp.json()

print("✅ Google Sheets Data:")
for row in data.get("values", []):
    print(row)
