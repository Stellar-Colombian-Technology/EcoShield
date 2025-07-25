# infrastructure/config/ConfigSwagger.py
import os
import yaml
from fastapi.openapi.utils import get_openapi

def setup_swagger(app):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
            
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description="",
            routes=app.routes,
            contact=app.contact
        )

        if "components" not in openapi_schema:
            openapi_schema["components"] = {}
            
        openapi_schema["components"]["securitySchemes"] = {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
        
        openapi_schema["security"] = [{"bearerAuth": []}]

        openapi_schema["servers"] = [
            {
                "url": "http://localhost:3000",
                "description": "Local Server"
            }
        ]
        
        app.openapi_schema = openapi_schema
        return openapi_schema

    app.openapi = custom_openapi

def generate_swagger_yaml(app):
    if not app.openapi_schema:
        app.openapi()
    
    media_dir = os.path.join(os.path.dirname(__file__), "../../../media/docs")
    os.makedirs(media_dir, exist_ok=True)
    file_path = os.path.join(media_dir, "swagger.yml")

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(app.openapi_schema, f, allow_unicode=True, sort_keys=False)

    print(f"Swagger exportado a: {file_path}")