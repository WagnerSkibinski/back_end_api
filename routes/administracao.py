from flask import Blueprint, jsonify, request

from services.json_manager import append_log, load_data, save_data


administracao_bp = Blueprint("administracao", __name__)

# ok
@administracao_bp.get("/administracao/leitos")
def listar_leitos():
	leitos = load_data("leitos.json")
	return jsonify(leitos), 200

# duvida de id
@administracao_bp.put("/administracao/leitos/<int:id_leito>")
def atualizar_leito(id_leito):
	dados = request.get_json(silent=True) or {}
	leitos = load_data("leitos.json")

	for leito in leitos:
		if leito.get("id") == id_leito:
			leito.update(dados)
			save_data("leitos.json", leitos)
			append_log("update", "leitos", {"id": id_leito})
			return jsonify(leito), 200

	return jsonify({"erro": "Leito não encontrado"}), 404


# ok
@administracao_bp.get("/administracao/relatorios/resumo")
def relatorio_resumo():
	pacientes = load_data("pacientes.json")
	profissionais = load_data("profissionais.json")
	consultas = load_data("consultas.json")
	leitos = load_data("leitos.json")

	ocupados = [item for item in leitos if item.get("status") == "Ocupado"]
	return jsonify(
		{
			"total_pacientes": len(pacientes),
			"total_profissionais": len(profissionais),
			"total_consultas": len(consultas),
			"leitos_total": len(leitos),
			"leitos_ocupados": len(ocupados),
		}
	), 200
