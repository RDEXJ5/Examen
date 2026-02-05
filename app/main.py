from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Importación relativa: al estar en la misma carpeta 'app', usamos .routers
from .routers import peliculas

app = FastAPI(
    title="PeliPal - Sistema de Gestión de Cines",
    description="Sistema para la gestión de películas, salas y funciones de cine",
    version="1.0.0"
)

# ---------------------------
# Rutas base ajustadas a tu imagen
# ---------------------------
# BASE_DIR será la carpeta 'app'
BASE_DIR = Path(__file__).resolve().parent

# ---------------------------
# Montar archivos estáticos
# ---------------------------
# Usamos el path relativo correcto dentro de 'app'
static_path = BASE_DIR / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# ---------------------------
# Configurar Jinja2
# ---------------------------
# Apuntamos a 'app/templates' usando la variable BASE_DIR
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# ---------------------------
# Routers
# ---------------------------
app.include_router(peliculas.router, prefix="/api/v1", tags=["Películas"])

@app.get("/", tags=["Inicio"])
async def home(request: Request):
    from .routers.peliculas import peliculas_db

    total_peliculas = len(peliculas_db)
    generos = {p["genero"] for p in peliculas_db}
    clasificaciones = {p["clasificacion"] for p in peliculas_db}

    context = {
        "request": request,
        "titulo": "PeliPal",
        "descripcion": "Sistema de Gestión de Cines desarrollado con FastAPI",
        "total_peliculas": total_peliculas,
        "total_generos": len(generos),
        "total_clasificaciones": len(clasificaciones),
        "features": [
            {"icono": "🎬", "titulo": "Películas", "descripcion": "Gestión completa del catálogo"},
            {"icono": "🏢", "titulo": "Salas", "descripcion": "Administración de salas"},
            {"icono": "⏰", "titulo": "Funciones", "descripcion": "Control de horarios"},
            {"icono": "📊", "titulo": "Estadísticas", "descripcion": "Reportes del sistema"}
        ]
    }
    return templates.TemplateResponse("home.html", context)