import streamlit as st
import unicodedata

# 1) Função para normalizar acentos (á -> a)
def remover_acentos(texto):
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

st.title("Conversor de Texto para Bolinhas")

# 2) Caixa de texto aumentada para parágrafos
entrada = st.text_area("Digite seu texto (com parágrafos e acentos):", height=200)

if st.button("Gerar Bolinhas"):
    if entrada:
        # Normaliza o texto para ignorar acentos (Requisito 1)
        texto_limpo = remover_acentos(entrada).lower()
        
        # Divide por quebras de linha para respeitar parágrafos (Requisito 2)
        paragrafos = texto_limpo.split('\n')
        
        for paragrafo in paragrafos:
            if not paragrafo.strip(): # Se for linha vazia, pula
                st.write("") 
                continue
                
            cols = st.columns(len(paragrafo) if len(paragrafo) > 0 else 1)
            
            for i, char in enumerate(paragrafo):
                with cols[i]:
                    if char == " ":
                        st.write(" ")
                    # 3) Bolinha de cor diferente para pontuação
                    elif char in ".,!?;:":
                        st.markdown('<div style="height: 20px; width: 20px; background-color: #7f8c8d; border-radius: 50%;"></div>', unsafe_allow_html=True)
                    # Letras normais
                    elif 'a' <= char <= 'z':
                        st.markdown('<div style="height: 20px; width: 20px; background-color: #3498db; border-radius: 50%;"></div>', unsafe_allow_html=True)
            
            # Espaço entre parágrafos (Requisito 2)
            st.write("---") 
    else:
        st.warning("Por favor, digite algum texto.")
