import tkinter as tk
import unicodedata

def remover_acentos(texto):
    # Normaliza o texto para remover acentos (ex: á -> a)
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def desenhar_bolinhas():
    # Limpa o canvas antes de desenhar
    canvas.delete("all")
    
    # Pega o texto da caixa de texto (multilinha)
    texto_bruto = text_input.get("1.0", tk.END)
    texto = remover_acentos(texto_bruto).lower()
    
    x_inicial = 20
    y_inicial = 30
    x, y = x_inicial, y_inicial
    raio = 10
    espacamento = 30
    largura_maxima = 560 # Limite lateral do canvas

    for char in texto:
        if char == '\n': # Pula linha se houver um parágrafo
            x = x_inicial
            y += espacamento + 10
            continue
            
        if char == " ": # Espaço em branco
            x += espacamento
        elif char in ".,!?;:": # Pontuação (Bolinha de cor diferente)
            canvas.create_oval(x, y, x + raio*2, y + raio*2, fill="#7f8c8d", outline="black")
            x += espacamento
        elif 'a' <= char <= 'z': # Letras normais
            canvas.create_oval(x, y, x + raio*2, y + raio*2, fill="#3498db", outline="black")
            x += espacamento
        
        # Quebra de linha automática se chegar na borda do canvas
        if x > largura_maxima:
            x = x_inicial
            y += espacamento

# Configuração da Janela Principal
root = tk.Tk()
root.title("Conversor de Texto para Bolinhas")
root.geometry("6000x700")

# Interface
label = tk.Label(root, text="Digite seu texto (com parágrafos e acentos):", font=("Arial", 12))
label.pack(pady=10)

# Caixa de texto multilinha (Text no lugar de Entry)
text_input = tk.Text(root, height=5, width=50, font=("Arial", 12))
text_input.pack(pady=5)

btn_gerar = tk.Button(root, text="Gerar Bolinhas", command=desenhar_bolinhas, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"))
btn_gerar.pack(pady=10)

# Canvas para desenhar
canvas = tk.Canvas(root, width=580, height=400, bg="white", highlightthickness=1, highlightbackground="black")
canvas.pack(pady=10)

root.mainloop()
