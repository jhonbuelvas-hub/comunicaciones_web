@app.route("/nueva", methods=["GET", "POST"])
def nueva():
    if "usuario" not in session:
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
