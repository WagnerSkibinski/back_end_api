from flask import Blueprint, jsonify, request

from services.json_manager import append_log, load_data, next_id, save_data


telemedicina_bp = Blueprint("telemedicina", __name__)


@telemedicina_bp.get("/telemedicina/sessoes")
def listar_sessoes():
	return jsonify(load_data("telemedicina.json")), 200



# Não sei pq não vai (version1.0)
@telemedicina_bp.post("/telemedicina/sessoes")
def criar_sessao():
	dados = request.get_json(silent=True) or {}
	campos = ["consulta", "paciente", "profissional", "data", "hora"]
	faltando = [campo for campo in campos if campo not in dados]
	if faltando:
		return jsonify({"erro": "Campos obrigatórios ausentes", "campos": faltando}), 400

	sessoes = load_data("telemedicina.json")
	nova = {
		"id": next_id(sessoes),
		"consulta": dados["consulta"],
		"paciente": dados["paciente"],
		"profissional": dados["profissional"],
		"data": dados["data"],
		"hora": dados["hora"],
		"link": dados.get("link", f"https://tele.vidaplus.local/sala/{next_id(sessoes)}"),
		"status": dados.get("status", "Agendada"),
	}
	sessoes.append(nova)
	save_data("telemedicina.json", sessoes)
	append_log("create", "telemedicina", {"id": nova["id"]})
	return jsonify(nova), 201


# Verificar erro  na chave
@telemedicina_bp.put("/telemedicina/sessoes/<int:id_sessao>/encerrar")
def encerrar_sessao(id_sessao):
	sessoes = load_data("telemedicina.json")
	for sessao in sessoes:
		if sessao.get("id") == id_sessao:
			sessao["status"] = "Concluida"
			save_data("telemedicina.json", sessoes)
			append_log("update", "telemedicina", {"id": id_sessao, "status": "Concluida"})
			return jsonify(sessao), 200

	return jsonify({"erro": "Sessão não encontrada"}), 404
