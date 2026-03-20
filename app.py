from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def obtener_comunicaciones():
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, fecha, radicado_interno, tipo, asunto, emisor, receptor
            FROM comunicaciones
            ORDER BY fecha DESC
        """)

        datos = cursor.fetchall()
        conn.close()
        return datos

    except Exception as e:
        print("ERROR:", e)
        return []

@app.route("/")
def index():
    comunicaciones = obtener_comunicaciones()
    return render_template("index.html", comunicaciones=comunicaciones)


if __name__ == "__main__":
    app.run(debug=True)
