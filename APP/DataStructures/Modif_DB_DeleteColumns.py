import sqlite3

#To see easy the db file is to drag bdfiel into:  https://inloop.github.io/sqlite-viewer/
#or by using the command c.execute('SELECT * FROM estudiantes")
#print (c.fetchall()) a list is generated

#Get data table features PRAGMA table_info(table1);

#Connect with bd or Create if doesnt exist
conn=sqlite3.connect('APP/DataStructures/Predict_model.db')


#Create cursor
c = conn.cursor()

#Delete columns
#crear una nueva tabla sin el campo que quieres eliminar,
#volcar los datos a esta,
#eliminar la tabla original
#renombrar la nueva tabla

#c.execute("""DROP TABLE t1_backup""")

c.execute("""CREATE TABLE t1_backup(Model_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_Time TEXT,
            Path_Model TEXT,
            N_epochs_Done INTEGER,
            Seed_Model_id_FRGN INTEGER,
            Colm_T_Predict INTEGER,
            loss REAL,
            mean_squared_error REAL,
            val_loss REAL,
            val_mean_squared_error REAL,
            FOREIGN KEY(Seed_Model_id_FRGN) REFERENCES Seed_Model(Seed_Model_id))""")

c.execute("""INSERT INTO t1_backup
            
            SELECT 
            Model_id,
            date_Time,
            Path_Model,
            N_epochs_Done,
            Seed_Model_id_FRGN,
            Colm_T_Predict,
            loss,
            mean_squared_error,
            val_loss,
            val_mean_squared_error 
            
            FROM Models""")


c.execute("""DROP TABLE Models""")


c.execute("""CREATE TABLE Models(Model_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_Time TEXT,
            Path_Model TEXT,
            N_epochs_Done INTEGER,
            Seed_Model_id_FRGN INTEGER,
            Colm_T_Predict INTEGER,
            loss REAL,
            mean_squared_error REAL,
            val_loss REAL,
            val_mean_squared_error REAL,
            FOREIGN KEY(Seed_Model_id_FRGN) REFERENCES Seed_Model(Seed_Model_id))""")

c.execute("""INSERT INTO Models SELECT
          
        Model_id,
        date_Time,
        Path_Model,
        N_epochs_Done,
        Seed_Model_id_FRGN,
        Colm_T_Predict,
        loss,
        mean_squared_error,
        val_loss,
        val_mean_squared_error
     
        FROM t1_backup""")

c.execute("""DROP TABLE t1_backup""")

conn.commit()