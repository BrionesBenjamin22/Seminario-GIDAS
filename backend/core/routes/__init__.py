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
from core.routes.programa_actividades_rutas import planificacion_grupo_bp
from core.routes.programa_incentivos_rutas import programa_incentivos_bp
from core.routes.visita_rutas import visita_academica_bp
from core.routes.tipo_registro_rutas import tipo_registro_propiedad_bp
from core.routes.registro_propiedad_rutas import registros_propiedad_bp
from core.routes.autores_rutas import autor_bp
from core.routes.documentacion_rutas import documentacion_bibliografica_bp
from core.routes.tipo_erogacion_rutas import tipo_erogacion_bp
from core.routes.erogacion_rutas import erogacion_bp
from core.routes.equipamiento_rutas import equipamiento_bp
from core.routes.distinciones_rutas import distincion_recibida_bp
from core.routes.trabajo_reunion_rutas import trabajo_reunion_cientifica_bp

blueprints = [
    auth_bp,
    becario_bp,
    categoria_utn_bp,
    fuente_financiamiento_bp,
    grupo_utn_bp,
    investigador_bp,
    personal_bp,
    personal_completo_bp,
    planificacion_grupo_bp,
    programa_incentivos_bp,
    tipo_personal_bp,
    tipo_formacion_becario_bp,
    tipo_dedicacion_bp,
    visita_academica_bp,
    tipo_registro_propiedad_bp,
    registros_propiedad_bp,
    autor_bp,
    documentacion_bibliografica_bp,
    tipo_erogacion_bp,
    erogacion_bp,
    equipamiento_bp,
    distincion_recibida_bp,
    trabajo_reunion_cientifica_bp,
]
