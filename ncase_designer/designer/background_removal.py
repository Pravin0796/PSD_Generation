import requests

REMOVE_BG_API_KEY = "<your_remove_bg_api_key>"

def remove_background(image_path, output_path):
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': image_file},
            data={'size': 'auto'},
            headers={'X-Api-Key': REMOVE_BG_API_KEY}
        )
    if response.status_code == 200:
        with open(output_path, 'wb') as out:
            out.write(response.content)
        return output_path
    else:
        raise Exception(f"Remove.bg Error: {response.status_code} - {response.text}")
