import streamlit as st
import unicodedata

def remover_acentos(texto):
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def renderizar_bolinhas(texto_bruto):
    texto = remover_acentos(texto_bruto).lower()
    linhas = texto.split('\n')
    
    # Cores
    cor_letra = "#3498db"   # Azul
    cor_ponto = "#e74c3c"   # Vermelho (ou a cor que preferir para destaque)
    
    html_gerado = "<div style='line-height: 2.5;'>"
    
    for linha in linhas:
        if not linha.strip():
            html_gerado += "<br>" # Mantém o parágrafo vazio se houver
            continue
            
        for char in linha:
            if char == " ":
                # Espaço vazio
                html_gerado += "<span style='margin-right: 25px;'></span>"
            elif char in ".,!?;:":
                # Bolinha de pontuação
                html_gerado += f"<span style='height: 15px; width: 15px; background-color: {cor_ponto}; border-radius: 50%; display: inline-block; margin-right: 10px; border: 1px solid black;'></span>"
            elif 'a' <= char <= 'z':
                # Bolinha de letra
                html_gerado += f"<span style='height: 15px; width: 15px; background-color: {cor_letra}; border-radius: 50%; display: inline-block; margin-right: 10px; border: 1px solid black;'></span>"
        
        html_gerado += "<br>" # Quebra de linha ao fim de cada parágrafo
        
    html_gerado += "</div>"
    return html_gerado

# Interface Streamlit
st.title("Conversor de Texto em Bolinhas")
st.markdown("Os acentos serão removidos e as pontuações terão cores diferentes.")

# Área de texto (Multilinha e maior)
entrada = st.text_area("Digite seu texto aqui:", height=200)

if st.button("Gerar Visualização"):
    if entrada:
        resultado_html = renderizar_bolinhas(entrada)
        st.markdown("---")
        st.write("### Resultado:")
        st.markdown(resultado_html, unsafe_allow_html=True)
    else:
        st.warning("Por favor, digite algum texto.")
