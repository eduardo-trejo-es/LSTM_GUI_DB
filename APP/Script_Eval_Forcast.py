import pandas as pd


basePath="APP/ModelForcast/CL=F/Model_12/Forcast_83/"
ForcastVCS_Path=basePath+"ForcastDataSet.csv"
ForcastResult=basePath+"ForcastDataSetResult.csv"

df=pd.read_csv(ForcastVCS_Path, index_col=0)

Direction_Forcast=[]
Direction_Real=[]
firstDate=df.index[0]
print(df.shape)
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

            
df.to_csv(path_or_buf=ForcastResult,index=True)