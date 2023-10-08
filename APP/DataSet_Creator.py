
from PyQt5.QtCore import *

###   Model creation
from tensorflow.keras.layers import Dense, Activation 
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense, Dropout
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.layers.core import Activation

from datetime import datetime
import time

### Check if model is created
import os.path as path

class DL_DataSet(QThread):
    Update_Progress = pyqtSignal(int)
    Update_Progress_String = pyqtSignal(str)
    Update_DataSetCreationStatus = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.Date_Time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.Path_DataSet = ""
        self.Seed_DataSet_id_FRGN =0
        self.DataSet_id_Just_Created=0
    
    def Set_SeedParam(self,val_0,val_1,val_2,val_3,val_4,val_5,val_6,val_7,val_8,
                      val_9,val_10,val_11,val_12,val_13,val_14,val_15,val_16,val_17):
        self.CurrentSeedDataRow = val_0
        self.Item = val_1
        self.BackDays = val_2
        self.Open_C = val_3
        self.High_C = val_4
        self.Low_C = val_5
        self.Close_C = val_6
        self.Volume_C = val_7
        self.Open_FFT_C = val_8
        self.High_FFT_C = val_9
        self.Low_FFT_C = val_10
        self.Close_FFT_C = val_11
        self.Volum_FFT_C  = val_12
        self.Day_Wk_N_C  = val_13
        self.Month_N_C = val_14
        self.Day_Month_C = val_15
        self.Year_C = val_16
        self.FFT_Frec = val_17
    
    def Set_Last_DataSet_Crated(self,val):
        self.Last_DataSet_Crated=val
        
    def Get_NewDataSet_Data(self):
        return self.Date_Time,self.Path_DataSet,self.Seed_DataSet_id_FRGN
    
    def Get_DataSet_id_Just_Created(self):
        return self.DataSet_id_Just_Created
    
    def GetModelCreationStatus(self):
        pass
    
    def run(self):
        
        self.Update_DataSetCreationStatus.emit(False)
        self.Date_Time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.Path_DataSet = "DATASET_PATH/TEST"
        self.Seed_DataSet_id_FRGN =self.CurrentSeedDataRow
        self.DataSet_id_Just_Created=self.Last_DataSet_Crated+1
        
        self.Update_DataSetCreationStatus.emit(True)