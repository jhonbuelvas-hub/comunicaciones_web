from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def obtener_comunicaciones(filtro="todas"):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        condicion = ""

        if filtro == "recibidas":
            condicion = "WHERE UPPER(tipo) = 'RECIBIDA'"
        elif filtro == "enviadas":
            condicion = "WHERE UPPER(tipo) = 'ENVIADA'"

        query = f"""
            SELECT id, fecha, radicado_interno, tipo, asunto, emisor, receptor
            FROM comunicaciones
            {condicion}
            ORDER BY fecha DESC
        """

        cursor.execute(query)
        datos = cursor.fetchall()
        conn.close()
        return datos

    except Exception as e:
        print("ERROR:", e)
        return []


@app.route("/")
def index():
    filtro = request.args.get("filtro", "todas")
    comunicaciones = obtener_comunicaciones(filtro)
    return render_template("index.html", comunicaciones=comunicaciones, filtro=filtro)


if __name__ == "__main__":
    app.run(debug=True)
