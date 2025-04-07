
import requests
import re
from pathlib import Path
import os

def _interfere_filename(headers: object):
    # Interfere filename from content-disposition
    cd = headers.get("content-disposition")
    if not cd: return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0: return None
    return fname[0].replace('"', '')

def download_file(
    url: str,
    headers: object,
    path: Path,
    allow_redirects: bool = True,
    exist_ok: bool = False
):
    # Download file and interfere filename
    res: requests.Response = requests.get(url=url, headers=headers, allow_redirects=allow_redirects)
    filepath: str = os.path.join(path, _interfere_filename(res.headers))

    # Make consistency checks
    if not res.ok: raise ConnectionError(res.content)
    if not os.path.exists(path): os.makedirs(path, exist_ok=True)
    if os.path.exists(filepath) and not exist_ok: raise FileExistsError(f"File {filepath} already exists!")
    
    # Save file
    with open(filepath, 'wb') as f: f.write(res.content)