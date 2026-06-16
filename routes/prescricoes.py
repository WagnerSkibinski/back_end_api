from flask import Blueprint, jsonify, request

from services.json_manager import append_log, load_data, next_id, save_data


prescricoes_bp = Blueprint("prescricoes", __name__)


@prescricoes_bp.get("/prescricoes")
def listar_prescricoes():
    return jsonify(load_data("prescricoes.json")), 200

# ok
@prescricoes_bp.get("/prescricoes/<int:id_prescricao>")
def buscar_prescricao(id_prescricao):
    prescricoes = load_data("prescricoes.json")
    prescricao = next((item for item in prescricoes if item.get("id") == id_prescricao), None)
    if not prescricao:
        return jsonify({"erro": "Prescrição não encontrada"}), 404
    return jsonify(prescricao), 200

# ok
@prescricoes_bp.post("/prescricoes")
def cadastrar_prescricao():
    dados = request.get_json(silent=True) or {}
    campos = ["paciente", "profissional", "medicamentos", "orientacoes", "data"]
    faltando = [campo for campo in campos if campo not in dados]
    if faltando:
        return jsonify({"erro": "Campos obrigatórios ausentes", "campos": faltando}), 400

    prescricoes = load_data("prescricoes.json")
    nova = {
        "id": next_id(prescricoes),
        "paciente": dados["paciente"],
        "profissional": dados["profissional"],
        "medicamentos": dados["medicamentos"],
        "orientacoes": dados["orientacoes"],
        "data": dados["data"],
    }
    prescricoes.append(nova)
    save_data("prescricoes.json", prescricoes)
    append_log("create", "prescricoes", {"id": nova["id"]})
    return jsonify(nova), 201

#  revisar def
@prescricoes_bp.put("/prescricoes/<int:id_prescricao>")
def editar_prescricao(id_prescricao):
    dados = request.get_json(silent=True) or {}
    prescricoes = load_data("prescricoes.json")

    for prescricao in prescricoes:
        if prescricao.get("id") == id_prescricao:
            prescricao.update(dados)
            save_data("prescricoes.json", prescricoes)
            append_log("update", "prescricoes", {"id": id_prescricao})
            return jsonify(prescricao), 200

    return jsonify({"erro": "Prescrição não encontrada"}), 404

# ok
@prescricoes_bp.delete("/prescricoes/<int:id_prescricao>")
def excluir_prescricao(id_prescricao):
    prescricoes = load_data("prescricoes.json")
    atualizadas = [item for item in prescricoes if item.get("id") != id_prescricao]
    if len(atualizadas) == len(prescricoes):
        return jsonify({"erro": "Prescrição não encontrada"}), 404

    save_data("prescricoes.json", atualizadas)
    append_log("delete", "prescricoes", {"id": id_prescricao})
    return jsonify({"mensagem": "Prescrição excluída com sucesso"}), 200

