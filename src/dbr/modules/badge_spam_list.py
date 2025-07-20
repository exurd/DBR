from zipfile import ZipFile, BadZipFile
import io
import os

from .get_request_url import get_request_url

try:
    import zstandard as zstd
except ImportError:
    print("Could not import zstandard python library...")


def zstd_extract_lines(filename):
    """Extracts lines from zstandard file."""
    try:
        with zstd.open(filename, mode="r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            f.close()
            return lines
    except (zstd.ZstdError, OSError) as e:
        print(f"Error reading file {filename}: {e}")
        return []


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
