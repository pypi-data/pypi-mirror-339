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

def download_mod(url: str = None, mod_id: str = None, save_dir: str = None, overwrite: bool = False):
    """
    Downloads a mod from Steam Workshop using its URL or ID.
    
    Parameters:
        url (str): Full URL to the mod page. Example: https://steamcommunity.com/sharedfiles/filedetails/?id=123456789
        mod_id (str): Steam Workshop mod ID. Can be used instead of URL.
        save_dir (str): Folder path to save the mod. Defaults to current working directory.
        overwrite (bool): Whether to overwrite the file if it already exists.
    
    Returns:
        str: Path to the downloaded file.
    """
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
        download_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}"
        print(f"Downloading mod from {download_url} ...")

        response = requests.get(download_url, stream=True, timeout=10)
        response.raise_for_status()

        total_size = int(response.headers.get("Content-Length", 0))
        with open(file_path, "wb") as file, tqdm(
            total=total_size, unit="B", unit_scale=True, desc=file_name
        ) as progress:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    progress.update(len(chunk))

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
