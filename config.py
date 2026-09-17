import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-secreta-para-el-proyecto-2026")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(INSTANCE_DIR, "helpdesk.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Correo: notificación al usuario cuando su ticket es respondido ---
    # Se leen de variables de entorno para no dejar contraseñas en el código.
    # Si MAIL_USERNAME / MAIL_PASSWORD no están configuradas, el sistema sigue
    # funcionando normalmente, solo no se envía el correo (se avisa en el panel).
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "menguetrk@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "mbvxrhtovocezwvy")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
