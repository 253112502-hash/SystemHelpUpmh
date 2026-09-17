from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Optional, Email


class TicketForm(FlaskForm):
    nombre_reporta = StringField("Nombre", validators=[DataRequired()])
    correo_reporta = StringField("Correo", validators=[Optional(), Email()])
    ubicacion_id = SelectField("Salón/Ubicación", coerce=int)
    tipo_problema = SelectField("Tipo de problema", choices=[
        ("computadora", "Computadora"),
        ("proyector", "Proyector"),
        ("red", "Red/Internet"),
        ("otro", "Otro")
    ])
    descripcion = TextAreaField("Descripción del problema", validators=[DataRequired()])
    submit = SubmitField("Enviar reporte")


class LoginForm(FlaskForm):
    correo = StringField("Correo", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")
