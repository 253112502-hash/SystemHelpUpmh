[README.md](https://github.com/user-attachments/files/32315870/README.md)
# Mesa de Ayuda (Helpdesk) — Proyecto Integrador

Sistema de tickets para reportar y dar seguimiento a fallas de equipo, proyectores
y red en salones de clase.

Interfaz con tema oscuro, componentes interactivos (selector de tipo de problema,
chips de estatus/prioridad, contador de caracteres) y notificación automática
por correo cuando Sistemas responde un ticket.

## Cómo correrlo (primera vez)

1. Abre esta carpeta en VS Code.
2. Abre una terminal y crea el entorno virtual:
   ```
   python -m venv venv
   ```
3. Actívalo:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
5. Inicializa la base de datos (crea el usuario admin y salones de ejemplo):
   ```
   python inicializar.py
   ```
6. Corre el servidor:
   ```
   python app.py
   ```
7. Abre en el navegador:
   - Formulario público: http://127.0.0.1:5000/reportar
   - Panel de administrador: http://127.0.0.1:5000/login

## Usuario administrador de prueba

- Correo: `admin@escuela.mx`
- Contraseña: `admin123`

**Cámbialos** antes de usarlo en producción (edita `inicializar.py` o crea otro
usuario directamente en la base de datos).

## Configurar el correo de notificación (opcional pero recomendado)

Cuando Sistemas responde un ticket que tiene correo registrado, el sistema
intenta enviarle un correo automático al usuario avisándole el nuevo estatus
y la respuesta. Si no configuras esto, **el sistema sigue funcionando igual**,
solo no se manda el correo (verás un aviso amarillo en el panel).

Para activarlo con una cuenta de Gmail:

1. En tu cuenta de Google, activa la verificación en dos pasos y genera una
   **"contraseña de aplicación"** (no uses tu contraseña normal):
   https://myaccount.google.com/apppasswords
2. Antes de correr `python app.py`, define estas variables de entorno:

   **Windows (PowerShell):**
   ```
   $env:MAIL_USERNAME="tucuenta@gmail.com"
   $env:MAIL_PASSWORD="la-contraseña-de-aplicación-de-16-letras"
   ```

   **Mac/Linux:**
   ```
   export MAIL_USERNAME="tucuenta@gmail.com"
   export MAIL_PASSWORD="la-contraseña-de-aplicación-de-16-letras"
   ```
3. Corre `python app.py` normalmente en esa misma terminal.

Si usas otro proveedor de correo (Outlook, uno institucional, etc.), también
puedes definir `MAIL_SERVER` y `MAIL_PORT` (revisa `config.py`).

## Estructura del proyecto

```
helpdesk/
├── app.py                    → rutas, lógica principal y envío de correo
├── config.py                 → configuración (clave secreta, BD, correo)
├── models.py                 → modelos: Usuario, Ubicacion, Ticket
├── forms.py                  → formularios (reporte y login)
├── inicializar.py            → crea admin y salones de ejemplo (correr una vez)
├── requirements.txt          → librerías necesarias
├── static/css/style.css      → tema oscuro
├── static/js/app.js          → interactividad (chips, contador, etc.)
├── templates/                → plantillas HTML
└── instance/helpdesk.db      → base de datos SQLite (se crea sola)
```

## Qué se ajustó en esta revisión

- Protección CSRF activada en todo el sitio, incluyendo el formulario de
  respuesta de tickets (antes no la tenía).
- `user_loader` actualizado a la API moderna de SQLAlchemy 2.0.
- Fechas cambiadas a UTC "aware" (ya no usan la función deprecada
  `datetime.utcnow()`).
- El formulario de reporte ahora avisa con un mensaje claro si todavía no hay
  salones registrados, en vez de fallar.
- El campo "prioridad" (ya existía en la base de datos pero nunca se mostraba
  ni se podía editar) ahora es visible y editable desde el panel.
- Notificación por correo al usuario cuando su ticket es respondido.
- Rediseño completo de las 4 pantallas con tema oscuro e interactivo.

## Próximos pasos sugeridos (extras para subir la calificación)

- Dashboard con gráficas (Chart.js) de fallas más frecuentes por salón.
- Código QR por salón que precargue la ubicación en el formulario.
- Manejo de varios roles de usuario (usando el campo `rol` que ya existe).

Si algo falla al correrlo, revisa que el entorno virtual esté activado y que
`pip install -r requirements.txt` haya terminado sin errores.
