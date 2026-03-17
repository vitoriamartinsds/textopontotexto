import streamlit as st
import matplotlib.pyplot as plt
import unicodedata
import io
import string

# Função para remover acentos
def remover_acentos(texto):
    return "".join(c for c in unicodedata.normalize('NFD', texto)
                    if unicodedata.category(c) != 'Mn')

# --- NOVO: divide em páginas ---
def dividir_em_paginas(frase, linhas_por_pagina=30):
    linhas = frase.split("\n")
    
    palavras_por_linha = []
    for linha in linhas:
        palavras = linha.split()
        if palavras:
            palavras_por_linha.extend(palavras)
        else:
            palavras_por_linha.append("")  # mantém quebra de parágrafo
    
    paginas = []
    for i in range(0, len(palavras_por_linha), linhas_por_pagina):
        paginas.append(palavras_por_linha[i:i+linhas_por_pagina])
    
    return paginas

# Função principal de geração do gráfico (por página)
def gerar_grafico(palavras):
    frase_limpa = [remover_acentos(p.upper()) for p in palavras]
    
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n_letras = len(alfabeto)
    
    pontos_grandes_x, pontos_grandes_y = [], []
    pontos_pequenos_x, pontos_pequenos_y = [], []
    pontos_pontuacao_x, pontos_pontuacao_y = [], []
    
    espacamento_vertical = 1  # ajustado para caber 30 linhas
    
    for p_idx, palavra in enumerate(frase_limpa):
        x, y = 0, -p_idx * espacamento_vertical
        
        for i in range(len(palavra)):
            char = palavra[i]
            
            if char in string.punctuation:
                pontos_pontuacao_x.append(x)
                pontos_pontuacao_y.append(y)
                continue
            
            if char not in alfabeto: 
                continue
            
            pontos_grandes_x.append(x)
            pontos_grandes_y.append(y)
            
            if i + 1 < len(palavra):
                prox_char = palavra[i+1]
                
                if prox_char not in alfabeto:
                    continue
                
                idx_atual = alfabeto.index(char)
                idx_prox = alfabeto.index(prox_char)
                
                distancia = (idx_prox - idx_atual) if idx_prox >= idx_atual else (n_letras - idx_atual) + idx_prox
                direcao_direita = (i % 2 == 0)
                
                for d in range(1, distancia):
                    if direcao_direita:
                        pontos_pequenos_x.append(x + d)
                        pontos_pequenos_y.append(y)
                    else:
                        pontos_pequenos_x.append(x)
                        pontos_pequenos_y.append(y - d)
                
                if direcao_direita: x += distancia
                else: y -= distancia

    # --- TAMANHO FIXO A3 ---
    fig, ax = plt.subplots(figsize=(11.69, 16.54))

    # ajuste simples de escala
    total = len(pontos_grandes_x)
    if total < 50:
        s_big, s_small, s_p = 60, 10, 40
    else:
        s_big, s_small, s_p = 120, 20, 80

    ax.scatter(pontos_pequenos_x, pontos_pequenos_y, s=s_small, c='#2c3e50')
    ax.scatter(pontos_grandes_x, pontos_grandes_y, s=s_big, c='#2c3e50', edgecolors="black")
    ax.scatter(pontos_pontuacao_x, pontos_pontuacao_y, s=s_p, c='red')
    
    ax.set_aspect('equal')
    ax.axis('off')
    
    return fig

# --- Interface ---
st.title("textopontotexto")

estado_privado = st.toggle("esconder")

# máscara tipo senha
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
        
        paginas = dividir_em_paginas(texto_usuario)
        
        for i, pagina in enumerate(paginas):
            st.subheader(f"Página {i+1}")
            
            fig = gerar_grafico(pagina)
            st.pyplot(fig)
            
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches='tight', dpi=300)
            
            st.download_button(
                label=f"salvar página {i+1}",
                data=buf.getvalue(),
                file_name=f"texto_pagina_{i+1}.png",
                mime="image/png"
            )
    else:
        st.warning("digite primeiro.")
