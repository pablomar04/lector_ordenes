from pymongo import MongoClient
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Setup MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("No se encontró MONGO_URI en las variables de entorno.")

client = MongoClient(MONGO_URI)
db = client["work"]
collection = db["orders"]

def listen_for_scanner():
    print("--- QR Scanner Ready ---")
    print("Please scan a code now (or type 'exit' to quit)...")

    while True:
        try:
            qr_data = input("Scan Data: ").strip()

            if qr_data.lower() == 'exit':
                print("Exiting...")
                break

            if qr_data:
                document = {
                    "orden": qr_data,
                    "scanned_at": datetime.datetime.now(),
                    "source": "handheld_scanner"
                }
                
                result = collection.insert_one(document)
                print(f"✅ Successfully uploaded: {qr_data}")
                print(f"   Database ID: {result.inserted_id}\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    listen_for_scanner()
