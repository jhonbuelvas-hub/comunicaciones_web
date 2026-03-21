from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta"

# -----------------------------
# LOGIN
# -----------------------------
def validar_usuario(usuario, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE usuario = ? AND password = ?
    """, (usuario, password))

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
        usuario = request.form["usuario"]
        password = request.form["password"]

        user = validar_usuario(usuario, password)

        if user:
            session["usuario"] = usuario
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
# CONSULTA COMUNICACIONES
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
        SELECT id, fecha, tipo, asunto, responsable,
               fecha_limite, respondida
        FROM comunicaciones
        {condicion}
        ORDER BY fecha DESC
    """

    cursor.execute(query)
    datos = cursor.fetchall()
    conn.close()
    return datos


# -----------------------------
# HOME (PROTEGIDO)
# -----------------------------
@app.route("/")
def index():
    if not login_requerido():
        return redirect("/login")

    filtro = request.args.get("filtro", "todas")
    datos = obtener_comunicaciones(filtro)

    return render_template("index.html", comunicaciones=datos, filtro=filtro)


# -----------------------------
# NUEVA COMUNICACION
# -----------------------------
@app.route("/nueva", methods=["GET", "POST"])
def nueva():
    if not login_requerido():
        return redirect("/login")

    if request.method == "POST":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO comunicaciones (
            fecha, fecha_llegada, tipo, medio,
            asunto, emisor, receptor,
            radicado_interno, radicado_externo,
            especialidad, responsable, prioridad,
            fecha_limite, dias_respuesta,
            observaciones, respondida
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            request.form["fecha"],
            request.form["fecha_llegada"],
            request.form["tipo"],
            request.form["medio"],
            request.form["asunto"],
            request.form["emisor"],
            request.form["receptor"],
            request.form["radicado_interno"],
            request.form["radicado_externo"],
            request.form["especialidad"],
            request.form["responsable"],
            request.form["prioridad"],
            request.form["fecha_limite"],
            request.form["dias_respuesta"],
            request.form["observaciones"]
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("form.html", accion="Nueva", c=None)


# -----------------------------
# EDITAR COMUNICACION
# -----------------------------
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if not login_requerido():
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute("""
        UPDATE comunicaciones SET
            fecha=?, fecha_llegada=?, tipo=?, medio=?,
            asunto=?, emisor=?, receptor=?,
            radicado_interno=?, radicado_externo=?,
            especialidad=?, responsable=?, prioridad=?,
            fecha_limite=?, dias_respuesta=?,
            observaciones=?, respondida=?
        WHERE id=?
        """, (
            request.form["fecha"],
            request.form["fecha_llegada"],
            request.form["tipo"],
            request.form["medio"],
            request.form["asunto"],
            request.form["emisor"],
            request.form["receptor"],
            request.form["radicado_interno"],
            request.form["radicado_externo"],
            request.form["especialidad"],
            request.form["responsable"],
            request.form["prioridad"],
            request.form["fecha_limite"],
            request.form["dias_respuesta"],
            request.form["observaciones"],
            request.form.get("respondida", 0),
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute("""
    SELECT id, fecha, fecha_llegada, tipo, medio,
           asunto, emisor, receptor,
           radicado_interno, radicado_externo,
           especialidad, responsable, prioridad,
           fecha_limite, dias_respuesta,
           observaciones, respondida
    FROM comunicaciones WHERE id=?
    """, (id,))

    c = cursor.fetchone()
    conn.close()

    return render_template("form.html", accion="Editar", c=c)


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
