import os
import shutil

# Caminho base onde estão suas imagens
base_dir = "../datasets/processed"
splits = ['train', 'val', 'test']
crops = ['corn', 'soybean']

print("🔧 Iniciando reorganização das pastas...")

for split in splits:
    split_path = os.path.join(base_dir, split)
    
    if not os.path.exists(split_path):
        print(f"⚠️ Pasta não encontrada: {split_path}")
        continue
        
    print(f"\n📂 Processando: {split}")
    
    for crop in crops:
        crop_path = os.path.join(split_path, crop)
        
        # Verifica se a pasta da cultura (corn/soybean) existe
        if os.path.exists(crop_path):
            # Lista todas as doenças dentro dela
            diseases = os.listdir(crop_path)
            
            for disease in diseases:
                src = os.path.join(crop_path, disease)
                
                # Nome novo: corn_rust, soybean_healthy (para não misturar)
                new_folder_name = f"{crop}_{disease}"
                dst = os.path.join(split_path, new_folder_name)
                
                # Move a pasta para fora
                if os.path.isdir(src):
                    # Se já existe (caso tenha rodado antes), não sobrescreve
                    if not os.path.exists(dst):
                        shutil.move(src, dst)
                        print(f"   Movido: {disease} -> {new_folder_name}")
                    else:
                        print(f"  ℹ Já existe: {new_folder_name}")
            
            # Tenta apagar a pasta da cultura vazia
            try:
                os.rmdir(crop_path)
                print(f"  🗑️ Pasta vazia removida: {crop}")
            except OSError:
                print(f"  ⚠️ Não foi possível remover {crop} (talvez ainda tenha arquivos?)")

print("\n✨ Concluído! Agora suas pastas mostram as 12 doenças diretamente.")