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
        username = request.form["username"]
        password = request.form["password"]

        user = validar_usuario(username, password)

        if user:
            session["usuario"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -----------------------------
# LISTAR
# -----------------------------
def obtener_comunicaciones():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, fecha, radicado_interno, tipo, asunto, emisor, receptor, respondida
        FROM comunicaciones
        ORDER BY fecha DESC
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos


@app.route("/")
def index():
    if not login_requerido():
        return redirect("/login")

    datos = obtener_comunicaciones()
    return render_template("index.html", comunicaciones=datos)


# -----------------------------
# NUEVA COMUNICACION
# -----------------------------
@app.route("/nueva", methods=["GET", "POST"])
def nueva():
    if not login_requerido():
        return redirect("/login")

    if request.method == "POST":
        data = (
            request.form["fecha"],
            request.form["radicado"],
            request.form["tipo"],
            request.form["asunto"],
            request.form["emisor"],
            request.form["receptor"]
        )

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO comunicaciones
            (fecha, radicado_interno, tipo, asunto, emisor, receptor, respondida)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        """, data)

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("form.html", accion="Nueva")


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

        data = (
            request.form["fecha"],
            request.form["radicado"],
            request.form["tipo"],
            request.form["asunto"],
            request.form["emisor"],
            request.form["receptor"],
            id
        )

        cursor.execute("""
            UPDATE comunicaciones
            SET fecha=?, radicado_interno=?, tipo=?, asunto=?, emisor=?, receptor=?
            WHERE id=?
        """, data)

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute("SELECT * FROM comunicaciones WHERE id=?", (id,))
    comunicacion = cursor.fetchone()
    conn.close()

    return render_template("form.html", accion="Editar", c=comunicacion)


if __name__ == "__main__":
    app.run(debug=True)
