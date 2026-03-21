from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta"

# -----------------------------
# LOGIN
# -----------------------------
def validar_usuario(username, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE usuario = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()
    return user


def login_requerido():
    return "usuario" in session


# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = validar_usuario(
            request.form["username"],
            request.form["password"]
        )

        if user:
            session["usuario"] = request.form["username"]
            return redirect("/")
        else:
            return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -----------------------------
# CONSULTA
# -----------------------------
def obtener_comunicaciones(filtro="todas"):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    condicion = ""

    if filtro == "recibidas":
        condicion = "WHERE UPPER(tipo) = 'RECIBIDA'"
    elif filtro == "enviadas":
        condicion = "WHERE UPPER(tipo) = 'ENVIADA'"

    query = f"""
        SELECT id, fecha, radicado_interno, tipo,
               asunto, emisor, receptor, respondida
        FROM comunicaciones
        {condicion}
        ORDER BY fecha DESC
    """

    cursor.execute(query)
    datos = cursor.fetchall()
    conn.close()
    return datos


# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def index():
    if not login_requerido():
        return redirect("/login")

    filtro = request.args.get("filtro", "todas")
    datos = obtener_comunicaciones(filtro)

    return render_template("index.html", comunicaciones=datos, filtro=filtro)


# -----------------------------
# NUEVA
# -----------------------------
@app.route("/nueva", methods=["GET", "POST"])
def nueva():
    if not login_requerido():
        return redirect("/login")

    if request.method == "POST":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO comunicaciones
            (fecha, radicado_interno, tipo, asunto, emisor, receptor, respondida)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (
            request.form["fecha"],
            request.form["radicado"],
            request.form["tipo"],
            request.form["asunto"],
            request.form["emisor"],
            request.form["receptor"]
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("form.html", accion="Nueva", c=None)


# -----------------------------
# EDITAR
# -----------------------------
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if not login_requerido():
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute("""
            UPDATE comunicaciones
            SET fecha=?, radicado_interno=?, tipo=?, asunto=?, emisor=?, receptor=?
            WHERE id=?
        """, (
            request.form["fecha"],
            request.form["radicado"],
            request.form["tipo"],
            request.form["asunto"],
            request.form["emisor"],
            request.form["receptor"],
            id
        ))

        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM comunicaciones WHERE id=?", (id,))
    c = cursor.fetchone()
    conn.close()

    return render_template("form.html", accion="Editar", c=c)


if __name__ == "__main__":
    app.run(debug=True)
