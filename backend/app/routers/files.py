import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

router = APIRouter(prefix="/files", tags=["Files"])

class FileOperationRequest(BaseModel):
    path: str
    content: Optional[str] = None
    is_directory: bool = False

class RenameRequest(BaseModel):
    old_path: str
    new_path: str

BASE_DIR = os.path.abspath("generated_projects") # Sanitize this in real prod

def secure_path(path: str) -> str:
    # Basic path traversal protection
    # In a real app, use a more robust sandbox
    full_path = os.path.abspath(os.path.join(BASE_DIR, path))
    if not full_path.startswith(BASE_DIR):
        raise HTTPException(status_code=403, detail="Access denied: Path outside project root")
    return full_path

@router.post("/create")
def create_file_or_folder(request: FileOperationRequest):
    full_path = secure_path(request.path)
    
    if request.is_directory:
        os.makedirs(full_path, exist_ok=True)
        return {"message": f"Directory created: {request.path}"}
    else:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(request.content or "")
        return {"message": f"File created: {request.path}"}

@router.delete("/delete")
def delete_file_or_folder(path: str = Body(..., embed=True)):
    full_path = secure_path(path)
    
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File or directory not found")

    if os.path.isdir(full_path):
        shutil.rmtree(full_path)
    else:
        os.remove(full_path)
    
    return {"message": f"Deleted: {path}"}

@router.put("/rename")
def rename_file_or_folder(request: RenameRequest):
    old_full_path = secure_path(request.old_path)
    new_full_path = secure_path(request.new_path)
    
    if not os.path.exists(old_full_path):
        raise HTTPException(status_code=404, detail="Source path not found")
        
    if os.path.exists(new_full_path):
        raise HTTPException(status_code=409, detail="Destination path already exists")

    os.rename(old_full_path, new_full_path)
    return {"message": f"Renamed {request.old_path} to {request.new_path}"}
