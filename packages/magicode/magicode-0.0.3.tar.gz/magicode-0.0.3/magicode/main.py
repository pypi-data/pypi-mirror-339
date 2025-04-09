import warnings
warnings.filterwarnings("ignore")

import os
import json
from pathlib import Path
import click
import keyring
import requests
from typing import List
import mimetypes
from tqdm import tqdm

CONFIG_DIR = Path.home() / '.magicode'
CONFIG_FILE = CONFIG_DIR / 'config.json'
SERVICE_NAME = 'magicode'

def load_credentials():
    """Load credentials from config file if they exist"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def save_credentials(email, token):
    """Save credentials to config file"""
    CONFIG_DIR.mkdir(exist_ok=True)
    credentials = {
        'email': email,
        'token': token
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(credentials, f)

def get_credentials():
    """Get credentials from system keyring"""
    email = keyring.get_password(SERVICE_NAME, 'email')
    token = keyring.get_password(SERVICE_NAME, 'token')
    return email, token

def save_credentials_system(email, token):
    """Save credentials to system keyring"""
    keyring.set_password(SERVICE_NAME, 'email', email)
    keyring.set_password(SERVICE_NAME, 'token', token)

@click.group()
def cli():
    """MagiCode CLI tool"""
    pass

@cli.command()
def auth():
    """Authenticate with MagiCode"""
    # Check if credentials already exist
    existing_email, existing_token = get_credentials()
    if existing_email and existing_token:
        if not click.confirm('Credentials already exist. Do you want to overwrite them?'):
            click.echo('Authentication cancelled.')
            return

    email = click.prompt('Please enter your email')
    token = click.prompt('Please enter your secret token', hide_input=True)
    
    # Verify credentials before saving
    click.echo('Verifying credentials...')
    try:
        # Test credentials by requesting a presigned URL for a test file
        bucket_name = "magicode-user-data-store"
        verify_response = requests.post(
            'https://www.magicode.ai/api/s3-cli',
            params={'bucket': bucket_name},
            json={
                'email': email,
                'secretKey': token,
                'fileName': 'test-verification.txt',
            }
        )
        
        if verify_response.status_code != 200:
            click.echo(f'Invalid credentials. Authentication failed.', err=True)
            return
            
        click.echo('Credentials verified successfully.')
        save_credentials(email, token)
        save_credentials_system(email, token)
        click.echo('Credentials saved.')
    except Exception as e:
        click.echo(f'Error verifying credentials: {str(e)}', err=True)

@cli.command()
def logout():
    """Clear stored credentials"""
    try:
        keyring.delete_password(SERVICE_NAME, 'email')
        keyring.delete_password(SERVICE_NAME, 'token')
        click.echo('Logged out successfully.')
    except keyring.errors.PasswordDeleteError:
        click.echo('No credentials found.')

@cli.command()
@click.argument('source')
def upload(source: str):
    """Upload a file or folder to MagiCode
    
    SOURCE: Path to the file or folder to upload
    """
    # Get credentials
    email, token = get_credentials()
    if not email or not token:
        click.echo('Please authenticate first using the auth command.', err=True)
        return

    path = Path(source)
    if not path.exists():
        click.echo(f'Path does not exist: {path}', err=True)
        return

    files_to_upload: List[Path] = []
    folders_to_upload: List[Path] = []
    
    # Collect all files and folders
    if path.is_file():
        files_to_upload.append(path)
    else:
        # Add the root folder if it's a directory
        folders_to_upload.append(path)
        # Collect all subdirectories and files
        for item in path.rglob('*'):
            if item.is_file():
                files_to_upload.append(item)
            elif item.is_dir():
                folders_to_upload.append(item)

    total_items = len(files_to_upload) + len(folders_to_upload)
    error = False 
    errored_items = []
    current_index = 0

    # Upload empty content for folders first
    for folder_path in folders_to_upload:
        current_index += 1
        try:
            click.echo(f'Creating folder {current_index}/{total_items}: {folder_path}/')
            
            # Get relative path for the folder
            relative_path = folder_path.relative_to(path.parent)
            # Ensure folder path ends with '/'
            folder_key = str(relative_path) + '/' if not str(relative_path).endswith('/') else str(relative_path)

            # bucket name depends on the destination 
            bucket_name = "magicode-user-data-store"
            
            # Get presigned URL
            presigned_response = requests.post(
                'https://www.magicode.ai/api/s3-cli',
                params={'bucket': bucket_name},
                json={
                    'email': email,
                    'secretKey': token,
                    'fileName': folder_key,
                }
            )

            if presigned_response.status_code != 200:
                error = True
                errored_items.append(folder_path)
                continue

            presigned_data = presigned_response.json()
            presigned_url = presigned_data['presignedUrl']

            # Upload empty content for folder
            upload_response = requests.put(
                presigned_url,
                data=b'',
                headers={
                    'Content-Type': 'application/x-directory',
                    'Content-Length': '0'
                }
            )

            if upload_response.status_code not in (200, 204):
                error = True
                errored_items.append(folder_path)
                continue

        except Exception as e:
            error = True
            errored_items.append(folder_path)
            continue

    # Upload files
    for file_path in files_to_upload:
        current_index += 1
        try:
            click.echo(f'Uploading file {current_index}/{total_items}: {file_path}')
            
            # Get relative path for the file
            relative_path = file_path.relative_to(path.parent)

            # bucket name depends on the destination 
            bucket_name = "magicode-user-data-store"
            
            # Get presigned URL
            presigned_response = requests.post(
                'https://www.magicode.ai/api/s3-cli',
                params={'bucket': bucket_name},
                json={
                    'email': email,
                    'secretKey': token,
                    'fileName': str(relative_path),
                }
            )

            if presigned_response.status_code != 200:
                error = True
                errored_items.append(file_path)
                continue

            presigned_data = presigned_response.json()
            presigned_url = presigned_data['presignedUrl']

            # Upload file using presigned URL with progress bar
            file_size = os.path.getsize(file_path)
            with open(file_path, 'rb') as f:
                with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                    content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
                    file_data = f.read()
                    
                    def upload_callback(chunk_size):
                        pbar.update(chunk_size)
                    
                    upload_response = requests.put(
                        presigned_url,
                        data=file_data,
                        headers={
                            'Content-Type': content_type,
                            'Content-Length': str(file_size)
                        }
                    )
                    pbar.update(file_size - pbar.n)  # Ensure bar reaches 100%

            if upload_response.status_code not in (200, 204):
                error = True
                errored_items.append(file_path)
                continue

        except Exception as e:
            error = True
            errored_items.append(file_path)
            continue

    if error:
        click.echo(f'Upload has completed with errors.') 
        click.echo(f'The following items were not uploaded:') 
        for item in errored_items: 
            click.echo(f'  - {item}') 
        click.echo(f'Please check your credentials and try again.')
    else: 
        click.echo('Upload completed successfully.')

if __name__ == '__main__':
    cli()
