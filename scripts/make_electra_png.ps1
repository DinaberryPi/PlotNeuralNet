# PowerShell script to generate PNG from LaTeX with ACL double-column width
# ACL double-column width: 7 inches = 17.78 cm

$FILENAME = "electra_arch"

# Compile LaTeX to PDF
pdflatex -interaction=nonstopmode "${FILENAME}.tex"

# Clean up auxiliary files
Remove-Item -ErrorAction SilentlyContinue *.aux, *.log, *.vscodeLog

# Convert PDF to PNG with ACL double-column width
# 7 inches at 300 DPI = 2100 pixels wide
# Using ImageMagick if available
if (Get-Command magick -ErrorAction SilentlyContinue) {
    magick -density 300 "${FILENAME}.pdf" -resize 2100x -quality 100 "${FILENAME}.png"
    Write-Host "PNG generated: ${FILENAME}.png (2100px wide, ACL double-column width)"
}
elseif (Get-Command convert -ErrorAction SilentlyContinue) {
    convert -density 300 "${FILENAME}.pdf" -resize 2100x -quality 100 "${FILENAME}.png"
    Write-Host "PNG generated: ${FILENAME}.png (2100px wide, ACL double-column width)"
}
elseif (Get-Command gs -ErrorAction SilentlyContinue) {
    # Using Ghostscript as fallback
    gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r300 -dGraphicsAlphaBits=4 -dTextAlphaBits=4 -dUseCropBox -sOutputFile="${FILENAME}.png" "${FILENAME}.pdf"
    Write-Host "PNG generated: ${FILENAME}.png (300 DPI, may need manual resizing to 2100px width)"
}
else {
    Write-Host "Error: No image conversion tool found (ImageMagick or Ghostscript required)"
    Write-Host "PDF generated: ${FILENAME}.pdf"
    Write-Host "Please install ImageMagick or Ghostscript to convert to PNG"
    exit 1
}

