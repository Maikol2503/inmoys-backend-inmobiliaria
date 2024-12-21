from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from config.setting import Settings
# from decouple import config


settings = Settings()

try:
    # user= config("USER_NAME")
    # host= config("HOST")
    # password = config("PASSWORD")
    # db= config("DB")
    # url = f"mysql+pymysql://{user}:{password}@{host}:3306/{db}"

    engine = create_engine(settings.database_url)
    meta = MetaData()
    conn = engine.connect()
    Base = declarative_base()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

except SQLAlchemyError as e:
   
    print(f"Error al conectar a la base de datos: {e}")
    # Puedes agregar aquí el manejo de la excepción según tus necesidades

    