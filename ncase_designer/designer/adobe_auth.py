import time
import json
import jwt
import requests
from pathlib import Path
from cryptography.hazmat.primitives import serialization

# Load Adobe credentials
with open('config/credentials.json', 'r') as f:
    config = json.load(f)

# Read private key
private_key_path = Path(config['private_key_path'])
private_key = private_key_path.read_text()

def get_access_token():
    jwt_payload = {
        "iss": config["org_id"],
        "sub": config["technical_account_id"],
        "aud": f"{config['ims_endpoint']}/c/{config['client_id']}",
        "exp": int(time.time()) + 60 * 60,
        f"{config['ims_endpoint']}/s/{config['meta_scopes'][0]}": True,
    }

    encoded_jwt = jwt.encode(
        jwt_payload,
        private_key,
        algorithm="RS256"
    )

    data = {
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "jwt_token": encoded_jwt
    }

    response = requests.post(f"{config['ims_endpoint']}/ims/exchange/jwt", data=data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Error getting token: {response.status_code} {response.text}")
