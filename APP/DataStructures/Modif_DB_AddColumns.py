import sqlite3

#To see easy the db file is to drag bdfiel into:  https://inloop.github.io/sqlite-viewer/
#or by using the command c.execute('SELECT * FROM estudiantes")
#print (c.fetchall()) a list is generated

#Connect with bd or Create if doesnt exist
conn=sqlite3.connect('APP/DataStructures/Predict_model.db')


#Create cursor
c = conn.cursor()


#Add colum
#c.execute("""ALTER TABLE 'Models' ADD val_mean_squared_error REAL""")
          
          
#c.execute("""DROP TABLE Relation_Model_Datasets""")

#c.execute("""
#        CREATE TABLE Relation_Model_Datasets(
#            Rltion_ModelDataSet_id INTEGER PRIMARY KEY AUTOINCREMENT,
#            Model_id_FRGN INTEGER,
#            DataSet_id_FRGN INTEGER,
#            FOREIGN KEY(Model_id_FRGN) REFERENCES Models(Model_id),
#            FOREIGN KEY(DataSet_id_FRGN) REFERENCES DataSet(DataSet_id)
#        )
#        """)


c.execute("""INSERT INTO Relation_Model_Datasets (Model_id_FRGN,DataSet_id_FRGN) VALUES(35,2) """)

conn.commit()
          