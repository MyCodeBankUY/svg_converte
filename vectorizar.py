import sys
import os
import subprocess
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(png_path, processed_path, binarize=False, contrast=1.5, median_filter_size=3):
    try:
        img = Image.open(png_path).convert("L")
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)
        img = img.filter(ImageFilter.MedianFilter(size=median_filter_size))

        if binarize:
            img = img.point(lambda p: 255 if p > 128 else 0)

        img.save(processed_path)
        return True
    except Exception as e:
        print(f"❌ Error en preprocesamiento: {e}")
        return False

def raster_to_svg(png_path, potrace_options=None, binarize=False, contrast=1.5):
    if not os.path.isfile(png_path):
        print(f"❌ El archivo '{png_path}' no existe.")
        return

    if not png_path.lower().endswith(".png"):
        print("❌ El archivo debe ser PNG con extensión .png")
        return

    base_dir = os.path.dirname(png_path)
    vector_dir = os.path.join(base_dir, "Vector")
    os.makedirs(vector_dir, exist_ok=True)

    bmp_path = os.path.splitext(png_path)[0] + "_processed.bmp"

    if not preprocess_image(png_path, bmp_path, binarize=binarize, contrast=contrast):
        return

    svg_name = os.path.splitext(os.path.basename(png_path))[0] + ".svg"
    svg_path = os.path.join(vector_dir, svg_name)

    cmd = ["potrace", bmp_path, "-s", "-o", svg_path]
    if potrace_options:
        cmd.extend(potrace_options)

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ SVG generado en: {svg_path}")
    except subprocess.CalledProcessError as e:
        print("❌ Error al ejecutar Potrace:")
        print(e.stderr.decode())
    finally:
        if os.path.exists(bmp_path):
            os.remove(bmp_path)
