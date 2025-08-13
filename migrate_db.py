#!/usr/bin/env python3
"""
Script de migración para agregar campos activity_type e is_active
Ejecuta este archivo antes de iniciar tu aplicación
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text, inspect
from app.database import engine

def check_column_exists(table_name, column_name):
    """Verifica si una columna existe en la tabla"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def migrate():
    print("🚀 Iniciando migración de base de datos...")
    
    with engine.begin() as conn:  # Usar transacción
        try:
            # Verificar si la tabla activities existe
            inspector = inspect(engine)
            if 'activities' not in inspector.get_table_names():
                print("❌ Tabla 'activities' no encontrada. Asegúrate de que la base de datos esté inicializada.")
                return False
            
            # Verificar y agregar activity_type
            if not check_column_exists('activities', 'activity_type'):
                print("➕ Agregando columna 'activity_type'...")
                conn.execute(text("ALTER TABLE activities ADD COLUMN activity_type VARCHAR DEFAULT 'Tour Gastronómico'"))
                print("✅ Columna 'activity_type' agregada correctamente")
            else:
                print("⚠️  Columna 'activity_type' ya existe")
            
            # Verificar y agregar is_active
            if not check_column_exists('activities', 'is_active'):
                print("➕ Agregando columna 'is_active'...")
                conn.execute(text("ALTER TABLE activities ADD COLUMN is_active BOOLEAN DEFAULT 1"))  # SQLite usa 1 para true
                print("✅ Columna 'is_active' agregada correctamente")
            else:
                print("⚠️  Columna 'is_active' ya existe")
            
            # Actualizar registros existentes
            print("🔄 Actualizando registros existentes...")
            result1 = conn.execute(text("UPDATE activities SET activity_type = 'Tour Gastronómico' WHERE activity_type IS NULL OR activity_type = ''"))
            result2 = conn.execute(text("UPDATE activities SET is_active = 1 WHERE is_active IS NULL"))
            
            print(f"✅ {result1.rowcount} registros actualizados con activity_type")
            print(f"✅ {result2.rowcount} registros actualizados con is_active")
            
            # Verificar que todo esté correcto
            result = conn.execute(text("SELECT COUNT(*) as count FROM activities"))
            total_activities = result.fetchone()[0]
            print(f"📊 Total de actividades en la base de datos: {total_activities}")
            
            print("✅ Migración completada exitosamente!")
            return True
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            return False

def verify_migration():
    """Verifica que la migración se haya ejecutado correctamente"""
    print("\n🔍 Verificando migración...")
    
    try:
        with engine.connect() as conn:
            # Verificar estructura de la tabla
            result = conn.execute(text("PRAGMA table_info(activities)"))
            columns = result.fetchall()
            
            print("\n📋 Estructura actual de la tabla 'activities':")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Verificar que las nuevas columnas existen
            column_names = [col[1] for col in columns]
            if 'activity_type' in column_names and 'is_active' in column_names:
                print("✅ Todas las columnas necesarias están presentes")
                
                # Mostrar algunos datos de ejemplo
                result = conn.execute(text("SELECT name, activity_type, is_active FROM activities LIMIT 3"))
                rows = result.fetchall()
                if rows:
                    print("\n📄 Datos de ejemplo:")
                    for row in rows:
                        print(f"  - {row[0]} | {row[1]} | {'Activa' if row[2] else 'Inactiva'}")
                
                return True
            else:
                print("❌ Faltan columnas necesarias")
                return False
                
    except Exception as e:
        print(f"❌ Error verificando migración: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRACIÓN DE BASE DE DATOS - RUTAS GASTRONÓMICAS")
    print("=" * 60)
    
    # Ejecutar migración
    if migrate():
        # Verificar migración
        if verify_migration():
            print("\n🎉 ¡Migración exitosa! Ya puedes iniciar tu aplicación.")
        else:
            print("\n⚠️  Migración completada pero hay problemas en la verificación.")
    else:
        print("\n❌ Migración fallida. Revisa los errores anteriores.")
    
    print("=" * 60)