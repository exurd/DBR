import os
from zipfile import ZipFile, BadZipFile
import io

from .get_request_url import get_request_url


def download_spam_lists(folder=os.getcwd()):
    """
    This downloads text files from exurd/badge-spam-lists; a bunch of text
    files containing place IDs from various Roblox badge chains.
    """
    print("Downloading badge spam lists...")
    zip_req = get_request_url("https://github.com/exurd/badge-spam-lists/archive/refs/heads/main.zip")
    if zip_req.ok:
        try:
            with ZipFile(io.BytesIO(zip_req.content)) as zf:
                zf.extractall(folder)
                zf.close()
            print("Success!")
            return True
        except BadZipFile:
            print("Zip file could not be read.")
            return False
    print("Failed to download zip file.")
    return False
