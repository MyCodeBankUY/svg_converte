import streamlit as st
import os
from procesador import test_contrasts
from tempfile import NamedTemporaryFile

st.set_page_config(page_title="Vectorizar PNG a SVG", layout="centered")
st.title("🎨 Vectorizador PNG → SVG")

png_file = st.file_uploader("📤 Subí tu imagen PNG", type=["png"])

st.subheader("⚙️ Configuración")

usar_default = st.checkbox("✅ Usar configuración predeterminada", value=True)

if usar_default:
    # Configuración predefinida
    contrasts = [1.0, 1.3, 1.5, 1.7, 2.0]
    binarize = False
    potrace_opts = ["--alphamax", "1.0", "--turdsize", "10"]

    st.markdown(f"""
    🔧 <small><b>Contrastes:</b> {contrasts}</small>  
    🔲 <small><b>Binarizar:</b> {binarize}</small>  
    ⚙️ <small><b>Opciones Potrace:</b> {" ".join(potrace_opts)}</small>
    """, unsafe_allow_html=True)

else:
    # Configuración manual
    contrasts = st.multiselect("Contrastes a probar", [1.0, 1.3, 1.5, 1.7, 2.0], default=[1.5])
    binarize = st.checkbox("Binarizar imagen", value=False)

    st.markdown("**Opciones avanzadas de Potrace:**")
    alphamax = st.slider("Alphamax", 0.0, 5.0, 1.0, 0.1)
    turdsize = st.slider("Turdsize", 0, 100, 10)
    potrace_opts = ["--alphamax", str(alphamax), "--turdsize", str(turdsize)]

# Botón de acción
if png_file and st.button("🚀 Vectorizar"):
    with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(png_file.read())
        tmp_path = tmp.name

    st.info("Procesando... por favor esperá unos segundos.")

    test_contrasts(tmp_path, contrasts=contrasts, binarize=binarize, potrace_opts=potrace_opts)

    base_name = os.path.splitext(os.path.basename(tmp_path))[0]

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
