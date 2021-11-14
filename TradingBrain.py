from tensorflow.keras.models import Model
from deepevolution import wrap_keras

wrap_keras()


class TradingBrain(Model):
    def __init__(self):
        super.__init__()

