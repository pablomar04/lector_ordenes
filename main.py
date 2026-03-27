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
                # Verificar si la orden ya existe
                existing = collection.find_one({"orden": qr_data})
                if existing:
                    scanned_at = existing.get("scanned_at", "fecha desconocida")
                    raise ValueError(
                        f"La orden '{qr_data}' ya fue registrada el {scanned_at}."
                    )

                document = {
                    "orden": qr_data,
                    "scanned_at": datetime.datetime.now(),
                    "source": "handheld_scanner"
                }

                result = collection.insert_one(document)
                print(f"✅ Successfully uploaded: {qr_data}")
                print(f"   Database ID: {result.inserted_id}\n")

        except ValueError as e:
            print(f"⚠️  Orden duplicada: {e}\n")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    listen_for_scanner()
