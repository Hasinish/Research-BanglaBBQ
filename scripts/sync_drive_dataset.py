"""
sync_drive_dataset.py
---------------------
Idempotent synchronization script between local Dataset_BanglaBBQ_New/
and the shared Google Drive benchmark directory.

Google Drive Folder:
https://drive.google.com/drive/folders/1_Ui3wfvYvEF9b8HWsMZc7QUB2iID8Ibe
Root Folder ID: 1_Ui3wfvYvEF9b8HWsMZc7QUB2iID8Ibe

Ensures that whenever local canonical JSONLs change, existing files
in Google Drive are updated in-place without duplicating folders or files.
"""

import os
import sys
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "Dataset_BanglaBBQ_New"
DRIVE_ROOT_FOLDER_ID = "1_Ui3wfvYvEF9b8HWsMZc7QUB2iID8Ibe"

def get_drive_service():
    token_file = ROOT / "token.json"
    if not token_file.exists():
        raise FileNotFoundError(f"Missing OAuth token file at {token_file}")
    creds = Credentials.from_authorized_user_file(str(token_file))
    return build('drive', 'v3', credentials=creds)

def list_children(service, parent_id):
    """List all non-trashed children (files and folders) inside a parent folder."""
    items = []
    page_token = None
    while True:
        res = service.files().list(
            q=f"'{parent_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)",
            pageToken=page_token
        ).execute()
        items.extend(res.get('files', []))
        page_token = res.get('nextPageToken')
        if not page_token:
            break
    return items

def create_folder(service, name, parent_id):
    metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    return service.files().create(body=metadata, fields='id, name').execute()

def update_file(service, file_id, local_path: Path):
    media = MediaFileUpload(str(local_path), mimetype='application/jsonl', resumable=True)
    request = service.files().update(fileId=file_id, media_body=media, fields='id, name, size')
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"      Syncing {int(status.progress() * 100)}%...", flush=True)
    return response

def upload_new_file(service, local_path: Path, parent_id):
    metadata = {
        'name': local_path.name,
        'parents': [parent_id]
    }
    media = MediaFileUpload(str(local_path), mimetype='application/jsonl', resumable=True)
    request = service.files().create(body=metadata, media_body=media, fields='id, name, size')
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"      Uploading {int(status.progress() * 100)}%...", flush=True)
    return response

def sync_all():
    print(f"[*] Initializing Drive sync with root folder: {DRIVE_ROOT_FOLDER_ID}")
    service = get_drive_service()
    
    # 1. Fetch remote category subfolders
    remote_root_items = list_children(service, DRIVE_ROOT_FOLDER_ID)
    remote_folders = {
        item['name']: item['id']
        for item in remote_root_items
        if item['mimeType'] == 'application/vnd.google-apps.folder'
    }
    
    # 2. Iterate local category subdirectories
    local_subdirs = sorted([d for d in DATASET_ROOT.iterdir() if d.is_dir()])
    print(f"[*] Found {len(local_subdirs)} local category subdirectories in {DATASET_ROOT.name}")
    
    total_synced = 0
    total_updated = 0
    total_uploaded = 0
    
    for sub_dir in local_subdirs:
        cat_name = sub_dir.name
        if cat_name in remote_folders:
            cat_folder_id = remote_folders[cat_name]
        else:
            print(f"  [+] Creating missing Drive subfolder: {cat_name}")
            folder_obj = create_folder(service, cat_name, DRIVE_ROOT_FOLDER_ID)
            cat_folder_id = folder_obj['id']
            remote_folders[cat_name] = cat_folder_id
            
        # Get existing remote files in this subfolder
        remote_files = {
            item['name']: item
            for item in list_children(service, cat_folder_id)
            if item['mimeType'] != 'application/vnd.google-apps.folder'
        }
        
        local_jsonls = sorted(list(sub_dir.glob("*.jsonl")))
        for f in local_jsonls:
            local_size = f.stat().st_size
            if f.name in remote_files:
                remote_info = remote_files[f.name]
                remote_size = int(remote_info.get('size', 0))
                
                # Check if size matches
                if local_size != remote_size:
                    print(f"  [UPDATE] {cat_name}/{f.name}: size mismatch (Local: {local_size} vs Drive: {remote_size}). Updating...")
                    update_file(service, remote_info['id'], f)
                    total_updated += 1
                else:
                    # File is already up to date
                    pass
            else:
                print(f"  [UPLOAD] {cat_name}/{f.name}: file not found on Drive. Uploading...")
                upload_new_file(service, f, cat_folder_id)
                total_uploaded += 1
            total_synced += 1

    print("\n" + "=" * 60)
    print(f"DRIVE SYNC COMPLETE!")
    print(f"Total Canonical JSONL files verified: {total_synced}")
    print(f"Files updated in-place:               {total_updated}")
    print(f"New files uploaded:                   {total_uploaded}")
    print(f"Drive Folder Link: https://drive.google.com/drive/folders/{DRIVE_ROOT_FOLDER_ID}")
    print("=" * 60)

if __name__ == "__main__":
    sync_all()
