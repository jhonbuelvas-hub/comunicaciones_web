from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

# -----------------------------
# LOGIN
# -----------------------------
def validar_usuario(username, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    return user


# -----------------------------
# PROTEGER RUTAS
# -----------------------------
def login_requerido():
    return "usuario" in session


# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = validar_usuario(username, password)

        if user:
            session["usuario"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -----------------------------
# DATOS
# -----------------------------
def obtener_comunicaciones(filtro="todas", busqueda=""):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        condicion = "WHERE 1=1"

        if filtro == "recibidas":
            condicion += " AND UPPER(tipo) = 'RECIBIDA'"
        elif filtro == "enviadas":
            condicion += " AND UPPER(tipo) = 'ENVIADA'"

        if busqueda:
            condicion += f"""
            AND (
                asunto LIKE '%{busqueda}%'
                OR emisor LIKE '%{busqueda}%'
                OR receptor LIKE '%{busqueda}%'
                OR radicado_interno LIKE '%{busqueda}%'
            )
            """

        query = f"""
            SELECT 
                id, fecha, radicado_interno, tipo,
                asunto, emisor, receptor, respondida
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
# HOME PROTEGIDO
# -----------------------------
@app.route("/")
def index():
    if not login_requerido():
        return redirect("/login")

    filtro = request.args.get("filtro", "todas")
    busqueda = request.args.get("q", "")

    comunicaciones = obtener_comunicaciones(filtro, busqueda)

    return render_template(
        "index.html",
        comunicaciones=comunicaciones,
        filtro=filtro,
        busqueda=busqueda
    )


if __name__ == "__main__":
    app.run(debug=True)
