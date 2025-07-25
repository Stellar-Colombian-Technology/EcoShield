# Server.py
import os
import uvicorn
from dotenv import load_dotenv
from api.App import app
from infrastructure.config.ConfigSwagger import setup_swagger, generate_swagger_yaml
from infrastructure.config.Db import connect_to_db

load_dotenv()

engine, conn, meta = connect_to_db()

setup_swagger(app)

generate_swagger_yaml(app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    uvicorn.run("Server:app", host="localhost", port=port, reload=True)