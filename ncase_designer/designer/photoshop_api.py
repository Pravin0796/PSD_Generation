import requests
import json

from . import adobe_auth
from .adobe_auth import get_access_token

PHOTOSHOP_API_URL = "https://image.adobe.io/pie/psdService"
HEADERS = lambda token: {
    "Authorization": f"Bearer {token}",
    "x-api-key": "<your_client_id>",
    "Content-Type": "application/json"
}

def upload_template_psd(psd_file_path):
    token = get_access_token()

    # Step 1: Upload PSD to cloud
    with open(psd_file_path, "rb") as f:
        response = requests.post(
            f"{PHOTOSHOP_API_URL}/upload",
            headers={
                "Authorization": f"Bearer {token}",
                "x-api-key": "<your_client_id>",
                "Content-Type": "application/octet-stream"
            },
            data=f
        )
    response.raise_for_status()
    return response.json()["uri"]

def apply_edits(template_uri, edits_json):
    token = get_access_token()
    payload = {
        "inputs": {
            "href": template_uri,
            "storage": "adobe"
        },
        "options": edits_json
    }

    response = requests.post(
        f"{PHOTOSHOP_API_URL}/job",
        headers=HEADERS(token),
        data=json.dumps(payload)
    )
    response.raise_for_status()
    return response.json()

def add_subject_layer(template_uri, subject_png_path, layer_name="B. New Subject", target_layer="C. Subject"):
    token = get_access_token()

    with open(subject_png_path, "rb") as f:
        upload_resp = requests.post(
            f"{PHOTOSHOP_API_URL}/upload",
            headers={
                "Authorization": f"Bearer {token}",
                "x-api-key": "<your_client_id>",
                "Content-Type": "application/octet-stream"
            },
            data=f
        )
    upload_resp.raise_for_status()
    subject_uri = upload_resp.json()["uri"]

    # Create layer edit
    payload = {
        "inputs": {
            "href": template_uri,
            "storage": "adobe"
        },
        "options": {
            "edits": [
                {
                    "operation": "add-image",
                    "href": subject_uri,
                    "layerName": layer_name,
                    "insertBelowLayerName": target_layer,
                    "resize": {
                        "scaleMode": "fit",
                        "width": 600,
                        "height": 800
                    }
                },
                {
                    "operation": "copy-layer-style",
                    "fromLayerName": target_layer,
                    "toLayerName": layer_name
                }
            ]
        }
    }

    response = requests.post(
        f"{PHOTOSHOP_API_URL}/job",
        headers=HEADERS(token),
        data=json.dumps(payload)
    )
    response.raise_for_status()
    return response.json()

def update_text_layers(template_uri, subject_name, team_name):
    token = get_access_token()

    payload = {
        "inputs": {
            "href": template_uri,
            "storage": "adobe"
        },
        "options": {
            "edits": [
                {
                    "operation": "update-text",
                    "layerName": "D. Subject Name",
                    "text": subject_name,
                    "style": {
                        "fontSize": 14,
                        "font": "Arial-BoldMT"
                    }
                },
                {
                    "operation": "update-text",
                    "layerName": "E. Team Name",
                    "text": team_name,
                    "style": {
                        "fontSize": 10,
                        "font": "ArialMT"
                    }
                }
            ]
        }
    }

    response = requests.post(
        f"{PHOTOSHOP_API_URL}/job",
        headers=HEADERS(token),
        data=json.dumps(payload)
    )
    response.raise_for_status()
    return response.json()


def add_white_spot_layer(template_uri, white_spot_path):
    token = get_access_token()

    # Upload the image first (or use direct URL if hosted)
    image_uri = upload_subject_image(white_spot_path)

    payload = {
        "inputs": {
            "href": template_uri,
            "storage": "adobe"
        },
        "options": {
            "edits": [
                {
                    "operation": "add-image",
                    "layerName": "A. White Spot",
                    "image": {"href": image_uri, "storage": "adobe"},
                    "position": {"x": 0, "y": 0},
                    "size": {"width": 1000, "height": 1400}
                }
            ]
        }
    }

    response = requests.post(
        f"{PHOTOSHOP_API_URL}/job",
        headers=HEADERS(token),
        data=json.dumps(payload)
    )
    return response.json()
