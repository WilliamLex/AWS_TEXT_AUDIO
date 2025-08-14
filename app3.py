import streamlit as st
import base64
import requests
import time

LAMBDA_URL = "https://msam31n5i0.execute-api.us-east-1.amazonaws.com/default/placasvh"

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🎙️ Transcripción por Lambda</h1>", unsafe_allow_html=True)

if "texto_transcrito" not in st.session_state:
    st.session_state.texto_transcrito = ""

# Subir archivo
uploaded_file = st.file_uploader("📤 Sube un archivo de audio", type=["mp3", "wav", "m4a"])

if uploaded_file:
    audio_bytes = uploaded_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    file_name = uploaded_file.name

    if st.button("🔄 Enviar a Lambda para transcripción"):
        with st.spinner("🔄 Transcribiendo audio en Lambda..."):
            payload = {
                "file_name": file_name,
                "audio_base64": audio_base64
            }
            try:
                response = requests.post(LAMBDA_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.texto_transcrito = data.get("transcription", "")
                    st.success("✅ Transcripción completada")
                else:
                    st.error(f"❌ Lambda devolvió error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"❌ Error enviando a Lambda: {e}")

# Mostrar texto transcrito
st.subheader("📝 Texto transcrito")
st.text_area("Edita el texto si es necesario", value=st.session_state.texto_transcrito, height=200)
