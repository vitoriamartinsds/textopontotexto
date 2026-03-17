import streamlit as st
import matplotlib.pyplot as plt
import unicodedata
import io
import string

# Função para remover acentos
def remover_acentos(texto):
    return "".join(c for c in unicodedata.normalize('NFD', texto)
                    if unicodedata.category(c) != 'Mn')

# Função principal de geração do gráfico
def gerar_grafico(frase):
    frase_limpa = remover_acentos(frase.upper())
    
    linhas = frase_limpa.split("\n")  # suporte a parágrafos
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n_letras = len(alfabeto)
    
    pontos_grandes_x, pontos_grandes_y = [], []
    pontos_pequenos_x, pontos_pequenos_y = [], []
    pontos_pontuacao_x, pontos_pontuacao_y = [], []  # NOVO
    
    espacamento_vertical = 2 
    
    linha_offset = 0
    
    for linha in linhas:
        palavras = linha.split()
        
        for p_idx, palavra in enumerate(palavras):
            x, y = 0, -(linha_offset + p_idx) * espacamento_vertical
            
            for i in range(len(palavra)):
                char = palavra[i]
                
                # --- PONTUAÇÃO ---
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
                    
                    # ignora pontuação na lógica de distância
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
        
        linha_offset += len(palavras) + 1  # espaço entre parágrafos

    # --- AJUSTE DINÂMICO DO TAMANHO ---
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
    
    # --- PONTUAÇÃO (cor diferente) ---
    ax.scatter(pontos_pontuacao_x, pontos_pontuacao_y, s=80, c='red', zorder=4)
    
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

# --- Interface do Streamlit ---
st.title("textopontotexto")

estado_privado = st.toggle("esconder")

tipo_input = "default"
if estado_privado:
    st.write("")
    tipo_input = "password"

# ALTERADO: agora permite parágrafos
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
