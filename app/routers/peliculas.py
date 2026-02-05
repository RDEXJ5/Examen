from fastapi import APIRouter, Query

router = APIRouter(prefix="/peliculas", tags=["Películas"])

peliculas_db = [
    {"id": 1, "titulo": "Inception", "genero": "Ciencia ficción", "clasificacion": "B"},
    {"id": 2, "titulo": "Titanic", "genero": "Romance", "clasificacion": "B"},
    {"id": 3, "titulo": "Avengers", "genero": "Acción", "clasificacion": "B"},
    {"id": 4, "titulo": "Coco", "genero": "Animación", "clasificacion": "A"},
]

@router.get("/")
async def listar_peliculas(
    search: str | None = Query(None, description="Buscar por título, género o clasificación")
):
    resultados = peliculas_db

    if search:
        resultados = [
            p for p in peliculas_db
            if search.lower() in p["titulo"].lower()
            or search.lower() in p["genero"].lower()
            or search.lower() in p["clasificacion"].lower()
        ]

    return {
        "total": len(resultados),
        "peliculas": resultados
    }
