import requests

BASE_URL = "http://localhost:8000/profissionais"



def listar_profissionais():
    response = requests.get(BASE_URL)

    if response.status_code == 200:
        return response.json()

    print("Erro:", response.text)
    return None


def buscar_profissional(id_profissional):
    response = requests.get(f"{BASE_URL}/{id_profissional}")

    if response.status_code == 200:
        return response.json()

    print("Profissional não encontrado.")
    return None


def cadastrar_profissional(
    nome,
    especialidade,
    crm,
    telefone,
    email
):

    dados = {
        "nome": nome,
        "especialidade": especialidade,
        "crm": crm,
        "telefone": telefone,
        "email": email
    }

    response = requests.post(
        BASE_URL,
        json=dados
    )

    return response.json()

def editar_profissional(
    id_profissional,
    nome,
    especialidade,
    crm,
    telefone,
    email
):

    dados = {
        "nome": nome,
        "especialidade": especialidade,
        "crm": crm,
        "telefone": telefone,
        "email": email
    }

    response = requests.put(
        f"{BASE_URL}/{id_profissional}",
        json=dados
    )

    return response.json()


def excluir_profissional(id_profissional):

    response = requests.delete(
        f"{BASE_URL}/{id_profissional}"
    )

    if response.status_code == 200:
        print("Profissional excluído com sucesso.")
    else:
        print(response.text)

