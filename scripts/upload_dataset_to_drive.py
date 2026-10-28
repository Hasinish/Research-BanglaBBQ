import os
import sys
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "Dataset_BanglaBBQ_New"

def get_drive_service():
    creds = Credentials.from_authorized_user_file(str(ROOT / "token.json"))
    return build('drive', 'v3', credentials=creds)

def create_folder(service, name, parent_id=None):
    metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        metadata['parents'] = [parent_id]
    folder = service.files().create(body=metadata, fields='id, name, webViewLink').execute()
    return folder

def upload_file(service, file_path: Path, parent_id):
    file_metadata = {
        'name': file_path.name,
        'parents': [parent_id]
    }
    media = MediaFileUpload(
        str(file_path),
        mimetype='application/jsonl',
        resumable=True,
        chunksize=5 * 1024 * 1024
    )
    request = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, size'
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"      Upload {int(status.progress() * 100)}%...", flush=True)
            
    return response

def main():
    service = get_drive_service()
    print("Connected to Google Drive API successfully.")
    
    # 1. Create Root Folder
    root_folder_name = "Dataset_BanglaBBQ_New"
    print(f"\n[1] Creating root folder '{root_folder_name}' in Google Drive...")
    root_folder = create_folder(service, root_folder_name)
    root_id = root_folder['id']
    root_link = root_folder.get('webViewLink')
    print(f"    Created Root Folder ID: {root_id}")
    print(f"    Initial Link: {root_link}")
    
    # Set permission so anyone with link can view (or keep accessible to user)
    try:
        service.permissions().create(
            fileId=root_id,
            body={'type': 'anyone', 'role': 'reader'},
            fields='id'
        ).execute()
        print("    Permissions set: Anyone with link can view.")
    except Exception as e:
        print(f"    Note on permissions: {e} (accessible via owner account)")
        
    # Re-fetch webViewLink
    res = service.files().get(fileId=root_id, fields='webViewLink').execute()
    final_link = res.get('webViewLink', root_link)
    
    # 2. Iterate Subfolders & Upload Files
    subdirs = sorted([d for d in DATASET_ROOT.iterdir() if d.is_dir()])
    print(f"\n[2] Found {len(subdirs)} category subdirectories to upload.")
    
    uploaded_files_count = 0
    total_bytes = 0
    
    for i, sub_dir in enumerate(subdirs, 1):
        print(f"\n--- [{i}/{len(subdirs)}] Processing folder: {sub_dir.name} ---")
        cat_folder = create_folder(service, sub_dir.name, parent_id=root_id)
        cat_folder_id = cat_folder['id']
        print(f"    Drive subfolder created: {cat_folder_id}")
        
        jsonl_files = sorted(list(sub_dir.glob("*.jsonl")))
        for f in jsonl_files:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"    Uploading file: {f.name} ({size_mb:.2f} MB)...")
            uploaded = upload_file(service, f, parent_id=cat_folder_id)
            uploaded_files_count += 1
            total_bytes += f.stat().st_size
            print(f"      Uploaded ID: {uploaded.get('id')} (Verified size: {uploaded.get('size')} bytes)")
            
    print("\n======================================================================")
    print("UPLOAD COMPLETE!")
    print(f"Total Category Folders Created: {len(subdirs)}")
    print(f"Total JSONL Files Uploaded: {uploaded_files_count}")
    print(f"Total Transferred Volume: {total_bytes / (1024*1024):.2f} MB")
    print(f"Google Drive Folder Link: {final_link}")
    print("======================================================================")
    
    return final_link

if __name__ == "__main__":
    main()
