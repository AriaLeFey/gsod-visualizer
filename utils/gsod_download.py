import requests, os, tarfile
from pathlib import Path
from bs4 import BeautifulSoup
from tqdm import tqdm

def load_dir(gsod_data_dir):
    if not gsod_data_dir.exists():
        os.mkdir(gsod_data_dir)

        return False
    else:
        return True

def download():
    gsod_data_dir = Path.cwd() / 'gsod_data'

    if not load_dir(gsod_data_dir):
        target_url = 'https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/'

        response = requests.get(target_url, stream=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            archive_set = soup.find_all('a')
            
            for archive in archive_set[-1:]:
                if '.tar.gz' in archive['href']:
                    target_archive_url = ''.join((target_url, archive['href']))
                    target_donwload_path = gsod_data_dir / archive['href']
                    
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

        for file in gsod_data_dir.iterdir():
            with tarfile.open(gsod_data_dir / file) as tar:
                tar.extractall(gsod_data_dir / str(file).removesuffix('.tar.gz'))
    
    else:
        print('Data has already been downlaoded')