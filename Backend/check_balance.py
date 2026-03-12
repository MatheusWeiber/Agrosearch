import os

dataset_path = os.path.join("backend", "datasets", "raw")

print(f"RELATÓRIO DE DADOS: {dataset_path}\n")
print(f"{'CULTURA':<10} | {'CLASSE / DOENÇA':<25} | {'QTD IMAGENS'}")
print("-" * 55)

total_geral = 0

# Verifica se a pasta existe
if not os.path.exists(dataset_path):
    print("Erro: Pasta de datasets não encontrada.")
else:
    # Varre as culturas dentro do dataset
    for cultura in os.listdir(dataset_path):
        cultura_path = os.path.join(dataset_path, cultura)
        
        if os.path.isdir(cultura_path):
            # Varre as doenças dentro da cultura
            for classe in os.listdir(cultura_path):
                classe_path = os.path.join(cultura_path, classe)
                
                if os.path.isdir(classe_path):
                    # Conta quantos arquivos tem na pasta (ignorando arquivos ocultos)
                    qtd = len([f for f in os.listdir(classe_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
                    
                    print(f"{cultura:<10} | {classe:<25} | {qtd}")
                    total_geral += qtd

print("-" * 55)
print(f"TOTAL GERAL: {total_geral} imagens")
