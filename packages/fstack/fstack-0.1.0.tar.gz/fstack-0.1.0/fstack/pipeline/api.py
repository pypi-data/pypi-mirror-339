import requests
import os 

BASE_URL = os.getenv("BASE_URL")

def create_repo(
    key_id:str, api_key:str,
    provider_id:str,
    service:str,
    space_id: str
):
    url = BASE_URL + "/cli/repositories/url"
    print(url)
    data = {
    "provider_id": provider_id,
    "service": service,
    "space_id": space_id
    }
    headers = {
        "x-key-id": key_id,
        "x-api-key": api_key
    }
    response = requests.post(url, json=data, headers=headers)
    print("Código de estado:", response.status_code)
    print("Respuesta del servidor:", response.text)
    return response, response.status_code, response.text


def get_token(
    key_id:str, api_key:str,
    provider_id:str,
):
    url = BASE_URL + "/cli/repositories/login"
    data = {
    "provider_id": provider_id
    }
    headers = {
        "x-key-id": key_id,
        "x-api-key": api_key
    }
    response = requests.post(url, json=data, headers=headers)
    print("Código de estado:", response.status_code)
    print("Respuesta del servidor:", response.text)


def stop_deploy(
    key_id:str, api_key:str,
    deployment_id:str,
):
    url = BASE_URL + f"/cli/deployments/{deployment_id}/stop"
    headers = {
        "x-key-id": key_id,
        "x-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    print("Código de estado:", response.status_code)
    print("Respuesta del servidor:", response.text)



def status_deploy(
    key_id:str, api_key:str,
    deployment_id:str,
):
    url = BASE_URL + f"/cli/deployments/{deployment_id}/status"
    headers = {
        "x-key-id": key_id,
        "x-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    print("Código de estado:", response.status_code)
    print("Respuesta del servidor:", response.text)



def status_deploy(
    key_id:str, api_key:str,
    deployment_id:str,
    version:str
):
    url = BASE_URL + f"/cli/deployments/{deployment_id}/start{version}"
    headers = {
        "x-key-id": key_id,
        "x-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    print("Código de estado:", response.status_code)
    print("Respuesta del servidor:", response.text)


def space_deployments(
    key_id:str, api_key:str,
    space_id:str,
):
    url = BASE_URL + f"/cli/spaces/{space_id}/deployments"
    headers = {
        "x-key-id": key_id,
        "x-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    print("Código de estado:", response.status_code)
    print("Respuesta del servidor:", response.text)