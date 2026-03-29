import tensorflow as tf
import numpy as np
import time
import cleanlab as cl
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.utils import compute_class_weight
from monitorGpu import GPUMonitor


print('Iniciando configuracoes...')
meu_monitor = GPUMonitor()

datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,           # Gira a imagem levemente
    width_shift_range=0.2,       # Move para os lados
    height_shift_range=0.2,      # Move para cima/baixo
    shear_range=0.2,             # Deforma
    zoom_range=0.3,              # Aproxima
    horizontal_flip=True,        # Espelha horizontalmente
    vertical_flip=True,          # Espelha verticalmente
    brightness_range=[0.6, 1.4], # Varia o brilho simulando diferentes iluminações
    channel_shift_range=30,      # Varia as cores simulando diferentes câmeras
    fill_mode='nearest'          # Preenche espaços vazios após transformações
)
train_path = '../datasets/processed/train' 
val_path = '../datasets/processed/val'
test_path = '../datasets/processed/test'

print('Carregando geradores de imagens...')
inicio1 = time.time()
# Treino
train_generator = datagen.flow_from_directory(
    train_path,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Validacao
val_generator = datagen.flow_from_directory(
    val_path,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Teste
test_generator = datagen.flow_from_directory(
    test_path,  
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False 
)
fim1 = time.time()
print(f"Tempo de treinamento: {(fim1 - inicio1)/60:.2f} minutos")
# Captura o numero de classes automaticamente
num_classes = len(train_generator.class_indices)
print(f"Detectadas {num_classes} classes.")

# MODELO
print('Construindo o modelo...')
model = Sequential()
# Conv2d: Camada de convolução 2D
# MaxPooling2D: Camada de pooling 2D
# Flatten: Camada de flattening (transforma a saída em um vetor)
# Dense: Camada densa (transforma a saída em um vetor)
# Softmax: Camada de saída softmax (transforma a saída em uma probabilidade)
# Camadas de Convolucao
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(64, (3, 3,), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(128, (3, 3,), activation='relu'))
model.add(MaxPooling2D((2, 2)))

# Camadas Densas
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.3))


model.add(Dense(num_classes, activation='softmax'))

print('Compilando modelo...')

optimizer = Adam(learning_rate=0.0001)

model.compile(
    optimizer='adam',                  
    loss='categorical_crossentropy',   
    metrics=['accuracy']              
)

model.summary()

# calcular pesos 
print("Calculando pesos das classes...")
cls_train = train_generator.classes
classes = np.unique(cls_train)
weights = compute_class_weight(class_weight='balanced', classes=classes, y=cls_train)
class_weights_dict = dict(zip(classes, weights))
print("Pesos:", class_weights_dict)

# treino
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

print('Iniciando treinamento (Fit)...')

inicio = time.time()
meu_monitor = GPUMonitor()

history = model.fit(
    train_generator,
    epochs=150,
    validation_data=val_generator,
    callbacks=[early_stop],
    class_weight=class_weights_dict
)

fim = time.time()
print(f"Tempo de treinamento: {(fim - inicio)/60:.2f} minutos")

#fim
print("Salvando arquivos...")
model.save("model_diagnostic_v3.h5")
np.save('historico_treino.npy', history.history)

print("Avaliando no Test Set final...")
test_loss, test_acc = model.evaluate(test_generator)
print(f"Acuracia Final no Teste: {test_acc*100:.2f}%")

print("Tudo pronto! Agora rode o arquivo 'gerar_graficos.py' para ver os resultados visuais.")