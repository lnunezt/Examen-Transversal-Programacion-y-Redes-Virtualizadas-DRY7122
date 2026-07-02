from netmiko import ConnectHandler

# Parametros de conexion al equipo
csr1kv = {
    'device_type': 'cisco_ios',
    'host':   '192.168.56.103', # IP del router
    'username': 'cisco',        # Usuario de acceso
    'password': 'cisco123!',    # Contraseña de acceso
}

# Lista de comandos para configurar EIGRP Nombrado (IPv4 e IPv6)
comandos_eigrp = [
    'ipv6 unicast-routing',
    'router eigrp CORE',
    
    # Configuracion IPv4 AS 100
    'address-family ipv4 unicast autonomous-system 100',
    'network 192.168.56.0 0.0.0.255',
    'af-interface default',
    'passive-interface',
    'exit-af-interface',
    'exit-address-family',
    
    # Configuracion IPv6 AS 100
    'address-family ipv6 unicast autonomous-system 100',
    'af-interface default',
    'passive-interface',
    'exit-af-interface',
    'exit-address-family'
]

print("Iniciando conexion...")

try:
    # Establecer conexion SSH
    conexion = ConnectHandler(**csr1kv)
    print("Conexion exitosa. Aplicando configuracion EIGRP...")

    # Enviar bloque de comandos
    conexion.send_config_set(comandos_eigrp)
    
    # Validar configuracion aplicada
    print("\nValidando parametros con 'show running-config | section eigrp':\n")
    salida_validacion = conexion.send_command('show running-config | section eigrp')
    print(salida_validacion)

    # Cerrar sesion
    conexion.disconnect()
    print("\nProceso finalizado correctamente.")

except Exception as e:
    print(f"Ocurrio un error en la ejecucion: {e}")