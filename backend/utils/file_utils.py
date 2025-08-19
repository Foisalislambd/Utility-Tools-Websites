"""File utility functions"""
import hashlib
import magic
import zipfile
import io
from typing import Dict, Any
from fastapi import UploadFile

async def calculate_file_hash(file: UploadFile, algorithm: str = "md5") -> Dict[str, Any]:
    """Calculate hash of uploaded file"""
    try:
        contents = await file.read()
        
        algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512
        }
        
        if algorithm not in algorithms:
            return {"result": "Unsupported algorithm", "success": False}
        
        hash_obj = algorithms[algorithm]()
        hash_obj.update(contents)
        result = hash_obj.hexdigest()
        
        return {
            "filename": file.filename,
            "hash": result,
            "algorithm": algorithm.upper(),
            "file_size": len(contents),
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

async def get_file_info(file: UploadFile) -> Dict[str, Any]:
    """Get detailed file information"""
    try:
        contents = await file.read()
        
        # File type detection
        try:
            mime_type = magic.from_buffer(contents, mime=True)
            file_type = magic.from_buffer(contents)
        except:
            mime_type = file.content_type or "unknown"
            file_type = "Unknown"
        
        # Basic info
        info = {
            "filename": file.filename,
            "size": len(contents),
            "mime_type": mime_type,
            "file_type": file_type,
            "success": True
        }
        
        # File extension
        if file.filename:
            extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ""
            info["extension"] = extension
        
        # Calculate hashes
        info["hashes"] = {
            "md5": hashlib.md5(contents).hexdigest(),
            "sha1": hashlib.sha1(contents).hexdigest(),
            "sha256": hashlib.sha256(contents).hexdigest()
        }
        
        return info
    except Exception as e:
        return {"result": str(e), "success": False}

async def extract_zip_info(file: UploadFile) -> Dict[str, Any]:
    """Extract information from ZIP file"""
    try:
        contents = await file.read()
        
        with zipfile.ZipFile(io.BytesIO(contents), 'r') as zip_file:
            file_list = []
            total_size = 0
            total_compressed = 0
            
            for info in zip_file.filelist:
                file_info = {
                    "filename": info.filename,
                    "size": info.file_size,
                    "compressed_size": info.compress_size,
                    "compression_ratio": round((1 - info.compress_size / info.file_size) * 100, 2) if info.file_size > 0 else 0,
                    "date_time": f"{info.date_time[0]}-{info.date_time[1]:02d}-{info.date_time[2]:02d} {info.date_time[3]:02d}:{info.date_time[4]:02d}:{info.date_time[5]:02d}",
                    "is_directory": info.filename.endswith('/')
                }
                file_list.append(file_info)
                total_size += info.file_size
                total_compressed += info.compress_size
            
            overall_compression = round((1 - total_compressed / total_size) * 100, 2) if total_size > 0 else 0
            
            return {
                "filename": file.filename,
                "total_files": len(file_list),
                "total_size": total_size,
                "total_compressed": total_compressed,
                "overall_compression": overall_compression,
                "files": file_list,
                "success": True
            }
    except Exception as e:
        return {"result": str(e), "success": False}

def analyze_file_duplicates(file_hashes: list) -> Dict[str, Any]:
    """Find duplicate files based on hashes"""
    try:
        from collections import defaultdict
        
        hash_groups = defaultdict(list)
        
        for file_info in file_hashes:
            hash_groups[file_info['hash']].append(file_info['filename'])
        
        duplicates = {hash_val: files for hash_val, files in hash_groups.items() if len(files) > 1}
        
        return {
            "total_files": len(file_hashes),
            "unique_files": len(hash_groups),
            "duplicate_groups": len(duplicates),
            "duplicates": duplicates,
            "space_wasted": sum(len(files) - 1 for files in duplicates.values()),
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def convert_file_format(file_content: bytes, from_format: str, to_format: str) -> Dict[str, Any]:
    """Convert between file formats (basic implementation)"""
    try:
        # This is a simplified implementation
        # In production, you'd use specific libraries for each format
        
        if from_format.lower() == "txt" and to_format.lower() == "pdf":
            # Text to PDF conversion would require reportlab
            return {"result": "PDF conversion requires additional setup", "success": False}
        
        # For now, return the original content
        return {
            "converted_content": base64.b64encode(file_content).decode(),
            "from_format": from_format,
            "to_format": to_format,
            "size": len(file_content),
            "success": True,
            "note": "Basic conversion - full implementation requires format-specific libraries"
        }
    except Exception as e:
        return {"result": str(e), "success": False}