from PIL import Image

def create_white_spot_layer(subject_cutout_path, output_path):
    img = Image.open(subject_cutout_path).convert("L")  # Grayscale
    white_img = Image.new("L", img.size, 0)  # All black initially
    white_mask = img.point(lambda p: 255 if p > 10 else 0)  # Binary mask
    white_img.paste(255, mask=white_mask)  # Paste white using mask
    white_img = white_img.convert("RGBA")
    white_img.save(output_path)
