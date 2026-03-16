import streamlit as st
import matplotlib.pyplot as plt
import unicodedata
import io

# Função para remover acentos
def remover_acentos(texto):
    return "".join(c for c in unicodedata.normalize('NFD', texto)
                    if unicodedata.category(c) != 'Mn')

# Função principal de geração do gráfico
def gerar_grafico(frase):
    frase_limpa = remover_acentos(frase.upper())
    palavras = frase_limpa.split()
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n_letras = len(alfabeto)
    
    pontos_grandes_x, pontos_grandes_y = [], []
    pontos_pequenos_x, pontos_pequenos_y = [], []
    
    # Configurações de estilo fixas
    espacamento_vertical = 2 
    
    for p_idx, palavra in enumerate(palavras):
        x, y = 0, -(p_idx * espacamento_vertical)
        
        for i in range(len(palavra)):
            char = palavra[i]
            if char not in alfabeto: continue
            
            pontos_grandes_x.append(x)
            pontos_grandes_y.append(y)
            
            if i + 1 < len(palavra):
                idx_atual = alfabeto.index(char)
                idx_prox = alfabeto.index(palavra[i+1])
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

    # --- AJUSTE DINÂMICO DO TAMANHO DA PÁGINA ---
    todos_x = pontos_grandes_x + pontos_pequenos_x
    todos_y = pontos_grandes_y + pontos_pequenos_y
    
    if todos_x and todos_y:
        largura = max(todos_x) - min(todos_x)
        altura = max(todos_y) - min(todos_y)
        # Define um fator de escala para converter unidades de dados em polegadas
        fator_escala = 0.5 
        fig_width = max(8, largura * fator_escala)
        fig_height = max(8, altura * fator_escala)
    else:
        fig_width, fig_height = 8, 8

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    # s=120 e s=20 agora parecerão consistentes pois o figsize acompanha o volume de dados
    ax.scatter(pontos_pequenos_x, pontos_pequenos_y, s=20, c='#2c3e50', marker='.', alpha=0)
    ax.scatter(pontos_grandes_x, pontos_grandes_y, s=120, c='#2c3e50', edgecolors="black", zorder=3)
    
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

# --- Interface do Streamlit ---
st.title("textopontotexto")

estado_privado = st.toggle("esconder")

# Define o padrão como "default"
tipo_input = "default"

# Sobrescreve apenas se for privado
if estado_privado:
    st.write("")
    tipo_input = "password"

texto_usuario = st.text_input("escreve", type=tipo_input)

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
