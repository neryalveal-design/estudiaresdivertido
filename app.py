import streamlit as st
from openai import OpenAI

# Configurar cliente GPT (necesita API key)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎮 Juego de Lenguaje con GPT")

# Subir guía
uploaded_file = st.file_uploader("Sube tu guía en Word o PDF", type=["docx", "pdf"])

if uploaded_file:
    texto = uploaded_file.read()  # se simplifica, el profe puede dar código listo para extraer texto
    st.write("✅ Guía cargada correctamente")

    # Prompt para GPT
    prompt = f"""
    A partir del siguiente texto de una guía de lenguaje, genera 5 preguntas de opción múltiple
    con 4 alternativas cada una. Señala la respuesta correcta con un asterisco (*).
    Texto: {texto}
    """

    if st.button("Generar preguntas"):
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )
        st.write("### Preguntas generadas por GPT")
        st.write(respuesta.choices[0].message.content)
