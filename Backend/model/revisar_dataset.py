import pandas as pd
import shutil
import os
import tkinter as tk
from PIL import Image, ImageTk

# Caminho base onde estão as pastas das doenças
CAMINHO_BASE = r'D:\Programacao\Python Code\AppDoecas\Backend\datasets\processed\train'

# Lê o CSV gerado pelo Cleanlab
df = pd.read_csv('suspeitas_bipolaris_southern.csv')

# Relatório do que foi feito
relatorio = []

# =============================================
# BLOCO 1 — Move automaticamente as óbvias
# =============================================

obvias = df[df['confianca_sugestao'] >= 0.95]
intermediarias = df[(df['confianca_sugestao'] >= 0.70) & (df['confianca_sugestao'] < 0.95)]
ignoradas = df[df['confianca_sugestao'] < 0.70]

print(f"Óbvias (>= 0.95): {len(obvias)} imagens — serão movidas automaticamente")
print(f"Intermediárias (0.70 a 0.95): {len(intermediarias)} imagens — você vai decidir")
print(f"Ignoradas (< 0.70): {len(ignoradas)} imagens — serão puladas")
print()

movidas = 0
erros = 0

for _, linha in obvias.iterrows():
    caminho_origem = os.path.join(CAMINHO_BASE, linha['arquivo'])
    nome_foto = os.path.basename(linha['arquivo'])
    caminho_destino = os.path.join(CAMINHO_BASE, linha['classe_sugerida'], nome_foto)

    if os.path.exists(caminho_origem):
        shutil.move(caminho_origem, caminho_destino)
        print(f"Movido automaticamente: {nome_foto} → {linha['classe_sugerida']}")
        relatorio.append({
            'arquivo': nome_foto,
            'acao': 'movido_automatico',
            'de': linha['rotulo_atual'],
            'para': linha['classe_sugerida'],
            'confianca': linha['confianca_sugestao']
        })
        movidas += 1
    else:
        print(f"ERRO - não encontrado: {caminho_origem}")
        erros += 1

print(f"\nBloco 1 concluído — {movidas} movidas, {erros} erros")
print("Iniciando revisão visual...\n")

# =============================================
# BLOCO 2 — Revisão visual das intermediárias
# =============================================

# Converte para lista para poder navegar por índice
lista_intermediarias = intermediarias.to_dict('records')
indice_atual = [0]  # lista pra poder modificar dentro das funções do tkinter

# Se não tiver intermediárias, pula esse bloco
if len(lista_intermediarias) == 0:
    print("Nenhuma imagem intermediária para revisar.")
