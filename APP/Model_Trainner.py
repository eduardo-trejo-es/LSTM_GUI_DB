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
        self.epoch_Represent_first_Part=20
        self.epoch_Represent_Precent_total=80
        
        
        
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

    def Get_LastLoss(self):
        return self.LastLoss
    
    def Get_LastMean_Squared_error(self):
        return self.LastMean_Squared_error
    
    def Get_LastValLoss(self):
        return self.LastValLoss
    
    def Get_LastValMeanSquared_Error(self):
        return self.LastValMeanSquared_Error
    
    def run(self):
        #is this one the old working trainer versi
        ColumToforcast=self.ColumToforcast
        numEpochs=self.numEpochs
        Model_Path=self.Model_Path
        Data_CSV=self.Data_CSV
        percentageData=self.percentageData
        Np_pasdays=self.Np_pasdays
        
        self.Update_Progress_String.emit("Trainning about to start")
        self.Update_Progress.emit(self.epoch_Represent_first_Part)
        
        print(ColumToforcast)
        print(numEpochs)
        print(Model_Path)
        print(Data_CSV)
        print(percentageData)
        print(Np_pasdays)
        
        # Set the callback function
        self.trainer_model.set_callback(self.update_Epoch)
        
        training_result,self.losses=self.trainer_model.to_train(int(ColumToforcast),int(numEpochs),Model_Path,Data_CSV,int(percentageData),int(Np_pasdays))
        
        #getting the lats value loss
        loss=self.losses["loss"][len(self.losses)-1:].values[0]
        self.LastLoss=loss
        
        #getting the lats value mean_squared_error
        Mean_Squared_error=self.losses["mean_squared_error"][len(self.losses)-1:].values[0]
        self.LastMean_Squared_error=Mean_Squared_error
        
        #getting the lats value val_loss
        ValLoss=self.losses["val_loss"][len(self.losses)-1:].values[0]
        self.LastValLoss=ValLoss
        
        #getting the lats value val_mean_squared_error
        ValMeanSquared_Error=self.losses["val_mean_squared_error"][len(self.losses)-1:].values[0]
        self.LastValMeanSquared_Error=ValMeanSquared_Error
        
        self.Update_Progress_String.emit("Trainning finished")
        self.Update_Progress.emit(100)
        
        
        time.sleep(3)
        self.Update_Progress_String.emit("To do another tranning session")
        self.Update_Progress.emit(0)
        self.Update_TrainningProcssStatus.emit(True)
    
    def update_Epoch(self,epoch): 
        numEpochs=self.numEpochs
        current_Doing_Epoch=int(epoch)+1
        
        CurrenEpochPrecent_and_Already_Done=int(((current_Doing_Epoch*self.epoch_Represent_Precent_total)/int(numEpochs))+self.epoch_Represent_first_Part)
        print("..........................")
        print(type(CurrenEpochPrecent_and_Already_Done))
        self.SetEpochs_done(current_Doing_Epoch)
        
        print("percentage"+str(CurrenEpochPrecent_and_Already_Done))
        self.Update_Progress_String.emit("Trainning in process, last epoch: "+str(epoch) +" of "+str(numEpochs))
        self.Update_Progress.emit(int(CurrenEpochPrecent_and_Already_Done))


        