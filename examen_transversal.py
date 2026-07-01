"""
Asignatura: Programación y Redes Virtualizadas
Evaluación: Examen Transversal
"""

import os

def limpiar_pantalla():
    """Limpieza del terminal."""
    os.system('clear' if os.name == 'posix' else 'cls')

def desplegar_integrantes():
    """Almacena e imprime los datos de los integrantes."""
    grupo_integrantes = [
        {
            "nombre": "Leonardo",
            "apellido": "Nunez"
        },
        {
            "nombre": "Martin",
            "apellido": "Pardo"
        },
    ]
    
    print("=" * 50)
    print("         EVALUACIÓN: EXAMEN TRANSVERSAL")
    print("   ASIGNATURA: PROGRAMACIÓN DE REDES VIRTUALIZADAS")
    print("=" * 50)
    print(" INTEGRANTES DEL GRUPO DE TRABAJO:")
    print("-" * 50)
    
    for i, integrante in enumerate(grupo_integrantes, start=1):
        print(f"  {i}. {integrante['nombre']} {integrante['apellido']}")
        
    print("=" * 50)

if __name__ == "__main__":
    limpiar_pantalla()
    desplegar_integrantes()
