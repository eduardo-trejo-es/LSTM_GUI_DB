import sqlite3

#To see easy the db file is to drag bdfiel into:  https://inloop.github.io/sqlite-viewer/
#or by using the command c.execute('SELECT * FROM estudiantes")
#print (c.fetchall()) a list is generated

#Connect with bd or Create if doesnt exist
conn=sqlite3.connect('Predict_model.db')


#Create cursor
c = conn.cursor()


#Create tables
c.execute("""
        CREATE TABLE Models(
            Model_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_Time TEXT,
            Path_Model TEXT,
            N_epochs_Done INTEGER,
            Seed_Data_id_FRGN INTEGER,
            DataSet_id_FRGN INTEGER,
            Forcasting_Result_id_FRGN INTEGER,
            Colm_T_Predict,
            FOREIGN KEY(DataSet_id_FRGN) REFERENCES DataSet(DataSet_id),
            FOREIGN KEY(Seed_Data_id_FRGN) REFERENCES Seed_Data(Seed_Data_id),
            FOREIGN KEY(Forcasting_Result_id_FRGN) REFERENCES Forcasting_Resul(Forcasting_Resul_id)
        )
        """)

#
c.execute("""
        CREATE TABLE Seed_Data(
            Seed_Data_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Columns_N INTEGER,
            LSTM_1_N_Units INTEGER,
            LSTM_2_N_Units INTEGER,
            Lyr_Drop_Coeff REAL,
            Lyr_Dns_N_Units INTEGER,
            Lyr_Dns_Rgzr_Coeff REAL,
            Optmzer_Adam_Coeff TEXT,
            BackDays INTEGER
        )
        """)

c.execute("""
        CREATE TABLE Forcasting_Resul(
            Forcasting_Resul_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date_time TEXT,
            Total_Movement_Right INTEGER,
            Total_Movement_Right_Per100 REAL,
            Rows_Considered INTEGER,
            Total_Diff_Mag_earned REAL,
            Total_Diff_earned_Per100 REAL,
            Total_Diff_Mag_lose REAL,
            Total_Diff_lose_Per100 REAL,
            Total_Mag_Mvmnts REAL,
            Real_Mag_earned REAL,
            Real_earned_Per100 REAL
        )
    """)

c.execute("""
        CREATE TABLE DataSet(
            DataSet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date_Time TEXT,
            Path_DataSet TEXT,
            Seed_DataSet_id_FRGN INTEGER,
            FOREIGN KEY(Seed_DataSet_id_FRGN) REFERENCES Seed_DataSet(SeedDataSet_id)    
        )
    """)

c.execute("""
        CREATE TABLE Seed_DataSet(
            SeedDataSet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Item TEXT,
            BackDays INTEGER,
            Open_C INTEGER,
            High_C INTEGER,
            Low_C INTEGER,
            Close_C INTEGER,
            Volume_C INTEGER,
            Open_FFT_C INTEGER,
            High_FFT_C INTEGER,
            Low_FFT_C INTEGER,
            Close_FFT_C INTEGER,
            Volum_FFT_C INTEGER,
            Day_Wk_N_C INTEGER,
            Day_MonthNDay_C INTEGER,
            Year_C INTEGER,
            FFT_Frec TEXT
        )
    """)
