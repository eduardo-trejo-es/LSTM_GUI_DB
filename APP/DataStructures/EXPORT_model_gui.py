

import sqlite3
import os
import json
import shutil

def export_model(model_id, db_path="APP/DataStructures/Predict_model.db"):
    # Conexión a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener datos del modelo
    cursor.execute("SELECT * FROM Models WHERE Model_id = ?", (model_id,))
    model_row = cursor.fetchone()
    if not model_row:
        print(f"❌ Modelo con ID {model_id} no encontrado.")
        return

    model_columns = [description[0] for description in cursor.description]
    model_data = dict(zip(model_columns, model_row))

    # Obtener datos de Seed_Model
    seed_model_id = model_data["Seed_Model_id_FRGN"]
    cursor.execute("SELECT * FROM Seed_Model WHERE Seed_Model_id = ?", (seed_model_id,))
    seed_row = cursor.fetchone()
    seed_data = None
    if seed_row:
        seed_columns = [description[0] for description in cursor.description]
        seed_data = dict(zip(seed_columns, seed_row))

    # Obtener relación con dataset
    cursor.execute("SELECT DataSet_id_FRGN FROM Relation_Model_Datasets WHERE Model_id_FRGN = ?", (model_id,))
    rel_row = cursor.fetchone()
    relation_data = {"DataSet_id_FRGN": rel_row[0]} if rel_row else None

    conn.close()

    # Preparar estructura para exportación
    export_dict = {
        "model": model_data,
        "seed_model": seed_data,
        "relation_model_dataset": relation_data
    }

    # Crear carpeta de exportación
    export_dir = f"APP/Exports/Model_{model_id}"
    os.makedirs(export_dir, exist_ok=True)

    # Exportar a JSON
    json_path = os.path.join(export_dir, f"Model_{model_id}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(export_dict, f, indent=4)

    # Copiar archivo .keras si existe
    keras_filename = model_data.get("Path_Model")
    if keras_filename and os.path.isfile(keras_filename):
        shutil.copy(keras_filename, os.path.join(export_dir, os.path.basename(keras_filename)))
        print(f"✅ Modelo y archivo .keras exportados a: {export_dir}")
    else:
        print(f"⚠️ Archivo .keras no encontrado: {keras_filename}, solo se exportó el .json")

# Ejemplo de uso:
export_model(213)