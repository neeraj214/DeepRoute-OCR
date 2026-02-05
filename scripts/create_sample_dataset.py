import os
from PIL import Image, ImageDraw, ImageFont

def create_sample_dataset(base_dir="datasets/ocr_eval"):
    images_dir = os.path.join(base_dir, "images")
    labels_dir = os.path.join(base_dir, "labels")
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    
    samples = [
        ("sample1", "Hello World"),
        ("sample2", "OCR Testing"),
        ("sample3", "1234567890")
    ]
    
    for name, text in samples:
        # Create Image
        img = Image.new('RGB', (400, 100), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        # Use default font or try to load one. 
        # Default font is very small/bad, but let's try.
        # Ideally we load a ttf, but to avoid dependency on system fonts, we'll use simple drawing.
        d.text((10, 40), text, fill=(0, 0, 0))
        
        img_path = os.path.join(images_dir, f"{name}.png")
        img.save(img_path)
        
        # Create Label
        txt_path = os.path.join(labels_dir, f"{name}.txt")
        with open(txt_path, "w") as f:
            f.write(text)
            
    print(f"Created {len(samples)} samples in {base_dir}")

if __name__ == "__main__":
    create_sample_dataset()
