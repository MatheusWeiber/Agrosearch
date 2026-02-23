import os
import random
from PIL import Image

INPUT_FOLDER = os.path.join("..", "datasets", "raw")
OUTPUT_FOLDER = os.path.join("..", "datasets", "processed")
TARGET_SIZE = (224, 224)
SPLIT_RATIOS = {"train": 0.7, "val": 0.2, "test": 0.1}

def process_and_copy(image_list, source_dir, class_name, set_name):
    dest_dir = os.path.join(OUTPUT_FOLDER, set_name, class_name)
    os.makedirs(dest_dir, exist_ok=True)

    count = 0
    for filename in image_list:
        try:
            src_path = os.path.join(source_dir, filename)
            dest_path = os.path.join(dest_dir, filename)

            with Image.open(src_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img_resized = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
                img_resized.save(dest_path, optimize=True, quality=90)
                count += 1
                
        except Exception as e:
            print(f"Erro no arquivo {filename}: {e}")

    return count

if os.path.exists(OUTPUT_FOLDER):
    print("Aviso: A pasta 'processed' ja existe.")

print(f"Iniciando processamento...")
print(f"Origem: {INPUT_FOLDER}")
print(f"Destino: {OUTPUT_FOLDER}")

classes = []
for root, dirs, files in os.walk(INPUT_FOLDER):
    if not dirs and files: 
        rel_path = os.path.relpath(root, INPUT_FOLDER)
        classes.append(rel_path)

print(f"Encontradas {len(classes)} classes.")

total_processed = 0

for class_name in classes:
    print(f"Processando classe: {class_name}...")
    
    
    source_dir = os.path.join(INPUT_FOLDER, class_name)
    all_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    
    #Embaralha as imagens
    random.shuffle(all_files)

    # Calcula quantos arquivos vão para cada lugar
    total_files = len(all_files)
    train_count = int(total_files * SPLIT_RATIOS["train"])
    val_count = int(total_files * SPLIT_RATIOS["val"])

    # Divide as listas
    train_files = all_files[:train_count]
    val_files = all_files[train_count : train_count + val_count]
    test_files = all_files[train_count + val_count:]
    
    # Processa cada grupo
    t_saved = process_and_copy(train_files, source_dir, class_name, "train")
    v_saved = process_and_copy(val_files, source_dir, class_name, "val")
    ts_saved = process_and_copy(test_files, source_dir, class_name, "test")
    
    print(f"   Treino: {t_saved} | Validacao: {v_saved} | Teste: {ts_saved}")
    total_processed += (t_saved + v_saved + ts_saved)

print("-" * 30)
print(f"Concluido. Total processado: {total_processed}")