from django.http import JsonResponse
from .adobe_auth import get_access_token
from .background_removal import remove_background
from .photoshop_api import upload_template_psd, apply_edits, add_subject_layer, update_text_layers


def test_adobe_auth(request):
    try:
        token = get_access_token()
        return JsonResponse({"access_token": token})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def test_photoshop(request):
    psd_path = "designer/assets/templates/card1.psd"  # Example template
    uri = upload_template_psd(psd_path)

    edits = {
        "edits": [
            {
                "operation": "text-set",
                "layerName": "D. Subject Name",
                "text": "Joe Smith"
            },
            {
                "operation": "text-set",
                "layerName": "E. Team Name",
                "text": "Red Rangers"
            }
        ]
    }

    result = apply_edits(uri, edits)
    return JsonResponse(result)

def generate_card(request):
    # Step 1: Remove background
    input_path = "designer/assets/uploads/joe.jpg"
    cutout_path = "designer/assets/uploads/joe_cutout.png"
    remove_background(input_path, cutout_path)

    # Step 2: Upload PSD and add subject
    template_path = "designer/assets/templates/card1.psd"
    template_uri = upload_template_psd(template_path)

    # Step 3: Add subject to PSD
    result = add_subject_layer(template_uri, cutout_path)

    return JsonResponse(result)

def generate_card(request):
    subject_name = "Joe Smith"
    team_name = "Red Rangers"

    # Assume background removal and subject upload already done
    template_path = "designer/assets/templates/card1.psd"
    template_uri = upload_template_psd(template_path)

    # Add subject to PSD
    cutout_path = "designer/assets/uploads/joe_cutout.png"
    add_subject_layer(template_uri, cutout_path)

    # Update subject and team name text layers
    update_text_layers(template_uri, subject_name, team_name)

    return JsonResponse({"message": "Text layers updated successfully"})
