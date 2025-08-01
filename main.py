import os
from vectorizar import raster_to_svg  # asumo que vectorizar.py está en el mismo folder
import shutil

def test_contrasts(png_path, contrasts, binarize=False, potrace_opts=None):
    base_dir = os.path.dirname(png_path)
    base_name = os.path.splitext(os.path.basename(png_path))[0]

    for c in contrasts:
        # Crear carpeta por contraste
        output_dir = os.path.join(base_dir, f"Vector_contrast_{c}")
        os.makedirs(output_dir, exist_ok=True)

        # Modificar raster_to_svg para que reciba carpeta destino
        bmp_path = os.path.splitext(png_path)[0] + f"_processed_{c}.bmp"
        svg_path = os.path.join(output_dir, base_name + ".svg")

        print(f"\nProbando contraste: {c}")

        # Usar versión adaptada de preprocess_image y Potrace desde vectorizar.py
        # Para eso, llamamos al raster_to_svg modificado con estos paths

        # Como raster_to_svg original no acepta output_dir ni bmp_path,
        # te dejo aquí una función adaptada para esto:

        from PIL import Image, ImageEnhance, ImageFilter
        import subprocess

        try:
            # Preprocesar imagen con contraste c
            img = Image.open(png_path).convert("L")
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(c)
            if not binarize:
                img = img.filter(ImageFilter.MedianFilter(size=3))
            else:
                img = img.point(lambda p: 255 if p > 128 else 0)
            img.save(bmp_path)

            # Ejecutar Potrace
            cmd = ["potrace", bmp_path, "-s", "-o", svg_path]
            if potrace_opts:
                cmd.extend(potrace_opts)

            subprocess.run(cmd, check=True)

            print(f"SVG guardado en: {svg_path}")

        except Exception as e:
            print(f"Error con contraste {c}: {e}")
        finally:
            if os.path.exists(bmp_path):
                os.remove(bmp_path)

if __name__ == "__main__":
    contrasts = [1.0, 1.3, 1.5, 1.7, 2.0]  # valores a probar
    png_path = "PIZZZA.png"  # ruta a tu imagen
    binarize = False
    potrace_opts = ["--alphamax", "1.0", "--turdsize", "10"]

    test_contrasts(png_path, contrasts, binarize=binarize, potrace_opts=potrace_opts)
