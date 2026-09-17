"""
Script de inicialización: crea las tablas, un usuario administrador
y algunos salones de ejemplo. Correr UNA sola vez.
"""
from werkzeug.security import generate_password_hash

try:
    from .app import app
    from .models import db, Usuario, Ubicacion
except ImportError:  # pragma: no cover
    from app import app
    from models import db, Usuario, Ubicacion

with app.app_context():
    db.create_all()

    if not Usuario.query.filter_by(correo="admin@escuela.mx").first():
        admin = Usuario(
            nombre="Administrador",
            correo="admin@escuela.mx",
            password_hash=generate_password_hash("admin123"),
            rol="admin"
        )
        db.session.add(admin)
        print("Administrador creado: admin@escuela.mx / admin123")
    else:
        print("El administrador ya existía")

    if Ubicacion.query.count() == 0:
        salones = ["Salón 1", "Salón 2", "Laboratorio de Redes", "Sala de Cómputo"]
        for s in salones:
            db.session.add(Ubicacion(salon=s))
        print("Salones de ejemplo creados:", salones)
    else:
        print("Ya existían salones")

    db.session.commit()
    print("Inicialización completa.")
