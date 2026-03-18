import streamlit as st
import matplotlib.pyplot as plt
import unicodedata
import io
import string

def remover_acentos(texto):
    return "".join(c for c in unicodedata.normalize('NFD', texto)
                    if unicodedata.category(c) != 'Mn')

def gerar_grafico(frase):
    frase_limpa = remover_acentos(frase.upper())
    
    linhas = frase_limpa.split("\n")
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n_letras = len(alfabeto)
    
    pontos_grandes_x, pontos_grandes_y = [], []
    pontos_pequenos_x, pontos_pequenos_y = [], []
    pontos_pontuacao_x, pontos_pontuacao_y = [], []
    
    espacamento_vertical = 2 
    linha_offset = 0
    
    for linha in linhas:
        palavras = linha.split()
        
        for p_idx, palavra in enumerate(palavras):
            x, y = 0, -(linha_offset + p_idx) * espacamento_vertical
            
            ultimo_x, ultimo_y = x, y
            
            for i in range(len(palavra)):
                char = palavra[i]
                
                if char in string.punctuation:
                    # ponto ao lado do último ponto da letra
                    pontos_pontuacao_x.append(ultimo_x + 0.6)
                    pontos_pontuacao_y.append(ultimo_y)
                    continue
                
                if char not in alfabeto:
                    continue
                
                pontos_grandes_x.append(x)
                pontos_grandes_y.append(y)
                
                ultimo_x, ultimo_y = x, y
                
                if i + 1 < len(palavra):
                    prox_char = palavra[i+1]
                    
                    if prox_char not in alfabeto:
                        continue
                    
                    idx_atual = alfabeto.index(char)
                    idx_prox = alfabeto.index(prox_char)
                    
                    distancia = (idx_prox - idx_atual) if idx_prox >= idx_atual else (n_letras - idx_atual) + idx_prox
                    direcao_direita = (i % 2 == 0)
                    
                    if distancia > 2:
                        for d in range(1, distancia):
                            if direcao_direita:
                                pontos_pequenos_x.append(x + d)
                                pontos_pequenos_y.append(y)
                            else:
                                pontos_pequenos_x.append(x)
                                pontos_pequenos_y.append(y - d)
                    
                    if direcao_direita:
                        x += distancia
                    else:
                        y -= distancia
        
        linha_offset += len(palavras) + 1

    todos_x = pontos_grandes_x + pontos_pequenos_x + pontos_pontuacao_x
    todos_y = pontos_grandes_y + pontos_pequenos_y + pontos_pontuacao_y
    
    if todos_x and todos_y:
        largura = max(todos_x) - min(todos_x)
        altura = max(todos_y) - min(todos_y)
        fator_escala = 0.5 
        fig_width = max(8, largura * fator_escala)
        fig_height = max(8, altura * fator_escala)
    else:
        fig_width, fig_height = 8, 8

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    ax.scatter(pontos_pequenos_x, pontos_pequenos_y, s=20, c='#2c3e50', marker='.', alpha=1)
    ax.scatter(pontos_grandes_x, pontos_grandes_y, s=120, c='#2c3e50', edgecolors="black", zorder=3)
    ax.scatter(pontos_pontuacao_x, pontos_pontuacao_y, s=80, c='red', zorder=4)
    
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

# --- Interface ---
st.title("ponto_palavra")

estado_privado = st.toggle("esconder")

if estado_privado:
    st.markdown("""
        <style>
        textarea {
            -webkit-text-security: disc;
        }
        </style>
    """, unsafe_allow_html=True)

texto_usuario = st.text_area("escreve", height=200)

if st.button("pronto"):
    if texto_usuario:
        figura = gerar_grafico(texto_usuario)
        st.pyplot(figura)
        
        buf = io.BytesIO()
        figura.savefig(buf, format="png", bbox_inches='tight', dpi=100)
        byte_im = buf.getvalue()
        
        st.download_button(
            label="salvar",
            data=byte_im,
            file_name="textopontotexto.png",
            mime="image/png"
        )
    else:
        st.warning("digite primeiro.")
