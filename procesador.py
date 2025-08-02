import os
from vectorizar import raster_to_svg
from PIL import Image, ImageEnhance, ImageFilter
import subprocess

def test_contrasts(png_path, contrasts, binarize=False, potrace_opts=None):
    base_dir = os.path.dirname(png_path)
    base_name = os.path.splitext(os.path.basename(png_path))[0]

    for c in contrasts:
        output_dir = os.path.join(base_dir, f"Vector_contrast_{c}")
        os.makedirs(output_dir, exist_ok=True)

        bmp_path = os.path.splitext(png_path)[0] + f"_processed_{c}.bmp"
        svg_path = os.path.join(output_dir, base_name + ".svg")

        try:
            img = Image.open(png_path).convert("L")
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(c)
            if not binarize:
                img = img.filter(ImageFilter.MedianFilter(size=3))
            else:
                img = img.point(lambda p: 255 if p > 128 else 0)
            img.save(bmp_path)

            cmd = ["potrace", bmp_path, "-s", "-o", svg_path]
            if potrace_opts:
                cmd.extend(potrace_opts)

            subprocess.run(cmd, check=True)

        except Exception as e:
            print(f"Error con contraste {c}: {e}")
        finally:
            if os.path.exists(bmp_path):
                os.remove(bmp_path)
