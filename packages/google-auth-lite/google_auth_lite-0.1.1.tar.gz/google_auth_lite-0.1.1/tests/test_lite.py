# tests/test_lite.py

import os
import pytest
from google_auth_rewired.lite import GoogleAuthLite
from google_auth_rewired.scopes import DRIVE_READONLY


SERVICE_ACCOUNT_FILE = "key.json"


@pytest.mark.skipif(not os.path.exists(SERVICE_ACCOUNT_FILE), reason="key.json not found")
def test_instance_creation():
    """Sanity check: Can we create an instance of GoogleAuthLite?"""
    auth = GoogleAuthLite(SERVICE_ACCOUNT_FILE)
    assert auth.credentials is not None


@pytest.mark.skipif(not os.path.exists(SERVICE_ACCOUNT_FILE), reason="key.json not found")
def test_get_access_token():
    """Ensure access token can be retrieved and is non-empty."""
    auth = GoogleAuthLite(SERVICE_ACCOUNT_FILE)
    token = auth.get_access_token()
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.skipif(not os.path.exists(SERVICE_ACCOUNT_FILE), reason="key.json not found")
def test_drive_list_files():
    """Live test: call Google Drive API with read-only scope."""
    auth = GoogleAuthLite(SERVICE_ACCOUNT_FILE, scopes=[DRIVE_READONLY])
    response = auth.get("https://www.googleapis.com/drive/v3/files")
    assert response.status_code == 200
    assert "files" in response.json()
