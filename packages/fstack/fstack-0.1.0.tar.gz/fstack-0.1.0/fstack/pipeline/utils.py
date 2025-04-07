
import yaml

def get_yml():
    """Carga el fs-config, ejecuta el pipeline de imagen docker"""
    ruta_archivo = "faststack-config.yml"
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = yaml.safe_load(archivo)  # Convierte el YAML en un diccionario
            # print(yaml.dump(datos, default_flow_style=False, sort_keys=False, allow_unicode=True))
            return datos
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'.")

    except yaml.YAMLError as e:
        print(f"Error al procesar el YAML: {e}")