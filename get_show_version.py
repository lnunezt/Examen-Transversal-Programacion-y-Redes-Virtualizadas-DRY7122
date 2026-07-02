from netmiko import ConnectHandler
    from netmiko.exceptions import NetmikoTimeoutError, NetmikoAuthenticationError
except ModuleNotFoundError:
    try:
        from netmiko import NetmikoTimeoutError, NetmikoAuthenticationError
    except ImportError:
        from netmiko import (
            NetMikoTimeoutException as NetmikoTimeoutError,
            NetMikoAuthenticationException as NetmikoAuthenticationError,
        )

# Datos de conexión al dispositivo Cisco CSR1000v
csr1000v = {
    "device_type": "cisco_ios",
    "host": "192.168.56.103",
    "username": "cisco",
    "password": "cisco123!",
    "secret": "cisco123!",
    "port": 22,
}


def obtener_version(device):
    # Se conecta al router, entra en modo enable y ejecuta show version
    try:
        print(f"Conectando a {device['host']} ...")
        conexion = ConnectHandler(**device)
        conexion.enable()

        comando = "show version"
        salida = conexion.send_command(comando, delay_factor=2)

        conexion.disconnect()
        return salida

    except NetmikoTimeoutError:
        print("Error: Tiempo de espera agotado. Verifica IP/conectividad.")
    except NetmikoAuthenticationError:
        print("Error: Fallo de autenticación. Verifica usuario/contraseña.")
    except Exception as e:
        print(f"Error inesperado: {e}")

    return None


def guardar_salida(contenido, hostname="CSR1000v"):
    # Guarda la salida del comando en un archivo de texto
    import os
    nombre_archivo = f"ios_configurations/show_version_{hostname}.txt"
    os.makedirs("ios_configurations", exist_ok=True)

    with open(nombre_archivo, "w") as f:
        f.write(contenido)

    print(f"Salida guardada en: {nombre_archivo}")


if __name__ == "__main__":
    resultado = obtener_version(csr1000v)

    if resultado:
        print("\n--- Show Version ---\n")
        print(resultado)
        guardar_salida(resultado)
    else:
        print("No se pudo obtener el show version.")