import os
from PIL import Image

def compress_image(image_path, quality=80):
    try:
        img = Image.open(image_path)
        
        file_name, ext = os.path.splitext(image_path)
        output_path = f"{file_name}_compressed{ext}"
        
        img.save(output_path, optimize=True, quality=quality)
        
        original_size = os.path.getsize(image_path)
        compressed_size = os.path.getsize(output_path)
        reduction = (1 - compressed_size / original_size) * 100
        
        return f"{output_path} (Reduced by {reduction:.1f}%)"
    except Exception as e:
        raise Exception(f"Failed to compress image: {str(e)}") 