import os
import re
import requests
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(
    filename="mod_download.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def download_mod(url: str = None, mod_id: str = None, save_dir: str = None, 
                 overwrite: bool = False, use_api: bool = True) -> str:
    """
    Downloads a mod from Steam Workshop using either a full URL or a mod ID.
    
    If use_api is True, the download is performed via the custom API endpoint.
    Otherwise, it attempts a direct download from Steam (which may not yield a valid ZIP).
    
    Parameters:
        url (str): Full URL to the mod page (e.g. "https://steamcommunity.com/sharedfiles/filedetails/?id=123456789").
        mod_id (str): The Steam Workshop mod ID. Used if URL is not provided.
        save_dir (str): Folder path where the mod will be saved. Defaults to the current directory.
        overwrite (bool): Whether to overwrite the file if it already exists.
        use_api (bool): Whether to use the custom API endpoint for downloading.
        
    Returns:
        str: The full path to the downloaded file.
        
    Raises:
        ValueError: if neither a valid URL nor mod ID is provided.
        RuntimeError: for unexpected errors during download.
    """
    # If URL is provided, extract the mod ID
    if url:
        match = re.search(r'id=(\d+)', url)
        if match:
            mod_id = match.group(1)
        else:
            logging.error("Failed to extract mod ID from the URL.")
            raise ValueError("Invalid URL: could not extract mod ID.")
    
    if not mod_id:
        logging.error("No mod ID provided.")
        raise ValueError("You must provide a valid mod URL or mod ID.")

    file_name = f"mod_{mod_id}.zip"
    
    if not save_dir:
        save_dir = os.getcwd()
    
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file_name)
    
    if os.path.exists(file_path) and not overwrite:
        logging.info(f"File already exists: {file_path}")
        print(f"Download skipped: '{file_name}' already exists.")
        return file_path

    try:
        # Use the custom API endpoint if desired
        if use_api:
            # Construye la URL de descarga usando tu API real.
            # La API espera un parámetro 'url' con la URL completa de Steam.
            download_url = (
                f"https://steamworkshopdownloader.up.railway.app/api/download"
                f"?url=https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}"
            )
        else:
            download_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}"
        
        print(f"Downloading mod from {download_url} ...")
        response = requests.get(download_url, stream=True, timeout=10)
        response.raise_for_status()
        
        # Verify that the response is a ZIP file
        content_type = response.headers.get("Content-Type", "")
        if "zip" not in content_type.lower():
            logging.error(f"Invalid content type: {content_type}")
            raise ValueError("The response is not a valid ZIP file.")
        
        total_size = int(response.headers.get("Content-Length", 0))
        with open(file_path, "wb") as file, tqdm(
            total=total_size, unit="B", unit_scale=True, desc=file_name
        ) as progress:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    progress.update(len(chunk))
        
        # Check if the file was properly downloaded
        if os.path.getsize(file_path) == 0:
            os.remove(file_path)
            logging.error("Downloaded file is empty, removed file.")
            raise RuntimeError("Downloaded file is empty, download failed.")
        
        logging.info(f"Mod downloaded successfully: {file_path}")
        print(f"Downloaded: {file_path}")
        return file_path

    except requests.exceptions.Timeout:
        logging.error("Download timed out.")
        raise TimeoutError("Download request timed out.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Download request failed: {e}")
        raise ConnectionError(f"Request failed: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise RuntimeError(f"An unexpected error occurred: {e}")
