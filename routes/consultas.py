import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

HEADERS = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}


def listar_consultas():
    response = requests.get(
        f"{BASE_URL}/consultas",
        headers=HEADERS
    )

    if response.status_code == 200:
        return response.json()

    print("Erro:", response.text)
    return None



def buscar_consulta(id_consulta):
    response = requests.get(
        f"{BASE_URL}/consultas/{id_consulta}",
        headers=HEADERS
    )

    if response.status_code == 200:
        return response.json()

    print("Consulta não encontrada.")
    return None



def cadastrar_consulta(paciente,profissional,data,hora,tipo):

    dados = {
        "paciente": paciente,
        "profissional": profissional,
        "data": data,
        "hora": hora,
        "tipo": tipo
    }

    response = requests.post(
        f"{BASE_URL}/consultas",
        json=dados,
        headers=HEADERS
        
    )

    return response.json()


def editar_consulta(id_consulta,dados):

    response = requests.put(
        f"{BASE_URL}/consulta/{id_consulta}",
        json=dados,
        headers=HEADERS
    )

    return response.json()


def excluir_consulta(id_consulta):

    response = requests.delete(
        f"{BASE_URL}/consultas/{id_consulta}",
        headers=HEADERS
    )

    if response.status_code == 200:
        print("Consulta excluída com sucesso.")
    else:
        print(response.text)
