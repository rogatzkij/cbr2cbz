# CBR/PDF to CBZ Converter

This script converts CBR (Comic Book RAR Archive) or PDF files into the more widely compatible CBZ format.

## Installation

~~~shell
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
~~~

## Usage

**Command Line:**

```bash
python convert_to_cbz.py <input_file>
```

Replace <input_file> with the path to your CBR or PDF file.
The script will automatically create a CBZ file in the same directory as the input file, using the original filename with a .cbz extension.


**Example:**

```bash
python convert_to_cbz.py my_comic.cbr
```
This will convert `my_comic.cbr` to `my_comic.cbz`.

**Supported File Types:**
* **CBR** (Comic Book RAR Archive): Extracts images from the archive and packs them into a CBZ file.
* **PDF**: Converts each page of the PDF to a JPEG image, then zips those images into a CBZ file.

