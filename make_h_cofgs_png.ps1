# PowerShell script to generate PNG from Python script (run from project root)
# This script runs the Python script to generate .tex, compiles it to PDF, and converts to PNG

$FILENAME = "h_cofgs_architecture"
$SCRIPT_DIR = Join-Path $PSScriptRoot "pycore"

# Change to pycore directory
Set-Location $SCRIPT_DIR

Write-Host "Step 1: Generating LaTeX file from Python script..."
python "${FILENAME}.py"

if (-not (Test-Path "${FILENAME}.tex")) {
    Write-Host "Error: Failed to generate ${FILENAME}.tex"
    exit 1
}

Write-Host "Step 2: Compiling LaTeX to PDF..."
pdflatex -interaction=nonstopmode "${FILENAME}.tex"

if (-not (Test-Path "${FILENAME}.pdf")) {
    Write-Host "Error: Failed to generate ${FILENAME}.pdf"
    exit 1
}

# Clean up auxiliary files
Write-Host "Step 3: Cleaning up auxiliary files..."
Remove-Item -ErrorAction SilentlyContinue *.aux, *.log, *.vscodeLog

# Convert PDF to PNG with ACL double-column width
# 7 inches at 300 DPI = 2100 pixels wide
Write-Host "Step 4: Converting PDF to PNG..."
if (Get-Command magick -ErrorAction SilentlyContinue) {
    magick -density 300 "${FILENAME}.pdf" -resize 2100x -quality 100 "${FILENAME}.png"
    Write-Host "[OK] PNG generated: ${FILENAME}.png (2100px wide, ACL double-column width)"
}
elseif (Get-Command convert -ErrorAction SilentlyContinue) {
    convert -density 300 "${FILENAME}.pdf" -resize 2100x -quality 100 "${FILENAME}.png"
    Write-Host "[OK] PNG generated: ${FILENAME}.png (2100px wide, ACL double-column width)"
}
elseif (Get-Command gs -ErrorAction SilentlyContinue) {
    # Using Ghostscript as fallback
    gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r300 -dGraphicsAlphaBits=4 -dTextAlphaBits=4 -dUseCropBox -sOutputFile="${FILENAME}.png" "${FILENAME}.pdf"
    Write-Host "[OK] PNG generated: ${FILENAME}.png (300 DPI, may need manual resizing to 2100px width)"
}
else {
    Write-Host "Warning: No image conversion tool found (ImageMagick or Ghostscript required)"
    Write-Host "PDF generated: ${FILENAME}.pdf"
    Write-Host "Please install ImageMagick or Ghostscript to convert to PNG"
    Write-Host "You can download ImageMagick from: https://imagemagick.org/script/download.php"
    exit 1
}

Write-Host ""
Write-Host "[OK] All done! PNG file: pycore\${FILENAME}.png"

