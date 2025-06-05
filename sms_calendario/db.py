import psycopg2
from config import DB_PARAMS
from datetime import datetime

def get_log_mensajeria():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT fecha, funcion, registros FROM reportes.log_mensajeria")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    eventos = []
    for fecha, funcion, registros in rows:
        eventos.append({
            "title": f"{funcion} ({registros})",    
            "start": fecha.isoformat(),
            "color": "#3182ce" if 'sms' in funcion.lower() else "#38a169",
            "editable": False
        })
    return eventos
        


def  get_sms_programado():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT tipo, fecha_envio, d1, h1, d2, h2 FROM reportes.sms_programado")
    rows = cur.fetchall()
    cur.close()
    conn.close()    

    eventos = []

    for tipo, fecha_envio, d1, h1, d2, h2 in rows:
        eventos.append(
            {
        "title": f"{tipo}: Día {d1} {h1} → Día {d2} {h2}",
        "start": fecha_envio.isoformat(),
        "color": "#9f7aea",
        "editable": True,
        "extendedProps": {
            "tipo": tipo, "d1": d1, "h1": h1, "d2": d2, "h2": h2
            }
        }
        )

    return eventos

def insertar_programacion(data):
    print(">>> DATOS RECIBIDOS:", data)

    fecha_inicio = data["fecha_inicio"]
    fecha_fin = data["fecha_fin"]
    d1 = str(int(fecha_inicio.split("-")[2]))
    d2 = str(int(fecha_fin.split("-")[2]))
    h1 = datetime.strptime(data["hora_inicio"], "%H:%M").strftime("%I:%M %p").lower()
    h2 = datetime.strptime(data["hora_fin"], "%H:%M").strftime("%I:%M %p").lower()


    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        print(">>> Conexión exitosa")
        cur.execute( """
            INSERT INTO reportes.sms_programado(tipo, fecha_envio, d1, h1, d2, h2)
            VALUES (%s, %s, %s, %s, %s, %s)    
        """, (
            data["tipo"],
            fecha_inicio,
            d1,
            h1,
            d2,
            h2
        ))
        conn.commit()
        print(">>> INSERT realizado correctamente")

        cur.close()
        conn.close()
    except Exception as e:
        print(">>> ERROR durante inserción:", e)
