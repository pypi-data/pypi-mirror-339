from google_auth_rewired.lite import GoogleAuthLite
from google_auth_rewired.scopes import GCS_FULL

# Replace these with your actual bucket and file
bucket_name = "your-bucket-name"
destination_blob = "uploaded.txt"
file_path = "local_file.txt"

auth = GoogleAuthLite("key.json", scopes=[GCS_FULL])

with open(file_path, "rb") as file_data:
    headers = {"Content-Type": "application/octet-stream"}
    url = f"https://storage.googleapis.com/upload/storage/v1/b/{bucket_name}/o?uploadType=media&name={destination_blob}"

    response = auth.post(url, headers=headers, data=file_data)

print("Status:", response.status_code)
print("Response:", response.json())
