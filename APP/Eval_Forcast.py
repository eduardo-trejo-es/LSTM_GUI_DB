
from PyQt5.QtCore import *

from datetime import datetime
import time

import pandas as pd
import numpy as np

### Check if model is created
import os.path as path

class DL_Evaluator(QThread):
    Update_Progress = pyqtSignal(int)
    Update_Progress_String = pyqtSignal(str)
    Update_EvaluationStatus = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.TotalRight=0
        self.Right_precentage=0
        self.RowConsidered=0
        self.Total_diff_Earned=0
        self.diff_earned_percentage=0
        self.Total_diff_lose=0
        self.diff_lose_percentage=0
        self.total_movements=0
        self.Real_earned=0
        self.RealEarnedPercentage=0
        self.TotalPercentage=0
        self.Forcast_id_Used=0
        self.selecteditem=""
        self.selectedModel=0
        self.selectedForcast=0
    
    def Set_Forcast_id(self,val):
        self.Forcast_id_Used=val
    
    def Set_ForcastPath(self,val):
        self.forcastpath=val
        
    def Set_RowConsidered(self,val):
        self.RowConsidered=val
        
    def Set_TotalRight(self,val):
        self.TotalRight=val
        
    def Set_Right_precentage(self,val):
        self.Right_precentage=val
        
    def Set_Total_diff_Earned(self,val):
        self.Total_diff_Earned=val
        
    def Set_Total_diff_lose(self,val):
        self.Total_diff_lose=val
        
    def Set_total_movements(self,val):
        self.total_movements=val
        
    def Set_diff_earned_percentage(self,val):
        self.diff_earned_percentage=val
        
    def Set_diff_lose_percentage(self,val):
        self.diff_lose_percentage=val
        
    def Set_Real_earned(self,val):
        self.Real_earned=val
        
    def Set_TotalPercentage(self,val):
        self.TotalPercentage=val
        
    def Set_RealEarnedPercentage(self,val):
        self.RealEarnedPercentage=val
        
    def Set_selectedItem(self,val):
        self.selecteditem=val
        
    def Set_selectedModel(self,val):
        self.selectedModel=val
    
    def Set_selectedForcastId(self,val):
        self.selectedForcast=val
    
    def Get_All_DataDB(self):
        return (self.TotalRight,self.Right_precentage,self.RowConsidered,self.Total_diff_Earned,
                self.diff_earned_percentage, self.Total_diff_lose, self.diff_lose_percentage,
                self.total_movements,self.Real_earned,self.RealEarnedPercentage,self.TotalPercentage,
                self.Forcast_id_Used,)
    
    """Total_Movement_Right self.TotalRight
    Total_Movement_Right_Per100 self.Right_precentage
    Rows_Considered : self.RowConsidered
    
    Total_Diff_Mag_earned, self.Total_diff_Earned
    Total_Diff_earned_Per100 self.diff_earned_percentage
    
    Total_Diff_Mag_lose, self.Total_diff_lose,
    Total_Diff_lose_Per100,self.diff_lose_percentage
    
    Total_Mag_Mvmnts, self.total_movements,
    
    Real_Mag_earned, self.Real_earned
    Real_earned_Per100 self.RealEarnedPercentage
    
    Total_Mag_Mvmnts_Per100 self.TotalPercentage"""
    
    def run(self):
        df=pd.read_csv(self.forcastpath, index_col=0)
        self.evaluate(df)
        """try:
            df=pd.read_csv(self.forcastpath, index_col=0)
            self.evaluate(self,df)
        except:
            print("An error occure trying to retrive the forcast dataSet ")"""
        
        time.sleep(1)
        self.Update_EvaluationStatus.emit(True)


    def evaluate(self,DF):
        df=DF
        Direction_Forcast=[]
        Direction_Real=[]
        firstDate=df.index[0]

        ##Direction forcast close price and  Real close price
        for i in range(0,df.shape[0]):
            #Direction_Forcast
            if df.index[i]==firstDate: 
                Direction_Forcast.append("null")
                Direction_Real.append("null")
            else:
                if i<(df.shape[0]-1):
                    #Getting the Direction of forcast close price
                    if df['Forcast'][i]>df['Forcast'][i-1]:
                        Direction_Forcast.append("Up")
                    elif df['Forcast'][i]<df['Forcast'][i-1]:
                        Direction_Forcast.append("Down")
                    else:
                        Direction_Real.append("equal")
                else:
                    Direction_Forcast.append("null")
                #Getting the Direction of Real close price   
                if i<(df.shape[0]-1):
                    if df['Close'][i+1]>df['Close'][i]:
                        Direction_Real.append("Up")
                    elif df['Close'][i+1]<df['Close'][i]:
                        Direction_Real.append("Down")
                    else:
                        Direction_Real.append("equal")
                else:
                    Direction_Real.append("null")
                

        df["Forcast_Direction"]=Direction_Forcast
        df["Real_Direction"]=Direction_Real
        
        #Result bool, diff right and diff wrong
        Move_Result=[]

        for i in range(0,df.shape[0]):
            #Direction_Forcast
            if df.index[i]==firstDate: 
                Move_Result.append("null")
            else:
                #Getting the result 
                if i<(df.shape[0]-1):
                    if df['Forcast_Direction'][i]==df['Real_Direction'][i]:
                        Move_Result.append(1)
                    else:
                        Move_Result.append(0)
                else:
                    Move_Result.append("null")

        df["Result"]=Move_Result

        ##diff right and diff wrong
        diff_right=[]
        diff_wrong=[]

        for i in range(0,df.shape[0]):
            #Direction_Forcast
            if df.index[i]==firstDate: 
                diff_right.append(0)
                diff_wrong.append(0)
            else:
                #Getting diff right 
                if i<(df.shape[0]-1):
                    if df['Result'][i]==1:
                        diff_right.append(abs(df['Close'][i+1]-df['Close'][i]))
                    else:
                        diff_right.append(0)
                else:
                    diff_right.append(0)
                
                #Getting diff wrong
                if i<(df.shape[0]-1):
                    if df['Result'][i]==0:
                        diff_wrong.append(abs(df['Close'][i+1]-df['Close'][i]))
                    else:
                        diff_wrong.append(0)
                else:
                    diff_wrong.append(0)
                    
        df["diff_right"]=diff_right
        df["diff_wrong"]=diff_wrong


        #Howmany Rows considered?
        RowConsidered=df.shape[0]-2
        
        #Total right
        TotalRight=0
        for i in range(0,df.shape[0]):
            if df.index[i]==firstDate: 
                pass
            else:
                if i<(df.shape[0]-1):
                    TotalRight=TotalRight+df['Result'][i]
        print(TotalRight)
        

        #Right %
        Right_precentage=TotalRight*100/RowConsidered
        print(Right_precentage)
        


        #Total diff earned
        Total_diff_Earned=0
        for i in range(0,df.shape[0]):
            if df.index[i]==firstDate: 
                pass
            else:
                if i<(df.shape[0]-1):
                    Total_diff_Earned=Total_diff_Earned+df['diff_right'][i]

        print("Total_diff_Earned"+str(Total_diff_Earned))

        #Total diff lose
        Total_diff_lose=0
        for i in range(0,df.shape[0]):
            if df.index[i]==firstDate: 
                pass
            else:
                if i<(df.shape[0]-1):
                    Total_diff_lose=Total_diff_lose+df['diff_wrong'][i]
                
        print("Total_diff_lose"+str(Total_diff_lose))
        
        #total movements
        total_movements=Total_diff_lose+Total_diff_Earned
        print("total_movements"+str(total_movements))
        

        #diff earned %
        diff_earned_percentage=Total_diff_Earned*100/total_movements
        print("diff_earned_percentage"+str(diff_earned_percentage))
        

        #diff lose %
        diff_lose_percentage=Total_diff_lose*100/total_movements
        print("diff_lose_percentage"+str(diff_lose_percentage))
        

        #Real earned
        Real_earned=Total_diff_Earned-Total_diff_lose
        print("Real_earned"+str(Real_earned))
        

        #Total percentages
        TotalPercentage=diff_earned_percentage+diff_lose_percentage
        print("TotalPercentage"+str(TotalPercentage))
        

        #Real earned%
        RealEarnedPercentage=Real_earned*100/total_movements
        print("RealEarnedPercentage"+str(RealEarnedPercentage))
        

        #####   Results
        self.Set_RowConsidered(RowConsidered)
        self.Set_TotalRight(TotalRight)
        self.Set_Right_precentage(Right_precentage)
        self.Set_Total_diff_Earned(Total_diff_Earned)
        self.Set_Total_diff_lose(Total_diff_lose)
        self.Set_total_movements(total_movements)
        self.Set_diff_earned_percentage(diff_earned_percentage)
        self.Set_diff_lose_percentage(diff_lose_percentage)
        self.Set_Real_earned(Real_earned)
        self.Set_TotalPercentage(TotalPercentage)
        self.Set_RealEarnedPercentage(RealEarnedPercentage)

        
                    
        #df.to_csv(path_or_buf=ForcastResult,index=True)
        