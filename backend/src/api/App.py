from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.AuthRouter import router as AuthRouter

app = FastAPI(
    title="EcoShield360 API",
    version="1.0.0",
    contact={
        "name": "Stellar Colombian technology",
        "url": "https://www.stellarco.online/",
        "email": "stellarcolsupp@gmail.com"
    },
    docs_url="/api-docs"
)

# Routers
app.include_router(AuthRouter)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)