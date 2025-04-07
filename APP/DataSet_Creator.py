import sys
sys.path.append("Pakages/DataSetgenPacks")

#"/Users/eduardo/Desktop/GUI_LSTM_FFT/Pakages/DataSetgenPacks"

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

from datetime import datetime, date
import time

### Check if model is created
import os.path as path
import os
from dotenv import load_dotenv
# Cargar variables del archivo .env
load_dotenv()


##DataSet Creator

# import all classes
from Retriver_and_Processor_Dataset import DatasetGenerator



class DL_DataSet(QThread):
    Update_Progress = pyqtSignal(int)
    Update_Progress_String = pyqtSignal(str)
    Update_DataSetCreationStatus = pyqtSignal(bool)
    


    def __init__(self):
        super().__init__()
        #self.Date_Time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.Date_Time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.Path_DataSet = ""
        self.Seed_DataSet_id_FRGN =0
        self.DataSet_id_Just_Created=0
        Api_Key=os.getenv("TU_API_KEY")
        PasswordCaptial=os.getenv("PASSWORDCAPITAL")
        correoCapital= os.getenv("EMAILUSER")
        
        self.dataSet_Gen = DatasetGenerator(Api_Key,PasswordCaptial,correoCapital)
        
    
    def Set_SeedParam(self,val1):
        self.SeedDataSetList=list(val1)
        self.CurrentSeedDataRow=self.SeedDataSetList[0]
            
            
    def Set_Last_DataSet_Crated(self,val):
        self.Last_DataSet_Crated=val
        
    def Set_TypeProcessToDo(self,val):
        self.TypeProcessToDo=val
        
    def Set_DataSetToUpdate(self,val):
        self.DataSetToUpdateId=val
        
    def Set_BackDaysConsideredFFT(self,val):
        self.BackDaysConsideredFFT=val
        
    def Get_DataSetToUpdate(self):
        return self.DataSetToUpdateId
        
    def Get_TypeProcessToDo(self):
        return self.TypeProcessToDo
        
    def Get_NewDataSet_Data(self):
        return self.Date_Time,self.Path_DataSet,self.Seed_DataSet_id_FRGN
    
    def Get_DataSet_id_Just_Created(self):
        return self.DataSet_id_Just_Created
    
    def GetModelCreationStatus(self):
        pass
    
    
    
    def run(self):
        
        self.Update_DataSetCreationStatus.emit(False)
        #self.Date_Time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.Date_Time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        self.Update_Progress_String.emit("Initializing DataSet creation")
        self.Update_Progress.emit(0)
        
        
        self.Seed_DataSet_id_FRGN =self.CurrentSeedDataRow
        if self.TypeProcessToDo=="1":
            self.DataSet_id_Just_Created=self.Last_DataSet_Crated+1
        else:
            self.DataSet_id_Just_Created=self.DataSetToUpdateId
        
        
        StartDay="2010-01-04T00:00:00"
        #EndDate="2001-06-15"
        EndDate=date.today().strftime("%Y-%m-%dT%H:%M:%S")
        
        ObjectiveFilePath=self.ToCreateOrUpdateDataSet(self.DataSet_id_Just_Created,self.SeedDataSetList,StartDay,EndDate,self.TypeProcessToDo)
        self.Path_DataSet = ObjectiveFilePath
        
        #Verify if objective DataSet was created
        if ObjectiveFilePath:
            self.Update_Progress_String.emit("DataSet Succesfully created")
            self.Update_Progress.emit(100)
            time.sleep(3)
            self.Update_Progress_String.emit("Ready to create another DataSet")
            self.Update_Progress.emit(0)
            self.Update_DataSetCreationStatus.emit(True)
        else:
            self.Update_Progress_String.emit("DataSet was not succesfully created")
            self.Update_Progress.emit(95)
            time.sleep(3)
            self.Update_Progress_String.emit("Ready to create another DataSet")
            self.Update_Progress.emit(0)
            self.Update_DataSetCreationStatus.emit(False)
        
        
    
    
    def ToCreateOrUpdateDataSet(self,DataSetId,SeedDataSetlist,dateStart,dateEnd,ProcessToDo):
        print("this is the one: "+str(SeedDataSetlist[1]))
        
        self.Update_Progress_String.emit("Creating DataSet")
        self.Update_Progress.emit(25)
        
        itemName=SeedDataSetlist[1]
        BackDays=int(SeedDataSetlist[2])
        Open_C=SeedDataSetlist[3]
        High_C=SeedDataSetlist[4]
        Low_C=SeedDataSetlist[5]
        Close_C=SeedDataSetlist[6]
        Volume_C=SeedDataSetlist[7]
        Open_FFT_C=SeedDataSetlist[8]
        High_FFT_C=SeedDataSetlist[9]
        Low_FFT_C=SeedDataSetlist[10]
        Close_FFT_C=SeedDataSetlist[11]
        Volum_FFT_C=SeedDataSetlist[12]
        Day_Wk_N_C=SeedDataSetlist[13]
        Day_MonthNDay_C=SeedDataSetlist[14]
        Year_C=SeedDataSetlist[15]
        FFT_Frec=SeedDataSetlist[16]
        UpDown_C=SeedDataSetlist[17]
        Column=SeedDataSetlist[18]
        DevStnd_C=SeedDataSetlist[19]
        MaxBackDist=int(SeedDataSetlist[20])
        BackPeriod=int(SeedDataSetlist[21])
        BollngBand_C=SeedDataSetlist[22]
        
         
        ParentPath= "APP/DataSets/"
        BasePath="{}/Id{}".format(itemName,DataSetId)
        pathTocreated=path.join(ParentPath,BasePath)
        
        Original_Path_Retiving=pathTocreated+"/BaseDataSet.csv"
        Onlyonecolumn=pathTocreated+"/DataSetPopingUp.csv"
        LastOnetwice=pathTocreated+"/DataSet_LastOneTwice.csv"
        DirectionPrice=pathTocreated+"/DataSet_DirePrice.csv"
        DayNumAddedPath=pathTocreated+"/DataSet_DayNum.csv"
        MonthAddedPath=pathTocreated+"/DataSet_month.csv"
        yearAddedPath=pathTocreated+"/DataSet_year.csv"
        UpDoneAddedPath=pathTocreated+"/DataSet_UpDown.csv"
        NormalD_Path=pathTocreated+"/DataSet_DevStnd.csv"
        FFTAddedPath=pathTocreated+"/DataSet_FFTColumns.csv"
        LastPopcolum=pathTocreated+"/DataSet_lastPoppingColums.csv"
        BollingerPath=pathTocreated+"/DataSet_Bollng_bands.csv"
        
        self.Update_Progress_String.emit("DataSet Path created")
        self.Update_Progress.emit(50)
        
        #Verifying if FFT to do
        FFT_ToDo=False
        if Open_FFT_C==1 or High_FFT_C==1 or Low_FFT_C==1 or Close_FFT_C==1 or Volum_FFT_C==1:
            FFT_ToDo=True
        
        #Check is directory exist, otherwise To Create A Directory With Subdirectories
        
        if path.exists(pathTocreated):
            pass
        else:
            os.makedirs(pathTocreated)

        if ProcessToDo=="1": #Create a new
            addToOld=False
            self.dataSet_Gen.RetivingDataPrices(itemName,dateStart, dateEnd,Original_Path_Retiving,Original_Path_Retiving,addToOld)
            self.Update_Progress_String.emit("Base DataSet Created created")
            self.Update_Progress.emit(60)
        elif ProcessToDo=="0": #Create update
            addToOld=True
            self.dataSet_Gen.UpdateToday(itemName,Original_Path_Retiving,addToOld)
            self.Update_Progress_String.emit("Base DataSet Updated")
            self.Update_Progress.emit(60)
        
        #columns to pop up # Solution applying a mask
        Colums_Selection_FFT=[Open_FFT_C,High_FFT_C,Low_FFT_C,Close_FFT_C,Volum_FFT_C] 
        Colums_Selection=[Open_C,High_C,Low_C,Close_C,Volume_C]
        columns=['Open','High','Low','Close','Volume']
        ColumnsToPop=[]
        
        for i in range(0,len(Colums_Selection)):
            print(i)
            if Colums_Selection[i]==0 and Colums_Selection_FFT[i]==0:
                ColumnsToPop.append(columns[i])
        self.dataSet_Gen.PopListdf(ColumnsToPop,Original_Path_Retiving,Onlyonecolumn)
        self.Update_Progress_String.emit("Columns Poped from base dataset")
        self.Update_Progress.emit(65)

        #To add the day of the week 0=monday, 1=tuesday .... 4= friday
        if Day_Wk_N_C==1:
            self.Update_Progress_String.emit("Adding WeeDay columns")
            self.dataSet_Gen.AddColumnWeekDay(Onlyonecolumn, DayNumAddedPath,False)
            self.dataSet_Gen.PopListdf(ColumnsToPop,Original_Path_Retiving,Onlyonecolumn)
            self.Update_Progress_String.emit("WeeDay columns added")
            self.Update_Progress.emit(73)
        else:
            DayNumAddedPath=Onlyonecolumn
        
            
            
        #To add the number*100 Month of the year: january = 100, dicember=1200
        # and Day of the month 1...30 or 1...28 or 1...31
        if Day_MonthNDay_C==1:
            self.Update_Progress_String.emit("Adding Month and month day columns")
            self.dataSet_Gen.AddColumnMothandDay(DayNumAddedPath, MonthAddedPath,False)
            self.Update_Progress_String.emit("Month and month day columns added")
            self.Update_Progress.emit(80)
        else:
            MonthAddedPath=DayNumAddedPath

        #To add the year
        if Year_C==1:
            self.Update_Progress_String.emit("Adding Year column")
            self.dataSet_Gen.AddColumnYear(MonthAddedPath,yearAddedPath)
            self.Update_Progress_String.emit("Year column added")
            self.Update_Progress.emit(85)
        else:
            yearAddedPath=MonthAddedPath
        
        #To Add UpDown
        if UpDown_C==1:
            self.Update_Progress_String.emit("Adding UpDown")
            self.dataSet_Gen.AddUpDown(yearAddedPath,UpDoneAddedPath,Column)
            self.Update_Progress_String.emit("UpDown Added")
            self.Update_Progress.emit(88)
        else:
            UpDoneAddedPath=yearAddedPath
            
        #To add DevStnd
        if DevStnd_C==1:
            self.Update_Progress_String.emit("Addeding Standard deviation ")
            self.dataSet_Gen.Add_normal_distribution(UpDoneAddedPath,NormalD_Path,MaxBackDist,BackPeriod,Column)
            self.Update_Progress_String.emit("Standard deviation Added")
            self.Update_Progress.emit(90)
        else:
            NormalD_Path=UpDoneAddedPath
            
        #To add bollinger bands
        if BollngBand_C==1:
            self.Update_Progress_String.emit("Addeding bollinger bands ")
            self.dataSet_Gen.Add_bollinger_bands(NormalD_Path,BollingerPath,BackPeriod,Column)
            self.Update_Progress_String.emit("bollinger bands Added")
            self.Update_Progress.emit(94)
        else:
            BollingerPath=NormalD_Path

        #Generate new FFT columns
        if FFT_ToDo:
            Colums_Selection_FFT=[Open_FFT_C,High_FFT_C,Low_FFT_C,Close_FFT_C,Volum_FFT_C]
            columns=['Open','High','Low','Close','Volume']
            ColumnsToFFT=[]
            for i in range(0,len(columns)):
                if Colums_Selection_FFT[i]==1:
                    ColumnsToFFT.append(columns[i])

            #backdaysToconsider=self.BackDaysConsideredFFT+1
            backdaysToconsider=BackDays+1
            inicialPath=BollingerPath
            FFTNew_FileData=FFTAddedPath
            frec=self.Convert(FFT_Frec)
            
            
            self.Update_Progress_String.emit("Adding FFT columns columns added")
            self.Update_Progress.emit(95)
            self.dataSet_Gen.getTheLastFFTValue(backdaysToconsider,frec,ColumnsToFFT,inicialPath, FFTNew_FileData)
        
        else:
            FFTNew_FileData=BollingerPath
        
        



        Colums_FFT_Selection=[Open_FFT_C,High_FFT_C,Low_FFT_C,Close_FFT_C,Volum_FFT_C]
        Colums_Selection=[Open_C,High_C,Low_C,Close_C,Volume_C]
        columns=['Open','High','Low','Close','Volume']
        ColumnsToPop=[]
        
        
        self.Update_Progress_String.emit("Popping last columns...")
        for i in range(0,len(Colums_Selection)):
            if Colums_Selection[i]==0 and Colums_FFT_Selection[i]==1:
                ColumnsToPop.append(columns[i])
        self.dataSet_Gen.PopListdf(ColumnsToPop,FFTNew_FileData,LastPopcolum)
        self.Update_Progress_String.emit("Final DataSet Created :)")
        self.Update_Progress.emit(100)
        
        #Return the resulting DataSet
        return LastPopcolum
    
    def Convert(self,string1):
        FinalList=[]
        li = list(string1.split(","))
        for i in li:
            FinalList.append(int(i))
        return FinalList

        