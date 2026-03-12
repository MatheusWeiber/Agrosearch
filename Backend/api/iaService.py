import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
import io


# Os dois pontos (..) fazem o Python voltar uma pasta e entrar na pasta 'model'
diagnosticModel = tf.keras.models.load_model('../model/model_diagnostic_V3.h5')

classes = [
    'corn_bipolaris_spot', 'corn_common_rust', 'corn_ear_rot', 'corn_healthy',
    'corn_northern_leaf_blight', 'corn_southern_rust', 'corn_white_spot',
    'soybean_asian_rust', 'soybean_bacterial_blight', 'soybean_frog_eye_spot',
    'soybean_healthy', 'soybean_target_spot'
]

def processAndDiagnose(imageBytesContent):
    
    img = Image.open(io.BytesIO(imageBytesContent))
    
    resizedImg = img.resize((224, 224))
    imgArray = image.img_to_array(resizedImg)
    imgArray = imgArray / 255.0  
    imgArray = np.expand_dims(imgArray, axis=0) 
    
    rawPrediction = diagnosticModel.predict(imgArray, verbose=0)
    predictList = rawPrediction.flatten()
    
    pairs = list(zip(classes, predictList))
    sortedList = sorted(pairs, key=lambda x: x[1], reverse=True)
    winner = sortedList[0]
    
    return {
        "diagnostic": winner[0].upper(),
        "confidence": round(winner[1] * 100, 2)
    }