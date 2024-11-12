import pandas as pd
import yfinance as yf
from datetime import date, timedelta

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

import cmath

class DatasetGenerator:
    def RetivingDataPrices_Yahoo(self,Name_Item,From, to,csvFileName,csvFileName_New,addToOld):
        startDate=From
        endDate= to
        name_item= Name_Item

        df=yf.download(name_item,start = startDate, end = endDate,interval='1d',threads = True)
        df.pop("Adj Close")
        
        self.SavingDataset(df,csvFileName, csvFileName_New, addToOld)
        
    def PopListdf(self,columns,csvFileName, csvFileName_New,):
        df=pd.read_csv(csvFileName, index_col="Date")
        Column=columns
        for i in Column:
            print(i)
            print(type(i))
            df.pop(i)
        self.SavingDataset(df,csvFileName, csvFileName_New,False)
              
    def SavingDataset(self,df,csvFileName, csvFileName_New,Add_to_old):
        #####      Saving Data In CSV file   ##
        if Add_to_old:
            try:
                existing=pd.read_csv(csvFileName, index_col="Date")
                #print(existing)
                #print(type(existing))
                try:
                    #existing = existing.append(df)
                    existing = pd.concat([existing,df])
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
            print(dateIndex)
            d_name = pd.Timestamp(i)
            weekday_Name.append(str(d_name.day_name()))
            weekday_Number.append(d_name.dayofweek)
            print(weekday_Number)
            
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
        
    def Add_ColumsFourier_Transform_Df_Return(self,Periodic_Components_num,column_to_use, DataSet):
        df=DataSet
     
        Colum_Used=column_to_use
        periodic_components_num=Periodic_Components_num
        print("using colum"+str(Colum_Used))
        
        for e in Colum_Used :
            for j in periodic_components_num :
        
                data_FT = df[e]
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
                
                
                

                fft_list_m10= np.copy(fft_list); 
                fft_list_m10[j:-j]=0
                data_fourier=np.fft.ifft(fft_list_m10)
                
                
                Magnitud=[]
                Angle=[]
                for i in data_fourier:
                    magnitud, angle=cmath.polar(i)
                    Magnitud.append(magnitud)
                    Angle.append(angle)
                
                df["FFT_Mag_{}_{}".format(e,j)]=Magnitud
                df["FFT_Angl_{}_{}".format(e,j)]=Angle
                
                #print("this is the last df"+str(df.head))     
        return df
    
    def UpdateToday(self, ItemName,CsvFileName,addToOld):
        startDate=""
        endDate=str(date.today())
        itemName=ItemName
        csvFileName=CsvFileName
        df=pd.read_csv(csvFileName, index_col="Date")
        
        
        
        startDate=df.index[df.shape[0]-1:]
        startDate=str(np.datetime64(startDate[0])+np.timedelta64(1, 'D'))[0:10]

        print(endDate)
        print(startDate)
        self.RetivingDataPrices_Yahoo(itemName,startDate,endDate,csvFileName,csvFileName, addToOld)
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
        colum=Colum #Now is a list
        csvFileName=CsvFileName
        newFilepath=NewFilepath
        backdaysToconsider=BackdaysToconsider
        NewLastFFTDataset = pd.DataFrame({})
        FinalLastFFTDataset = pd.DataFrame({})
        frec=Frec # Now is a list
        
        df=pd.read_csv(csvFileName, index_col="Date")
        #df.shape[0])  ---> is the row numbers like 5566 days
        
        
        for i in range(backdaysToconsider,df.shape[0]+1):
                    
            df_short=df[:i] #starting from row 0 values up to backdays-1 and increase until df.shape[0] 
            NewLastFFTDataset=self.Add_ColumsFourier_Transform_Df_Return(frec,colum, df_short)
            print(NewLastFFTDataset)
            NewLastFFTDataset=NewLastFFTDataset.iloc[-1:]#getting only the last one
            print(NewLastFFTDataset)
            
            FinalLastFFTDataset=pd.concat([FinalLastFFTDataset,NewLastFFTDataset])  
        
        print(FinalLastFFTDataset.tail)
        
        self.SavingDataset(FinalLastFFTDataset,newFilepath, newFilepath, False)
    
    def AddUpDown(self,csvFileName,csvFileName_New,Column):
        df=pd.read_csv(csvFileName, index_col="Date")
        firstDone=False
        day_t=0
        day_t_oneless=0
        MvmtResult=0
        MvmtResultList=[]
        for i in df[Column]:
            day_t=i
            if firstDone==False:
                MvmtResult=0
                firstDone=True
            else:
                if day_t<day_t_oneless:
                    MvmtResult=0
                elif day_t>day_t_oneless:
                    MvmtResult=1

            MvmtResultList.append(MvmtResult)
            day_t_oneless=day_t

        df["UpDown"]=MvmtResultList
        
        self.SavingDataset(df,csvFileName, csvFileName_New,False)
    
    def Add_normal_distribution(self,csvFileName_NormalD,NewdfPath_NormalD,MaxBackDist,BackPeriod,Column):
        df=pd.read_csv(csvFileName_NormalD, index_col="Date")
        New_df=df
        #print(New_df.shape[0])
        maxBackDist=MaxBackDist
        backPeriod_init=0
        backPeriod_end=BackPeriod
        #print("New_df.shape[0]: "+str(New_df.shape[0]))
        loan_Column_df=df[Column]

        sigmaOofset_Plus_list=[]
        sigmaOofset_less_list=[]
        All_Area_list=[]


        while maxBackDist<=New_df.shape[0]:
            temporalDataSet=loan_Column_df[backPeriod_init:maxBackDist]
            print(temporalDataSet)
            mu=temporalDataSet.describe()[1:2] #Getting the mean value

            temporalNumpyDtaSet=temporalDataSet.to_numpy()
            sigma=np.std(temporalNumpyDtaSet) # Sigma standard deviation


            SubPeriod_df=temporalDataSet[temporalDataSet.shape[0]-backPeriod_end:]
            print(SubPeriod_df)
            SubPer_Max = SubPeriod_df.max()
            SubPer_min = SubPeriod_df.min()



            sigmaOofset_Plus_list.append(SubPer_Max)

            sigmaOofset_less_list.append(SubPer_min)

            All_Area=norm.cdf(SubPer_Max,loc=mu,scale=sigma)-norm.cdf(SubPer_min,loc=mu,scale=sigma)#getting the accumulative normal distribution "Area under the curve"
            All_Area_list.append(All_Area)

            backPeriod_init+=1
            maxBackDist+=1


        New_df_=New_df[MaxBackDist-1:]
        #print(New_df_.shape())

        Name_New_Column_1=Column+"MaxVSubPeriod"
        Name_New_Column_2=Column+"All_Area"
        Name_New_Column_3=Column+"minVSuberiod"
        New_df_[Name_New_Column_1]=sigmaOofset_less_list
        New_df_[Name_New_Column_2]=All_Area_list
        New_df_[Name_New_Column_3]=sigmaOofset_Plus_list

        self.SavingDataset(New_df_,csvFileName_NormalD, NewdfPath_NormalD, False)  