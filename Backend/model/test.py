import tensorflow as tf
print("Versão do TF:", tf.__version__)
gpus = tf.config.list_physical_devices('GPU')
print("GPUs detectadas:", gpus)

if not gpus:
    print("❌ O TensorFlow NÃO está vendo sua RTX 3060. Ele está usando a CPU.")
else:
    print(f"✅ Sucesso! Encontrei: {gpus}")