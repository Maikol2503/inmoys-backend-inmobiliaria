from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.wsgi import WSGIMiddleware
import os

from fastapi.templating import Jinja2Templates
from config.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from administracion.API_login.routes.register import admiRegister
from administracion.API_login.routes.login import admiLogin

from administracion.API_clients.routes.add import addClient

# from administracion.API_contrato.routes.add import addContrato
# from administracion.API_contrato.routes.get import getContrato

from administracion.API_property.routes.add import addProperties
from administracion.API_property.routes.get import getProperties
from administracion.API_property.routes.public_get import publicProperties
from administracion.API_property.routes.update import updateProperties
from administracion.API_property.routes.delete import deleteProperties

from mail.mail import sendEmail 
app = FastAPI()
jinja2Templates = Jinja2Templates(directory="templates")

#servir imagenes 
app.mount("/images", StaticFiles(directory='imagenes'), name="images")
app.mount("/images-for-web", StaticFiles(directory='imagenes-para-web'), name="images")

app.include_router(admiRegister)
app.include_router(admiLogin)

app.include_router(addClient)

app.include_router(addProperties)
app.include_router(getProperties)
app.include_router(updateProperties)
app.include_router(deleteProperties)

app.include_router(publicProperties)

app.include_router(sendEmail)

Base.metadata.create_all(bind=engine)

    # "http://localhost:4300",
    # "http://localhost:4200",

origins = [
    "https://inmoys-dashboard.vercel.app",
    "https://inmoys-umber.vercel.app",
    
]

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir solicitudes de estos orígenes
    allow_credentials=True,  # Permitir envío de cookies con solicitudes
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/")
def root():
    return {
        "message":"Hola desde la ruta main."
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)