#!/usr/bin/env python3
"""
Convert PDF to PNG with ACL double-column width (7 inches = 2100px at 300 DPI)
"""

import sys
import os

def convert_with_pdf2image(pdf_path, output_path, width_px=2100, dpi=300):
    """Convert PDF to PNG using pdf2image library"""
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, dpi=dpi)
        if images:
            img = images[0]
            # Resize to target width while maintaining aspect ratio
            aspect_ratio = img.height / img.width
            new_height = int(width_px * aspect_ratio)
            img_resized = img.resize((width_px, new_height), resample=3)  # 3 = LANCZOS
            img_resized.save(output_path, 'PNG', quality=100)
            print(f"PNG generated: {output_path} ({width_px}x{new_height}px, ACL double-column width)")
            return True
    except ImportError:
        print("pdf2image not installed. Install with: pip install pdf2image")
        print("Also requires poppler: https://github.com/oschwartz10612/poppler-windows/releases/")
        return False
    except Exception as e:
        print(f"Error with pdf2image: {e}")
        return False

def convert_with_pypdfium2(pdf_path, output_path, width_px=2100, dpi=300):
    """Convert PDF to PNG using pypdfium2 library with auto-cropping"""
    try:
        import pypdfium2 as pdfium
        from PIL import Image, ImageChops
        
        pdf = pdfium.PdfDocument(pdf_path)
        page = pdf[0]
        # Render at high DPI
        bitmap = page.render(scale=dpi/72.0)
        pil_image = bitmap.to_pil()
        
        # Auto-crop white borders (trim whitespace) but keep some padding
        bg = Image.new(pil_image.mode, pil_image.size, pil_image.getpixel((0, 0)))
        diff = ImageChops.difference(pil_image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            # Add padding: 20 pixels on each side
            padding = 20
            left = max(0, bbox[0] - padding)
            top = max(0, bbox[1] - padding)
            right = min(pil_image.width, bbox[2] + padding)
            bottom = min(pil_image.height, bbox[3] + padding)
            pil_image = pil_image.crop((left, top, right, bottom))
        
        # Resize to target width
        aspect_ratio = pil_image.height / pil_image.width
        new_height = int(width_px * aspect_ratio)
        img_resized = pil_image.resize((width_px, new_height), Image.Resampling.LANCZOS)
        img_resized.save(output_path, 'PNG', quality=100)
        print(f"PNG generated: {output_path} ({width_px}x{new_height}px, ACL double-column width, auto-cropped)")
        return True
    except ImportError:
        print("pypdfium2 not installed. Install with: pip install pypdfium2")
        return False
    except Exception as e:
        print(f"Error with pypdfium2: {e}")
        return False

def main():
    pdf_file = "electra_arch.pdf"
    png_file = "electra_arch.png"
    
    if not os.path.exists(pdf_file):
        print(f"Error: {pdf_file} not found")
        return 1
    
    # Try pypdfium2 first (easier to install, no external dependencies)
    if convert_with_pypdfium2(pdf_file, png_file):
        return 0
    
    # Fallback to pdf2image
    if convert_with_pdf2image(pdf_file, png_file):
        return 0
    
    print("\nNo conversion library available.")
    print("Please install one of the following:")
    print("  1. pypdfium2: pip install pypdfium2")
    print("  2. pdf2image: pip install pdf2image (also requires poppler)")
    print("\nOr use ImageMagick/Ghostscript if available.")
    return 1

if __name__ == "__main__":
    sys.exit(main())

