import json
import requests
import time

API_KEY = "RIedjaXdoYC6Nsut9LloWwdAltAnqHY72zHOllzPETJS"
TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"
TOKEN_FILE = "token.json"

# حفظ التوكن في ملف JSON
def save_token_to_file(token_data):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f)

# استرجاع التوكن من ملف JSON
def load_token_from_file():
    try:
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"access_token": None, "expires_at": 0}

# الحصول على توكن جديد
def get_new_access_token():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
        'apikey': API_KEY
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        token_response = response.json()
        token_data = {
            "access_token": token_response['access_token'],
            "expires_at": token_response['expiration']
        }
        save_token_to_file(token_data)
        print("تم الحصول على Access Token جديد.")
        return token_response['access_token']
    else:
        print(f"خطأ: {response.status_code}")
        print(response.text)
        return None

# التحقق من صلاحية التوكن وتجديده إذا لزم الأمر
def get_valid_access_token():
    token_data = load_token_from_file()
    current_time = int(time.time())

    if token_data['access_token'] is None or current_time >= token_data['expires_at']:
        print("انتهت صلاحية التوكن. يتم تجديده الآن...")
        return get_new_access_token()
    else:
        return token_data['access_token']
