import sqlite3

#To see easy the db file is to drag bdfiel into:  https://inloop.github.io/sqlite-viewer/
#or by using the command c.execute('SELECT * FROM estudiantes")
#print (c.fetchall()) a list is generated

#Connect with bd or Create if doesnt exist
conn=sqlite3.connect('APP/DataStructures/Predict_model.db')


#Create cursor
c = conn.cursor()


#Add colum
c.execute("""ALTER TABLE 'Models' ADD val_mean_squared_error REAL""")
          
          