from flask import Flask, render_template, redirect, url_for, flash, request  # type: ignore[reportMissingImports]
from flask_login import LoginManager, login_user, logout_user, login_required  # type: ignore[reportMissingImports]
from flask_wtf.csrf import CSRFProtect  # type: ignore[reportMissingImports]
from flask_mail import Mail, Message  # type: ignore[reportMissingImports]
from werkzeug.security import check_password_hash  # type: ignore[reportMissingImports]
from datetime import datetime, timezone

try:
    from .config import Config
    from .models import db, Usuario, Ubicacion, Ticket
    from .forms import TicketForm, LoginForm
except ImportError:  # pragma: no cover
    from config import Config
    from models import db, Usuario, Ubicacion, Ticket
    from forms import TicketForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

csrf = CSRFProtect(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))


ESTATUS_LEGIBLE = {
    "pendiente": "Pendiente",
    "en_proceso": "En proceso",
    "resuelto": "Resuelto",
}


def enviar_correo_respuesta(ticket):
    """Notifica al usuario que reportó el ticket que hubo una respuesta.
    Devuelve True si el correo se envió, False si no se pudo (sin tronar la app)."""
    if not app.config.get("MAIL_USERNAME") or not app.config.get("MAIL_PASSWORD"):
        app.logger.warning(
            "Correo no configurado (faltan MAIL_USERNAME/MAIL_PASSWORD); "
            "no se notificó el ticket #%s.", ticket.id
        )
        return False
    try:
        estatus = ESTATUS_LEGIBLE.get(ticket.estatus, ticket.estatus)
        salon = ticket.ubicacion.salon if ticket.ubicacion else "-"
        msg = Message(
            subject=f"Ticket #{ticket.id} actualizado — {estatus}",
            recipients=[ticket.correo_reporta],
            body=(
                f"Hola {ticket.nombre_reporta or ''},\n\n"
                f"Tu ticket #{ticket.id} sobre \"{ticket.tipo_problema}\" en {salon} "
                f"fue actualizado por el equipo de Sistemas.\n\n"
                f"Estatus actual: {estatus}\n"
                f"Respuesta: {ticket.comentario_resolucion}\n\n"
                f"Gracias por tu reporte.\n"
                f"— Mesa de Ayuda, Sistemas"
            ),
        )
        mail.send(msg)
        return True
    except Exception as e:
        app.logger.error("No se pudo enviar el correo del ticket #%s: %s", ticket.id, e)
        return False


@app.route("/")
def inicio():
    return redirect(url_for("reportar"))


@app.route("/reportar", methods=["GET", "POST"])
def reportar():
    form = TicketForm()
    ubicaciones = Ubicacion.query.order_by(Ubicacion.salon).all()
    form.ubicacion_id.choices = [(u.id, u.salon) for u in ubicaciones]

    if not ubicaciones:
        flash(
            "Aún no hay salones registrados en el sistema. Pide al administrador "
            "que corra 'python inicializar.py' antes de reportar.",
            "warning",
        )
        return render_template("reportar.html", form=form)

    if form.validate_on_submit():
        ticket = Ticket(
            nombre_reporta=form.nombre_reporta.data,
            correo_reporta=form.correo_reporta.data,
            ubicacion_id=form.ubicacion_id.data,
            tipo_problema=form.tipo_problema.data,
            descripcion=form.descripcion.data
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Ticket enviado correctamente", "success")
        return redirect(url_for("reportar"))
    return render_template("reportar.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(correo=form.correo.data).first()
        if usuario and check_password_hash(usuario.password_hash, form.password.data):
            login_user(usuario)
            return redirect(url_for("admin_dashboard"))
        flash("Correo o contraseña incorrectos", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/admin")
@login_required
def admin_dashboard():
    filtro = request.args.get("estatus", "todos")
    query = Ticket.query
    if filtro != "todos":
        query = query.filter_by(estatus=filtro)
    tickets = query.order_by(Ticket.fecha_creacion.desc()).all()

    resumen = {
        "todos": Ticket.query.count(),
        "pendiente": Ticket.query.filter_by(estatus="pendiente").count(),
        "en_proceso": Ticket.query.filter_by(estatus="en_proceso").count(),
        "resuelto": Ticket.query.filter_by(estatus="resuelto").count(),
    }
    return render_template(
        "admin_dashboard.html", tickets=tickets, filtro=filtro, resumen=resumen
    )


@app.route("/admin/ticket/<int:ticket_id>", methods=["GET", "POST"])
@login_required
def ticket_detalle(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if request.method == "POST":
        nuevo_estatus = request.form.get("estatus")
        nueva_prioridad = request.form.get("prioridad")
        comentario = (request.form.get("comentario") or "").strip()

        if nuevo_estatus not in ("pendiente", "en_proceso", "resuelto"):
            flash("Estatus no válido.", "danger")
            return render_template("ticket_detalle.html", ticket=ticket)

        ticket.estatus = nuevo_estatus
        if nueva_prioridad in ("baja", "media", "alta"):
            ticket.prioridad = nueva_prioridad
        ticket.comentario_resolucion = comentario
        if nuevo_estatus == "resuelto" and not ticket.fecha_resolucion:
            ticket.fecha_resolucion = datetime.now(timezone.utc)
        elif nuevo_estatus != "resuelto":
            ticket.fecha_resolucion = None
        db.session.commit()

        if ticket.correo_reporta and comentario:
            if enviar_correo_respuesta(ticket):
                flash("Ticket actualizado y el usuario fue notificado por correo.", "success")
            else:
                flash(
                    "Ticket actualizado, pero no se pudo enviar el correo "
                    "(revisa la configuración MAIL_USERNAME / MAIL_PASSWORD).",
                    "warning",
                )
        else:
            flash("Ticket actualizado.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("ticket_detalle.html", ticket=ticket)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
