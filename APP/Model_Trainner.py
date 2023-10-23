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
        self.trainer_model = Model_Trainer()
        
    def SetColumToForcast(self,val):
        self.ColumToforcast=val
        
    def SetnumEpochs(self,val):
        self.numEpochs=val
        
    def SetModel_Path(self,val):
        self.Model_Path=val
        
    def SetData_CSV(self,val):
        self.Data_CSV=val
    
    def SetpercentageData(self,val):
        self.percentageData=val
    def SetNp_pasdays(self,val):
        self.Np_pasdays=val
    
    def run(self):
        print("Hello world trainnig Scrip running :)")
        #is this one the old working trainer versi
        ColumToforcast=self.ColumToforcast
        numEpochs=self.numEpochs
        Model_Path=self.Model_Path
        Data_CSV=self.Data_CSV
        percentageData=self.percentageData
        Np_pasdays=self.Np_pasdays
        training_result=self.trainer_model.to_train(ColumToforcast,numEpochs,Model_Path,Data_CSV,percentageData,Np_pasdays)
        