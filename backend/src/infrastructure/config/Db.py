import os
import urllib.parse
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

# Datos para conexión
user = os.getenv("DB_USER")
password = urllib.parse.quote_plus(os.getenv("DB_PASSWORD")) 
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Engine y session factory global
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_database_if_not_exists():
    try:
        system_url = f"postgresql://{user}:{password}@{host}:{port}/postgres"
        system_engine = create_engine(system_url, isolation_level='AUTOCOMMIT')

        with system_engine.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": dbname}
            )
            exists = result.scalar() is not None

            if not exists:
                conn.execute(text(f"CREATE DATABASE {dbname}"))
                print(f"✅ Base de datos '{dbname}' creada exitosamente.")
            else:
                print(f"📦 La base de datos '{dbname}' ya existe.")

    except SQLAlchemyError as e:
        print("❌ Error al verificar o crear la base de datos:", e)


def connect_to_db():
    try:
        conn = engine.connect()
        meta = MetaData()
        print("✅ Conexión a la base de datos exitosa.")
        return engine, conn, meta
    except SQLAlchemyError as e:
        print("❌ Error al conectar con la base de datos:", e)
        return None, None, None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
