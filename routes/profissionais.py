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


def listar_profissionais():
    response = requests.get(
        f"{BASE_URL}",
        headers=HEADERS
    )

    if response.status_code == 200:
        return response.json()

    print("Erro:", response.text)
    return None


def buscar_profissional(id_profissional):
    response = requests.get(
        f"{BASE_URL}/profissional/{id_profissional}",
        headers=HEADERS

    )

    if response.status_code == 200:
        return response.json()

    print("Profissional não encontrado.")
    return None


def cadastrar_profissional(nome,especialidade,crm,telefone,email):

    dados = {
        "nome": nome,
        "especialidade": especialidade,
        "crm": crm,
        "telefone": telefone,
        "email": email
    }

    response = requests.post(
        f"{BASE_URL}/profissional",
        json=dados,
        headers=HEADERS
        
    )

    return response.json()

def editar_profissional(id_profissional, dados):

    response = requests.put(
        f"{BASE_URL}/proficional/{id_profissional}",
        json=dados,
        headers=HEADERS
    )

    return response.json()


def excluir_profissional(id_profissional):

    response = requests.delete(
        f"{BASE_URL}/profissional/{id_profissional}",
        headers=HEADERS
    )

    if response.status_code == 200:
        print("Profissional excluído com sucesso.")
    else:
        print(response.text)

