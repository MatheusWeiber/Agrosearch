import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, classification_report

# --- CONFIGURACOES GERAIS ---
HISTORY_PATH = 'historico_treino.npy'
MODEL_PATH = 'model_mobilenet_V1.h5'
TEST_DIR = '../datasets/processed/test' # Verifique se o caminho esta correto
IMG_SIZE = (224, 224)

def plotar_evolucao_treino():
    print("Gerando graficos de evolucao (Acuracia e Loss)...")
    
    try:
        # allow_pickle=True e necessario para carregar o dicionario
        history = np.load(HISTORY_PATH, allow_pickle=True).item()
    except FileNotFoundError:
        print(f"Aviso: Arquivo '{HISTORY_PATH}' nao encontrado. Pulei os graficos de evolucao.")
        return

    # Extrai dados
    acc = history['accuracy']
    val_acc = history['val_accuracy']
    loss = history['loss']
    val_loss = history['val_loss']
    epochs_range = range(len(acc))

    # Cria a figura
    plt.figure(figsize=(12, 5))

    # Grafico 1: Acuracia
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Treino (Estudo)')
    plt.plot(epochs_range, val_acc, label='Validacao (Prova)', linestyle='--')
    plt.legend(loc='lower right')
    plt.title('Evolucao da Acuracia')
    plt.xlabel('Epocas')
    plt.ylabel('Acerto (0-1)')
    plt.grid(True, alpha=0.3)

    # Grafico 2: Erro (Loss)
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Treino (Estudo)')
    plt.plot(epochs_range, val_loss, label='Validacao (Prova)', linestyle='--')
    plt.legend(loc='upper right')
    plt.title('Evolucao do Erro (Loss)')
    plt.xlabel('Epocas')
    plt.ylabel('Erro')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('grafico_performance.png', dpi=300)
    print("Grafico salvo como 'grafico_performance.png'")
    plt.show()

def plotar_matriz_confusao():
    print("\nGerando Matriz de Confusao (Isso usa o modelo para prever o Teste)...")

    # 1. Verifica arquivos
    if not os.path.exists(MODEL_PATH):
        print(f"Erro: Modelo '{MODEL_PATH}' nao encontrado.")
        return
    if not os.path.exists(TEST_DIR):
        print(f"Erro: Pasta de teste '{TEST_DIR}' nao encontrada. Rode 'criar_teste.py'.")
        return

    # 2. Carrega Modelo e Dados
    model = tf.keras.models.load_model(MODEL_PATH)
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=IMG_SIZE,
        batch_size=32,
        class_mode='categorical',
        shuffle=False # IMPORTANTE: False para nao baguncar a ordem
    )

    # 3. Previsao
    print("Calculando previsoes...")
    predictions = model.predict(test_generator)
    y_pred = np.argmax(predictions, axis=1)
    y_true = test_generator.classes
    class_names = list(test_generator.class_indices.keys())

    # 4. Plotagem
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    
    plt.ylabel('Verdadeiro')
    plt.xlabel('Predito pela IA')
    plt.title('Matriz de Confusao')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('grafico_matriz_confusao.png', dpi=300)
    print("Matriz salva como 'grafico_matriz_confusao.png'")
    
    # 5. Imprime relatorio no terminal tambem
    print("\nRelatorio de Metricas:")
    print(classification_report(y_true, y_pred, target_names=class_names))
    plt.show()

# --- BLOCO PRINCIPAL ---
if __name__ == "__main__":
    # Chama as duas funcoes em sequencia
    plotar_evolucao_treino()
    plotar_matriz_confusao()