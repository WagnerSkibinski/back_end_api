import requests



def get_clientes(id_paciente):
    response = requests.get(f"http://localhost:8000/pacientes/{id_paciente}")

    if response.status_code == 200:
        print(response.json())
    else:
        print(response.text)
        
        
def post_clientes(nome, cpf, tel, email):
    dados = {
    "nome": f"{nome}",
    "cpf": f"{cpf}",
    "telefone": f"{tel}",
    "email": f"{email}"
    }

    response = requests.post(
        "http://localhost:8000/pacientes",
        json=dados
    )

    print(response.status_code)
    print(response.json())
    
    
def delete_clientes(id_paciente):
    response = requests.delete(
    f"http://localhost:8000/pacientes/{id_paciente}"
    )

    print(response.status_code)
    print(response.text)
    Minha dúvida