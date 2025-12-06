#!/bin/bash

# Script to generate PNG from LaTeX with ACL double-column width
# ACL double-column width: 7 inches = 17.78 cm

FILENAME="electra_arch"

# Compile LaTeX to PDF
pdflatex -interaction=nonstopmode ${FILENAME}.tex

# Clean up auxiliary files
rm -f *.aux *.log *.vscodeLog

# Convert PDF to PNG with ACL double-column width
# 7 inches at 300 DPI = 2100 pixels wide
# Using ImageMagick if available
if command -v magick &> /dev/null; then
    magick -density 300 ${FILENAME}.pdf -resize 2100x -quality 100 ${FILENAME}.png
    echo "PNG generated: ${FILENAME}.png (2100px wide, ACL double-column width)"
elif command -v convert &> /dev/null; then
    convert -density 300 ${FILENAME}.pdf -resize 2100x -quality 100 ${FILENAME}.png
    echo "PNG generated: ${FILENAME}.png (2100px wide, ACL double-column width)"
elif command -v gs &> /dev/null; then
    # Using Ghostscript as fallback
    gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r300 -dGraphicsAlphaBits=4 -dTextAlphaBits=4 -dUseCropBox -sOutputFile=${FILENAME}.png ${FILENAME}.pdf
    echo "PNG generated: ${FILENAME}.png (300 DPI, may need manual resizing to 2100px width)"
else
    echo "Error: No image conversion tool found (ImageMagick or Ghostscript required)"
    echo "PDF generated: ${FILENAME}.pdf"
    echo "Please install ImageMagick or Ghostscript to convert to PNG"
    exit 1
fi

