import json
import os
from pathlib import Path
from cryptography.fernet import Fernet

class CredentialManager:
    def __init__(self):
        self.cred_file = Path("backend/credentials.enc")
        self.key_file = Path("backend/secret.key")
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_create_key(self):
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
    
    def save_credential(self, website, username, password):
        credentials = self.load_all_credentials()
        credentials[website] = {
            "username": username,
            "password": password
        }
        
        encrypted_data = self.cipher.encrypt(json.dumps(credentials).encode())
        with open(self.cred_file, 'wb') as f:
            f.write(encrypted_data)
        
        print(f"✅ Credentials saved for {website}")
        return True
    
    def get_credential(self, website):
        credentials = self.load_all_credentials()
        return credentials.get(website.lower(), None)
    
    def load_all_credentials(self):
        if not self.cred_file.exists():
            return {}
        
        try:
            with open(self.cred_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Error loading credentials: {e}")
            return {}
    
    def delete_credential(self, website):
        credentials = self.load_all_credentials()
        if website in credentials:
            del credentials[website]
            
            encrypted_data = self.cipher.encrypt(json.dumps(credentials).encode())
            with open(self.cred_file, 'wb') as f:
                f.write(encrypted_data)
            
            print(f"✅ Deleted credentials for {website}")
            return True
        return False

credential_manager = CredentialManager()