import os
import shutil

# Configurações de Origem (Casa Velha) e Destino (Casa Nova)
source_root = "Doencas plantas"
dest_root = os.path.join("backend", "datasets", "raw")

# Mapa da Mudança: "Pasta Antiga" -> "Pasta Nova"
# Baseado no print que você mandou
folder_mapping = {
    # --- SOJA ---
    os.path.join("doencasSoja", "Ferrugem"):               os.path.join("soybean", "asian_rust"),
    os.path.join("doencasSoja", "ManchaAlvo"):             os.path.join("soybean", "target_spot"),
    os.path.join("doencasSoja", "CrestamentoBacteriano"):  os.path.join("soybean", "bacterial_blight"),
    os.path.join("doencasSoja", "OlhoDeSapo"):             os.path.join("soybean", "frog_eye_spot"),
    os.path.join("doencasSoja", "Saudavel"):               os.path.join("soybean", "healthy"),
    os.path.join("doencasSoja", "LagartaDaSoja"):          os.path.join("soybean", "caterpillar"), # Adicionei essa extra que vi na sua foto

    # --- MILHO ---
    os.path.join("doencasMilho", "FerrugemComum"):         os.path.join("corn", "common_rust"),
    os.path.join("doencasMilho", "FerrugemPolissora"):     os.path.join("corn", "southern_rust"),
    os.path.join("doencasMilho", "ManchaDeTurcicum"):      os.path.join("corn", "northern_leaf_blight"),
    os.path.join("doencasMilho", "Saudavel"):              os.path.join("corn", "healthy"),
    # Adicionando as outras do milho que vi no print para não perder nada:
    os.path.join("doencasMilho", "ManchaBipolaris"):       os.path.join("corn", "bipolaris_spot"),
    os.path.join("doencasMilho", "ManchaBranca"):          os.path.join("corn", "white_spot"),
    os.path.join("doencasMilho", "PodridaodaEspiga"):      os.path.join("corn", "ear_rot"),
}

print("🚛 Iniciando a mudança das fotos...\n")

moved_count = 0

for old_subpath, new_subpath in folder_mapping.items():
    # Caminhos completos
    old_folder = os.path.join(source_root, old_subpath)
    new_folder = os.path.join(dest_root, new_subpath)

    # Verifica se a pasta antiga existe
    if os.path.exists(old_folder):
        # Garante que a pasta nova existe (cria se precisar)
        os.makedirs(new_folder, exist_ok=True)

        # Pega todos os arquivos da pasta antiga
        files = os.listdir(old_folder)
        
        for file_name in files:
            # Pega só imagens (evita copiar arquivos ocultos de sistema)
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                src_file = os.path.join(old_folder, file_name)
                dst_file = os.path.join(new_folder, file_name)
                
                # Move o arquivo
                shutil.move(src_file, dst_file)
                moved_count += 1
                print(f"📦 Movido: {file_name} -> {new_subpath}")
    else:
        print(f" Pasta antiga não encontrada: {old_subpath} (Pulei)")

print(f"\n Mudança concluída! Total de imagens movidas: {moved_count}")
print("Agora seus dados estão padronizados dentro de 'backend/datasets/raw'.")