from datetime import date
from sqlalchemy.exc import IntegrityError
from app import create_app
from extension import db

from core.models.grupo import GrupoInvestigacionUtn
from core.models.personal import Personal, Becario, Investigador, TipoDedicacion, TipoFormacion
from core.models.tipo_personal import TipoPersonal
from core.models.proyecto_investigacion import ProyectoInvestigacion, TipoProyecto
from core.models.equipamiento import Equipamiento
from core.models.transferencia_socio import TransferenciaSocioProductiva, TipoContrato
from core.models.articulo_divulgacion import ArticuloDivulgacion
from core.models.trabajo_revista import TrabajosRevistasReferato
from core.models.trabajo_reunion import TrabajoReunionCientifica, TipoReunion
from core.models.fuente_financiamiento import FuenteFinanciamiento
from core.models.registro_patente import TipoRegistroPropiedad

def get_or_create(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
    return instance

def seed_db():
    app = create_app()
    with app.app_context():
        print("====== Creando Datos Básicos ======")
        
        # Grupo
        grupo1 = get_or_create(
            GrupoInvestigacionUtn,
            mail="gidas@utn.edu.ar",
            nombre_unidad_academica="UTN FRRe",
            objetivo_desarrollo="Desarrollo de Software",
            nombre_sigla_grupo="GIDAS"
        )
        print(f"Grupo ID: {grupo1.id}")

        grupo2 = get_or_create(
            GrupoInvestigacionUtn,
            mail="cenit@utn.edu.ar",
            nombre_unidad_academica="UTN FRBA",
            objetivo_desarrollo="Inteligencia Artificial",
            nombre_sigla_grupo="CENIT"
        )
        
        # Tipos
        tp_inv = get_or_create(TipoPersonal, nombre="Investigador")
        tp_bec = get_or_create(TipoPersonal, nombre="Becario")
        tp_ptaa = get_or_create(TipoPersonal, nombre="PTAA")
        tp_prof = get_or_create(TipoPersonal, nombre="Profesional")
        
        td_sim = get_or_create(TipoDedicacion, nombre="Simple")
        tf_gra = get_or_create(TipoFormacion, nombre="Grado")
        tc_serv = get_or_create(TipoContrato, nombre="Servicios Técnicos")
        t_proy = get_or_create(TipoProyecto, nombre="PID")
        tr_cong = get_or_create(TipoReunion, nombre="Congreso")
        ff_utn = get_or_create(FuenteFinanciamiento, nombre="UTN")
        
        tr_pat = get_or_create(TipoRegistroPropiedad, nombre="Patente")
        tr_util = get_or_create(TipoRegistroPropiedad, nombre="Modelo de Utilidad")
        tr_soft = get_or_create(TipoRegistroPropiedad, nombre="Software")

        print("====== Creando Personal ======")
        if not db.session.query(Personal).filter_by(nombre_apellido="Juan Perez PTAA").first():
            db.session.add(Personal(nombre_apellido="Juan Perez PTAA", horas_semanales=10, tipo_personal_id=tp_ptaa.id, grupo_utn_id=grupo1.id))
        
        if not db.session.query(Personal).filter_by(nombre_apellido="Ana Sanchez Prof").first():
            db.session.add(Personal(nombre_apellido="Ana Sanchez Prof", horas_semanales=40, tipo_personal_id=tp_prof.id, grupo_utn_id=grupo2.id))

        if not db.session.query(Investigador).filter_by(nombre_apellido="Dra. Maria Gomez").first():
            db.session.add(Investigador(nombre_apellido="Dra. Maria Gomez", horas_semanales=20, tipo_dedicacion_id=td_sim.id, grupo_utn_id=grupo1.id))

        if not db.session.query(Becario).filter_by(nombre_apellido="Carlos Ruiz Becario").first():
            db.session.add(Becario(nombre_apellido="Carlos Ruiz Becario", horas_semanales=15, tipo_formacion_id=tf_gra.id, grupo_utn_id=grupo1.id, fuente_financiamiento_id=ff_utn.id))

        db.session.commit()

        print("====== Creando Proyectos ======")
        if not db.session.query(ProyectoInvestigacion).filter_by(codigo_proyecto=2001).first():
            db.session.add(ProyectoInvestigacion(
                codigo_proyecto=2001,
                nombre_proyecto="Optimización con IA",
                descripcion_proyecto="Modelos predictivos para la industria",
                fecha_inicio=date(2023, 1, 1),
                tipo_proyecto_id=t_proy.id,
                grupo_utn_id=grupo1.id,
                fuente_financiamiento_id=ff_utn.id
            ))
            
        if not db.session.query(ProyectoInvestigacion).filter_by(codigo_proyecto=2002).first():
            db.session.add(ProyectoInvestigacion(
                codigo_proyecto=2002,
                nombre_proyecto="Big Data en Salud",
                descripcion_proyecto="Gestión de históricos",
                fecha_inicio=date(2024, 2, 1),
                tipo_proyecto_id=t_proy.id,
                grupo_utn_id=grupo2.id,
                fuente_financiamiento_id=ff_utn.id
            ))
        db.session.commit()

        print("====== Creando Equipamiento ======")
        if not db.session.query(Equipamiento).filter_by(denominacion="Servidor GPU V100").first():
            db.session.add(Equipamiento(
                denominacion="Servidor GPU V100",
                descripcion_breve="Procesamiento intensivo",
                fecha_incorporacion=date(2023, 5, 10),
                monto_invertido=1500000.0,
                grupo_utn_id=grupo1.id
            ))
        db.session.commit()

        print("====== Creando Transferencias ======")
        if not db.session.query(TransferenciaSocioProductiva).filter_by(demandante="Hospital Local").first():
            db.session.add(TransferenciaSocioProductiva(
                numero_transferencia=1001,
                denominacion="Transferencia Demo Hosp",
                demandante="Hospital Local",
                descripcion_actividad="Implementación de historia clínica",
                monto=250000.0,
                fecha_inicio=date(2023, 6, 1),
                tipo_contrato_id=tc_serv.id,
                grupo_utn_id=grupo1.id
            ))
        db.session.commit()

        print("====== Creando Publicaciones ======")
        if not db.session.query(ArticuloDivulgacion).filter_by(titulo="El futuro del software").first():
            db.session.add(ArticuloDivulgacion(
                titulo="El futuro del software",
                descripcion="Divulgación en blog regional",
                fecha_publicacion=date(2023, 8, 15),
                grupo_utn_id=grupo1.id
            ))

        if not db.session.query(TrabajosRevistasReferato).filter_by(titulo_trabajo="Modelos Optimizados V2").first():
            db.session.add(TrabajosRevistasReferato(
                titulo_trabajo="Modelos Optimizados V2",
                nombre_revista="IEEE Transactions on SE",
                editorial="IEEE",
                issn="1234-5678",
                pais="USA",
                fecha=date(2023, 10, 1),
                tipo_reunion_id=tr_cong.id,
                grupo_utn_id=grupo1.id
            ))

        if not db.session.query(TrabajoReunionCientifica).filter_by(titulo_trabajo="Avances en ML 2024").first():
            db.session.add(TrabajoReunionCientifica(
                titulo_trabajo="Avances en ML 2024",
                nombre_reunion="Congreso CAI",
                procedencia="Nacional",
                fecha_inicio=date(2024, 9, 1),
                tipo_reunion_id=tr_cong.id,
                grupo_utn_id=grupo1.id
            ))

        db.session.commit()
        print("====== Seed Completado con Exito ======")

if __name__ == "__main__":
    seed_db()
