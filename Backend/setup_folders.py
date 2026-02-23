import os

# Caminho onde vamos criar a estrutura oficial
base_path = os.path.join("backend", "datasets", "raw")

# Dicionário: Planta -> Lista de Doenças (Traduzindo sua estrutura para Inglês)
folders_to_create = {
    "soybean": [        # Antigo "doencasSoja"
        "healthy",              # Saudavel
        "asian_rust",           # Ferrugem
        "target_spot",          # ManchaAlvo
        "bacterial_blight",     # CrestamentoBacteriano
        "frog_eye_spot"         # OlhoDoSapo
    ],
    "corn": [           # Antigo "doencasMilho"
        "healthy",              # Saudavel
        "common_rust",          # FerrugemComum
        "southern_rust",        # FerrugemPolissora
        "northern_leaf_blight"  # ManchaDeTurcicum
    ]
}

print(f"🚀 Criando estrutura em: {base_path}...\n")

for plant, diseases in folders_to_create.items():
    for disease in diseases:
        # Cria o caminho: backend/datasets/raw/soybean/asian_rust
        full_path = os.path.join(base_path, plant, disease)
        os.makedirs(full_path, exist_ok=True)
        print(f"✅ Criado: {full_path}")

print("\n✨ Tudo pronto! Pastas organizadas em Inglês.")