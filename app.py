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

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(pontos_pequenos_x, pontos_pequenos_y, s=20, c='#95a5a6', marker='.', alpha=0.4)
    ax.scatter(pontos_grandes_x, pontos_grandes_y, s=120, c='#2c3e50', edgecolors="black", zorder=3)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

# --- Interface do Streamlit ---
st.title("textopontotexto")

# Para evitar o NameError, definimos um estado inicial fixo ou usamos um valor padrão
# O st.toggle retorna True se ativado, False se desativado
estado_privado = st.toggle("Ativar/Desativar modo privado")

# Lógica para mudar o rótulo dinamicamente baseado no estado atual
if estado_privado:
    st.write("Modo: Privado (Sua frase está oculta)")
    tipo_input = "password"
else:
    st.write("Modo: Público (Sua frase está visível)")
    tipo_input = "default"

texto_usuario = st.text_input("Escreva sua frase:", type=tipo_input)

if st.button("pronto"):
    if texto_usuario:
        figura = gerar_grafico(texto_usuario)
        st.pyplot(figura)
        
        buf = io.BytesIO()
        figura.savefig(buf, format="png", bbox_inches='tight')
        byte_im = buf.getvalue()
        
        st.download_button(
            label="Baixar imagem como PNG",
            data=byte_im,
            file_name="meu_padrao.png",
            mime="image/png"
        )
    else:
        st.warning("Por favor, digite algo primeiro.")
