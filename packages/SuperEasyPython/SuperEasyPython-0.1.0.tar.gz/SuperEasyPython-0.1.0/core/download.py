import os
import requests
from tqdm import tqdm  # Для прогресс-бара

def download_file(url: str, save_path: str = None, resume: bool = False) -> str:
    """
    Downloading files from  url (not wget).
    
    :param url: Link on file.
    :param save_path: Path for save (if None — name taken from URL).
    :param resume: Resuming download in case of interruption.
    :return: Path to the downloaded file.
    """
    if save_path is None:
        save_path = os.path.basename(url.split("?")[0])  # Удаляем параметры запроса

    # Докачка
    mode = "ab" if resume and os.path.exists(save_path) else "wb"
    downloaded_size = os.path.getsize(save_path) if mode == "ab" else 0

    headers = {}
    if downloaded_size:
        headers["Range"] = f"bytes={downloaded_size}-"

    response = requests.get(url, stream=True, headers=headers)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0)) + downloaded_size

    with open(save_path, mode) as f, tqdm(
        unit="B",
        unit_scale=True,
        total=total_size,
        initial=downloaded_size,
        desc=save_path,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))

    return save_path