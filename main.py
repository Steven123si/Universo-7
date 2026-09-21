from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import crear_tablas, sembrar_datos
from routers import auth, planetas, razas

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    sembrar_datos()
    yield

app = FastAPI(
    title="RazasDBZ",
    description="API REST de Planetas y Razas DBZ.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(planetas.router)
app.include_router(razas.router)

@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "¡Bienvenido a la API del Universo DB! Revisa /docs para explorar los endpoints."}