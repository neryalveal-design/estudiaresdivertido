import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import docx
import unicodedata

# Configurar cliente de GPT (requiere que hayas guardado tu API key en Streamlit → Edit secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎮 Juego de Lenguaje con GPT")
st.write("Sube una guía en PDF o Word y genera un quiz interactivo.")

# Función para limpiar y normalizar texto
def limpiar_texto(texto):
    return unicodedata.normalize("NFKD", texto).encode("utf-8", "ignore").decode("utf-8")

# Función para extraer texto de un PDF
def leer_pdf(archivo):
    reader = PdfReader(archivo)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() + "\n"
    return texto

# Función para extraer texto de un Word
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

    # Selección de fragmento (para no enviar todo el documento)
    if "Vocabulario" in texto_guia:
        inicio = texto_guia.find("Vocabulario")
        fragmento = texto_guia[inicio : inicio + 1500]
    else:
        fragmento = texto_guia[:1500]

    # Prompt que los estudiantes pueden modificar
    prompt = f"""
    A partir del siguiente texto de una guía de lenguaje, crea 5 preguntas de opción múltiple
    con 4 alternativas cada una. Señala la respuesta correcta con un asterisco (*).
    Nivel: estudiantes de enseñanza media.
    Texto: {limpiar_texto(fragmento)}
    """

    if st.button("Generar preguntas"):
        with st.spinner("Generando preguntas con GPT..."):
            respuesta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
        
        preguntas = respuesta.choices[0].message.content
        st.subheader("📝 Preguntas generadas por GPT")
        st.write(preguntas)

        st.info("Tip: Edita el prompt para cambiar el tipo de juego (verdadero/falso, crucigrama, adivinanzas, etc.)")
