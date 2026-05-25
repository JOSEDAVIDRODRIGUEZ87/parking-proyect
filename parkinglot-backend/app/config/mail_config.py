from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="tu_correo@gmail.com",
    MAIL_PASSWORD="tu_app_password",  # 🔥 NO contraseña normal, APP PASSWORD
    MAIL_FROM="tu_correo@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fast_mail = FastMail(conf)