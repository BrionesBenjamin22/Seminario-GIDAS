from sqlalchemy import or_
from core.services.search_registry import SEARCH_ENTITIES


class SearchService:
    """
    Servicio de búsqueda global del sistema.
    Orquesta:
    - búsquedas semánticas (secciones/módulos)
    - búsquedas en entidades registradas
    """

    # =========================
    # Secciones semánticas
    # =========================
    SEARCH_SECTIONS = [
        {
            "keywords": ["becario", "becarios"],
            "result": {
                "type": "section",
                "title": "Becarios",
                "description": "Listado de becarios del sistema",
                "url": "/becarios"
            }
        },
        {
            "keywords": ["investigador", "investigadores"],
            "result": {
                "type": "section",
                "title": "Investigadores",
                "description": "Listado de investigadores",
                "url": "/investigadores"
            }
        },
        {
            "keywords": ["personal"],
            "result": {
                "type": "section",
                "title": "Personal",
                "description": "Personal del grupo de investigación",
                "url": "/personal"
            }
        },
        {
            "keywords": [
                "transferencia",
                "transferencias",
                "transferencia socio productiva",
                "socio productiva"
            ],
            "result": {
                "type": "section",
                "title": "Transferencias Socio Productivas",
                "description": "Actividades de vinculación y transferencia",
                "url": "/transferencias"
            }
        },
        {
            "keywords": [
                "proyecto",
                "proyectos",
                "proyecto de investigacion",
                "investigacion"
            ],
            "result": {
                "type": "section",
                "title": "Proyectos de Investigación",
                "description": "Proyectos de investigación y desarrollo",
                "url": "/proyectos"
            }
        },
        {
            "keywords": [
                "documentacion",
                "documentacion bibliografica",
                "bibliografia",
                "libros",
                "autores"
            ],
            "result": {
                "type": "section",
                "title": "Documentación Bibliográfica",
                "description": "Libros, autores y material bibliográfico",
                "url": "/documentacion"
            }
        },
        {
            "keywords": [
                "articulo",
                "articulos",
                "divulgacion",
                "articulo de divulgacion",
                "articulos de divulgacion"
            ],
            "result": {
                "type": "section",
                "title": "Artículos de Divulgación",
                "description": "Artículos de divulgación científica",
                "url": "/articulos-divulgacion"
            }
        },
        {
            "keywords": [
                "trabajo",
                "trabajos",
                "reunion cientifica",
                "reuniones cientificas",
                "congreso",
                "congresos",
                "jornadas"
            ],
            "result": {
                "type": "section",
                "title": "Trabajos en Reuniones Científicas",
                "description": "Trabajos presentados en congresos y jornadas",
                "url": "/trabajos-reunion-cientifica"
            }
        },
        {
            "keywords": [
                "distincion",
                "distinciones",
                "premio",
                "premios",
                "reconocimiento",
                "reconocimientos"
            ],
            "result": {
                "type": "section",
                "title": "Proyectos con Distinciones",
                "description": "Proyectos de investigación que recibieron premios o reconocimientos",
                "url": "/proyectos?filtro=distinciones"
            }
        },
        {
            "keywords": [
                "equipamiento",
                "equipo",
                "equipos",
                "instrumental",
                "hardware"
            ],
            "result": {
                "type": "section",
                "title": "Equipamiento",
                "description": "Equipamiento e infraestructura del grupo",
                "url": "/equipamiento"
            }
        },
        {
            "keywords": [
                "visita",
                "visitas",
                "visita academica",
                "visitas academicas",
                "delegacion",
                "intercambio"
            ],
            "result": {
                "type": "section",
                "title": "Visitas Académicas",
                "description": "Visitas académicas e intercambios institucionales",
                "url": "/visitas-academicas"
            }
        },
        {
            "keywords": [
                "revista",
                "revistas",
                "referato",
                "revista con referato",
                "publicacion",
                "publicaciones",
                "paper",
                "articulo cientifico"
            ],
            "result": {
                "type": "section",
                "title": "Trabajos en Revistas con Referato",
                "description": "Publicaciones científicas en revistas con referato",
                "url": "/trabajos-revistas"
            }
        },
        {
            "keywords": [
                "participacion",
                "participaciones",
                "evento",
                "eventos",
                "charla",
                "conferencia",
                "workshop",
                "exposicion",
                "ponencia"
            ],
            "result": {
                "type": "section",
                "title": "Participaciones Relevantes",
                "description": "Participaciones en eventos académicos y científicos",
                "url": "/participaciones-relevantes"
            }
        }









    ]

    # =========================
    # API pública
    # =========================
    @staticmethod
    def search(query: str) -> list:
        if not query or len(query.strip()) < 2:
            return []

        query_clean = query.lower().strip()
        query_ilike = f"%{query_clean}%"

        results = []

        # 1️⃣ Secciones semánticas (módulos)
        results.extend(SearchService._search_sections(query_clean))

        # 2️⃣ Entidades registradas
        results.extend(SearchService._search_entities(query_ilike))

        return results

    # =========================
    # Búsqueda de secciones
    # =========================
    @staticmethod
    def _search_sections(query_clean: str) -> list:
        results = []

        for section in SearchService.SEARCH_SECTIONS:
            if any(keyword in query_clean for keyword in section["keywords"]):
                results.append(section["result"])

        return results

    # =========================
    # Búsqueda genérica en entidades
    # =========================
    @staticmethod
    def _search_entities(query_ilike: str) -> list:
        results = []

        for entity in SEARCH_ENTITIES:
            model = entity["model"]
            fields = entity["fields"]
            serializer = entity["serializer"]

            filters = [
                getattr(model, field).ilike(query_ilike)
                for field in fields
            ]

            matches = (
                model.query
                .filter(or_(*filters))
                .limit(5)   # 🔒 límite por entidad
                .all()
            )

            results.extend(serializer(obj) for obj in matches)

        return results
