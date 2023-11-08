import sys

sys.path.append("/Users/eduardo/Desktop/GUI_LSTM_FFT/Pakages/ForcastingPacks")
from Trainer_Predicting_Esamble import Model_Trainer

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import time

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
    
    def SetEpochs_done(self,val):
        self.Epochs_done=val
    
    def GetEpochs_done(self):
        return self.Epochs_done
        
    def Getlosses(self):
        return self.losses
    
    def run(self):
        print("Hello world trainnig Scrip running :)")
        #is this one the old working trainer versi
        ColumToforcast=self.ColumToforcast
        numEpochs=self.numEpochs
        Model_Path=self.Model_Path
        Data_CSV=self.Data_CSV
        percentageData=self.percentageData
        Np_pasdays=self.Np_pasdays
        
        print(ColumToforcast)
        print(numEpochs)
        print(Model_Path)
        print(Data_CSV)
        print(percentageData)
        print(Np_pasdays)
        training_result,self.losses=self.trainer_model.to_train(int(ColumToforcast),int(numEpochs),Model_Path,Data_CSV,int(percentageData),int(Np_pasdays))
        
        self.Update_Progress_String.emit("Trainning finished")
        self.Update_Progress.emit(100)
        self.SetEpochs_done(numEpochs)
        time.sleep(3)
        self.Update_Progress_String.emit("Ready to create another DataSet")
        self.Update_Progress.emit(0)
        self.Update_TrainningProcssStatus.emit(True)


        