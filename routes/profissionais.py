from flask import Blueprint, jsonify, request

from services.json_manager import append_log, load_data, next_id, save_data


profissionais_bp = Blueprint("profissionais", __name__)


@profissionais_bp.get("/profissionais")
def listar_profissionais():
    return jsonify(load_data("profissionais.json")), 200

# testar via postman
@profissionais_bp.get("/profissionais/<int:id_profissional>")
def buscar_profissional(id_profissional):
    profissionais = load_data("profissionais.json")
    profissional = next((item for item in profissionais if item.get("id") == id_profissional), None)
    if not profissional:
        return jsonify({"erro": "Profissional não encontrado"}), 404
    return jsonify(profissional), 200


@profissionais_bp.post("/profissionais")
def cadastrar_profissional():
    dados = request.get_json(silent=True) or {}
    campos = ["nome", "especialidade", "crm", "telefone", "email"]
    faltando = [campo for campo in campos if campo not in dados]
    if faltando:
        return jsonify({"erro": "Campos obrigatórios ausentes", "campos": faltando}), 400

    profissionais = load_data("profissionais.json")
    novo = {
        "id": next_id(profissionais),
        "nome": dados["nome"],
        "especialidade": dados["especialidade"],
        "crm": dados["crm"],
        "telefone": dados["telefone"],
        "email": dados["email"],
        "agenda": dados.get("agenda", []),
    }
    profissionais.append(novo)
    save_data("profissionais.json", profissionais)
    append_log("create", "profissionais", {"id": novo["id"]})
    return jsonify(novo), 201

# ok

@profissionais_bp.put("/profissionais/<int:id_profissional>")
def editar_profissional(id_profissional):
    dados = request.get_json(silent=True) or {}
    profissionais = load_data("profissionais.json")

    for profissional in profissionais:
        if profissional.get("id") == id_profissional:
            profissional.update(dados)
            save_data("profissionais.json", profissionais)
            append_log("update", "profissionais", {"id": id_profissional})
            return jsonify(profissional), 200

    return jsonify({"erro": "Profissional não encontrado"}), 404

# ok

@profissionais_bp.delete("/profissionais/<int:id_profissional>")
def excluir_profissional(id_profissional):
    profissionais = load_data("profissionais.json")
    atualizados = [item for item in profissionais if item.get("id") != id_profissional]
    if len(atualizados) == len(profissionais):
        return jsonify({"erro": "Profissional não encontrado"}), 404

    save_data("profissionais.json", atualizados)
    append_log("delete", "profissionais", {"id": id_profissional})
    return jsonify({"mensagem": "Profissional excluído com sucesso"}), 200

