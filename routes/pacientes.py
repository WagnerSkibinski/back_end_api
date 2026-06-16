from flask import Blueprint, jsonify, request

from services.json_manager import append_log, load_data, next_id, save_data


pacientes_bp = Blueprint("pacientes", __name__)


@pacientes_bp.get("/pacientes")
def listar_pacientes():
    
    return jsonify(load_data("pacientes.json")), 200


@pacientes_bp.get("/pacientes/<int:id_paciente>")
def buscar_paciente(id_paciente):
    pacientes = load_data("pacientes.json")
    paciente = next((item for item in pacientes if item.get("id") == id_paciente), None)
    if not paciente:
        
        return jsonify({"erro": "Paciente não encontrado"}), 404
    return jsonify(paciente), 200


@pacientes_bp.post("/pacientes")
def cadastrar_paciente():
    dados = request.get_json(silent=True) or {}
    campos = ["nome", "cpf", "telefone", "email", "data_nascimento", "endereco"]
    faltando = [campo for campo in campos if campo not in dados]
    if faltando:
        return jsonify({"erro": "Campos obrigatórios ausentes", "campos": faltando}), 400

    pacientes = load_data("pacientes.json")
    novo = {
        "id": next_id(pacientes),
        
        "nome": dados["nome"],
        "cpf": dados["cpf"],
        
        "telefone": dados["telefone"],
        
        "email": dados["email"],
        "data_nascimento": dados["data_nascimento"],
        "endereco": dados["endereco"],
        "historico": dados.get("historico", []),
    }
    pacientes.append(novo)
    save_data("pacientes.json", pacientes)
    append_log("create", "pacientes", {"id": novo["id"]})
    return jsonify(novo), 201


@pacientes_bp.put("/pacientes/<int:id_paciente>")
def editar_paciente(id_paciente):
    dados = request.get_json(silent=True) or {}
    pacientes = load_data("pacientes.json")

    for paciente in pacientes:
        if paciente.get("id") == id_paciente:
            paciente.update(dados)
            save_data("pacientes.json", pacientes)
            append_log("update", "pacientes", {"id": id_paciente})
            return jsonify(paciente), 200

    return jsonify({"erro": "Paciente não encontrado"}), 404


@pacientes_bp.delete("/pacientes/<int:id_paciente>")
def excluir_paciente(id_paciente):
    pacientes = load_data("pacientes.json")
    atualizados = [item for item in pacientes if item.get("id") != id_paciente]
    if len(atualizados) == len(pacientes):
        return jsonify({"erro": "Paciente não encontrado"}), 404

    save_data("pacientes.json", atualizados)
    append_log("delete", "pacientes", {"id": id_paciente})
    return jsonify({"mensagem": "Paciente excluído com sucesso"}), 200
