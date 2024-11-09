from cProfile import label
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense, Dropout

from sklearn.metrics import mean_squared_error,mean_absolute_error,explained_variance_score
import math
import mplfinance as mpf

import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.layers.core import Activation

# import sys module
import sys
sys.path.append("/Users/eduardo/Desktop/LSTM_Capital_API_220922/FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/Pakages/DataSetgenPacks")

# import all classes
from Retriver_and_Processor_Dataset import DatasetGenerator

class Forcast_Data:
  def __init__(self,Model_Path):
    self.model = keras.models.load_model(Model_Path)
    
    self.Real_Y_current=""
    self.Forcast_Close=""
    self.Real_Y_Close=""
    self.Forcasted_Date=""
    
    self.dataSet_Gen = DatasetGenerator()
    self.classment_Active=False #to allow UpDown binary forcast some other things were deleted
    
  def ToForcastfrom(self,ColumToforcast,ColumRealYToCompare,dateFromForcast,data_frame_Path,BackDays):
    csvFileName=data_frame_Path
    
  ########     Getting the Data     ######
    #Model_Path=model_Path
    df=pd.read_csv(csvFileName,index_col=0)
    backDaysRef=BackDays
    columToforcast=ColumToforcast
    columRealYToCompare=ColumRealYToCompare
    #Separate dates for future plotting
    Data_dates = df.index
    Data_dates=pd.to_datetime(Data_dates,utc=True)
    Data_dates=Data_dates.tz_localize(None)
    #....... dates .....#
    Dates_To_Use_To_Forcast=Data_dates[Data_dates.get_loc(dateFromForcast)-(backDaysRef-1):Data_dates.get_loc(dateFromForcast)+1]
    print(Dates_To_Use_To_Forcast)
    
    #print(Dates_To_Use_To_Forcast)
    
    Columns_N=df.shape[1]
    
    #Getting the columns name
    cols = list(df)[0:Columns_N]
    
    #New dataframe with only training data
    df_forcasting = df[cols].astype(float)

    #####       Scaling data     #####

    scaler = MinMaxScaler()

    scaler = scaler.fit(df_forcasting)
    DS_raw_scaled = scaler.transform(df_forcasting)
    
    print((DS_raw_scaled.shape))
    print("After delete column to forcast from dataset ")
    DS_raw_scaled=np.delete(DS_raw_scaled, columToforcast, 1)
    print((DS_raw_scaled.shape))
    

    ####    Scaling only the close colum   ####
    print(dateFromForcast)
    print("----------------------------------------------")
    print("\n")
    

    df_forcasting_close=df_forcasting[cols[columToforcast]].to_numpy()

    df_forcasting_close=df_forcasting_close.reshape(len(df_forcasting[cols[columToforcast]].to_numpy()),-1)
    scaler_Close = MinMaxScaler()
    scaler_Close = scaler_Close.fit(df_forcasting_close)
    #scaler_Close=df_forcasting.iloc[:,columToforcast]
    #scaler_Close=scaler_Close.to_numpy()
    #scaler_Close=np.reshape(scaler_Close,(scaler_Close.shape[0],1))

    ####   getting the 120 most present data  ####

    Batch_to_predict=DS_raw_scaled[df.index.get_loc(dateFromForcast)-(backDaysRef-1):df.index.get_loc(dateFromForcast)+1]
    #Batch_Real_Y_NonScaled=df_forcasting[df.index.get_loc(dateFromForcast)-1:df.shape[0]-1]
    Batch_Real_Y_NonScaled=df_forcasting[df.index.get_loc(dateFromForcast)-(backDaysRef-2):df.index.get_loc(dateFromForcast)+2]
    #print("Batch_to_predict_Y_NonScaled: {}".format(Batch_to_predict))
    #print("Batch_Real_Y_NonScaled: {}".format(Batch_Real_Y_NonScaled))
    
    Batch_Real_Y_NonScaled=np.array(Batch_Real_Y_NonScaled)
    #....... databatch .....#
    Batch_to_predict=np.reshape(Batch_to_predict,(1,backDaysRef,Columns_N-1))


    ##########################################
    #           Model Forcasting             #
    ##########################################
    Prediction_Saved=0
    temporalScalingBack=0
    #testingX=np.array(testingX)
    ######    Generating forcast data   ######
    
    
    Prediction_Saved = self.model.predict(Batch_to_predict) #the input is a 120 units of time batch
    print("###--- Pediction generated  ---- ")
    print(type(Prediction_Saved))
    print(Prediction_Saved)
    
    if self.classment_Active:
      ####  Traslating classification results ####
      Prediction_Saved_list=0.
      if Prediction_Saved[0][0] > Prediction_Saved[0][1]:
        Prediction_Saved_list=1.
      else:
        Prediction_Saved_list=0.
      
      Forcast_Close=Prediction_Saved_list

    else:
      #####       Scaling Back     #####
      AllPrediction_DS_scaled_Back=0
      AllPrediction_DS_scaled_Back=scaler_Close.inverse_transform(Prediction_Saved)
      
      
      Forcast_Close=0  
      Forcast_Close = AllPrediction_DS_scaled_Back[0][0]
      
    #######    Generating forcasted dates    #######

    lastTimedate=Dates_To_Use_To_Forcast[Dates_To_Use_To_Forcast.shape[0]-1:]
    lastTimedate=str(lastTimedate[0])

    lastTimedate=pd.Timestamp(str(lastTimedate))

    Forcasted_Dates=""
    
    timestampDate=pd.to_datetime(np.datetime64(lastTimedate))
    DayToAdded=0
    if timestampDate.dayofweek==4:
      DayToAdded=3
    else:
      DayToAdded=1
      
    lastTimedate=np.datetime64(lastTimedate) + np.timedelta64(DayToAdded, 'D')
    Forcasted_Dates=pd.Timestamp(np.datetime64(lastTimedate))
    self.Forcasted_Date=Forcasted_Dates
      
    #####        splitting Real y    #####
    
    
    Real_Y_Close=0
    Real_Y_current=0
    
    #Splitting data  real Y
    #print("The shape of Batch_Real_Y_NonScaled: " + str(Batch_Real_Y_NonScaled.shape))
    try:
      Real_Y_Close=df_forcasting[df.index.get_loc(dateFromForcast)+1:df.index.get_loc(dateFromForcast)+2]
      Real_Y_Close=Real_Y_Close[cols[columRealYToCompare]][0]
    except:
      Real_Y_Close=df_forcasting[df.index.get_loc(dateFromForcast):df.index.get_loc(dateFromForcast)+1]
      Real_Y_Close=Real_Y_Close[cols[columRealYToCompare]][0]
    
    Real_Y_current=df_forcasting[df.index.get_loc(dateFromForcast):df.index.get_loc(dateFromForcast)+1]
    Real_Y_current=Real_Y_current[cols[columToforcast]][0]
    #Real_Y_current=Batch_Real_Y_NonScaled[Batch_Real_Y_NonScaled.shape[0]-1][ColumToforcast]

    self.Real_Y_current=Real_Y_current
    self.Forcast_Close=Forcast_Close
    self.Real_Y_Close=Real_Y_Close
  
  def Get_UnicForcast_Real_Y_current(self):
    return self.Real_Y_current
  def Get_UnicForcast_Forcast_Close(self):
    return self.Forcast_Close
  def Get_UnicForcast_Real_Y_Close(self):
    return self.Real_Y_Close
  
  def Get_Forcasted_Date(self):
    return self.Forcasted_Date
  
  def RecurrentForcasting(self,n,date_from,OriginalSimpleDataSet2ColumnsPath,FFTOriginalFilePath,SimpleDataSet2ColumnsPath):
    #at the firt scan loop I use the base data set then the next I use the
    firstcicle=True
    
    d={}
    indx=[]
    df=pd.DataFrame(data=d,index=indx)
    CurrentCloseForcast=[]
    CurrentCloseDateForcast=[]
    
    #Filepath To generate the dataset files
    Original_Path_Retiving=SimpleDataSet2ColumnsPath
    Onlyonecolumn="/Users/eduardo/Desktop/LSTM_Capital_API_220922/FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/ForcastDataSetGen/CRUDE_OIL_Data_onlyClose.csv"
    DayNumAddedPath="/Users/eduardo/Desktop/LSTM_Capital_API_220922/FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/ForcastDataSetGen/CRUDE_OIL_Dataand_DayNum.csv"
    MonthAddedPath="/Users/eduardo/Desktop/LSTM_Capital_API_220922/FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/ForcastDataSetGen/CRUDE_OIL_Data_And_month.csv"
    yearAddedPath="/Users/eduardo/Desktop/LSTM_Capital_API_220922/FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/ForcastDataSetGen/CRUDE_OIL_Data_And_year.csv"
    FFTAddedPath="/Users/eduardo/Desktop/LSTM_Capital_API_220922/FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/ForcastDataSetGen/CRUDE_OIL_CloseFFT_100.csv"
    
    
    for i in range(0,n):
      if firstcicle == True:
        self.ToForcastfrom(date_from,FFTOriginalFilePath)
        firstcicle=False
        
        
      else:
        print(".............................................")
        
        #To the new Dataset File Path must be added the day 
        #The used to predict is not the same  that is saved
        
        columns=['Open','High','Low','Volume']
        self.dataSet_Gen.PopListdf(columns,Original_Path_Retiving,Onlyonecolumn)
        
        self.dataSet_Gen.AddColumnWeekDay(Onlyonecolumn, DayNumAddedPath,False)

        self.dataSet_Gen.AddColumnMothandDay(DayNumAddedPath, MonthAddedPath,False)

        self.dataSet_Gen.AddColumnYear(MonthAddedPath,yearAddedPath)
        
        Column='Close'
        frec=[100]
        #frec=[10,50,100 
        inicialPath=yearAddedPath
        FFTNew_FileData=FFTAddedPath
        backdaysToconsider=21
        firstDone=False
        for i in frec:
            if firstDone==True:
                inicialPath=FFTAddedPath
                FFTNew_FileData=FFTAddedPath 
            self.dataSet_Gen.getTheLastFFTValue(backdaysToconsider,i,Column,inicialPath, FFTNew_FileData)
            firstDone=True
        
        
        self.ToForcastfrom(CurrentCloseDateForcast,FFTNew_FileData)
        
      
      CurrentCloseForcast.append(self.Get_UnicForcast_Forcast_Close())
      CurrentCloseDateForcast.append(self.Get_Forcasted_Date())
        
      df["Close"]=CurrentCloseForcast
      df["Date"]=CurrentCloseDateForcast
      df_defin=df.set_index('Date')
        
      self.dataSet_Gen.SavingDataset(df_defin,OriginalSimpleDataSet2ColumnsPath, Original_Path_Retiving,True)
      
      
      
      
      
      
        
      
      
    
      
  

  