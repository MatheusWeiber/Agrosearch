import os
import requests
from dotenv import load_dotenv, find_dotenv

# Carrega as chaves do arquivo .env
load_dotenv(find_dotenv())

basePath = os.path.join("..", "datasets", "raw")

targets = {
    "corn/healthy": [
        "corn plant healthy leaf close up",
        "maize field green leaves",
        "healthy zea mays leaf texture",
        "corn crop no disease",
        "fresh corn leaves sunlight",
        "young corn plant whorl healthy"
    ],
    "corn/common_rust": [
        "corn common rust Puccinia sorghi",
        "maize common rust pustules",
        "corn leaf rust symptoms close up",
        "common rust vs southern rust corn", # Traz comparações ótimas
        "brown pustules corn leaf"
    ],
    "corn/ear_rot": [
        "corn ear rot Fusarium",
        "Gibberella ear rot corn",
        "Aspergillus ear rot maize", # Outro fungo comum
        "Diplodia ear rot white mold",
        "moldy corn cob close up",
        "corn kernel rot symptoms"
    ],
    "corn/northern_leaf_blight": [
        "northern corn leaf blight Exserohilum turcicum",
        "corn leaf blight cigar shaped lesions", # Sintoma clássico
        "maize northern leaf blight damage",
        "necrotic lesions corn leaf",
        "Exserohilum turcicum symptoms maize"
    ],
    
    "soybean/bacterial_blight": [
        "soybean bacterial blight Pseudomonas syringae",
        "bacterial blight soybean yellow halo", # Sintoma visual chave
        "soybean leaf water soaked lesions",
        "angular leaf spots soybean bacterial",
        "tattered soybean leaves blight"
    ]
}

print(f"Iniciando busca para {len(targets)} categorias...")

for target, query in targets.items():
    savePath = os.path.join(basePath, target)
    os.makedirs(savePath, exist_ok=True)
    print(f"Pasta verificada: {savePath}")
    print(f"Buscando no Google: {query}")

    params = {
        "engine": "google_images",
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "num": 80, 
    }

    try:
        # Tenta conectar
        response = requests.get("https://serpapi.com/search", params=params)
        
        # Se a API der erro (ex: chave errada), isso aqui avisa
        if response.status_code != 200:
            print(f"Erro na API: {response.text}")
            continue # Pula para a proxima doenca

        results = response.json()
        imagelist = results.get("images_results", [])
        
        print(f"Encontradas {len(imagelist)} imagens. Baixando...")

        # Loop de download (DENTRO do try)
        for i, image in enumerate(imagelist):
            try:
                imageUrl = image["original"]
                imageResponse = requests.get(imageUrl, timeout=5)
                imageContent = imageResponse.content
                
                fileName = f"google_{i}.jpg"
                fullPath = os.path.join(savePath, fileName)
                
                with open(fullPath, "wb") as f:
                    f.write(imageContent)
                print(f"Salvo: {fileName}")
                
            except Exception as erroDownload:
                print(f"Erro ao baixar imagem {i}: {erroDownload}")

    except Exception as e:
        print(f"Erro geral: {e}")