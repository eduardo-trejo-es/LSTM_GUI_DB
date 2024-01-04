import pandas as pd
df = pd.DataFrame([("a",),("b",)])

print(df.shape)

for i in df[0]:
    print(i)
    
