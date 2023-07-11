import pandas as pd
import yfinance as yf
from datetime import date, timedelta

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
        
        self.SavingDataset(df,csvFileName, csvFileName_New, True)
        
    def PopListdf(self,columns,csvFileName, csvFileName_New,):
        df=pd.read_csv(csvFileName, index_col="Date")
        Column=columns
        for i in Column:
            df.pop(i)
        self.SavingDataset(df,csvFileName, csvFileName_New,False)
              
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
    
    def AddColumnMothandDay(self,csvFileName, csvFileName_New,MothName_Too):
        df=pd.read_csv(csvFileName, index_col="Date")
        
        dateIndex=[]
        month_Name=[]
        Moth_Number=[]
        Day_of_Moth=[]
        for i in df.index:
            dateIndex.append(i)
            d_name = pd.Timestamp(i)
            month_Name.append(str(d_name.month_name()))
            Moth_Number.append(int(d_name.month)*100)
            Day_of_Moth.append(int(d_name.day))
            
        if MothName_Too:
            df["MonthName"]=month_Name
            df["Moth_Number"]=Moth_Number
            df["DayMonth"]=Day_of_Moth
        else:
            df["Month_Number"]=Moth_Number
            df["DayMonth"]=Day_of_Moth
            
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
        
    def AddRepeatedLastOne(self,csvFileName, csvFileName_New):
        df=pd.read_csv(csvFileName, index_col="Date")

        lastIndexRow=df.index[(df.shape[0]-1)]    
        LastRow=df.loc[lastIndexRow]
        print(lastIndexRow)
        time_stamp = pd.Timestamp(lastIndexRow)
        time_stamp=time_stamp+ timedelta(days=1) 
        #time_stamp_str=str(time_stamp)[0:10]
        

        df.loc[time_stamp]=LastRow
        
            
        self.SavingDataset(df,csvFileName, csvFileName_New,False)
        
        
    def Add_ColumsFourier_Transform(self,periodic_Components_num,column_to_use, Origin_File_Path,Destiny_File_Path,FileGenerated):
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
        
    def Add_ColumsFourier_Transform_Df_Return(self,periodic_Components_num,column_to_use, DataSet):
        df=DataSet
     
        Colum_Used=column_to_use
        #print("using colum"+str(Colum_Used))
        data_FT = df[Colum_Used]
        #print("This is the head"+str(data_FT.head))
        
        dateIndex=[]
        for i in data_FT.index:
            dateIndex.append(i)
        array_like=[]
            
        
        array_like=np.asarray(data_FT).tolist()
        The_fft = np.fft.fft(array_like)
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
        return df
    
    def UpdateToday(self, ItemName,CsvFileName):
        startDate=""
        endDate=str(date.today()+timedelta(days=1))
        itemName=ItemName
        csvFileName=CsvFileName
        df=pd.read_csv(csvFileName, index_col="Date")
        
        
        
        startDate=df.index[df.shape[0]-1:]
        startDate=str(np.datetime64(startDate[0])+np.timedelta64(1, 'D'))[0:10]

        print(endDate)
        print(startDate)
        self.RetivingDataPrices_Yahoo(itemName,startDate,endDate,csvFileName,csvFileName)
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
            print(i)
            existing=pd.read_csv(i, index_col="Date")
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
            
            print(len(dict_Columns))
            
            existing_Columns_Renamed=existing.rename(columns=dict_Columns)
            
            #Last_pd = pd.concat([Last_pd,existing_Columns_Renamed], axis=1,join='inner')
            
        
        Last_pd=self.deleterRowWhenNull(Last_pd)
        Last_pd.index.name='Date'
        print(Last_pd.shape)
        self.SavingDataset(Last_pd,NewFIleName, NewFIleName,False)
    
    def AddColumnPRCNTG(self,csvFileName, csvFileName_New):
        df=pd.read_csv(csvFileName, index_col="Date")
    
        columns_list=df.columns[0:5]

        indexDatesList=[]
        indexDatesDic={}
        for o in df.index:
            indexDatesList.append(o)
            
        ListPercentages=[]
        val_n=0
        val_n_1=0
        percentage_n_1=0
        First_val=True
        df_percentage=pd.DataFrame()
        for columns in columns_list:
            accu_=0
            First_val=True
            ListPercentages=[]
            for rows in df[columns]:
                val_n_1=rows
            
                if First_val==True:
                    First_val=False
                    ListPercentages.append(0)
                else:
                    try:
                        percentage_n_1=((val_n_1*100)/val_n)-100
                    except:
                        percentage_n_1=((val_n_1*100)/1)-100
                    ListPercentages.append(percentage_n_1)
                val_n=val_n_1
            
            df[columns+"_PRCNTG"]=ListPercentages
        df['Date']=indexDatesList
        df_percentage=df.set_index('Date')
                    
        self.SavingDataset(df_percentage,csvFileName, csvFileName_New,False)
    
    def AddColumnDirePrice(self,csvFileName, csvFileName_New):
        df=pd.read_csv(csvFileName, index_col="Date")
    
        columns_list=df.columns[0:5]

        indexDatesList=[]
        ListPercentages={}
        for o in df.index:
            indexDatesList.append(o)
            
        val_n=0
        val_n_1=0
        percentage_n_1=0
        First_val=True
        df_percentage=pd.DataFrame()
        for columns in columns_list:
            accu_=0
            First_val=True
            ListPercentages=[]
            for rows in df[columns]:
                val_n_1=rows
            
                if First_val==True:
                    First_val=False
                    ListPercentages.append(0)
                else:
                    try:
                        percentage_n_1=((val_n_1*100)/val_n)-100
                    except:
                        percentage_n_1=((val_n_1*100)/1)-100
                    ListPercentages.append(percentage_n_1)
                val_n=val_n_1
            
            df[columns+"_DirPrice"]=ListPercentages
        df['Date']=indexDatesList
        df_percentage=df.set_index('Date')
                    
        self.SavingDataset(df_percentage,csvFileName, csvFileName_New,False)
        
        
    def AddColumnInverseDirePrice(self,csvFileName, csvFileName_New):
        df=pd.read_csv(csvFileName, index_col="Date")
    
        columns_list=df.columns[0:5]

        indexDatesList=[]
        ListPercentages={}
        for o in df.index:
            indexDatesList.append(o)
            
        
        val_n=0
        val_n_1=0
        percentage_n_1=0
        First_val=True
        df_percentage=pd.DataFrame()
        for columns in columns_list:
            accu_=0
            First_val=True
            ListPercentages=[]
            for rows in df[columns]:
                val_n_1=rows
            
                if First_val==True:
                    First_val=False
                    ListPercentages.append(0)
                else:
                    try:
                        percentage_n_1=((val_n_1*100)/val_n)-100
                    except:
                        percentage_n_1=((val_n_1*100)/1)-100
                    ListPercentages.append(percentage_n_1*(-1))
                val_n=val_n_1
            
            df[columns+"_InvDirPrice"]=ListPercentages
        df['Date']=indexDatesList
        df_percentage=df.set_index('Date')
                    
        self.SavingDataset(df_percentage,csvFileName, csvFileName_New,False)
    
    
       
    def  getTheLastFFTValue(self,BackdaysToconsider,Frec,Colum,CsvFileName, NewFilepath):

        colum=Colum
        csvFileName=CsvFileName
        newFilepath=NewFilepath
        backdaysToconsider=BackdaysToconsider
        NewLastFFTDataset = pd.DataFrame({})
        FinalLastFFTDataset = pd.DataFrame({})
        frec=Frec
        
        df=pd.read_csv(csvFileName, index_col="Date")
        
        for i in range(backdaysToconsider,df.shape[0]+1):
            df_short=df[:i]
            NewLastFFTDataset=self.Add_ColumsFourier_Transform_Df_Return(frec,colum, df_short)
            
            NewLastFFTDataset=NewLastFFTDataset.iloc[-1:]
            print(NewLastFFTDataset)
            FinalLastFFTDataset=pd.concat([FinalLastFFTDataset,NewLastFFTDataset])  
        
        print(FinalLastFFTDataset.tail)
        
        self.SavingDataset(FinalLastFFTDataset,NewFilepath, NewFilepath, False)   