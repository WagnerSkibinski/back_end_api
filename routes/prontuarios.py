from flask import Blueprint, jsonify, request

from services.json_manager import append_log, load_data, next_id, save_data


prontuarios_bp = Blueprint("prontuarios", __name__)


@prontuarios_bp.get("/prontuarios")
def listar_prontuarios():
	return jsonify(load_data("prontuarios.json")), 200

# ok

@prontuarios_bp.get("/prontuarios/<int:id_prontuario>")
def buscar_prontuario(id_prontuario):
	prontuarios = load_data("prontuarios.json")
	prontuario = next((item for item in prontuarios if item.get("id") == id_prontuario), None)
	if not prontuario:
		return jsonify({"erro": "Prontuário não encontrado"}), 404
	return jsonify(prontuario), 200

# ok (version 1.0
# )
@prontuarios_bp.post("/prontuarios")
def cadastrar_prontuario():
	dados = request.get_json(silent=True) or {}
	campos = ["paciente", "profissional", "consulta", "evolucao", "data"]
	faltando = [campo for campo in campos if campo not in dados]
	if faltando:
		return jsonify({"erro": "Campos obrigatórios ausentes", "campos": faltando}), 400

	prontuarios = load_data("prontuarios.json")
	novo = {
		"id": next_id(prontuarios),
		"paciente": dados["paciente"],
		"profissional": dados["profissional"],
		"consulta": dados["consulta"],
		"evolucao": dados["evolucao"],
		"data": dados["data"],
	}
	prontuarios.append(novo)
	save_data("prontuarios.json", prontuarios)
	append_log("create", "prontuarios", {"id": novo["id"]})
	return jsonify(novo), 201

# ok

@prontuarios_bp.put("/prontuarios/<int:id_prontuario>")
def editar_prontuario(id_prontuario):
	dados = request.get_json(silent=True) or {}
	prontuarios = load_data("prontuarios.json")

	for prontuario in prontuarios:
		if prontuario.get("id") == id_prontuario:
			prontuario.update(dados)
			save_data("prontuarios.json", prontuarios)
			append_log("update", "prontuarios", {"id": id_prontuario})
			return jsonify(prontuario), 200

	return jsonify({"erro": "Prontuário não encontrado"}), 404
