import tensorflow as tf
import numpy as np
import time
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from sklearn.utils import compute_class_weight
from monitorGpu import GPUMonitor
from tensorflow.keras.applications import MobileNetV2

print(' Iniciando Transfer Learning com MobileNetV2...')

# --- 1. PREPARAR OS DADOS ---
# DATAGEN DE TREINO (Com distorção/Augmentation)
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

# DATAGEN DE VALIDAÇÃO/TESTE (Limpo, só normalizado)
val_test_datagen = ImageDataGenerator(rescale=1./255)

train_path = '../datasets/processed/train' 
val_path = '../datasets/processed/val'
test_path = '../datasets/processed/test'

print(' Carregando imagens...')

# Treino (Usa o datagen bagunçado)
train_generator = train_datagen.flow_from_directory(
    train_path,
    target_size=(224, 224),
    batch_size=32, # MobileNet aguenta batches maiores
    class_mode='categorical'
)

# Validação (Usa o datagen limpo)
val_generator = val_test_datagen.flow_from_directory(
    val_path,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Teste (Usa o datagen limpo e SEM shuffle)
test_generator = val_test_datagen.flow_from_directory(
    test_path,  
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False 
)

num_classes = len(train_generator.class_indices)
print(f"Detectadas {num_classes} classes.")

# --- 2. DEFINIR O MODELO (MobileNetV2) ---
print('Baixando o cérebro do MobileNetV2...')

# Baixa o modelo SEM a cabeça (include_top=False)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False # Congela os pesos (não treina o que ele já sabe)

print('Montando a nova cabeça do modelo...')
model = Sequential([
    base_model,                     # 1. O cérebro do Google
    GlobalAveragePooling2D(),       # 2. Resume as caracteristicas
    Dense(128, activation='relu'),  # 3. Aprende sobre SUAS doenças
    Dropout(0.5),                   # 4. Evita viciar
    Dense(num_classes, activation='softmax') # 5. Resposta final
])


print('Compilando...')
# Learning rate bem baixo para não estragar o pré-treino
optimizer = Adam(learning_rate=0.0001)

model.compile(
    optimizer=optimizer, # Usa a variavel que criamos, não a string 'adam'
    loss='categorical_crossentropy',   
    metrics=['accuracy']              
)

model.summary()

# --- 3. CALCULAR PESOS ---
print("Calculando pesos...")
cls_train = train_generator.classes
classes = np.unique(cls_train)
weights = compute_class_weight(class_weight='balanced', classes=classes, y=cls_train)
class_weights_dict = dict(zip(classes, weights))

# --- 4. TREINAMENTO ---
# Patience maior (10) porque Transfer Learning as vezes demora a engrenar
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
meu_monitor = GPUMonitor() # Monitor da GPU

print(' Iniciando treinamento...')
inicio = time.time()

history = model.fit(
    train_generator,
    epochs=50, # Transfer Learning aprende rápido, 50 costuma sobrar
    validation_data=val_generator,
    callbacks=[early_stop, meu_monitor], # Adicionei o monitor aqui
    class_weight=class_weights_dict
)

fim = time.time()
print(f"Tempo de treinamento: {(fim - inicio)/60:.2f} minutos")

# --- 5. FINALIZAÇÃO ---
print("Salvando modelo Transfer Learning...")
model.save("model_mobilenet_V1.h5") # Nome diferente para não sobrescrever o antigo
np.save('historico_mobilenet.npy', history.history)

print("Avaliando no Test Set...")
test_loss, test_acc = model.evaluate(test_generator)
print(f"Acurácia Final (MobileNet): {test_acc*100:.2f}%")