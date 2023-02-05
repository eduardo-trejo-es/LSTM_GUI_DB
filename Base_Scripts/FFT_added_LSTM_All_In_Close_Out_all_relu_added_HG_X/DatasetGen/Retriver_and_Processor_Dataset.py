import pandas as pd
import yfinance as yf
from datetime import date

import numpy as np
import matplotlib.pyplot as plt

import cmath

class DatasetGenerator:
    def RetivingDataPrices_Yahoo(self,Name_Item,From, to,csvFileName,csvFileName_New):
        startDate=From
        endDate= to
        name_item= Name_Item

        df=yf.download(name_item,start = startDate, end = endDate,interval='1d',threads = True)
        df.pop("Adj Close")
        """#df=yf.download('CL=F',start = startDate, end = endDate,interval='1d',threads = True)
        df_Crude_Oil=yf.download('CL=F',start = startDate, end = endDate,threads = True)
        df_Copper=yf.download('HG=F',start = startDate, end = endDate,threads = True)
        df_Steel=yf.download('X',start = startDate, end = endDate,threads = True)

        df_Crude_Oil.pop("Adj Close")
        df_Copper.pop("Adj Close")
        df_Steel.pop("Adj Close")
        
        #____________ Changing columns names _____________

        #####   Crude oil  CL=F
        dict_CL_F_Columns={'Open':'Open_CL=F', 'High':'High_CL=F', 'Low':'Low_CL=F', 'Close':'Close_CL=F','Volume':'Volume_CL=F'}
        df_Crude_Oil_Renam=df_Crude_Oil.rename(columns=dict_CL_F_Columns)

        #### Copper HG=F 
        dict_HG_F_Columns={'Open':'Open_HG=F', 'High':'High_HG=F', 'Low':'Low_HG=F', 'Close':'Close_HG=F','Volume':'Volume_HG=F'}
        df_Copper_Renam=df_Copper.rename(columns=dict_HG_F_Columns)

        #### Steel X
        dict_X_Columns={'Open':'Open_X', 'High':'High_X', 'Low':'Low_X', 'Close':'Close_X','Volume':'Volume_X'}
        df_steel_Renam=df_Steel.rename(columns=dict_X_Columns)
        
        Last_pd = pd.concat([df_Crude_Oil_Renam, df_Copper_Renam,df_steel_Renam], axis=1)"""
        
        self.SavingDataset(df,csvFileName, csvFileName_New, True)
        
            
    def SavingDataset(self,df,csvFileName, csvFileName_New,Add_to_old):
        #####      Saving Data In CSV file   ####
        if Add_to_old:
            try:
                existing=pd.read_csv(csvFileName, index_col="Date")
                #print(existing)
                #print(type(existing))
                try:
                    existing = existing.append(df)
                except :
                    print("could not be possible to add new rows")
                print("was try")
                print(existing)
                existing.to_csv(path_or_buf=csvFileName_New,index=True)
                
            except :
                
                print("was execpt")
                df.to_csv(path_or_buf=csvFileName_New,index=True)
        else:
            print("The actual data saved")
            df.to_csv(path_or_buf=csvFileName_New,index=True)
            

    def AddColumnWeekDay(self,csvFileName, csvFileName_New,DayName_Too):
        df=pd.read_csv(csvFileName, index_col="Date")
        
        dateIndex=[]
        weekday_Name=[]
        weekday_Number=[]
        for i in df.index:
            dateIndex.append(i)
            d_name = pd.Timestamp(i)
            weekday_Name.append(str(d_name.day_name()))
            weekday_Number.append(d_name.dayofweek)
            
        if DayName_Too:
            df["DayName"]=weekday_Name
            df["DayNumber"]=weekday_Number
        else:
            df["DayNumber"]=weekday_Number
            
        self.SavingDataset(df,csvFileName, csvFileName_New,False)
    
    def AddColumnMoth(self,csvFileName, csvFileName_New,MothName_Too):
        df=pd.read_csv(csvFileName, index_col="Date")
        
        dateIndex=[]
        month_Name=[]
        Moth_Number=[]
        for i in df.index:
            dateIndex.append(i)
            d_name = pd.Timestamp(i)
            month_Name.append(str(d_name.month_name()))
            Moth_Number.append(int(d_name.month)*100)
            
        if MothName_Too:
            df["MonthName"]=month_Name
            df["Moth_Number"]=Moth_Number
        else:
            df["Month_Number"]=Moth_Number
            
        self.SavingDataset(df,csvFileName, csvFileName_New,False)
    
    def AddColumnYear(self,csvFileName, csvFileName_New):
        df=pd.read_csv(csvFileName, index_col="Date")
        
        dateIndex=[]
        year_Number=[]
        for i in df.index:
            dateIndex.append(i)
            d_name = pd.Timestamp(i)
            year_Number.append(int(d_name.year))
            
        df["Year"]=year_Number
            
        self.SavingDataset(df,csvFileName, csvFileName_New,False)
        
        
    def Add_ColumsFourier_Transform(self,periodic_Components_num,column_to_use, Origin_File_Path,Destiny_File_Path):
        csvFileName=Origin_File_Path
        
        df=pd.read_csv(csvFileName, index_col="Date")
        
        Colum_Used=column_to_use
        #print("using colum"+str(Colum_Used))
        data_FT = df[Colum_Used]
        #print("This is the head"+str(data_FT.head))
        print(data_FT.shape)
        
        dateIndex=[]
        for i in data_FT.index:
            dateIndex.append(i)
        array_like=[]
        
        """var_inc=0
        for j in data_FT:
            array_like.append(j)
            var_inc=var_inc+1
            if var_inc==174: break"""
            
        
        array_like=np.asarray(data_FT).tolist()
        The_fft = np.fft.fft(array_like)
        print(The_fft)
        fft_df =pd.DataFrame({'fft':The_fft})
        fft_df['absolute']=fft_df['fft'].apply(lambda x: np.abs(x))
        fft_df['angle']=fft_df['fft'].apply(lambda x: np.angle(x))
        fft_list = np.asarray(fft_df['fft'].tolist())
        
        
        Periodic_Components_Num=periodic_Components_num

        fft_list_m10= np.copy(fft_list); 
        fft_list_m10[Periodic_Components_Num:-Periodic_Components_Num]=0
        data_fourier=np.fft.ifft(fft_list_m10)
        
        
        Magnitud=[]
        Angle=[]
        for i in data_fourier:
            magnitud, angle=cmath.polar(i)
            Magnitud.append(magnitud)
            Angle.append(angle)
        
        df["FFT_Mag_{}_{}".format(Colum_Used,periodic_Components_num)]=Magnitud
        df["FFT_Angl_{}_{}".format(Colum_Used,periodic_Components_num)]=Angle
        
        #print("this is the last df"+str(df.head))   
        
        self.SavingDataset(df,Origin_File_Path, Destiny_File_Path, False)
    
    def UpdateToday(self, CsvFileName):
        startDate=""
        endDate=str(date.today())
        
        csvFileName=CsvFileName
        df=pd.read_csv(csvFileName, index_col="Date")
        
        
        
        startDate=df.index[df.shape[0]-1:]
        startDate=str(np.datetime64(startDate[0])+np.timedelta64(1, 'D'))[0:10]

        print(endDate)
        print(startDate)
        self.RetivingDataPrices_Yahoo(startDate,endDate,csvFileName,csvFileName)
        #df=yf.download('CL=F',start = startDate, end = endDate,interval='1d',utc=True,threads = True)
    
    
    def deleterRowWhenNull(self,dataFrame):
        df_isnull=dataFrame.isnull().any(axis=1)
        df_isnull_index=dataFrame.index
        print(df_isnull_index)
        index_when_null=[]
        index_num=0
        for i in df_isnull:
            if i :index_when_null.append(df_isnull_index[index_num])
            index_num+=1
        print(index_when_null)
        dataFrame.drop(index_when_null, axis=0, inplace=True)

        return dataFrame
        
    def dfCombiner(self,PathListdf,NewFIleName):
        Last_pd=pd.DataFrame({})
        
        for i in PathListdf:
            existing=pd.read_csv(i, index_col="Date")
            print(existing.columns)
            if i.find("GH_F")!=-1:
                itemName="_GH_F"
            elif i.find("CRUDE_OIL")!=-1:
                itemName="_CRUDE_OIL"
            elif i.find("Steel_X")!=-1:
                itemName="_Steel_X"
            list_Orig_Columns=existing.columns
            list_New_Columns=[]
            
            for k in list_Orig_Columns:
                list_New_Columns.append(k+itemName)
            
            
            dict_Columns={}
            for j in range(0,len(list_Orig_Columns)):
                dict_Columns[list_Orig_Columns[j]]=list_New_Columns[j]
                
            existing_Columns_Renamed=existing.rename(columns=dict_Columns)
            
            
            Last_pd = pd.concat([Last_pd,existing_Columns_Renamed], axis=1)
            
        
        Last_pd=self.deleterRowWhenNull(Last_pd)
        Last_pd.index.name='Date'
        print(Last_pd.shape)
        self.SavingDataset(Last_pd,NewFIleName, NewFIleName,False)