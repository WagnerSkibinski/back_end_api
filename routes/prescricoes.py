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


def listar_prescricoes():
    response = requests.get(
        f"{BASE_URL}/prescricoes",
        headers=HEADERS
        
    )

    if response.status_code == 200:
        return response.json()

    print("Erro:", response.text)
    return None


def buscar_prescricao(id_prescricao):
    response = requests.get(
        f"{BASE_URL}/prescriocoes/{id_prescricao}",
        headers=HEADERS    
    )

    if response.status_code == 200:
        return response.json()

    print("Prescrição não encontrada.")
    return None


def cadastrar_prescricao(paciente, profissional, medicamentos, orientacoes, data):

    dados = {
        "paciente": paciente,
        "profissional": profissional,
        "medicamentos": medicamentos,
        "orientacoes": orientacoes,
        "data": data
    }

    response = requests.post(
        f"{BASE_URL}/prescricoes",
        json=dados,
        headers=HEADERS
    )

    return response.json()


def editar_prescricao(id_prescricao, dados):

    response = requests.put(
        f"{BASE_URL}/prescricoes/{id_prescricao}",
        json=dados,
        headers=HEADERS
    )

    return response.json()


def excluir_prescricao(id_prescricao):

    response = requests.delete(
        f"{BASE_URL}/prescricoes/{id_prescricao}",
        headers=HEADERS
    )

    if response.status_code == 200:
        print("Prescrição excluída com sucesso.")
    else:
        print(response.text)

