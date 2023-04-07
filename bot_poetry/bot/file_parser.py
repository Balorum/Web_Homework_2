import sys
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO =[]
AMR_AUDIO = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO =[]
MKV_VIDEO = []

DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
DOCX_DOCUMENTS1 =[]
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []

ZIP_ARCHIV = []
GZ_ARCHIV = []
TAR_ARCHIV = []
MY_OTHER = []

REGISTER_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,

    'ZIP': ZIP_ARCHIV,
    'GZ': GZ_ARCHIV,
    'TAR': TAR_ARCHIV,
    'DOC': DOC_DOCUMENTS,
    '(DOCX)': DOCX_DOCUMENTS1,
    'DOCX': DOCX_DOCUMENTS,
    'TXT': TXT_DOCUMENTS,
    'PDF': PDF_DOCUMENTS,
    'XLSX': XLSX_DOCUMENTS,
    'PPTX': PPTX_DOCUMENTS
}

SAVE_TO = {
    'JPEG': 'images',
    'PNG': 'images',
    'JPG': 'images',
    'SVG': 'images',
    'MP3': 'audios',
    'OGG': 'audios',
    'WAV': 'audios',
    'AMR': 'audios',
    'AVI': 'videos',
    'MP4': 'videos',
    'MOV': 'videos',
    'MKV': 'videos',

    'ZIP': 'archives',
    'GZ': 'archives',
    'TAR': 'archives',
    'DOC': 'documents',
    'DOCX': 'documents',
    'DOCX': 'documents',
    'TXT': 'documents',
    'PDF': 'documents',
    'XLSX': 'documents',
    'PPTX': 'documents'
}


FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        ext = get_extension(item.name)  
        fullname = folder / item.name  
        if not ext:  
            MY_OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)


if __name__ == '__main__':

    folder_for_scan = sys.argv[1]
    print(f'Start in folder {folder_for_scan}')

    scan(Path(folder_for_scan))
    print(f'Images jpeg: {JPEG_IMAGES}')
    print(f'Images jpg: {JPG_IMAGES}')
    print(f'Images svg: {SVG_IMAGES}')
    print(f'Audio mp3: {MP3_AUDIO}')
    print(f'Archiv zip: {ZIP_ARCHIV}')


    print(f'Types of files in folder: {EXTENSIONS}')
    print(f'Unknown files of types: {UNKNOWN}')

    print(FOLDERS[::-1])
