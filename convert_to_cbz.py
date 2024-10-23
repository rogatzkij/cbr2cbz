import argparse
import os
import shutil
import zipfile
from pathlib import Path

import rarfile
import pdf2image

def cbr_to_cbz(cbr_path, cbz_path = None):
    """Converts a CBR file to a CBZ file.

    Args:
      cbr_path: Path to the CBR file.
      cbz_path: Path to the CBZ file.
    """

    # Check if input and output paths are valid
    if not os.path.exists(cbr_path):
        raise FileNotFoundError(f"CBR file not found at: {cbr_path}")

    if not cbz_path:
        cbz_path = Path(cbr_path).with_suffix('.cbz')

    # Extract CBR contents to a temporary directory using rarfile
    temp_dir = Path(cbr_path).with_suffix('')
    with rarfile.RarFile(cbr_path, 'r') as cbr:
        cbr.extractall(temp_dir)

    # Create new CBZ archive
    with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_DEFLATED) as cbz:
        for root, _, files in os.walk(temp_dir):
            for filename in files:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, temp_dir)  # Get path relative to temp dir
                cbz.write(full_path, arcname=relative_path.replace(".jpg", ".jpeg"))

    # Remove temporary directory
    shutil.rmtree(temp_dir)

    print(f"CBR file converted to CBZ at: {cbz_path}")

def pdf_to_cbz(pdf_path, cbz_path = None):
    # Check if input and output paths are valid
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    if not cbz_path:
        cbz_path = Path(pdf_path).with_suffix('.cbz')

    # Convert PDF to images
    temp_dir = Path(pdf_path).with_suffix('')
    Path(temp_dir).mkdir(parents=True, exist_ok=True)
    images = pdf2image.convert_from_path(pdf_path, output_folder=temp_dir)

    # Save the images as jpeg and store their paths in a list
    image_paths = []
    for i, image in enumerate(images):
        image_path = Path(temp_dir) / f'page_{i}.jpg'
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)

    # Create a new zipfile and add the images to it
    with zipfile.ZipFile(cbz_path, 'w') as myzip:
        for image_path in image_paths:
            myzip.write(image_path)

    # Clean up - remove temporary image files
    shutil.rmtree(temp_dir)

    print(f"PDF file converted to CBZ at: {cbz_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert CBR or PDF into CBZ')
    parser.add_argument('file', help='CBR or PDF file')
    args = parser.parse_args()

    suffix = Path(args.file).suffix.lower()
    if suffix == '.cbr':
        cbr_to_cbz(args.file)
    elif suffix == '.pdf':
        pdf_to_cbz(args.file)
    else:
        print(f"Unsupported file type: {suffix}")
