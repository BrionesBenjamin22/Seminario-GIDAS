from core.routes.auth_rutas import auth_bp
from core.routes.tipo_personal_rutas import tipo_personal_bp
from core.routes.categoria_utn_routes import categoria_utn_bp
from core.routes.grupo_rutas import grupo_utn_bp
from core.routes.personal_rutas import personal_bp
from core.routes.tipo_dedicacion_rutas import tipo_dedicacion_bp
from core.routes.tipo_formacion_rutas import tipo_formacion_becario_bp
from core.routes.becario_rutas import becario_bp
from core.routes.fuente_financiamiento_rutas import fuente_financiamiento_bp
from core.routes.investigador_rutas import investigador_bp
from core.routes.personal_completo_ruta import personal_completo_bp


blueprints = [
    auth_bp,
    tipo_personal_bp,
    categoria_utn_bp,
    grupo_utn_bp,
    personal_bp,
    tipo_formacion_becario_bp,
    tipo_dedicacion_bp,
    becario_bp,
    fuente_financiamiento_bp,
    investigador_bp,
    personal_completo_bp
]
