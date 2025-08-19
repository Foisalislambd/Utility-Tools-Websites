"""Image utility functions"""
from PIL import Image, ExifTags
import io
import base64
from typing import Dict, Any
from fastapi import UploadFile

async def resize_image(file: UploadFile, width: int, height: int) -> Dict[str, Any]:
    """Resize image"""
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Get original dimensions
        original_width, original_height = image.size
        
        # Resize image
        resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
        
        # Convert to base64
        img_buffer = io.BytesIO()
        format = image.format or 'PNG'
        resized_image.save(img_buffer, format=format)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return {
            "image": f"data:image/{format.lower()};base64,{img_str}",
            "original_size": {"width": original_width, "height": original_height},
            "new_size": {"width": width, "height": height},
            "format": format,
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

async def compress_image(file: UploadFile, quality: int = 80) -> Dict[str, Any]:
    """Compress image"""
    try:
        # Read image
        contents = await file.read()
        original_size = len(contents)
        image = Image.open(io.BytesIO(contents))
        
        # Compress image
        img_buffer = io.BytesIO()
        format = image.format or 'JPEG'
        
        if format.upper() == 'PNG':
            # For PNG, optimize without quality loss
            image.save(img_buffer, format=format, optimize=True)
        else:
            # For JPEG and others, use quality setting
            image.save(img_buffer, format=format, quality=quality, optimize=True)
        
        compressed_size = len(img_buffer.getvalue())
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        compression_ratio = round((1 - compressed_size / original_size) * 100, 2)
        
        return {
            "image": f"data:image/{format.lower()};base64,{img_str}",
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": f"{compression_ratio}%",
            "quality": quality,
            "format": format,
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

async def convert_image_format(file: UploadFile, target_format: str) -> Dict[str, Any]:
    """Convert image format"""
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        original_format = image.format
        
        # Convert format
        if target_format.upper() == 'JPEG' and image.mode in ('RGBA', 'LA', 'P'):
            # Convert to RGB for JPEG
            image = image.convert('RGB')
        
        img_buffer = io.BytesIO()
        image.save(img_buffer, format=target_format.upper())
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return {
            "image": f"data:image/{target_format.lower()};base64,{img_str}",
            "original_format": original_format,
            "new_format": target_format.upper(),
            "size": {"width": image.width, "height": image.height},
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

async def get_image_metadata(file: UploadFile) -> Dict[str, Any]:
    """Extract image metadata"""
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Basic info
        info = {
            "filename": file.filename,
            "format": image.format,
            "mode": image.mode,
            "size": {"width": image.width, "height": image.height},
            "file_size": len(contents)
        }
        
        # EXIF data
        exif_data = {}
        if hasattr(image, '_getexif') and image._getexif():
            exif = image._getexif()
            for tag_id, value in exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                exif_data[tag] = str(value)
        
        info["exif"] = exif_data
        info["success"] = True
        
        return info
    except Exception as e:
        return {"result": str(e), "success": False}

def extract_colors_from_image(file_path: str, num_colors: int = 5) -> Dict[str, Any]:
    """Extract dominant colors from image"""
    try:
        from collections import Counter
        
        # This is a simplified version - in production you'd use more sophisticated algorithms
        image = Image.open(file_path)
        image = image.convert('RGB')
        
        # Resize for faster processing
        image = image.resize((150, 150))
        
        # Get all pixels
        pixels = list(image.getdata())
        
        # Count color frequencies
        color_counts = Counter(pixels)
        most_common = color_counts.most_common(num_colors)
        
        colors = []
        for (r, g, b), count in most_common:
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            colors.append({
                "hex": hex_color,
                "rgb": f"rgb({r}, {g}, {b})",
                "frequency": count
            })
        
        return {
            "colors": colors,
            "total_pixels": len(pixels),
            "unique_colors": len(color_counts),
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}