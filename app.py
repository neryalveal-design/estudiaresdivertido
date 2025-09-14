import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import docx

# Configurar cliente de GPT (la API key debe ir en los secrets de Streamlit)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎮 Juego de Lenguaje con GPT")
st.write("Sube una guía en PDF o Word y genera un quiz interactivo.")

# Función para extraer texto del PDF
def leer_pdf(archivo):
    reader = PdfReader(archivo)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() + "\n"
    return texto

# Función para extraer texto de Word
def leer_word(archivo):
    doc = docx.Document(archivo)
    texto = ""
    for p in doc.paragraphs:
        texto += p.text + "\n"
    return texto

# Subida de archivo
archivo = st.file_uploader("📂 Sube tu guía de lenguaje", type=["pdf", "docx"])

if archivo:
    if archivo.type == "application/pdf":
        texto_guia = leer_pdf(archivo)
    else:
        texto_guia = leer_word(archivo)

    st.success("✅ Guía cargada correctamente")

    # Prompt base (los estudiantes pueden editar esta parte)
    prompt = f"""
    A partir del siguiente texto de una guía de lenguaje, genera 5 preguntas de opción múltiple
    con 4 alternativas cada una. Marca la respuesta correcta con un asterisco (*).
    Nivel: estudiantes de enseñanza media.
    Texto: {texto_guia[:1500]}  # Se limita el texto para no exceder el contexto
    """

    if st.button("Generar preguntas"):
        with st.spinner("Generando preguntas con GPT..."):
            respuesta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
        
        preguntas = respuesta.choices[0].message.content
        st.subheader("📝 Preguntas generadas")
        st.write(preguntas)

        # Aquí los estudiantes pueden luego adaptar las preguntas en formato de quiz interactivo
        st.info("Ahora edita el prompt para transformar estas preguntas en un juego con puntaje.")
