import streamlit as st
from PyPDF2 import PdfReader
import docx

# --------------------------
# Funciones auxiliares
# --------------------------
def leer_pdf(archivo):
    reader = PdfReader(archivo)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() + "\n"
    return texto

def leer_word(archivo):
    doc = docx.Document(archivo)
    texto = ""
    for p in doc.paragraphs:
        texto += p.text + "\n"
    return texto

# --------------------------
# Interfaz Streamlit
# --------------------------
st.set_page_config(page_title="🎮 Generador de Quiz", page_icon="📝", layout="wide")

st.title("🎮 Generador de Quiz a partir de una Guía")
st.markdown("Sube tu guía en PDF o Word y responde un **quiz de 20 preguntas** basado en su contenido.")

# Subida de archivo
archivo = st.file_uploader("📂 Sube tu guía de ejercicios", type=["pdf", "docx"])

texto_guia = ""
if archivo:
    if archivo.type == "application/pdf":
        texto_guia = leer_pdf(archivo)
    else:
        texto_guia = leer_word(archivo)

    st.success("✅ Guía cargada correctamente")
    st.write("Vista previa del contenido:")
    st.text_area("Contenido de la guía", texto_guia[:1000] + "...", height=200)

    st.info("ℹ️ Como esta versión no usa GPT integrado, puedes generar preguntas con ChatGPT gratuito y pegarlas aquí.")

    # --------------------------
    # Preguntas predefinidas (ejemplo)
    # --------------------------
    preguntas = [
        {"pregunta": "¿Cuál es la idea principal de la guía que subiste?",
         "opciones": ["Vocabulario", "Conectores", "Ortografía", "Redacción"],
         "respuesta": "Vocabulario"},
        {"pregunta": "¿Qué significa la palabra 'Trascendental'?",
         "opciones": ["Algo trivial", "De gran importancia", "Un objeto físico", "Algo decorativo"],
         "respuesta": "De gran importancia"},
        {"pregunta": "¿Cuál de estos es un conector de oposición?",
         "opciones": ["Porque", "Pero", "Además", "Por ejemplo"],
         "respuesta": "Pero"},
        # ⚠️ Aquí se pueden agregar más preguntas hasta llegar a 20
    ]

    # --------------------------
    # Interfaz del quiz
    # --------------------------
    st.header("📝 Responde el quiz")
    puntaje = 0

    for i, p in enumerate(preguntas):
        st.subheader(f"Pregunta {i+1}: {p['pregunta']}")
        opcion = st.radio("Selecciona tu respuesta:", p["opciones"], key=i)
        if opcion == p["respuesta"]:
            puntaje += 1

    if st.button("Mostrar resultado final"):
        st.success(f"🎉 Tu puntaje final es {puntaje} de {len(preguntas)}")
        if puntaje == len(preguntas):
            st.balloons()
        elif puntaje > len(preguntas) // 2:
            st.info("👍 ¡Muy bien! Dominas gran parte del contenido.")
        else:
            st.warning("👀 Necesitas repasar más la guía.")
