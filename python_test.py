import time
import sys
sys.path.append("Pakages/DataSetgenPacks")

from datetime import datetime, timedelta
from InterCapital_Com import InterFaceCapitalCom


# 🔐 Credenciales y configuración
correo = "paginalalo9@gmail.com"
contrasena = "qwerTyui1?"
api_key = "OuPiou9fpS5M6HLD"
epic = "OIL_CRUDE"  # Cambiar por otro si deseas probar otro instrumento
start_date = "2025-07-29T00:00:00"
max_days_back = 10

# 🧠 Crear instancia de la clase
api = InterFaceCapitalCom(api_key, contrasena, correo)
api.authentication()


# 📆 Definir rango para el 27 de julio de 2025
from_date = "2025-07-25T00:00:00"
to_date = "2025-07-26T00:00:00"

# 🕒 Usar resolución 'HOUR'
resolution = "HOUR"
max_points = 1000  # puedes ajustar este valor según necesidad

print(f"\n📊 Probando recuperación de datos por hora para el {from_date} ➝ {to_date}")
result = api.BrutRetriveData(epic, from_date, to_date, resolution, max_points)

# 📋 Mostrar resumen del resultado
if result is not None and not result.empty:
    print(f"✅ Datos recibidos: {len(result)} puntos")
    for entry in result:
        print(entry)

    import pandas as pd

    # Convertir a DataFrame y guardar en CSV
    df = pd.DataFrame(result)
    df.to_csv("OIL_CRUDE_Hourly_2025_07_27.csv", index=False)
    print("💾 Datos guardados en OIL_CRUDE_Hourly_2025_07_27.csv")
else:
    print("❌ No se recibieron datos.")
