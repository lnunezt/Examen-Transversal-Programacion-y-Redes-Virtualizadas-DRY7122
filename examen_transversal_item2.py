#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asignatura: Programación de Redes Virtualizadas
Evaluación: Examen Transversal - Actividad 3 (Versión Corregida)
Descripción: Script que consume APIs REST dinámicas para geocodificación acotada
             por código de país y cálculo exacto de rutas viales Chile-Argentina.
"""

import requests

def obtener_coordenadas(ciudad, codigo_pais):
    """
    Consulta la API REST de OpenStreetMap acotando la búsqueda estrictamente
    al código de país (cl para Chile, ar para Argentina) para evitar rutas erróneas.
    """
    url_geo = "https://nominatim.openstreetmap.org/search"
    parametros = {
        "city": ciudad,
        "countrycodes": codigo_pais, # Restringe la búsqueda geográficamente al país correcto
        "format": "json",
        "limit": 1
    }
    # Cabecera User-Agent obligatoria por políticas de OpenStreetMap
    cabeceras = {"User-Agent": "ExamenTransversal_AsignaturaRedes/1.0"}
    
    try:
        response = requests.get(url_geo, params=parametros, headers=cabeceras)
        if response.status_code == 200 and len(response.json()) > 0:
            datos = response.json()[0]
            # Retorna formato "longitud,latitud"
            return f"{datos['lon']},{datos['lat']}"
    except Exception:
        pass
    return None

def main():
    # URL Base de la API REST de enrutamiento vial (OSRM)
    url_osrm = "http://router.project-osrm.org/route/v1/"

    print("==================================================")
    print("        SISTEMA DINÁMICO DE PLANIFICACIÓN         ")
    print("         (FILTRADO ESTRICTO DE PAÍSES)            ")
    print("==================================================")

    while True:
        print("\nIngrese los datos de las ciudades (o 's' para salir):")
        
        ciudad_origen = input("Ciudad de Origen (Chile): ").strip()
        if ciudad_origen.lower() == 's': 
            break
            
        ciudad_destino = input("Ciudad de Destino (Argentina): ").strip()
        if ciudad_destino.lower() == 's': 
            break

        print("\nBuscando coordenadas exactas en las APIs...")
        
        # 'cl' fuerza la búsqueda solo en Chile; 'ar' solo en Argentina
        coord_origen = obtener_coordenadas(ciudad_origen, "cl")
        coord_destino = obtener_coordenadas(ciudad_destino, "ar")

        if not coord_origen or not coord_destino:
            print("[Error] No se pudieron determinar las coordenadas. Asegúrese de escribir bien las ciudades.")
            continue

        print("\nSeleccione el medio de transporte:")
        print("1) Automóvil")
        print("2) Autobús de larga distancia")
        print("3) Bicicleta / Caminata")
        
        transporte = input("Opción: ").strip()
        if transporte.lower() == 's': 
            break

        perfil = "driving"
        url_peticion = f"{url_osrm}{perfil}/{coord_origen};{coord_destino}"

        response = requests.get(url_peticion)

        if response.status_code == 200:
            json_data = response.json()
            
            if json_data.get("code") != "Ok":
                print("[Error] No se encontró una ruta terrestre disponible entre estas ciudades.")
                continue

            metros = json_data["routes"][0]["distance"]
            segundos = json_data["routes"][0]["duration"]

            km = metros / 1000
            millas = km * 0.621371
            
            # Ajustes de tiempo lógicos por transporte
            if transporte == "2":
                segundos *= 1.25
            elif transporte == "3":
                # Escala de caminata real a 5 km/h
                segundos = (km / 5) * 3600

            horas = int(segundos // 3600)
            minutos = int((segundos % 3600) // 60)

            medios_txt = {"1": "Automóvil", "2": "Autobús", "3": "Bicicleta/Caminata"}
            medio_seleccionado = medios_txt.get(transporte, "Vehículo terrestre")

            print("\n" + "="*45)
            print("             RESULTADOS DEL VIAJE            ")
            print("="*45)
            print(f"Distancia en Kilómetros : {km:.2f} km")
            print(f"Distancia en Millas     : {millas:.2f} mi")
            print(f"Duración estimada       : {horas} horas y {minutos} minutos")
            print("-"*45)
            print("NARRATIVA DEL VIAJE:")
            print(f"Su viaje comenzará en la ciudad de {ciudad_origen.title()}, cruzando las fronteras")
            print(f"viales hacia {ciudad_destino.title()}. El trayecto se realizará en")
            print(f"{medio_seleccionado}, completando una distancia calculada de {km:.2f} km.")
            print(f"Recuerde portar sus documentos de identificación al día.")
            print("="*45)
        else:
            print(f"[Error HTTP] Fallo al calcular la ruta. Código: {response.status_code}")

if __name__ == "__main__":
    main()
