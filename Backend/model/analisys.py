import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from cleanlab.filter import find_label_issues

if __name__ == '__main__':

    modelo = load_model('model_mobilenet_V1.h5')

    datagen = ImageDataGenerator(rescale=1./255)

    dataset = datagen.flow_from_directory(
    r'D:\Programacao\Python Code\AppDoecas\Backend\datasets\processed\train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

    probabilidades = modelo.predict(dataset, verbose=1, workers=0)
    rotulos_reais = dataset.classes

    print("Shape probabilidades:", probabilidades.shape)
    print("Total imagens:", len(rotulos_reais))
    print("Classes:", dataset.class_indices)

    problemas = find_label_issues(
        labels=rotulos_reais,
        pred_probs=probabilidades,
        return_indices_ranked_by='self_confidence'
    )

    print(f"Total de imagens suspeitas: {len(problemas)}")
    print("Índices das mais suspeitas:", problemas[:20])

    nomes_arquivos = dataset.filenames
    indice_para_classe = {v: k for k, v in dataset.class_indices.items()}

    relatorio = []
    for idx in problemas:
        arquivo = nomes_arquivos[idx]
        rotulo_atual = indice_para_classe[rotulos_reais[idx]]
        prob_max = probabilidades[idx].max()
        classe_sugerida = indice_para_classe[probabilidades[idx].argmax()]

        relatorio.append({
            'indice': idx,
            'arquivo': arquivo,
            'rotulo_atual': rotulo_atual,
            'classe_sugerida': classe_sugerida,
            'confianca_sugestao': round(prob_max, 3)
        })

    df = pd.DataFrame(relatorio)
    df.to_csv('suspeitas_cleanlab.csv', index=False)
    print(df.head(30))

    par_problematico = df[
        (df['rotulo_atual'].isin(['corn_bipolaris_spot', 'corn_southern_rust'])) &
        (df['classe_sugerida'].isin(['corn_bipolaris_spot', 'corn_southern_rust'])) &
        (df['rotulo_atual'] != df['classe_sugerida'])
    ]

    print(f"\nConfusões bipolaris ↔ southern_rust: {len(par_problematico)}")
    print(par_problematico[['arquivo', 'rotulo_atual', 'classe_sugerida', 'confianca_sugestao']])

    par_problematico.to_csv('suspeitas_bipolaris_southern.csv', index=False)