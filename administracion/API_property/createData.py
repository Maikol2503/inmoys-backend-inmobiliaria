from faker import Faker
import random
import string

class CreateData:
    def __init__(self):
        self.fake = Faker()
    

    def datageneral(self, data):
        dataGeneral = {
            'sku': self.generate_sku(data.tipo[0] + data.transaccion[0]),
            'descripcion': data.descripcion,
            'precio': data.precio,
            'tipo': data.tipo,
            'transaccion': data.transaccion,
            'disponibilidad': data.disponibilidad,
            'provincia':  data.provincia,
            'ciudad':data.ciudad,
            'zona': data.zona,
            'cp': data.cp,
            'numeroCalle': data.numeroCalle,
            'nombreCalle': data.nombreCalle,
            'planta': data.planta,
            'puerta': data.puerta,
        }
        return dataGeneral

    def vivienda(self, data):
        vivienda_data = self.datageneral(data)
        vivienda_data['detalles'] = {
                'tamano': data.detalles['tamano'],
                'habitaciones': data.detalles['habitaciones'],
                'banos': data.detalles['banos'],
                'orientacion': data.detalles['orientacion'],
                'ascensor': data.detalles['ascensor'],
                'piscina': data.detalles['piscina'],
                'balcon': data.detalles['balcon'],
                'terraza': data.detalles['terraza'],
                'jardin': data.detalles['jardin'],
                'armarioEmpotrado': data.detalles['armarioEmpotrado'],
                'anoConstruccion': data.detalles['anoConstruccion'],
                'estadoInmueble': data.detalles['estadoInmueble'],
                'consumo': data.detalles['consumo'],
                'emisiones': data.detalles['emisiones'],
                'combustibleCalefaccion': data.detalles['combustibleCalefaccion'],
                'sistemaCalefaccion': data.detalles['sistemaCalefaccion'],
                'trastero': data.detalles['trastero'],
                'aire': data.detalles['aire'],
                'calefaccion': data.detalles['calefaccion'],
                'garaje': data.detalles['garaje'],
                'gimnasio': data.detalles['gimnasio']
                }
        return vivienda_data
    

    def oficina(self, data):
        oficina_data = self.datageneral(data)
        oficina_data['detalles'] = {
                'tamano': data.detalles['tamano'],
                'banos': data.detalles['banos'],
                'orientacion': data.detalles['orientacion'],
                'ascensor': data.detalles['ascensor'],
                'anoConstruccion': data.detalles['anoConstruccion'],
                'estadoInmueble': data.detalles['estadoInmueble'],
                'consumo': data.detalles['consumo'],
                'emisiones': data.detalles['emisiones'],
                'combustibleCalefaccion': data.detalles['combustibleCalefaccion'],
                'sistemaCalefaccion': data.detalles['sistemaCalefaccion'],
                'aire': data.detalles['aire'],
                'calefaccion': data.detalles['calefaccion'],
                'certificadoEnergetico': data.detalles['certificadoEnergetico'],
                'garaje': data.detalles['garaje'],
                'gimnasio': data.detalles['gimnasio']
                }
        return oficina_data
    

    def terreno(self, data):
        terrreno_data = self.datageneral(data)
        terrreno_data['detalles'] = {

        }
        return terrreno_data



    def generate_sku(self, prefijo: str):
        unique_id = self.fake.uuid4()
        prefix = prefijo.lower() + '-'  # Convierte el prefijo a minúsculas
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))  # Usa solo letras minúsculas
        sku = f"{prefix}{unique_id[:4]}-{suffix}".lower()  # Convierte todo el SKU a minúsculas
        return sku

