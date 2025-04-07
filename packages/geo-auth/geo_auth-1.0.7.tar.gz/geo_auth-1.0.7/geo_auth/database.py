import glob
import io
import logging
import os
import zipfile

import requests
from django.conf import settings

TOKEN = settings.TOKEN

DATABASES = {
    "DB11LITEBIN": "IP2LOCATION-LITE-DB11.BIN",  # Location database
    "DBASNLITEBIN": "IP2LOCATION-LITE-ASN.BIN",  # ASN database
}
APP_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIRECTORY = os.path.join(APP_DIR, "iplite_database")
def is_first_run():
    """Check if the database folder exists and contains valid database files."""
    if not os.path.exists(OUTPUT_DIRECTORY):
        return True  # Folder does not exist, so it's the first run

    db_files = glob.glob(os.path.join(OUTPUT_DIRECTORY, "*.BIN"))
    return len(db_files) == 0
# handle data download and extraction of zip file
def download_database():

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    # 🔥 Delete old database files
    for old_file in glob.glob(os.path.join(OUTPUT_DIRECTORY, "*")):
        os.remove(old_file)

    for db_code, db_filename in DATABASES.items():
        try:
            download_url = f"https://www.ip2location.com/download/?token={TOKEN}&file={db_code}"

            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            if response.headers.get("Content-Type") != "application/zip":
                logging.error(f"❌ Failed to download {db_filename}. Response: {response.text}")
                continue

            # Extract ZIP file
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(OUTPUT_DIRECTORY)

        except Exception as e:
            logging.error(f"❌ Error downloading {db_filename}: {e}")

def run_first_time_setup():
    """Run the first-time database download if needed."""
    if is_first_run():
        logging.info("🚀 Running first-time database download...")
        download_database()
        logging.info("✅ First-time setup completed!")
    else:
        logging.info("⚡ Database files already exist. Skipping first-time setup.")