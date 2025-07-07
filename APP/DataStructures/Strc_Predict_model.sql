-- Exportación solo de estructura de: APP/DataStructures/Predict_model.db

CREATE TABLE Seed_Model(
            Seed_Model_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Columns_N INTEGER,
            LSTM_1_N_Units INTEGER,
            LSTM_2_N_Units INTEGER,
            Lyr_Drop_Coeff REAL,
            Lyr_Dns_N_Units INTEGER,
            Lyr_Dns_Rgzr_Coeff REAL,
            Optmzer_Adam_Coeff TEXT,
            BackDays INTEGER
        );

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
            Real_earned_Per100 REAL,
            Model_id_FRGN INTEGER, Path_Forcast TEXT, Total_Mag_Mvmnts_Per100 REAL, EvalForcastPath TEXT, Stop_Loss REAL, Take_Profit REAL, Entry_Offset REAL, priceRefClose REAL, entyPriceRecmd REAL,
            FOREIGN KEY(Model_id_FRGN) REFERENCES Models(Model_id)
        );

CREATE TABLE DataSet(
            DataSet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date_Time TEXT,
            Path_DataSet TEXT,
            Seed_DataSet_id_FRGN INTEGER,
            FOREIGN KEY(Seed_DataSet_id_FRGN) REFERENCES Seed_DataSet(SeedDataSet_id)    
        );

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
        , UpDown_C INTEGER, UpDown_Clmn INTEGER, DevStnd_C INTEGER, MaxBackDist INTEGER, backPeriod INTEGER, BollngBand_C INTEGER);

CREATE TABLE Relation_Model_Datasets(
            Rltion_ModelDataSet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Model_id_FRGN INTEGER,
            DataSet_id_FRGN INTEGER,
            FOREIGN KEY(Model_id_FRGN) REFERENCES Models(Model_id),
            FOREIGN KEY(DataSet_id_FRGN) REFERENCES DataSet(DataSet_id)
        );

CREATE TABLE Models(Model_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_Time TEXT,
            Path_Model TEXT,
            N_epochs_Done INTEGER,
            Seed_Model_id_FRGN INTEGER,
            Colm_T_Predict INTEGER,
            loss REAL,
            mean_squared_error REAL,
            val_loss REAL,
            val_mean_squared_error REAL,
            FOREIGN KEY(Seed_Model_id_FRGN) REFERENCES Seed_Model(Seed_Model_id));

