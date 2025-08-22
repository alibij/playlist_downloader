import os
import requests
from urllib.parse import unquote


def download(url, path: str = "."):
    filename = unquote(os.path.basename(url))

    if not os.path.exists(path):
        os.mkdir(path)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        if os.path.exists(f"{path}/{filename}"):
            raise Exception("Exist file")

        with open(f"{path}/{filename}", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return filename
