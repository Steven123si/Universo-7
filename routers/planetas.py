from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from database import obtener_conexion
from modelos import PlanetaCrear, PlanetaRespuesta
from seguridad import obtener_usuario_actual, requerir_admin

router = APIRouter(prefix="/planetas", tags=["Planetas"])

@router.get("", response_model=List[PlanetaRespuesta])
def listar_planetas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM planetas")
    filas = cursor.fetchall()
    conexion.close()
    return [dict(f) for f in filas]

@router.get("/{id}", response_model=PlanetaRespuesta)
def obtener_planeta(id: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM planetas WHERE id = ?", (id,))
    fila = cursor.fetchone()
    conexion.close()
    if not fila:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planeta no encontrado")
    return dict(fila)

@router.post("", response_model=PlanetaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_planeta(planeta: PlanetaCrear, usuario: dict = Depends(obtener_usuario_actual)):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO planetas (nombre, galaxia) VALUES (?, ?)",
        (planeta.nombre, planeta.galaxia)
    )
    conexion.commit()
    nuevo_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM planetas WHERE id = ?", (nuevo_id,))
    nuevo_planeta = dict(cursor.fetchone())
    conexion.close()
    return nuevo_planeta

@router.put("/{id}", response_model=PlanetaRespuesta)
def actualizar_planeta(id: int, planeta: PlanetaCrear, usuario: dict = Depends(obtener_usuario_actual)):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE planetas SET nombre = ?, galaxia = ? WHERE id = ?",
        (planeta.nombre, planeta.galaxia, id)
    )
    conexion.commit()
    
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planeta no encontrado")
        
    cursor.execute("SELECT * FROM planetas WHERE id = ?", (id,))
    actualizado = dict(cursor.fetchone())
    conexion.close()
    return actualizado

# Operación exclusiva de Administrador con regla de integridad referencial
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_planeta(id: int, admin: dict = Depends(requerir_admin)):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Validar que no tenga razas asociadas
    cursor.execute("SELECT COUNT(*) FROM razas WHERE planeta_id = ?", (id,))
    if cursor.fetchone()[0] > 0:
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede destruir un planeta que aún tiene razas habiténdolo"
        )

    cursor.execute("DELETE FROM planetas WHERE id = ?", (id,))
    conexion.commit()
    
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planeta no encontrado")
        
    conexion.close()