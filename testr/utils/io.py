
import zipfile


def unzip(zip_file: str, dest_dir: str):
    """
    based on https://gist.github.com/swaroopjcse/6d789188a9cdb21d725767716669557f
    """
    try:
        zfile = zipfile.ZipFile(zip_file)
        for filename in zfile.namelist():
            zfile.extract(filename, dest_dir)
    except zipfile.BadZipfile:
        print(f"Cannot extract '{zip_file}': Not a valid zipfile.")