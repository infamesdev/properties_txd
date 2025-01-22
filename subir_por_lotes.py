import os
import subprocess
from pathlib import Path
import time

def obtener_tamano_archivos(ruta):
    archivos = []
    for archivo in Path(ruta).rglob('*'):
        if archivo.is_file():
            archivos.append({
                'ruta': archivo,
                'tamano': archivo.stat().st_size
            })
    return archivos

def crear_lotes(archivos, tamano_max_bytes=100*1024*1024):
    lotes = []
    lote_actual = []
    tamano_actual = 0
    
    for archivo in archivos:
        if tamano_actual + archivo['tamano'] > tamano_max_bytes:
            if lote_actual:
                lotes.append(lote_actual)
            lote_actual = [archivo]
            tamano_actual = archivo['tamano']
        else:
            lote_actual.append(archivo)
            tamano_actual += archivo['tamano']
    
    if lote_actual:
        lotes.append(lote_actual)
    
    return lotes

def subir_por_lotes():
    # Obtener todos los archivos
    archivos = obtener_tamano_archivos('.')
    lotes = crear_lotes(archivos)
    
    for i, lote in enumerate(lotes, 1):
        print(f"\nProcesando lote {i} de {len(lotes)}")
        
        # Agregar archivos del lote
        for archivo in lote:
            subprocess.run(['git', 'add', str(archivo['ruta'])])
        
        # Hacer commit y push
        subprocess.run(['git', 'commit', '-m', f'Subiendo lote {i} de archivos'])
        subprocess.run(['git', 'push'])
        
        print(f"Lote {i} subido exitosamente")
        time.sleep(2)  # Pequeña pausa entre lotes

if __name__ == "__main__":
    subir_por_lotes()