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
    nombre: str = Form('Sin Nombre'), 
    apellido: str = Form('Sin Apellido'), 
    email: str = Form('Sin Email'), 
    telefono: str = Form('Sin telefono'), 
    mensaje: str = Form('Sin mensaje'),
    sku: str = Form('SKU no especificado'),
):

    print(sku)
    try:
        # Crear el mensaje de correo
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = "ysalguerot@gmail.com"  # O reemplaza con tu correo para recibirlo tú mismo
        msg['Subject'] = "Nuevo mensaje de contacto"

        data = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'mensaje': mensaje,
            'sku': sku
        }

        # Generar el cuerpo del mensaje con la función
        body = body_message(data)
        
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




def body_message(data: dict) -> str:
    """
    Genera el cuerpo del mensaje de correo con el contenido de los datos proporcionados.
    """
    # Cuerpo del correo
    body = f"""
        <strong>Nombre:</strong> {data['nombre']} <br>
        <strong>Apellido:</strong> {data['apellido']} <br>
        <strong>Email:</strong> {data['email']} <br>
        <strong>Teléfono:</strong> {data['telefono']} <br>
        <strong>Mensaje:</strong> {data['mensaje']} <br>
    """
    # Agregar SKU si está presente
    if data.get('sku') != 'SKU no especificado':
        body += f"""
            <strong>Interés en propiedad:</strong> El cliente ha mostrado interés en la propiedad con SKU: {data['sku']} <br>
        """

    return body
