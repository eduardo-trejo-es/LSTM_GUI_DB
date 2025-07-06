import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('APP/DataStructures/Predict_model.db')
c = conn.cursor()

# Columnas a agregar
columns_to_add = [
    "Stop_Loss REAL",
    "Take_Profit REAL",
    "Entry_Offset REAL",
    "priceRefClose REAL",
    "entyPriceRecmd REAL"
]

# Agregar columnas (una por una, como requiere SQLite)
for col in columns_to_add:
    try:
        c.execute(f"ALTER TABLE 'Forcasting_Resul' ADD COLUMN {col}")
        print(f"Columna agregada: {col}")
    except sqlite3.OperationalError as e:
        print(f"❌ Error al agregar {col}: {e}")

# Guardar cambios
conn.commit()

# Puedes cerrar la conexión si no haces más operaciones
conn.close()
