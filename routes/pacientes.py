import requests

BASE_URL = "http://localhost:8000/pacientes"



def listar_pacientes():
    response = requests.get(BASE_URL)

    if response.status_code == 200:
        return response.json()

    print("Erro:", response.text)
    return None


def buscar_paciente(id_paciente):
    response = requests.get(f"{BASE_URL}/{id_paciente}")

    if response.status_code == 200:
        return response.json()

    print("Paciente não encontrado.")
    return None


def cadastrar_paciente(
    nome,
    cpf,
    telefone,
    email,
    data_nascimento,
    endereco
):

    dados = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "email": email,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    }

    response = requests.post(
        BASE_URL,
        json=dados
    )

    return response.json()


def editar_paciente(
    id_paciente,
    nome,
    cpf,
    telefone,
    email,
    data_nascimento,
    endereco
):

    dados = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "email": email,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    }

    response = requests.put(
        f"{BASE_URL}/{id_paciente}",
        json=dados
    )

    return response.json()


def excluir_paciente(id_paciente):

    response = requests.delete(
        f"{BASE_URL}/{id_paciente}"
    )

    if response.status_code == 200:
        print("Paciente excluído com sucesso.")
    else:
        print(response.text)
