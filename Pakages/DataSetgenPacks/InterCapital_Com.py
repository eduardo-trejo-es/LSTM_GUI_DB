import requests
import pandas as pd
import os
from dotenv import load_dotenv
# Cargar variables del archivo .env
load_dotenv()
from datetime import datetime, timedelta

class InterFaceCapitalCom:
    
    def __init__(self,TU_API_KEY_,PasswordCaptial_,correoCapital_):
        self.TU_API_KEY=TU_API_KEY_
        #PasswordCaptial="EduPro12?"
        self.PasswordCaptial=PasswordCaptial_
        self.correoCapital= correoCapital_
        self.CST=""
        self.SECURITY_TOKEN=""  
        self.authentication()   
    
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

        response = requests.post(SESSION_URL, json=PAYLOAD, headers=HEADERS)

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
        
        return result
        
    def BrutRetriveData(self, epic,from_, to_, resolution, max): 
        
        #Note: resolution : MINUTE, MINUTE_5, MINUTE_15, MINUTE_30, HOUR, HOUR_4, DAY, WEEK
        # 📌 EPIC del instrumento financiero que deseas consultar
        df= pd.DataFrame()
        EPIC = epic  # Cambia esto por el EPIC correcto

        # 📌 Parámetros para la consulta de precios
        PARAMS = {
            "resolution": resolution,
            "max": max,
            "from": from_,
            "to": to_
        }

        # 📌 Encabezados de autenticación
        HEADERS = {
            "X-SECURITY-TOKEN": self.SECURITY_TOKEN,
            "CST": self.CST,
            "X-CAP-API-KEY": self.TU_API_KEY  # Opcional, pero puede ayudar a evitar errores
        }

        print("\n Datos que se enviarán en la autenticación:")
        print(" X-SECURITY-TOKEN:", HEADERS["X-SECURITY-TOKEN"])
        print(" CST:", HEADERS["CST"])
        print(" X-CAP-API-KEY:", HEADERS["X-CAP-API-KEY"])
        
        print("parametters: -----------vvvvvvvv--------------")
        print("\n resolution: "+str(resolution))
        print(" max:", str(max))
        print(" from_: ", str(from_))
        print(" to_:", str(to_))
        
        #  Hacer la solicitud GET
        PRICES_URL = f"https://api-capital.backend-capital.com/api/v1/prices/{EPIC}"
        response = requests.get(PRICES_URL, headers=HEADERS, params=PARAMS)

        # Manejo de respuesta
        if response.status_code == 200:
            data = response.json()  # Convertimos la respuesta a JSON

            # Extraer la lista de precios desde el JSON
            if "prices" in data:
                price_data = data["prices"]

                # Convertir a un DataFrame de pandas
                df = pd.DataFrame(price_data)
                # Expandir columnas anidadas si es necesario
                if "openPrice" in df.columns:
                    df["Date"] = df["snapshotTimeUTC"]
                    df["Open"] = df["openPrice"].apply(lambda x: x["bid"])
                    df["High"] = df["highPrice"].apply(lambda x: x["bid"])
                    df["Low"] = df["lowPrice"].apply(lambda x: x["bid"])
                    df["Close"] = df["closePrice"].apply(lambda x: x["bid"])
                    df["Volume"] = df["lastTradedVolume"]
                    df.drop(["snapshotTimeUTC","snapshotTime","openPrice", "closePrice", "highPrice", "lowPrice","lastTradedVolume"], axis=1, inplace=True)
                    df.set_index("Date", inplace=True)


            else:
                print("No se encontraron datos de precios en la respuesta.")
        else:
            print(f"Error al obtener precios: {response.status_code}")
            print(response.text)
            
        
        return df
    
    def RetriveData(self, epic,from_, to_, resolution, max): 
        
        #Note: resolution : MINUTE, MINUTE_5, MINUTE_15, MINUTE_30, HOUR, HOUR_4, DAY, WEEK
        #EPIC del instrumento financiero que deseas consultar
        df_last= pd.DataFrame()
        df_init= pd.DataFrame()
        df=pd.DataFrame()
        to_Prov=""
        EPIC = epic  # Cambia esto por el EPIC correcto
        tries=0
        
        
        #Convertir la cadena a un objeto datetime
        from_dt = datetime.strptime(from_, "%Y-%m-%dT%H:%M:%S")
        # 📌 Sumar días (por ejemplo, 3 días)
        day_to_add = max
        to_Prov = from_dt + timedelta(days=day_to_add)
        to_Prov_str = to_Prov.strftime("%Y-%m-%dT%H:%M:%S")
        
        
        while tries<(max*10000):
            print(tries)
            print("new from"+from_)
            df_init=self.BrutRetriveData(epic,from_,to_Prov_str,resolution,max)
        
            df=pd.concat([df_last,df_init])
            # 📌 Eliminar índices duplicados y mantener solo la primera aparición
            
            df_last=df
            #Convertir la cadena a un objeto datetime
            try:
                if df_init.index[-1]==to_:
                    break
                
                from_=df_init.index[-1]    
                
                from_dt = datetime.strptime(from_, "%Y-%m-%dT%H:%M:%S")
                # 📌 Sumar días (por ejemplo, 3 días)
                day_to_add = max
                to_Prov = from_dt + timedelta(days=day_to_add)
                to_Prov_str = to_Prov.strftime("%Y-%m-%dT%H:%M:%S")
            except:
                print("capital df empty")
                break
                
        
        try:
            df = df.loc[~df.index.duplicated(keep="first")]
        except:
            print("capital df empty")
            
            
        return df
    


"""TU_API_KEY=os.getenv("TU_API_KEY")
PasswordCaptial=os.getenv("PASSWORDCAPITAL")
correoCapital= os.getenv("EMAILUSER")
print("--------------------------------------")
print(TU_API_KEY)
print(PasswordCaptial)
print("--------------------------------------")
instance = InterFaceCapitalCom(TU_API_KEY,PasswordCaptial,correoCapital)


epic= "OIL_CRUDE"  
resolution= "DAY" 
max = 999
StartDay="1983-03-30T00:00:00"
#EndDate="2001-06-15"
from_= "1983-03-30T00:00:00"
to= "2025-02-14T00:00:00"
df=instance.RetriveData(epic,from_, to, resolution, max)
#df=instance.RetriveData(epic,from_,to,resolution,max)

print(df)"""