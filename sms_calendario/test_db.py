# test_db.py
import psycopg2
from config import DB_PARAMS

try:
    print("Intentando conectar a la base de datos...")
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM reportes.sms_programado;")
    count = cur.fetchone()[0]
    print(f"Conexión exitosa. Registros actuales en sms_programado: {count}")
    cur.close()
    conn.close()
except Exception as e:
    print("Error al conectar a la base de datos:", e)

