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
                asunto LIKE '%{busqueda}%' OR
                emisor LIKE '%{busqueda}%' OR
                receptor LIKE '%{busqueda}%' OR
                radicado_interno LIKE '%{busqueda}%'
            )
            """

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
