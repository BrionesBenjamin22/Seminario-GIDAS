import os
import json
from app import create_app
from extension import db
from sqlalchemy import text

# =================================================================
# MAPA DE MODELOS
# Agrega aquí una entrada por cada modelo que quieras poder "seedear".
# El nombre del archivo JSON (sin .json) debe coincidir con la clave.
# =================================================================
from core.models.proyecto_investigacion import TipoProyecto
from core.models.fuente_financiamiento import FuenteFinanciamiento
from core.models.personal import TipoFormacion

MODEL_MAP = {
    "tipos_proyecto": TipoProyecto,
    "fuentes_financiamiento": FuenteFinanciamiento,
    "tipos_formacion": TipoFormacion,
}
# =================================================================

def seed_data():
    """
    Carga datos iniciales desde archivos JSON en la carpeta /seeds.
    El nombre de cada archivo JSON debe corresponder a una clave en MODEL_MAP.
    """
    app = create_app()
    with app.app_context():
        print("==============================================")
        print("Iniciando proceso de carga de datos (seeding)...")
        print("==============================================")

        seeds_dir = os.path.join(os.path.dirname(__file__), 'seeds')
        if not os.path.exists(seeds_dir):
            print(f"Directorio 'seeds' no encontrado. No se cargaron datos.")
            return

        for filename in os.listdir(seeds_dir):
            if filename.endswith('.json'):
                model_key = filename[:-5] # Quita la extensión .json
                if model_key in MODEL_MAP:
                    model_class = MODEL_MAP[model_key]
                    table_name = model_class.__tablename__
                    
                    print(f"\nProcesando '{filename}' para el modelo '{model_class.__name__}'...")

                    try:
                        with open(os.path.join(seeds_dir, filename), 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        # 1. Eliminar datos existentes
                        num_rows_deleted = db.session.query(model_class).delete()
                        if num_rows_deleted > 0:
                            print(f"  - Eliminados {num_rows_deleted} registros antiguos de la tabla '{table_name}'.")

                        # 2. Insertar nuevos datos
                        if not data:
                            print("  - El archivo JSON está vacío, no se insertaron nuevos datos.")
                            continue
                            
                        for item_data in data:
                            # Convierte el nombre a minúsculas si el campo existe
                            if 'nombre' in item_data and isinstance(item_data['nombre'], str):
                                item_data['nombre'] = item_data['nombre'].lower()
                            
                            item = model_class(**item_data)
                            db.session.add(item)
                        
                        db.session.commit()
                        print(f"  - Carga de {len(data)} registros exitosa.")

                    except Exception as e:
                        db.session.rollback()
                        print(f"  - ❌ ERROR al procesar '{filename}': {e}")
                        print("  - Se ha revertido la transacción para este modelo.")
                else:
                    print(f"\n- ⚠️ ADVERTENCIA: No se encontró un modelo en MODEL_MAP para el archivo '{filename}'.")

        print("\n==============================================")
        print("Proceso de carga finalizado.")
        print("==============================================")

if __name__ == "__main__":
    seed_data()
