import sys
sys.path.append("/Users/eduardo/Desktop/LSTM_Capital_API_220922/FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/Pakages/DataSetgenPacks")
sys.path.append("/Users/eduardo/Desktop/LSTM_Capital_API_220922/FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/Pakages/Model")
from Trainer_Predicting_Esamble import Model_Trainer
#from Forcaster_Model import Forcast_Data
from Forcaster_Model_DateFromToForcast import Forcast_Data

from Model_Creation import


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


inverseModel=0
OneColum=True

if OneColum:
    #Model_Path="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/Model/Models_fewColums/Model_LSTM_DayMonth20BackDlastFFTCloseValum100FFT"
    Model_Path="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/OnlyCloseColum/Model/Models_fewColums/Model_LSTM_DayMonth5BackDlastFFTCloseValum150FFT400units1e-6"
    Data_CSV="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/OnlyCloseColum/CRUDE_OIL_CloseFFT_150_5Backdys.csv"
    all_colums_Data_CSV="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/OnlyCloseColum/CRUDE_OIL_Data.csv"
    percentageData=100
    forcastPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/OnlyCloseColum/Forcasts/Focast_CloseDayMonth5backdayslastFFT150_300unit6training_20_05_2023.csv"
else:
    Model_Path="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/High_Low_Close/Model/Models_fewColums/Model_LSTM_DayMonth5BackDlastFFTCloseValum150FFT400units1e-6"
    Data_CSV="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/High_Low_Close/CRUDE_OIL_CloseFFT_150_5Backdys.csv"
    all_colums_Data_CSV="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/High_Low_Close/CRUDE_OIL_Data.csv"
    forcastPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/High_Low_Close/Forcasts/Focast_CloseDayMonth5backdayslastFFT150_300unit6training_20_05_2023.csv"
    percentageData=100
    

trainer_model = Model_Trainer()
forcaster =Forcast_Data(Model_Path)

#is this one the old working trainer version
#training_result=trainer_model.to_train(True,100,Model_Path,Data_CSV,percentageData,5)
# this last one was 6 of 6
#
date_from="2023-03-24 00:00:00"
date_from2="2023-03-23 00:00:00"
NewDataSetForcasts="/Users/eduardo/Desktop/LSTM_Capital_API_220922/FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/ForcastDataSetGen/CRUDE_OIL_DataNewDataSetForcasted.csv"

#This method returns the the last prediction made of the n asked forcasted.
#Also during process a new csv data file is generated, it contains the whole real data + the appended n forcasted data
#This is the new instance function : forcaster.RecurrentForcasting(3,date_from,SimpleDataSet2ColumnsPath,Data_CSV,NewDataSetForcasts)

#training_result=trainer_model.to_train(Model_Path,Data_CSV,percentageData)
"""
Real_Y_current,Real_Y_Forcast,Real_Y_Close=forcaster.ToForcast(1,"2023-02-27")
print(Real_Y_current)
print(Real_Y_Forcast)
print(Real_Y_Close) 
"""
########## forcasting instuctions below ########


saveAllandforcast=pd.DataFrame({})
fd_ColumnForcast_Close_Day=pd.DataFrame({})
all_df=pd.read_csv(all_colums_Data_CSV,index_col=0)

df=pd.read_csv(Data_CSV,index_col=0)
backdaysConsidered=5


backdaysConsideredToBForcasted=200
locpercentage=0
ColumnCurrent_Close_Day=[]
Real_Y_current=0
ColumnForcast_Close_Day=[]
Real_Y_Forcast=0
ColumnReal_Close_Day=[]
Real_Y_Close=0

forcastedDate=""
Columnforcasteddate=[]
Forcast_Dates=[]
Forcast_Dates_toshow=[]

ensambly=[]

indexDates=df.index

locpercentage=int((indexDates.shape[0]*percentageData)/100)

#datefiltredPercentage=indexDates[locpercentage:]
datefiltredPercentage=indexDates[indexDates.shape[0]-backdaysConsideredToBForcasted:]
for i in datefiltredPercentage:
    forcaster.ToForcastfrom(True,str(i),Data_CSV,backdaysConsidered)
    Real_Y_current=forcaster.Get_UnicForcast_Real_Y_current()
    Real_Y_Forcast=forcaster.Get_UnicForcast_Forcast_Close()
    Real_Y_Close=forcaster.Get_UnicForcast_Real_Y_Close()
    forcastedDate=forcaster.Get_Forcasted_Date()
    ColumnCurrent_Close_Day.append(Real_Y_current)
    ColumnForcast_Close_Day.append(Real_Y_Forcast)
    ColumnReal_Close_Day.append(Real_Y_Close)
    Columnforcasteddate.append(str(forcastedDate))
    Forcast_Dates.append(i)
    
    #if i == datefiltredPercentage[len(datefiltredPercentage)-2]: break
Forcast_Dates_toshow=Forcast_Dates

print(ColumnForcast_Close_Day)
print("---------------------------------------------------")
print(ColumnReal_Close_Day)


### Below df only has close forcast data and dates forcast data
fd_ColumnForcast_Close_Day=pd.DataFrame({'Forcast':ColumnForcast_Close_Day})
#fd_ColumnForcast_Close_Day=pd.DataFrame({'Forcast':ColumnForcast_Close_Day,'ForcastDateTShow':Forcast_Dates_toshow})
fd_ColumnForcast_Close_Day['Dates']=Forcast_Dates
fd_ColumnForcast_Close_Day=fd_ColumnForcast_Close_Day.set_index('Dates')

### Below df has all origianl colums and dates
Allandforcast=all_df[all_df.shape[0]-backdaysConsideredToBForcasted:]

frames = [Allandforcast, fd_ColumnForcast_Close_Day]

Final_Allandforcast = pd.concat(frames,axis=1)
print(Final_Allandforcast)

print(type(ColumnForcast_Close_Day))
print(type(ColumnReal_Close_Day))
plt.plot(ColumnForcast_Close_Day,label='ColumnForcast_Close_Day',color='orange', marker='o')
plt.plot(ColumnReal_Close_Day,label='ColumnReal_Close_Day',color='green', marker='*')
    #plt.plot([1,2,3,4])
plt.show()
#np.insert(a, a.shape[1], np.array((10, 10, 10, 10)), 1)
#print(ensambly_np.shape)
#print(ensambly_np.shape)
    # to convert to CSV

Final_Allandforcast.to_csv(path_or_buf=forcastPath,index=True)
