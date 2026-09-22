import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from database import obtener_conexion
from modelos import RazaCrear, RazaRespuesta, PlanetaConRazasRespuesta
from seguridad import obtener_usuario_actual, requerir_admin

router = APIRouter(prefix="/razas", tags=["Razas"])

# --- LECTURA ---
@router.get("", response_model=List[RazaRespuesta])
def listar_razas(usuario: dict = Depends(obtener_usuario_actual)):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM razas")
    filas = cursor.fetchall()
    conexion.close()
    return [dict(f) for f in filas]

@router.get("/{id}", response_model=RazaRespuesta)
def obtener_raza(id: int, usuario: dict = Depends(obtener_usuario_actual)):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM razas WHERE id = ?", (id,))
    fila = cursor.fetchone()
    conexion.close()
    if not fila:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raza no encontrada")
    return dict(fila)

@router.get("/planeta/{planeta_id}", response_model=PlanetaConRazasRespuesta)
def obtener_planeta_con_razas(planeta_id: int, usuario: dict = Depends(obtener_usuario_actual)):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            p.id AS p_id, p.nombre AS p_nombre, p.galaxia AS p_galaxia,
            r.id AS r_id, r.nombre AS r_nombre, r.fuerza_base AS r_fuerza, 
            r.habilidad_especial AS r_habilidad, r.planeta_id AS r_planeta_id
        FROM planetas p
        LEFT JOIN razas r ON p.id = r.planeta_id
        WHERE p.id = ?
    """, (planeta_id,))
    
    filas = cursor.fetchall()
    conexion.close()

    if not filas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planeta no encontrado"
        )

    primera = filas[0]
    planeta_dict = {
        "id": primera["p_id"],
        "nombre": primera["p_nombre"],
        "galaxia": primera["p_galaxia"],
        "razas": []
    }

    for f in filas:
        if f["r_id"] is not None:
            planeta_dict["razas"].append({
                "id": f["r_id"],
                "nombre": f["r_nombre"],
                "fuerza_base": f["r_fuerza"],
                "habilidad_especial": f["r_habilidad"],
                "planeta_id": f["r_planeta_id"]
            })

    return planeta_dict

@router.post("", response_model=RazaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_raza(raza: RazaCrear, admin: dict = Depends(requerir_admin)):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Validar existencia del planeta
    cursor.execute("SELECT id FROM planetas WHERE id = ?", (raza.planeta_id,))
    if not cursor.fetchone():
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El planeta con ID {raza.planeta_id} no existe en el universo"
        )

    try:
        cursor.execute(
            "INSERT INTO razas (nombre, fuerza_base, habilidad_especial, planeta_id) VALUES (?, ?, ?, ?)",
            (raza.nombre, raza.fuerza_base, raza.habilidad_especial, raza.planeta_id)
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Esta especie '{raza.nombre}' ya existe en el planeta actual"
        )
    
    cursor.execute("SELECT * FROM razas WHERE id = ?", (nuevo_id,))
    nueva_raza = dict(cursor.fetchone())
    conexion.close()
    return nueva_raza

@router.put("/{id}", response_model=RazaRespuesta)
def actualizar_raza(id: int, raza: RazaCrear, admin: dict = Depends(requerir_admin)):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT id FROM planetas WHERE id = ?", (raza.planeta_id,))
    if not cursor.fetchone():
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El planeta con ID {raza.planeta_id} no existe en el universo (Por ahora..)"
        )

    try:
        cursor.execute(
            "UPDATE razas SET nombre = ?, fuerza_base = ?, habilidad_especial = ?, planeta_id = ? WHERE id = ?",
            (raza.nombre, raza.fuerza_base, raza.habilidad_especial, raza.planeta_id, id)
        )
        conexion.commit()
    except sqlite3.IntegrityError:
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Esta especie '{raza.nombre}' ya existe en la base de datos"
        )
    
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raza no encontrada")
        
    cursor.execute("SELECT * FROM razas WHERE id = ?", (id,))
    actualizada = dict(cursor.fetchone())
    conexion.close()
    return actualizada

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_raza(id: int, admin: dict = Depends(requerir_admin)):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM razas WHERE id = ?", (id,))
    conexion.commit()
    
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raza no encontrada")
        
    conexion.close()