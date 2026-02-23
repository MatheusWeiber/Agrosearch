import os
import requests
from dotenv import load_dotenv, find_dotenv

# 1. Carregar a chave secreta
load_dotenv(find_dotenv())
minha_chave = os.environ.get("SERPAPI_API_KEY")

# 2. Definir o que queremos buscar
params = {
    "engine": "google_images",      # Qual motor usar (Google Imagens)
    "q": "corn plant healthy leaf", # O que pesquisar (Milho Saudável)
    "api_key": minha_chave,         # Nossa credencial
    "num": 5                        # Vamos pedir só 5 resultados para testar
}

print("🔑 Chave carregada:", minha_chave[:5] + "...") # Mostra só o começo pra confirmar
print("📡 Enviando pedido para o Google...")
# 3. Fazendo a busca de verdade
url_base = "https://serpapi.com/search"
resultado = requests.get(url_base, params=params)

# 4. Transformando a resposta (que vem em texto) para Dicionário Python (JSON)
dados = resultado.json()

# Vamos ver se deu certo?
if "images_results" in dados:
    lista_imagens = dados["images_results"]
    print(f"✅ Sucesso! O Google achou {len(lista_imagens)} imagens.")
    
    # Vamos imprimir o link da primeira imagem para ver se é real
    primeira_imagem = lista_imagens[0]
    print("🔗 Link da 1ª imagem:", primeira_imagem.get("original"))
else:
    print("❌ Erro:", dados.get("error"))
    # ... (seu código anterior que já funciona)

if "images_results" in dados:
    lista = dados["images_results"]
    
    # Vamos pegar só as 3 primeiras (do índice 0 até 3)
    for i, imagem in enumerate(lista[:3]):
        try:
            link_original = imagem["original"]
            print(f"baixando {i}: {link_original}")

            # 1. BATE NA PORTA DO SITE E PEDE A FOTO
            resposta_imagem = requests.get(link_original, timeout=5)
            
            # 2. GUARDA OS DADOS BINÁRIOS (OS BYTES DA FOTO)
            bytes_da_imagem = resposta_imagem.content

            # 3. CRIA O ARQUIVO NO PC
            # 'wb' significa Write Binary (Escrita Binária) - essencial para fotos!
            nome_arquivo = f"teste_milho_{i}.jpg"
            
            with open(nome_arquivo, "wb") as arquivo:
                arquivo.write(bytes_da_imagem)
                
            print(f"✅ Salvo: {nome_arquivo}")

        except Exception as erro:
            print(f"❌ Deu ruim na imagem {i}: {erro}")

print("🏁 Fim do teste!")