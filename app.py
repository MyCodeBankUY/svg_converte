import streamlit as st
import os
from procesador import test_contrasts
from tempfile import NamedTemporaryFile

st.set_page_config(page_title="Vectorizar PNG a SVG", layout="centered")
st.title("🎨 Vectorizador PNG → SVG")

# Subida de imagen PNG
png_file = st.file_uploader("📤 Subí tu imagen PNG", type=["png"])

# Configuración de parámetros
st.subheader("⚙️ Opciones de procesamiento")
contrasts = st.multiselect("Seleccioná niveles de contraste a probar", [1.0, 1.3, 1.5, 1.7, 2.0], default=[1.5])
binarize = st.checkbox("Binarizar imagen", value=False)

st.markdown("**Opciones avanzadas de Potrace:**")
alphamax = st.slider("Alphamax", 0.0, 5.0, 1.0, 0.1)
turdsize = st.slider("Turdsize", 0, 100, 10)

# Ejecutar procesamiento
if png_file and st.button("🚀 Vectorizar"):
    with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(png_file.read())
        tmp_path = tmp.name

    # Ejecutar vectorización
    output_opts = ["--alphamax", str(alphamax), "--turdsize", str(turdsize)]
    st.info("Procesando... por favor esperá unos segundos.")

    test_contrasts(tmp_path, contrasts=contrasts, binarize=binarize, potrace_opts=output_opts)

    base_name = os.path.splitext(os.path.basename(tmp_path))[0]

    # Mostrar y permitir descargar SVGs generados
    for c in contrasts:
        folder = os.path.join(os.path.dirname(tmp_path), f"Vector_contrast_{c}")
        svg_file = os.path.join(folder, base_name + ".svg")
        if os.path.exists(svg_file):
            with open(svg_file, "rb") as f:
                st.download_button(
                    label=f"📥 Descargar SVG (contraste {c})",
                    data=f,
                    file_name=f"{base_name}_contrast_{c}.svg",
                    mime="image/svg+xml"
                )
        else:
            st.warning(f"No se encontró SVG para contraste {c}")
