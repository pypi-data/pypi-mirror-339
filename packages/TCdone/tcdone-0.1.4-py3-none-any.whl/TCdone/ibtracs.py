import os
import requests
from pathlib import Path
from tqdm import tqdm

def download_ibtracs(destination="data", version="v04r00", fmt="csv"):
    """
    Download global IBTrACS tropical cyclone data from NOAA.

    Parameters:
        destination (str): Directory to save the downloaded file.
        version (str): IBTrACS version, e.g., 'v04r00'.
        fmt (str): File format, 'csv' or 'netcdf'.

    Returns:
        str: Path to the downloaded file.
    """
    base_url = (
        "https://www.ncei.noaa.gov/data/"
        "international-best-track-archive-for-climate-stewardship-ibtracs/"
    )
    subfolder = f"{version}/{fmt}/"
    filename = f"ibtracs.{version}.{fmt}.zip"
    url = base_url + subfolder + filename

    Path(destination).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(destination, filename)

    print(f"Downloading from: {url}")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(filepath, 'wb') as f, tqdm(
        desc=filename, total=total_size, unit='iB', unit_scale=True
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            size = f.write(chunk)
            bar.update(size)

    print(f"Saved to {filepath}")
    return filepath
