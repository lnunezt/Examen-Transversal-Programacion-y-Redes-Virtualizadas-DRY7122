print("--- Analizador de VLANs ---")
vlan = int(input("Ingrese el número de VLAN a evaluar: "))

if 1 <= vlan <= 1005:
    print("Es una VLAN de rango Normal")
elif 1006 <= vlan <= 4094:
    print("Es una VLAN de rango Extendido")
else:
    print("VLAN Inválida")
