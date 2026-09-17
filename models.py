from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()


def _ahora_utc():
    return datetime.now(timezone.utc)


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default="admin")


class Ubicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    salon = db.Column(db.String(50), nullable=False)
    edificio = db.Column(db.String(50))


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_reporta = db.Column(db.String(100))
    correo_reporta = db.Column(db.String(120))
    ubicacion_id = db.Column(db.Integer, db.ForeignKey("ubicacion.id"))
    tipo_problema = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    estatus = db.Column(db.String(20), default="pendiente")
    prioridad = db.Column(db.String(10), default="media")
    fecha_creacion = db.Column(db.DateTime, default=_ahora_utc)
    fecha_resolucion = db.Column(db.DateTime, nullable=True)
    comentario_resolucion = db.Column(db.Text, nullable=True)

    ubicacion = db.relationship("Ubicacion")
