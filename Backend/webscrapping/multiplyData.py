import os
import random
from PIL import Image, ImageEnhance, ImageOps

# 1. Definições Iniciais
basePath = os.path.join("..", "datasets", "raw")

targetDataset = [
    "corn/healthy",
    "corn/common_rust",
    "corn/ear_rot",
    "corn/northern_leaf_blight",
    "soybean/bacterial_blight",
]

# 2. A Função que cria as cópias
def augmentData(imagePath, saveFolder, filename_base):
    try:
        img = Image.open(imagePath)
        # Garante que e RGB (evita erro em PNGs transparentes)
        if img.mode != "RGB":
            img = img.convert("RGB")

        # --- VARIAÇÃO 1: ESPELHAMENTO (MIRROR) ---
        # Usamos mirror (horizontal) em vez de flip (vertical) 
        img_flip = ImageOps.mirror(img)
        img_flip.save(os.path.join(saveFolder, f"aug_flip_{filename_base}"))

        # --- VARIAÇÃO 2: ROTAÇÃO ---
        angle = random.randint(-15, 15)
        # expand=False é vital para não criar bordas pretas
        img_rot = img.rotate(angle, expand=False) 
        img_rot.save(os.path.join(saveFolder, f"aug_rot_{filename_base}"))

        # --- VARIAÇÃO 3: BRILHO ---
        enhancer = ImageEnhance.Brightness(img)
        factor = random.uniform(0.7, 1.3) # 0.7 = escuro, 1.3 = claro
        img_bright = enhancer.enhance(factor)
        img_bright.save(os.path.join(saveFolder, f"aug_bright_{filename_base}"))

        # --- VARIAÇÃO 4: ZOOM ---
        w, h = img.size
        zoom_factor = 0.85 # Cortar 15% das bordas
        left = w * (1 - zoom_factor) / 2
        top = h * (1 - zoom_factor) / 2
        right = w - left
        bottom = h - top
        
        img_zoom = img.crop((left, top, right, bottom))
        # Redimensiona de volta para o tamanho original com alta qualidade
        img_zoom = img_zoom.resize((w, h), Image.Resampling.LANCZOS) 
        img_zoom.save(os.path.join(saveFolder, f"aug_zoom_{filename_base}"))

        return True

    except Exception as e:  
        print(f"Erro ao processar imagem {filename_base}: {e}")
        return False

# 3. Execução Principal
print(" Iniciando a multiplicação das imagens...")

for folder in targetDataset:
    folderPath = os.path.join(basePath, folder)
    
    if not os.path.exists(folderPath):
        print(f" Pasta não encontrada: {folder}")
        continue

    print(f"\n Processando pasta: {folder}")
    
    all_files = os.listdir(folderPath)
    
    # Filtra apenas imagens originais (ignora as que já começam com "aug_")
    original_images = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith("aug_")]
    
    print(f"   Imagens originais encontradas: {len(original_images)}")
    
    count = 0
    for file_name in original_images:
        fullPath = os.path.join(folderPath, file_name)
        
        # Chama a função corrigida (augmentData)
        if augmentData(fullPath, folderPath, file_name):
            count += 4 # Conta 4 novas imagens por cada original
            print(f"   Gerando variações... (+{count})", end="\r")

    print(f"\n Concluído! {count} novas imagens criadas nesta pasta.")
print("\n Processo finalizado! Rode o check_balance.py para ver o resultado.")