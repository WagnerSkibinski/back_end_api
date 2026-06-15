BASE_URL = "http://localhost:8000/prescricoes"


def listar_prescricoes():
    response = requests.get(BASE_URL)

    if response.status_code == 200:
        return response.json()

    print("Erro:", response.text)
    return None


def buscar_prescricao(id_prescricao):
    response = requests.get(f"{BASE_URL}/{id_prescricao}")

    if response.status_code == 200:
        return response.json()

    print("Prescrição não encontrada.")
    return None


def cadastrar_prescricao(
    paciente,
    profissional,
    medicamentos,
    orientacoes,
    data
):

    dados = {
        "paciente": paciente,
        "profissional": profissional,
        "medicamentos": medicamentos,
        "orientacoes": orientacoes,
        "data": data
    }

    response = requests.post(
        BASE_URL,
        json=dados
    )

    return response.json()


def editar_prescricao(
    id_prescricao,
    paciente,
    profissional,
    medicamentos,
    orientacoes,
    data
):

    dados = {
        "paciente": paciente,
        "profissional": profissional,
        "medicamentos": medicamentos,
        "orientacoes": orientacoes,
        "data": data
    }

    response = requests.put(
        f"{BASE_URL}/{id_prescricao}",
        json=dados
    )

    return response.json()


def excluir_prescricao(id_prescricao):

    response = requests.delete(
        f"{BASE_URL}/{id_prescricao}"
    )

    if response.status_code == 200:
        print("Prescrição excluída com sucesso.")
    else:
        print(response.text)

