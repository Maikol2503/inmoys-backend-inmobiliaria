from fastapi import FastAPI, Form, APIRouter
from fastapi.responses import JSONResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.setting import Settings

settings = Settings()
sendEmail = APIRouter()

# Credenciales de tu correo
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = settings.correo
EMAIL_PASSWORD = settings.token


@sendEmail.post("/send-email")
async def send_email(
    nombre: str = Form(None), 
    apellido: str = Form(None), 
    email: str = Form(...), 
    telefono: str = Form(...), 
    mensaje: str = Form(None)
):

    print(EMAIL_ADDRESS, EMAIL_PASSWORD)
    try:
        # Crear el mensaje de correo
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = "mgarrido2503@gmail.com" # O reemplaza con tu correo para recibirlo tú mismo
        msg['Subject'] = "Nuevo mensaje de contacto"

        # Cuerpo del correo
        body = f"""
            <strong>Nombre:</strong> {nombre} <br>
            <strong>Apellido:</strong> {apellido} <br>
            <strong>Email:</strong> {email} <br>
            <strong>Teléfono:</strong> {telefono} <br>
            <strong>Mensaje:</strong> {mensaje} <br>
        """
        msg.attach(MIMEText(body, 'html'))

        # Enviar el correo
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Inicia la conexión de manera segura usando TLS
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Inicia sesión en tu cuenta de correo
            server.send_message(msg)

        # Retornar una respuesta de éxito
        return JSONResponse(content={"message": "Correo enviado correctamente"}, status_code=200)

    except smtplib.SMTPAuthenticationError:
        error_msg = "Error de autenticación. Verifica tu correo y contraseña."
        print(error_msg)  # Registro del error
        return JSONResponse(content={"error": error_msg}, status_code=401)
    
    except smtplib.SMTPConnectError:
        error_msg = "Error de conexión al servidor SMTP. Verifica tu conexión a Internet y la configuración del servidor."
        print(error_msg)  # Registro del error
        return JSONResponse(content={"error": error_msg}, status_code=503)

    except smtplib.SMTPException as e:
        error_msg = f"Error al enviar correo: {str(e)}"
        print(error_msg)  # Registro del error
        return JSONResponse(content={"error": error_msg}, status_code=500)

    except Exception as e:
        # Manejar cualquier otra excepción
        error_msg = f"Error inesperado: {str(e)}"
        print(error_msg)  # Registro del error
        return JSONResponse(content={"error": error_msg}, status_code=500)

# Recuerda incluir tu router en la aplicación principal si es necesario
# app = FastAPI()
# app.include_router(sendEmail)
