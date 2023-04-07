from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(
        filename.name.replace(filename.suffix, "")
    )

    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))

        for item in folder_for_file.iterdir():
            pass

    except shutil.ReadError:
        print(f"This is not an archive {filename}!")
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Error deleting folder {folder}")


USE_METHOD = {
    "JPEG": handle_media,
    "PNG": handle_media,
    "JPG": handle_media,
    "SVG": handle_media,
    "MP3": handle_media,
    "OGG": handle_media,
    "WAV": handle_media,
    "AMR": handle_media,
    "AVI": handle_media,
    "MP4": handle_media,
    "MOV": handle_media,
    "MKV": handle_media,
    "DOC": handle_media,
    "DOCX": handle_media,
    "DOCX": handle_media,
    "TXT": handle_media,
    "PDF": handle_media,
    "XLSX": handle_media,
    "PPTX": handle_media,
    "ZIP": handle_archive,
    "GZ": handle_archive,
    "TAR": handle_archive,
}


def main_file_folder(folder: Path):
    parser.scan(folder)
    save_to_keys = parser.SAVE_TO.keys()

    for path in save_to_keys:
        for file in parser.REGISTER_EXTENSIONS[path]:
            USE_METHOD[path](file, folder / parser.SAVE_TO[path])

    for file in parser.MY_OTHER:
        handle_other(file, folder / "MY_OTHER")

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


def path_function():
    try:
        folder = input("Write the path: ")
    except IndexError:
        print("Enter valid path to the folder")
    else:
        folder_for_scan = Path(folder)
        print(f"Start in folder {folder_for_scan.resolve()}")
        main_file_folder(folder_for_scan.resolve())


if __name__ == "__main__":
    while True:

        choice = input("Do you want to sort a folder? y/n: ")
        if choice.lower() in ("y", "yes"):
            path_function()
            print("The folder has been sorted")

        elif choice.lower() in ("n", "no"):
            break

