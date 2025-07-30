# Server.py
import os
import uvicorn
from dotenv import load_dotenv
from api.App import app
from infrastructure.config.Base import Base
from infrastructure.config.ConfigSwagger import setup_swagger, generate_swagger_yaml
from infrastructure.config.Db import connect_to_db, create_database_if_not_exists

from infrastructure.model.User import User
from infrastructure.model.EmailVerificationToken import EmailVerificationToken
from infrastructure.model.Role import Role


load_dotenv()

create_database_if_not_exists()

engine, conn, meta = connect_to_db()

Base.metadata.create_all(engine)

setup_swagger(app)

generate_swagger_yaml(app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    uvicorn.run("Server:app", host="localhost", port=port, reload=True)