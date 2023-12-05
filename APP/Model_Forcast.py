import sys
sys.path.append("FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/Pakages/ForcastingPacks")
#from Forcaster_Model import Forcast_Data
from Forcaster_Model_DateFromToForcast import Forcast_Data
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#To get date
from datetime import datetime
import time

from PyQt5.QtCore import *


class DL_Forcast(QThread):
    Update_Progress = pyqtSignal(int)
    Update_Progress_String = pyqtSignal(str)
    Update_ForcastingProcsStatus = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        #self.forcaster =Forcast_Data(Model_Path)
        self.Total_Movement_Right=0
        self.Total_Movement_Right_Per100=0
        self.Total_Diff_Mag_earned=0
        self.Total_Diff_earned_Per100=0
        self.Total_Diff_Mag_lose=0
        self.Total_Diff_lose_Per100=0
        self.Total_Mag_Mvmnts=0
        self.Real_Mag_earned=0
        self.Real_earned_Per100=0
        self.Real_earned_Per100=0
        self.FirstPercentageAbout_toStartForcast=20
        self.Forcasting_Represent_Precent_total=80
        
    def Set_ColumToforcast(self,val):
        self.ColumToforcast=val
        
    def Set_ColumRealYToCompare(self,val):
        self.ColumRealYToCompare=val
        
    def Set_dateFromForcast(self,val):
        self.dateFromForcast=val
        
    def Set_data_frame_Path(self,val):
        self.data_frame_Path=val
    
    def Set_BackDays(self,val):
        self.BackDays=val
        
    def Set_backdaysConsideredToBForcasted(self,val):
        self.backdaysConsideredToBForcasted=val
        #ColumToforcast, ColumRealYToCompare, dateFromForcast, data_frame_Path, BackDays
        
    def Set_all_colums_Data_CSV(self,val):
        self.all_colums_Data_CSV=val
    
    def Set_percentageData(self, val):
        self.percentageData=val
        
    def Set_FFtUsedQ(self,val):
        self.FFtUsedQ=val
    
    def Set_forcastPath(self,val):
        self.forcastPath=val
    
    def Set_ModelPath(self,val):
        self.Model_Path=val
        
    def Set_Model_id_Used(self,val):
        self.Model_Id_Used=val
    
    def Set_TrendImagePath(self,val):
        self.ImageTrendPath=val
        
    def Get_ColumForcast(self):       
        return self.ColumnForcast
    
    def Get_ColumReal(self):
        return self.ColumReal
    
    def Get_NewForcastingData(self):
        return (self.date_Time,self.Total_Movement_Right,self.Total_Movement_Right_Per100,
                self.Rows_Considered,self.Total_Diff_Mag_earned,self.Total_Diff_earned_Per100,
                self.Total_Diff_Mag_lose,self.Total_Diff_lose_Per100,self.Total_Mag_Mvmnts,
                self.Real_Mag_earned,self.Real_earned_Per100,self.Real_earned_Per100,self.Model_id_FRGN)
        
    def Get_TrendImageForcast(self):
        return self.ImageTrendPath
    
    def run(self):
        print("Forcast thread running")
        self.forcaster = Forcast_Data(self.Model_Path)

        ########## forcasting instuctions below #######
        Data_CSV=self.data_frame_Path
        all_colums_Data_CSV= self.all_colums_Data_CSV# Need To add to Table_Original or just determinate
        backdaysConsideredToBForcasted=int(self.backdaysConsideredToBForcasted)
        backdaysConsidered=int(self.BackDays)
        ColumToForcast=int(self.ColumToforcast)
        percentageData=int(self.percentageData)
        FFtUsedQ=self.FFtUsedQ
        
        saveAllandforcast=pd.DataFrame({})
        fd_ColumnForcast_Close_Day=pd.DataFrame({})
        all_df=pd.read_csv(all_colums_Data_CSV,index_col=0)
        print(all_df.shape)

        df=pd.read_csv(Data_CSV,index_col=0)
        print(df.shape)
        

        
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
        print(locpercentage)
        #datefiltredPercentage=indexDates[locpercentage:]
        #
        # if datefiltredPercentage=indexDates[indexDates.shape[0]-backdaysConsideredToBForcasted:]
        datefiltredPercentage=indexDates[locpercentage-backdaysConsideredToBForcasted:locpercentage]

        self.Update_Progress_String.emit("Forcasting about to start")
        self.Update_Progress.emit(self.FirstPercentageAbout_toStartForcast)
        
        DatesIndex=0
        
        for i in datefiltredPercentage:
            
            print("to be predict from: "+str(i))
            #ColumToforcast, ColumRealYToCompare, dateFromForcast, data_frame_Path, BackDays
            self.forcaster.ToForcastfrom(ColumToForcast,ColumToForcast,str(i),Data_CSV,backdaysConsidered)
            Real_Y_current=self.forcaster.Get_UnicForcast_Real_Y_current()
            Real_Y_Forcast=self.forcaster.Get_UnicForcast_Forcast_Close()
            Real_Y_Close=self.forcaster.Get_UnicForcast_Real_Y_Close()
            forcastedDate=self.forcaster.Get_Forcasted_Date()
            ColumnCurrent_Close_Day.append(Real_Y_current)
            ColumnForcast_Close_Day.append(Real_Y_Forcast)
            ColumnReal_Close_Day.append(Real_Y_Close)
            Columnforcasteddate.append(str(forcastedDate))
            Forcast_Dates.append(i)
            DatesIndex=DatesIndex+1
            self.update_DateForcasting(DatesIndex,i)
            
            
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
        #Allandforcast=all_df[all_df.shape[0]-backdaysConsideredToBForcasted:]

        if FFtUsedQ:
            #if fft considered:
            Allandforcast=all_df[locpercentage-backdaysConsideredToBForcasted+backdaysConsidered:locpercentage+backdaysConsidered]
        else:
            #if not FFT consider
            Allandforcast=all_df[locpercentage-backdaysConsideredToBForcasted:locpercentage]
        print(Allandforcast.shape)
        print(Allandforcast)
        print(fd_ColumnForcast_Close_Day.shape)
        print(fd_ColumnForcast_Close_Day)
        frames = [Allandforcast, fd_ColumnForcast_Close_Day]

        Final_Allandforcast = pd.concat(frames,axis=1)


        ######         this plot must be done at main thread     ###############
        #plt.plot(ColumnForcast_Close_Day,label='ColumnForcast_Close_Day',color='orange', marker='o')
        #plt.plot(ColumnReal_Close_Day,label='ColumnReal_Close_Day',color='green', marker='*')
        #plt.plot([1,2,3,4])
        #plt.show()
        #np.insert(a, a.shape[1], np.array((10, 10, 10, 10)), 1)
        #print(ensambly_np.shape)
        #print(ensambly_np.shape)
        # to convert to CSV
        
        
        #Creating the csv File
        Final_Allandforcast.to_csv(path_or_buf=self.forcastPath,index=True)
        
        #Getting Forcasting Data
        ### Model Data ###
        self.today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.date_Time=str(self.today)
        self.Rows_Considered=self.backdaysConsideredToBForcasted
        self.Model_id_FRGN=self.Model_Id_Used
        
        #Giving de columns to main thread to get the trend 
        self.ColumnForcast,self.ColumReal=ColumnForcast_Close_Day, ColumnReal_Close_Day
        
        self.Update_Progress_String.emit("Forcasting finished")
        self.Update_Progress.emit(100)
        time.sleep(3)
        self.Update_Progress_String.emit("Ready to get some other forcast")
        self.Update_Progress.emit(0)
        self.Update_ForcastingProcsStatus.emit(True)
        
    def update_DateForcasting(self,DateIndexDone,Date): 
        DatesToForcast=self.backdaysConsideredToBForcasted
        
        CurrenEpochPrecent_and_Already_Done=int(((int(DateIndexDone)*self.Forcasting_Represent_Precent_total)/int(DatesToForcast))+self.FirstPercentageAbout_toStartForcast)
        print("..........................")
        print(type(CurrenEpochPrecent_and_Already_Done))
        
        print("percentage"+str(CurrenEpochPrecent_and_Already_Done))
        self.Update_Progress_String.emit("Forcasting in process, last forcast: "+str(DateIndexDone)+" ("+str(Date)+")"+" of "+str(DatesToForcast))
        self.Update_Progress.emit(int(CurrenEpochPrecent_and_Already_Done))

        
        