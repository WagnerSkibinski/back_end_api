from flask import Blueprint, jsonify, request

from services.json_manager import append_log, load_data, next_id, save_data


consultas_bp = Blueprint("consultas", __name__)

# ok
def _conflito_horario(consultas, profissional, data, hora, ignorar_id=None):
    for consulta in consultas:
        if ignorar_id and consulta.get("id") == ignorar_id:
            continue
        if (
            consulta.get("profissional") == profissional
            and consulta.get("data") == data
            and consulta.get("hora") == hora
            and consulta.get("status") != "Cancelada"
        ):
            return True
    return False

# ok
@consultas_bp.get("/consultas")
def listar_consultas():
    return jsonify(load_data("consultas.json")), 200

# ok
@consultas_bp.get("/consultas/<int:id_consulta>")
def buscar_consulta(id_consulta):
    consultas = load_data("consultas.json")
    consulta = next((item for item in consultas if item.get("id") == id_consulta), None)
    if not consulta:
        return jsonify({"erro": "Consulta não encontrada"}), 404
    return jsonify(consulta), 200

# ok
@consultas_bp.post("/consultas")
def cadastrar_consulta():
    dados = request.get_json(silent=True) or {}
    campos = ["paciente", "profissional", "data", "hora", "tipo"]
    faltando = [campo for campo in campos if campo not in dados]
    if faltando:
        return jsonify({"erro": "Campos obrigatórios ausentes", "campos": faltando}), 400

    consultas = load_data("consultas.json")
    if _conflito_horario(consultas, dados["profissional"], dados["data"], dados["hora"]):
        return jsonify({"erro": "Conflito de agenda para o profissional"}), 409

    nova = {
        "id": next_id(consultas),
        "paciente": dados["paciente"],
        "profissional": dados["profissional"],
        "data": dados["data"],
        "hora": dados["hora"],
        "tipo": dados["tipo"],
        "status": dados.get("status", "Agendada"),
    }
    consultas.append(nova)
    save_data("consultas.json", consultas)
    append_log("create", "consultas", {"id": nova["id"]})
    return jsonify(nova), 201

# ok
@consultas_bp.put("/consultas/<int:id_consulta>")
def editar_consulta(id_consulta):
    dados = request.get_json(silent=True) or {}
    consultas = load_data("consultas.json")

    for consulta in consultas:
        if consulta.get("id") == id_consulta:
            novo_profissional = dados.get("profissional", consulta.get("profissional"))
            nova_data = dados.get("data", consulta.get("data"))
            nova_hora = dados.get("hora", consulta.get("hora"))
            if _conflito_horario(consultas, novo_profissional, nova_data, nova_hora, ignorar_id=id_consulta):
                return jsonify({"erro": "Conflito de agenda para o profissional"}), 409

            consulta.update(dados)
            save_data("consultas.json", consultas)
            append_log("update", "consultas", {"id": id_consulta})
            return jsonify(consulta), 200

    return jsonify({"erro": "Consulta não encontrada"}), 404

# ok
@consultas_bp.delete("/consultas/<int:id_consulta>")
def excluir_consulta(id_consulta):
    consultas = load_data("consultas.json")
    atualizadas = [item for item in consultas if item.get("id") != id_consulta]
    if len(atualizadas) == len(consultas):
        return jsonify({"erro": "Consulta não encontrada"}), 404

    save_data("consultas.json", atualizadas)
    append_log("delete", "consultas", {"id": id_consulta})
    return jsonify({"mensagem": "Consulta excluída com sucesso"}), 200
