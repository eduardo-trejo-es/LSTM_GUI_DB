import requests
import certifi
import ssl
import pandas as pd
import os
import time
from dotenv import load_dotenv
# Cargar variables del archivo .env
load_dotenv()
from datetime import datetime, timedelta
import urllib3
from types import SimpleNamespace
import json
import urllib.parse

class InterFaceCapitalCom:
    
    def __init__(self,TU_API_KEY_,PasswordCaptial_,correoCapital_):
        self.TU_API_KEY=TU_API_KEY_
        #PasswordCaptial="EduPro12?"
        self.PasswordCaptial=PasswordCaptial_
        self.correoCapital= correoCapital_
        self.CST=""
        self.SECURITY_TOKEN=""  
        #self.authentication()
    
    def authentication(self):  
        result="" 
                # 📌 Endpoint de autenticación
        SESSION_URL = "https://api-capital.backend-capital.com/api/v1/session"

        PAYLOAD = {
            "identifier": self.correoCapital,  # Usuario de Capital.com
            "password": self.PasswordCaptial,  # 🚀 Ahora usamos la contraseña cifrada con timestamp
            "encryptedPassword": False  # IMPORTANTE: Debe estar en True
        }

        HEADERS = {
            "X-CAP-API-KEY": self.TU_API_KEY,
            "Content-Type": "application/json"
        }

        print("\n📌 Datos que se enviarán en la autenticación:")
        print("📧 Correo:", PAYLOAD["identifier"])
        print("🔒 Contraseña cifrada:", PAYLOAD["password"])
        print("🔑 API Key:", HEADERS["X-CAP-API-KEY"])
        
        # Avant d'appeler requests

        try:
            
            # 🔐 Créer un contexte SSL propre
            ssl_context = ssl.create_default_context(cafile=certifi.where())

            # 🌐 Créer un gestionnaire HTTP sécurisé
            http = urllib3.PoolManager(ssl_context=ssl_context)

            # 🔄 Encoder les données JSON
            encoded_payload = json.dumps(PAYLOAD).encode('utf-8')

            # 📡 Requête POST via urllib3
            response_raw = http.request(
                "POST",
                SESSION_URL,
                body=encoded_payload,
                headers=HEADERS
            )

            # 📦 Adapter la réponse pour rester compatible avec le reste du code
            response = SimpleNamespace(
                status_code=response_raw.status,
                headers=response_raw.headers,
                text=response_raw.data.decode()
            )

            if response.status_code == 200:
                print("✅ Autenticación exitosa")
                result="Autenticación exitosa"
                tokens = response.headers
                self.CST = tokens.get("CST")
                self.SECURITY_TOKEN = tokens.get("X-SECURITY-TOKEN")
                print("CST Token:", self.CST)
                print("X-SECURITY-TOKEN:", self.SECURITY_TOKEN)
            else:
                print(f"❌ Error en la autenticación: {response.status_code}")
                result=f"❌ Error en la autenticación: {response.status_code}"
                print(response.text)
        except Exception as e:
            print(f"❌ EXCEPTION during authentication: {str(e)}")
            result = f"❌ Exception: {str(e)}"
            
        
        return result
        
    def BrutRetriveData(self, epic, from_, to_, resolution, max): 
        print("🟢 Entering BrutRetriveData()...")
        
        # Define request parameters
        PARAMS = {
            "resolution": resolution,
            "max": max,
            "from": from_,
            "to": to_
        }

        HEADERS = {
            "X-SECURITY-TOKEN": self.SECURITY_TOKEN,
            "CST": self.CST,
            "X-CAP-API-KEY": self.TU_API_KEY
        }

        PRICES_URL = f"https://api-capital.backend-capital.com/api/v1/prices/{epic}"

        print(f"📡 Fetching data from API: {PRICES_URL}")
        print(f"📅 Time Range: {from_} ➝ {to_}")
        
        try:
            # Create clean SSL context
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            http = urllib3.PoolManager(ssl_context=ssl_context)

            # Encode params to URL query string
            query_string = urllib.parse.urlencode(PARAMS)
            full_url = f"{PRICES_URL}?{query_string}"
            print(f"🔍 Full URL with params: {full_url}")

            # Send GET request manually
            response = http.request("GET", full_url, headers=HEADERS, timeout=30.0)

            # Set a timeout of 30 seconds
            #response = requests.get(PRICES_URL, headers=HEADERS, params=PARAMS, timeout=30,verify=certifi.where())

            print(f"🔄 API Response Status: {response.status}")

            if response.status != 200:
                print(f"❌ API Request Failed! Status Code: {response.status}")
                print(f"❌ Response: {response.data.decode()}")
                return pd.DataFrame()

            data = json.loads(response.data.decode())
            
            # Check if the response contains price data
            if "prices" not in data or not data["prices"]:
                print("⚠️ WARNING: API returned empty data!")
                return pd.DataFrame()

            # Convert to DataFrame
            df = pd.DataFrame(data["prices"])

            # Expand columns
            if "openPrice" in df.columns:
                df["Date"] = df["snapshotTimeUTC"]
                df["Open"] = df["openPrice"].apply(lambda x: x["bid"])
                df["High"] = df["highPrice"].apply(lambda x: x["bid"])
                df["Low"] = df["lowPrice"].apply(lambda x: x["bid"])
                df["Close"] = df["closePrice"].apply(lambda x: x["bid"])
                df["Volume"] = df["lastTradedVolume"]
                df.drop(["snapshotTimeUTC", "snapshotTime", "openPrice", "closePrice", 
                        "highPrice", "lowPrice", "lastTradedVolume"], axis=1, inplace=True)
                df.set_index("Date", inplace=True)

            print(f"✅ Successfully retrieved {len(df)} rows of data.")
            return df

        except urllib3.exceptions.HTTPError as e:
                print(f"❌ ERROR: HTTP error: {str(e)}")
                return pd.DataFrame()
        except Exception as e:
                print(f"❌ ERROR: An unexpected error occurred: {str(e)}")
                return pd.DataFrame()
    
    def RetriveData(self, epic, from_, to_, resolution, max_per_request=999): 
        print("🟢 Entering RetriveData()")
        
        #Verify Token expiration
        if not self.tokens_valid():
            print("🔐 Autenticación requerida. Ejecutando login...")
            auth_result = self.authentication()
            if "❌" in auth_result:
                print("❌ Falló la autenticación. Cancelando recuperación de datos.")
                return pd.DataFrame()

        df = pd.DataFrame()  # DataFrame final donde se almacenarán los datos
        EPIC = epic  
        tries = 0  
        MAX_TRIES = 1000  # Máximo número de intentos para evitar bucles infinitos

        from_dt = datetime.strptime(from_, "%Y-%m-%dT%H:%M:%S")
        to_dt = datetime.strptime(to_, "%Y-%m-%dT%H:%M:%S")

        total_days = (to_dt - from_dt).days  # Número total de días a recuperar
        processed_days = 0  # Lleva el seguimiento de los días procesados

        while from_dt < to_dt and tries < MAX_TRIES:
            # 🔹 Definir el nuevo límite: 999 días o los días restantes
            remaining_days = (to_dt - from_dt).days

            if resolution.upper() == "HOUR":
                # Para resolución HOUR, limitamos el bloque a máximo 3 días
                days_to_fetch = min(remaining_days, 3)
            else:
                days_to_fetch = min(remaining_days, max_per_request)

            # 🔹 Calcular la nueva fecha límite
            to_Prov = from_dt + timedelta(days=days_to_fetch)
            to_Prov_str = to_Prov.strftime("%Y-%m-%dT%H:%M:%S")
            from_str = from_dt.strftime("%Y-%m-%dT%H:%M:%S")

            print(f"🔄 Attempt {tries + 1}/{MAX_TRIES}: Fetching from {from_str} to {to_Prov_str}")

            df_new = self.BrutRetriveData(EPIC, from_str, to_Prov_str, resolution, max_per_request)

            if df_new.empty:
                print("⚠️ API returned no data. Stopping.")
                break  # ⛔ Evita bucles innecesarios

            df = pd.concat([df, df_new])  # Agregar nuevos datos al DataFrame final

            # 🔹 Actualizar la fecha de inicio para la siguiente iteración
            from_dt = to_Prov
            processed_days += days_to_fetch

            # 🔥 Emitir progreso en tiempo real
            progress = int((processed_days / total_days) * 100)
            print(f"📊 Progress: {progress}% complete")
            #self.socketio.emit("Update_progress", {"status": "Retrieving data...", "progress": progress})

            tries += 1  # Incrementar el contador de intentos
            time.sleep(4)  # Evitar saturar la API

        # 🗑️ Eliminar duplicados antes de devolver los datos
        if not df.empty:
            print("🗑️ Removing duplicate rows")
            df = df.loc[~df.index.duplicated(keep="first")]

        print("✅ Data retrieval completed!")
        return df


    def calculate_variable_days(self, from_date, limit=1, depth=0, max_depth=10):
        today = datetime.today()
        #from_dt = datetime.strptime(from_date, "%Y-%m-%dT%H:%M:%S")
        from_dt=from_date
        
        remaining_days = (today - from_dt).days  # 🔹 Días faltantes hasta hoy

        if remaining_days <= 0:
            return from_date  # ✅ Si la fecha de inicio es hoy o en el futuro, no hacemos nada

        # 🔥 Si quedan más de `limit` días, sumamos `limit`, si no, sumamos los días restantes
        dynamic_max = min(remaining_days, limit)

        to_Prov = from_dt + timedelta(days=dynamic_max)

        return to_Prov.strftime("%Y-%m-%dT%H:%M:%S"),remaining_days

    def tokens_valid(self):
        # Si los tokens están vacíos, no son válidos
        if not self.CST or not self.SECURITY_TOKEN:
            return False

        # 🔍 Realiza un ping a una ruta protegida para ver si sigue autenticado
        TEST_EPIC = "OIL_CRUDE"  # Un epic conocido cualquiera
        TEST_URL = f"https://api-capital.backend-capital.com/api/v1/prices/{TEST_EPIC}?resolution=MINUTE&max=1"

        HEADERS = {
            "X-SECURITY-TOKEN": self.SECURITY_TOKEN,
            "CST": self.CST,
            "X-CAP-API-KEY": self.TU_API_KEY
        }

        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            http = urllib3.PoolManager(ssl_context=ssl_context)
            response = http.request("GET", TEST_URL, headers=HEADERS, timeout=10)

            if response.status in [401, 403]:
                print("🔒 Tokens caducados.")
                return False

            print("🔐 Tokens aún válidos.")
            return True

        except Exception as e:
            print(f"❌ Error al validar tokens: {str(e)}")
            return False