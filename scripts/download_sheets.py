import json
import requests
from pathlib import Path
import os

sheets_config = json.loads(os.environ.get("SHEETS_JSON", "[]"))

DATA_DIR = Path("data/csv")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_csv(sheet_id: str, gid: str, filename: str):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    response = requests.get(url)
    response.raise_for_status()
    file_path = DATA_DIR / filename
    file_path.write_bytes(response.content)
    print(f"Downloaded {filename} from sheet {sheet_id} (gid={gid})")

def main():
    for sheet in sheets_config:
        download_csv(sheet["sheet_id"], sheet["gid"], sheet["filename"])

if __name__ == "__main__":
    main()
