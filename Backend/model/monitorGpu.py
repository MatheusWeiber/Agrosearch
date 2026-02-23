import pynvml
from tensorflow.keras.callbacks import Callback

class GPUMonitor(Callback):
    def __init__(self):
        # Inicializa a conexão com a placa
        pynvml.nvmlInit()
        self.handle = pynvml.nvmlDeviceGetHandleByIndex(0) # Pega a GPU 0 (a principal)

    def on_epoch_end(self, epoch, logs=None):
        # Pega as informações
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(self.handle)
        util = pynvml.nvmlDeviceGetUtilizationRates(self.handle)
        temp = pynvml.nvmlDeviceGetTemperature(self.handle, pynvml.NVML_TEMPERATURE_GPU)
        
        # Converte bytes para MegaBytes
        mem_used = mem_info.used / 1024**2
        mem_total = mem_info.total / 1024**2

        print(f"\n [GPU Status] Carga: {util.gpu}% | Memória: {mem_used:.0f}/{mem_total:.0f} MB | Temp: {temp}°C")

    def on_train_end(self, logs=None):
        # Fecha a conexão ao terminar
        pynvml.nvmlShutdown()