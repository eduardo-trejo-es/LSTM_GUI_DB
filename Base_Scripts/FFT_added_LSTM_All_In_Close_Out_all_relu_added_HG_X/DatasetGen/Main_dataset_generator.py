from Retriver_and_Processor_Dataset import *

dataSet_Gen= DatasetGenerator()


item_to_use=2
dateStart='2001-01-01'
dateEnd= '2023-02-04'

if item_to_use==0 :
    #######______________ CRUDE_Oil 'CL=F' _____________  ################
    itemName='CL=F'
    Original_Path_Retiving="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Data.csv"
    DayNumAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Dataand_DayNum.csv"
    MonthAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Data_And_month.csv"
    yearAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Data_And_year.csv"
    FFTAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Dataand_FFT_10_50_100.csv"
elif item_to_use==1:
    #######______________ Copper 'GH_F' _____________  ################
    itemName='HG=F'
    Original_Path_Retiving="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Copper_GH_F/Copper_Data.csv"
    DayNumAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Copper_GH_F/Copper_Dataand_DayNum.csv"
    MonthAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Copper_GH_F/Copper_Data_And_month.csv"
    yearAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Copper_GH_F/Copper_Data_And_year.csv"
    FFTAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Copper_GH_F/Copper_Dataand_FFT_10_50_100.csv"
else:
    #######______________ Steel  'X' _____________  ################
    itemName='X'
    Original_Path_Retiving="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Steel_X/Steel_Data.csv"
    DayNumAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Steel_X/Steel_Dataand_DayNum.csv"
    MonthAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Steel_X/Steel_Data_And_month.csv"
    yearAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Steel_X/Steel_Data_And_year.csv"
    FFTAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Steel_X/Steel_Dataand_FFT_10_50_100.csv"


"""
dataSet_Gen.RetivingDataPrices_Yahoo(itemName,dateStart, dateEnd,Original_Path_Retiving,Original_Path_Retiving)

#dataSet_Gen.UpdateToday(Original_Path_Retiving)

dataSet_Gen.AddColumnWeekDay(Original_Path_Retiving, DayNumAddedPath,False)

dataSet_Gen.AddColumnMoth(DayNumAddedPath, MonthAddedPath,False)

dataSet_Gen.AddColumnYear(MonthAddedPath,yearAddedPath)

#Generate new FFT columns done :)



#Column=['Open_CL=F','High_CL=F','Low_CL=F','Close_CL=F','Volume_CL=F','Open_HG=F','High_HG=F','Low_HG=F','Close_HG=F','Volume_HG=F','Open_X','High_X','Low_X','Close_X','Volume_X']
Column=['Open','High','Low','Close','Volume']
frec=[10,50,100]

inicialPath=yearAddedPath
FFTNew_FileData=FFTAddedPath
for i in Column:
    for j in frec:
        if i == Column[0] and j == frec[0]:
            dataSet_Gen.Add_ColumsFourier_Transform(j,i,inicialPath,FFTNew_FileData)
        else:   
            dataSet_Gen.Add_ColumsFourier_Transform(j,i,FFTNew_FileData,FFTNew_FileData)
"""
path_CSV_df=["FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Dataand_FFT_10_50_100.csv",
             "FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Copper_GH_F/Copper_Dataand_FFT_10_50_100.csv",
             "FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Steel_X/Steel_Dataand_FFT_10_50_100.csv"]

combined_path="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/Combined_GH_F_CL_F_X/CombinedGH_F_CL_F_X.csv"
dataSet_Gen.dfCombiner(path_CSV_df,combined_path)


            
            


