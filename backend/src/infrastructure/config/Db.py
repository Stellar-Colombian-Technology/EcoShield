from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import urllib.parse
import os

load_dotenv()

from sqlalchemy import text

def create_database_if_not_exists():
    try:
        user = os.getenv("DB_USER")
        password = urllib.parse.quote_plus(os.getenv("DB_PASSWORD")) 
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        dbname = os.getenv("DB_NAME")

        # Primero conecta al sistema base de datos 'postgres'
        system_url = f"postgresql://{user}:{password}@{host}:{port}/postgres"
        system_engine = create_engine(system_url, isolation_level='AUTOCOMMIT')  # Para poder crear DB

        with system_engine.connect() as conn:
            # Verifica si existe
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": dbname}
            )
            exists = result.scalar() is not None

            if not exists:
                conn.execute(text(f"CREATE DATABASE {dbname}"))
                print(f"Base de datos '{dbname}' creada exitosamente.")
            else:
                print(f"La base de datos '{dbname}' ya existe.")

    except SQLAlchemyError as e:
        print("Error al verificar o crear la base de datos:", e)


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