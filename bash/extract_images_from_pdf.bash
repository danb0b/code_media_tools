#!/bin/bash
MY_PATH="`dirname \"$0\"`"

python3 $MY_PATH/../python//media_tools/pdf_tools/extract_images_from_pdf.py "$@"


