from Trainer_Predicting_Esamble import Model_Trainer
#from Forcaster_Model import Forcast_Data
from Forcaster_Model_DateFromToForcast import Forcast_Data
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


inverseModel=0

if inverseModel:
    Model_Path="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/Model/ModelSigmoid_Tanh/Model_LSTM_FFT_43_sigmoid_Inversed"
    Data_CSV="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/Inversed_direcPrice/CRUDE_OIL_Dataand_FFT_10_50_100.csv"
    percentageData=95
    forcastPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/Forcasts/Focast15_02_2023inversed.csv"
else:
    #Model_Path="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/Model/ModelSigmoid_Tanh/Model_LSTM_FFT_43_PReLU_RealCloseValue"
    Model_Path="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/Model/Models_fewColums/Model_LSTM_CloseDayMonthYearFFT_only900FFT"
    #Model_Path="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/Model/ModelSigmoid_Tanh/Model_LSTM_FFT_43_sigmoid_RightSence"
    #Data_CSV="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Dataand_FFT_10_50_100.csv"
    Data_CSV="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Dataand_FFT_900.csv"
    percentageData=95
    forcastPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/Forcasts/Focast_CloseDayMonthYearFFT90019_02_2023.csv"

trainer_model = Model_Trainer()
forcaster = Forcast_Data(Model_Path,Data_CSV)

#training_result=trainer_model.to_train(Model_Path,Data_CSV,percentageData)
"""
Real_Y_current,Real_Y_Forcast,Real_Y_Close=forcaster.ToForcast(1,"2023-02-08")
print(Real_Y_current)
print(Real_Y_Forcast)
print(Real_Y_Close) 
"""
########## forcasting instuctions below ########

df=pd.read_csv(Data_CSV,index_col=0)

locpercentage=0
ColumnCurrent_Close_Day=[]
Real_Y_current=0
ColumnForcast_Close_Day=[]
Real_Y_Forcast=0
ColumnReal_Close_Day=[]
Real_Y_Close=0
Forcast_Dates=[]
ensambly=[]

indexDates=df.index

locpercentage=int((indexDates.shape[0]*percentageData)/100)

#datefiltredPercentage=indexDates[locpercentage:]
datefiltredPercentage=indexDates[indexDates.shape[0]-200:]
for i in datefiltredPercentage:
    print(i)
    Real_Y_current,Real_Y_Forcast,Real_Y_Close=forcaster.ToForcast(1,str(i))
    ColumnCurrent_Close_Day.append([Real_Y_current])
    ColumnForcast_Close_Day.append([Real_Y_Forcast])
    ColumnReal_Close_Day.append([Real_Y_Close])
    Forcast_Dates.append(str(i))
    
    
    
    #if i == datefiltredPercentage[len(datefiltredPercentage)-2]: break


print(ColumnForcast_Close_Day)
print("---------------------------------------------------")
print(ColumnReal_Close_Day)
ensambly_fin=pd.DataFrame({'Current':ColumnCurrent_Close_Day,'Forcast':ColumnForcast_Close_Day,'Real':ColumnReal_Close_Day})
ensambly_fin['Dates']=Forcast_Dates

plt.plot(ColumnForcast_Close_Day,label='ColumnForcast_Close_Day')
plt.plot(ColumnReal_Close_Day,label='ColumnReal_Close_Day')
    #plt.plot([1,2,3,4])
plt.show()
#np.insert(a, a.shape[1], np.array((10, 10, 10, 10)), 1)
#print(ensambly_np.shape)
#print(ensambly_np.shape)
    # to convert to CSV

ensambly_fin.to_csv(path_or_buf=forcastPath,index=False)