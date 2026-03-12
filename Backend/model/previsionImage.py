import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

Class = [
    'corn_bipolaris_spot', 'corn_common_rust', 'corn_ear_rot', 'corn_healthy',
    'corn_northern_leaf_blight', 'corn_southern_rust', 'corn_white_spot',
    'soybean_asian_rust', 'soybean_bacterial_blight', 'soybean_frog_eye_spot',
    'soybean_healthy', 'soybean_target_spot'
]
    
def makeDiagnostic(imgPath):
    print("\ Carregando IA e processando a imagem...")
    model = tf.keras.models.load_model('model_diagnostic_v3.h5')

    img = image.load_img(imgPath, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalização
    img_array = np.expand_dims(img_array, axis=0) # Lote de 1
   
    predict = model.predict(img_array, verbose=0)[0]
    
    pares_doenca_probabilidade = list(zip(Class, predict))
    
    lista_ordenada = sorted(pares_doenca_probabilidade, key=lambda x: x[1], reverse=True)
    
    top_3 = lista_ordenada[:3]

    print("\n" + "="*50)
    print(" RAIO-X DO DIAGNÓSTICO (TOP 3)")
    print("="*50)
    
    for i, (nome_classe, probabilidade) in enumerate(top_3):
        nome_formatado = nome_classe.upper()
        confianca = probabilidade * 100
        
        print(f" {i+1}º: {nome_formatado} ({confianca:.2f}%)")

    print("\n" + "="*45)
    print("  RESULTADO FINAL")
    print("="*45)
    
    vencedor_nome = top_3[0][0].upper()
    vencedor_confianca = top_3[0][1] * 100
    
    print(f" Diagnóstico: {vencedor_nome}")
    print(f" Confiança:   {vencedor_confianca:.2f}%")
    print("="*45 + "\n")

if __name__ == "__main__":
    
    foto_teste = r"D:\Programacao\Python Code\AppDoecas\frogeye-leaf-spot-2.webp"
    
    try:
        makeDiagnostic(foto_teste) 
    except FileNotFoundError:
        print(f"Erro: Não encontrei a imagem '{foto_teste}'.")