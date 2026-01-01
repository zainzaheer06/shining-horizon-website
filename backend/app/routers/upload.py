from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os
import uuid

from ..database import get_db
from ..config import settings
from ..services.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "svg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/image/{folder}")
async def upload_image(
    folder: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # Validate folder
    valid_folders = ["products", "categories", "brands"]
    if folder not in valid_folders:
        raise HTTPException(status_code=400, detail=f"Invalid folder. Must be one of: {valid_folders}")
    
    # Validate file extension
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}")
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max size: 5MB")
    
    # Generate unique filename
    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    
    # Create upload directory if not exists
    upload_dir = os.path.join(settings.UPLOAD_DIR, folder)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    filepath = os.path.join(upload_dir, unique_filename)
    with open(filepath, "wb") as f:
        f.write(content)
    
    # Return relative path for database storage
    relative_path = f"backend/uploads/{folder}/{unique_filename}"
    
    return {
        "filename": unique_filename,
        "path": relative_path,
        "url": f"/uploads/{folder}/{unique_filename}"
    }

@router.delete("/image")
async def delete_image(
    path: str,
    current_user: User = Depends(get_current_user)
):
    # Security check - only allow deleting from uploads folder
    if not path.startswith("backend/uploads/"):
        raise HTTPException(status_code=400, detail="Invalid path")
    
    full_path = os.path.join(settings.BASE_DIR, path.replace("backend/", ""))
    
    if os.path.exists(full_path):
        os.remove(full_path)
        return {"message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")
