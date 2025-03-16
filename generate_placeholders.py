from PIL import Image, ImageDraw, ImageFont
import os

# Create images directory if it doesn't exist
os.makedirs("images", exist_ok=True)

# List of tree names matching tree_data.py
trees = [
    "albizia", "ailante", "aulne", "arbre_judee", "chene",
    "erable", "hetre", "pin", "saule", "bouleau",
    "charme", "marronnier", "tilleul", "robinier",
    "platane", "orme", "peuplier", "if"
]

# Generate a simple colored rectangle for each tree
for tree in trees:
    # Create a new image with a white background
    img = Image.new('RGB', (400, 300), color='white')
    d = ImageDraw.Draw(img)

    # Draw a colored rectangle
    d.rectangle(((50, 50), (350, 250)), fill='lightgreen', outline='darkgreen', width=2)

    # Add tree name
    d.text((200, 150), tree, fill='black', anchor="mm")

    # Save the image
    img.save(f"images/{tree}.jpg")