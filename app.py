import streamlit as st
import unicodedata

# Função para tratar os acentos (Requisito 1)
def remover_acentos(texto):
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

st.title("Conversor de Texto para Bolinhas")

# Caixa de texto aumentada para aceitar parágrafos (Requisito 2)
entrada = st.text_area("Digite seu texto (com parágrafos e acentos):", height=200)

if st.button("Gerar Bolinhas"):
    if entrada:
        # Processa o texto para ignorar acentos e padronizar
        texto_processado = remover_acentos(entrada).lower()
        
        # Divide o texto por quebras de linha (Requisito 2)
        paragrafos = texto_processado.split('\n')
        
        resultado_html = ""
        for paragrafo in paragrafos:
            linha_html = "<div style='margin-bottom: 20px;'>" # Espaço entre parágrafos
            for char in paragrafo:
                if char == " ":
                    linha_html += "<span style='margin-right: 20px;'></span>"
                # Identifica pontuação para mudar a cor (Requisito 3)
                elif char in ".,!?;:":
                    linha_html += "<span style='height: 15px; width: 15px; background-color: #e74c3c; border-radius: 50%; display: inline-block; margin-right: 5px;'></span>"
                elif 'a' <= char <= 'z':
                    linha_html += "<span style='height: 15px; width: 15px; background-color: #3498db; border-radius: 50%; display: inline-block; margin-right: 5px;'></span>"
            linha_html += "</div>"
            resultado_html += linha_html
            
        st.markdown(resultado_html, unsafe_allow_html=True)
    else:
        st.warning("Por favor, digite algum texto.")
