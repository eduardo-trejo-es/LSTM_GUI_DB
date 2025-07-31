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

# 🔍 Ejecutar prueba de resolución
api.test_resolution_range(epic, start_date=start_date, max_days_back=max_days_back)

# 🚨 Test directo: ¿realmente hay datos horarios para OIL_CRUDE?
print("\n🚨 Test directo para verificar datos horarios (esperado: 24 filas)")
from_str = "2025-07-27T00:00:00"
to_str = "2025-07-27T23:59:00"
df_hour = api.BrutRetriveData(epic, from_str, to_str, resolution="HOUR", maxcandles=100)
print(f"🔢 Filas devueltas para 1 día con resolución HOUR: {len(df_hour)}")
print(df_hour.head())