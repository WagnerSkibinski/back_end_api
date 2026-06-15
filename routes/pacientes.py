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

def listar_pacientes():
    response = requests.get(
        f"{BASE_URL}/pacientes",
        headers=HEADERS                            
    )

    if response.status_code == 200:
        return response.json()

    print("Erro:", response.text)
    return None


def buscar_paciente(id_paciente):
    response = requests.get(
        f"{BASE_URL}/pacientes/{id_paciente}",
        headers=HEADERS
        )

    if response.status_code == 200:
        return response.json()

    print("Paciente não encontrado.")
    return None


def cadastrar_paciente(nome,cpf,telefone,email,data_nascimento,endereco):

    dados = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "email": email,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    }

    response = requests.post(
        f"{BASE_URL}/pacientes",
        json=dados,
        headers=HEADERS
    )

    return response.json()


def editar_paciente(id_paciente, dados):

    response = requests.put(
        f"{BASE_URL}/pacientes/{id_paciente}",
        json=dados,
        headers=HEADERS
    )

    return response.json()


def excluir_paciente(id_paciente):

    response = requests.delete(
        f"{BASE_URL}/pacientes{id_paciente}",
        headers=HEADERS
    )

    if response.status_code == 200:
        print("Paciente excluído com sucesso.")
    else:
        print(response.text)