else:
    # Cria a janela principal
    janela = tk.Tk()
    janela.title("Revisão de imagens — Agrosearch")
    janela.geometry("800x650")

    # Label que mostra informações da imagem atual
    info_label = tk.Label(janela, text="", font=("Arial", 11), wraplength=780, justify="left")
    info_label.pack(pady=10)

    # Label que mostra a imagem
    imagem_label = tk.Label(janela)
    imagem_label.pack()

    # Label de progresso
    progresso_label = tk.Label(janela, text="", font=("Arial", 10), fg="gray")
    progresso_label.pack(pady=5)

    def carregar_imagem(idx):
        linha = lista_intermediarias[idx]
        caminho = os.path.join(CAMINHO_BASE, linha['arquivo'])
        nome_foto = os.path.basename(linha['arquivo'])

        # Atualiza o texto de informação
        info_label.config(text=(
            f"Arquivo: {nome_foto}\n"
            f"Rótulo ATUAL: {linha['rotulo_atual']}\n"
            f"Cleanlab SUGERE: {linha['classe_sugerida']}\n"
            f"Confiança da sugestão: {linha['confianca_sugestao']}"
        ))

        # Atualiza o progresso
        progresso_label.config(text=f"Imagem {idx + 1} de {len(lista_intermediarias)}")

        # Carrega e exibe a imagem
        if os.path.exists(caminho):
            img = Image.open(caminho)
            img = img.resize((500, 400))
            foto = ImageTk.PhotoImage(img)
            imagem_label.config(image=foto)
            imagem_label.image = foto  # mantém referência para não ser coletado pelo garbage collector
        else:
            imagem_label.config(image="", text="Arquivo não encontrado")

    def proxima_imagem():
        indice_atual[0] += 1
        if indice_atual[0] >= len(lista_intermediarias):
            janela.destroy()  # fecha a janela quando acabar
        else:
            carregar_imagem(indice_atual[0])

    def acao_mover():
        linha = lista_intermediarias[indice_atual[0]]
        caminho_origem = os.path.join(CAMINHO_BASE, linha['arquivo'])
        nome_foto = os.path.basename(linha['arquivo'])
        caminho_destino = os.path.join(CAMINHO_BASE, linha['classe_sugerida'], nome_foto)

        if os.path.exists(caminho_origem):
            shutil.move(caminho_origem, caminho_destino)
            relatorio.append({
                'arquivo': nome_foto,
                'acao': 'movido_manual',
                'de': linha['rotulo_atual'],
                'para': linha['classe_sugerida'],
                'confianca': linha['confianca_sugestao']
            })
            print(f"Movido: {nome_foto} → {linha['classe_sugerida']}")
        proxima_imagem()

    def acao_manter():
        linha = lista_intermediarias[indice_atual[0]]
        nome_foto = os.path.basename(linha['arquivo'])
        relatorio.append({
            'arquivo': nome_foto,
            'acao': 'mantido',
            'de': linha['rotulo_atual'],
            'para': linha['rotulo_atual'],
            'confianca': linha['confianca_sugestao']
        })
        print(f"Mantido: {nome_foto}")
        proxima_imagem()

    def acao_deletar():
        linha = lista_intermediarias[indice_atual[0]]
        caminho_origem = os.path.join(CAMINHO_BASE, linha['arquivo'])
        nome_foto = os.path.basename(linha['arquivo'])

        if os.path.exists(caminho_origem):
            os.remove(caminho_origem)
            relatorio.append({
                'arquivo': nome_foto,
                'acao': 'deletado',
                'de': linha['rotulo_atual'],
                'para': 'deletado',
                'confianca': linha['confianca_sugestao']
            })
            print(f"Deletado: {nome_foto}")
        proxima_imagem()

    # Frame para os botões ficarem lado a lado
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=15)

    tk.Button(frame_botoes, text="Mover para sugerida", bg="green", fg="white",
              font=("Arial", 12), width=20, command=acao_mover).grid(row=0, column=0, padx=10)

    tk.Button(frame_botoes, text="Manter onde está", bg="gray", fg="white",
              font=("Arial", 12), width=20, command=acao_manter).grid(row=0, column=1, padx=10)

    tk.Button(frame_botoes, text="Deletar imagem", bg="red", fg="white",
              font=("Arial", 12), width=20, command=acao_deletar).grid(row=0, column=2, padx=10)

    # Carrega a primeira imagem e inicia o loop da janela
    carregar_imagem(0)
    janela.mainloop()

# =============================================
# BLOCO 3 — Ignora as abaixo de 0.70
# =============================================

print(f"\nIgnoradas (confiança < 0.70): {len(ignoradas)} imagens")
for _, linha in ignoradas.iterrows():
    nome_foto = os.path.basename(linha['arquivo'])
    relatorio.append({
        'arquivo': nome_foto,
        'acao': 'ignorado',
        'de': linha['rotulo_atual'],
        'para': '-',
        'confianca': linha['confianca_sugestao']
    })

# =============================================
# SALVA O RELATÓRIO FINAL
# =============================================

df_relatorio = pd.DataFrame(relatorio)
df_relatorio.to_csv('relatorio_revisao.csv', index=False)

print(f"\nRevisão concluída!")
print(f"Relatório salvo em: relatorio_revisao.csv")
print(df_relatorio['acao'].value_counts())