from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import urllib.parse
import os

load_dotenv()

def connect_to_db():
    try:
        user = os.getenv("DB_USER")
        password = urllib.parse.quote_plus(os.getenv("DB_PASSWORD")) 
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        dbname = os.getenv("DB_NAME")

        DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        engine = create_engine(DATABASE_URL)
        conn = engine.connect()
        meta = MetaData()

        print(" Conexión a la base de datos exitosa.")
        return engine, conn, meta

    except SQLAlchemyError as e:
        print(" Error al conectar con la base de datos:", e)
        return None, None, None