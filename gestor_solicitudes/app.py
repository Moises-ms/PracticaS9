from flask import (Flask, render_template, request, redirect,
                   url_for, flash)
import logica

app = Flask(__name__)
app.secret_key = "solo-para-aprendizaje-local"


def vista(**extra):
    return render_template(
        "index.html",
        pendientes=logica.cola_pendientes,
        historial=logica.pila_historial,
        siguiente=logica.consultar_siguiente(),
        stats=logica.estadisticas(),
        **extra,
    )


@app.get("/")
def inicio():
    return vista()


@app.post("/registrar")
def registrar():
    s, error = logica.registrar_con_control(
        request.form.get("cliente", ""), request.form.get("asunto", ""))
    if error == "duplicado":
        flash("Ya existe una solicitud pendiente igual (mismo cliente y asunto).", "warning")
    elif error:
        flash("Cliente y asunto son obligatorios.", "danger")
    else:
        flash(f"Solicitud #{s['id']} registrada.", "success")
    return redirect(url_for("inicio"))


@app.post("/atender")
def atender():
    s = logica.atender_siguiente()
    flash(f"Atendida: #{s['id']} {s['cliente']}." if s else "No hay pendientes.",
          "success" if s else "info")
    return redirect(url_for("inicio"))


@app.post("/deshacer")
def deshacer():
    s = logica.deshacer_ultima_atencion()
    flash(f"Restaurada: #{s['id']} {s['cliente']}." if s else "No hay atenciones que deshacer.",
          "success" if s else "info")
    return redirect(url_for("inicio"))


@app.get("/buscar")
def buscar():
    texto = request.args.get("id", "").strip()
    if not texto.isdigit():
        flash("Ingresa un ID numérico válido.", "danger")
        return redirect(url_for("inicio"))
    encontrado = logica.buscar_solicitud(int(texto))
    return vista(busqueda=texto, resultado=encontrado)


@app.post("/cancelar/<int:id_solicitud>")
def cancelar(id_solicitud):
    s = logica.cancelar_solicitud(id_solicitud)
    flash(f"Cancelada: #{s['id']}." if s else "Esa solicitud no está pendiente.",
          "success" if s else "warning")
    return redirect(url_for("inicio"))


@app.post("/deshacer-varias")
def deshacer_varias():
    texto = request.form.get("cantidad", "").strip()
    if not texto.isdigit() or int(texto) < 1:
        flash("La cantidad debe ser un entero mayor que 0.", "danger")
    else:
        restauradas = logica.deshacer_varias(int(texto))
        flash(f"Se restauraron {len(restauradas)} solicitud(es).",
              "success" if restauradas else "info")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
