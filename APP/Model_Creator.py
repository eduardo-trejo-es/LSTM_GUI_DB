
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

import time


class DL_Model(QThread):
    """RetrivingResult_Progress = pyqtSignal(int)
    ReadyToSend_Progress = pyqtSignal(int)
    Update_Progress = pyqtSignal(int)
    Update_Progress_String = pyqtSignal(str)"""
    Update_ModelCreationStatus = pyqtSignal(bool)
    
    
    
    def __init__(self):
        super().__init__()
        keras.backend.clear_session()  # Reseteo sencillo
        ### Model Data ###
        self.date_Time=""
        self.Path_Model=""
        self.N_epochs_Done=0
        self.DataSet_id_FRGN=0
        self.ModelCreationStatus=False
        
    def Set_SeedParam(self,val_0,val_1,val_2,val_3,val_4,val_5,val_6,val_7):#---------Layes are created
        ### Data Seed ####
        self.Seed_Data_id_FRGN=val_0
        self.LSTM1_Units=val_1
        self.LSTM2_Units=val_2
        self.LryDcoeff=val_3
        self.Lyr_Dns=val_4
        self.Lyr_Dn_Rgzr=val_5
        self.OptAdam_Co=val_6
        self.Colums=val_7
        
        
        
    def Get_NewModelData(self):
        return self.date_Time,self.Path_Model,self.N_epochs_Done,self.Seed_Data_id_FRGN,self.DataSet_id_FRGN
    
    def GetModelCreationStatus(self):
        return self.ModelCreationStatus
    
    def Set_Last_model_Crated(self,val):
        self.last_model_Created_N=val
        
        
        
    def run(self):
        self.Update_ModelCreationStatus.emit(False)
        time.sleep(5)
        #self.Update_Progress.emit(self.progess)
        
        ### Model Data ###
        self.date_Time="octube1"
        self.Path_Model="path/2"
        self.N_epochs_Done=0
        #SeedData is set at Set_SeedParam
        self.DataSet_id_FRGN=0
        last_model_Created_N=int(self.last_model_Created_N)+1
        
        #Note work: to know the next modelid works, this will be used to set the path model name
        #would be grate if I can test this predict next model id when is empty
        # Whats next: set the parameters and finally create the model :D
        
        print("the next model ID will be: " +str(last_model_Created_N))
        
        self.Update_ModelCreationStatus.emit(True)
        
        """n_future = 1   # Number of units(day, min, hour, etc..) we want to look into the future based on the past days.
        n_past =5
        OneColum=False


        if OneColum:
            Columns_N=7
            modelPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/OnlyCloseColum/Model/Models_fewColums/Model_LSTM_DayMonth5BackDlastFFTCloseValum150FFT300units1e-6_17Aug2023.keras"
        else:
            #in testing modelPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/High_Low_Close/Model/Models_fewColums/Model_LSTM_DayMonth5BackDlastFFTCloseValum150FFT300units1e-6_17Aug2023.keras"
            modelPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/High_Low_Close/Model/Models_fewColums/Model_LSTM_fft150_11BackDay.keras"
            
            Columns_N=11

        inputs=keras.Input(shape=(n_past,Columns_N))

        #LSTM_Layer1=keras.layers.LSTM(n_past, input_shape=(n_past,Columns_N), return_sequences=True,activation='PReLU')(inputs)
        LSTM_Layer1=keras.layers.LSTM(50, input_shape=(n_past,Columns_N), return_sequences=True,activation='PReLU')(inputs)

        #Dropout_layer2=keras.layers.Dropout(0.5)(LSTM_Layer1)# modify
        #x=Dropout_layer1=keras.layers.Dropout(0.2)(x)
        LSTM_Layer2=keras.layers.LSTM(100, return_sequences=False,activation='PReLU')(LSTM_Layer1)

        Dropout_layer3=keras.layers.Dropout(0.2)(LSTM_Layer2)# modify

        #---------------------------Outputs
        #dense=keras.layers.Dense(1,kernel_regularizer=tf.keras.regularizers.L1L2(l1=0.00001, l2=0.00001))(Dropout_layer3)# L1 + L2 penalties
        #dense=keras.layers.Dense(1)(Dropout_layer3)
        dense=keras.layers.Dense(1,kernel_regularizer=tf.keras.regularizers.L2(0.001))(Dropout_layer3)

        #-------Layers outputs are linked
        outputs=dense

        #-----The model it's created
        outputArray=[outputs]

        model=keras.Model(inputs=inputs, outputs=outputArray, name='Prices_Forcasting_LSTM_FFT')
        #model=keras.Model(inputs=[inputs,None], outputs=[outputs,outputs2,outputs3,outputs4,outputs5,outputs6], name='Prices_Prediction')
        #keras.utils.plot_model(model, "my_first_model_with_shape_info.png", show_shapes=True)


        #------------------- Loss and optimizer ----------------------------------------
        #got to ensure MeanAbsoluteError it's the good one for our data
        loss = keras.losses.MeanSquaredError(reduction="auto", name="mean_squared_error")

        #optim=keras.optimizers.Adam(1e-3)
        optim=keras.optimizers.Adam(1e-6)
        Metrics=["mean_squared_error"]

        losses={
            "dense": loss
        }

        #model.compile(loss=losses, optimizer=optim, metrics=Metrics)
        model.compile(loss=losses, optimizer=optim,metrics=Metrics)
        print(model.summary())

        #tf.keras.utils.plot_model(model, "FFT_added_LSTM/ModelGen/Model/Model_LSTM_31_FFT.png", show_shapes=True)


        model.save(modelPath,save_format="keras")"""