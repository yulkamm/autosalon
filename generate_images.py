from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(text, filename, color=(100, 150, 200)):
    img = Image.new('RGB', (400, 300), color=color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((400 - text_width) // 2, (300 - text_height) // 2)
    draw.text(position, text, fill=(255, 255, 255), font=font)
    
    img.save(filename)
    print(f"Created: {filename}")

os.makedirs('static/images/cars', exist_ok=True)
os.makedirs('static/images/contacts', exist_ok=True)

car_colors = [
    (200, 50, 50), (50, 100, 200), (50, 150, 50),
    (150, 50, 150), (200, 150, 50), (50, 150, 150),
    (150, 100, 50), (100, 100, 100), (200, 100, 150), (100, 150, 100)
]

for i in range(1, 11):
    create_placeholder_image(
        f"Car {i}",
        f"static/images/cars/car_{i}.jpg",
        color=car_colors[i-1]
    )

contact_colors = [
    (100, 100, 200), (200, 100, 100), (100, 200, 100),
    (200, 200, 100), (100, 200, 200), (200, 100, 200),
    (150, 150, 150), (200, 150, 100), (150, 100, 200), (100, 200, 150)
]

for i in range(1, 11):
    create_placeholder_image(
        f"Client {i}",
        f"static/images/contacts/contact_{i}.jpg",
        color=contact_colors[i-1]
    )

print("\nAll images created!")
