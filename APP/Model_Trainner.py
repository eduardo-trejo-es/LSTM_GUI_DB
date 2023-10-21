import sys

sys.path.append("/Users/eduardo/Desktop/GUI_LSTM_FFT/Pakages/ForcastingPacks")
from Trainer_Predicting_Esamble import Model_Trainer

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


from PyQt5.QtCore import *


class DL_Trainner(QThread):
    Update_Progress = pyqtSignal(int)
    Update_Progress_String = pyqtSignal(str)
    Update_TrainningProcssStatus = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
    
    def run(self):
        print("Hello world trainnig Scrip running :)")