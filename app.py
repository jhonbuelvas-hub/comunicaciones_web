from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# -----------------------------
# FUNCION PRINCIPAL
# -----------------------------
def obtener_comunicaciones(filtro="todas", busqueda=""):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        condicion = "WHERE 1=1"

        # FILTRO POR TIPO
        if filtro == "recibidas":
            condicion += " AND UPPER(tipo) = 'RECIBIDA'"
        elif filtro == "enviadas":
            condicion += " AND UPPER(tipo) = 'ENVIADA'"

        # BUSCADOR
        if busqueda:
            condicion += f"""
            AND (
                asunto LIKE '%{busqueda}%'
                OR emisor LIKE '%{busqueda}%'
                OR receptor LIKE '%{busqueda}%'
                OR radicado_interno LIKE '%{busqueda}%'
            )
            """

        # CONSULTA
        query = f"""
            SELECT 
                id,
                fecha,
                radicado_interno,
                tipo,
                asunto,
                emisor,
                receptor,
                respondida
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


# -----------------------------
# RUTA PRINCIPAL
# -----------------------------
@app.route("/")
def index():
    filtro = request.args.get("filtro", "todas")
    busqueda = request.args.get("q", "")

    comunicaciones = obtener_comunicaciones(filtro, busqueda)

    return render_template(
        "index.html",
        comunicaciones=comunicaciones,
        filtro=filtro,
        busqueda=busqueda
    )


# -----------------------------
# EJECUCION LOCAL
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
