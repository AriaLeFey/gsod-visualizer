import requests, sys, tarfile, os
from pathlib import Path, PosixPath
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime

GSOD_DATA_DIR : PosixPath = Path.cwd() / 'gsod_data/'

def find_dir(date: datetime) -> bool:
    try:
        if not GSOD_DATA_DIR.exists():
            os.mkdir(GSOD_DATA_DIR)

        return (GSOD_DATA_DIR / Path(str(date.year))).exists()
    except AttributeError:
        print(f"ERROR: Incorrect date used.", file=sys.stderr)
        exit()

def download_archive(date: datetime.date) -> None:
    target_url : str = 'https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/'

    response = requests.get(target_url, stream=True)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
            
        archive_set = soup.find_all('a')
        
        for archive in archive_set:
            if '.tar.gz' in archive['href'] and str(date.year) in archive['href']:
                    target_archive_url = ''.join((target_url, archive['href']))
                    target_donwload_path = GSOD_DATA_DIR / archive['href']
                        
                    archive_response = requests.get(target_archive_url, stream=True)
                    if archive_response.status_code == 200:
                        total_size = int(archive_response.headers.get("content-length", 0))
                        block_size = 1024

                        print(f'Downloading {target_archive_url}')
                        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
                            with open(target_donwload_path, "wb") as file:
                                for data in archive_response.iter_content(block_size):
                                    progress_bar.update(len(data))
                                    file.write(data)

        extract_path = GSOD_DATA_DIR / str(date.year)

        for tar_file in GSOD_DATA_DIR.iterdir():
            with tarfile.open(GSOD_DATA_DIR / tar_file) as tar:
                tar.extractall(extract_path)
