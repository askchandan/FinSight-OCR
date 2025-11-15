import os
import zipfile
import subprocess
from dotenv import load_dotenv


load_dotenv()

DATASET = os.getenv("DATASET_LINK")

class KaggleLoader:
    def __init__(self, dataset=DATASET, download_path='./data/raw/', extract_path='./data/extracted/'):
        self.dataset = dataset
        self.download_path = download_path
        self.extract_path = extract_path

        os.makedirs(download_path, exist_ok=True)

    
    def download(self):
        print("Downloading dataset from Kaggle...")

        cmd = [
            'kaggle', 'datasets', 'download',
            '-d', self.dataset,
            '-p', self.download_path,
            '--force'
        ]

        subprocess.run(cmd, check=True)
        print("Download completed.")

    
    def extract(self):
        zip_files = [f for f in os.listdir(self.download_path) if f.endswith('.zip')]
        if not zip_files:
            raise FileNotFoundError("No zip files found in the download path.")

        zip_path = os.path.join(self.download_path, zip_files[0])
        extract_to = os.path.join(self.extract_path)

        print(f'Extracting {zip_path} to {extract_to}...')

        os.makedirs(extract_to, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        print("Extraction completed.")
        return extract_to
    
