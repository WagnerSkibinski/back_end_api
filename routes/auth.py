from flask import Blueprint, jsonify, request

from services.json_manager import append_log


auth_bp = Blueprint("auth", __name__)

# usuario padrao
_USUARIOS_FIXOS = {
	"admin@vidaplus.com": {"senha": "admin123", "perfil": "admin", "nome": "Administrador"},
	"medico@vidaplus.com": {"senha": "med123", "perfil": "profissional", "nome": "Dr. Demo"},
	"paciente@vidaplus.com": {"senha": "pac123", "perfil": "paciente", "nome": "Paciente Demo"},
}

# ok
@auth_bp.post("/auth/login")
def login():
	dados = request.get_json(silent=True) or {}
	email = dados.get("email")
	senha = dados.get("senha")

	usuario = _USUARIOS_FIXOS.get(email)
	if not usuario or usuario.get("senha") != senha:
		append_log("login_failed", "auth", {"email": email})
		return jsonify({"erro": "Credenciais inválidas"}), 401

	token = f"token-{usuario['perfil']}-{email}"
	append_log("login_success", "auth", {"email": email, "perfil": usuario["perfil"]})
	return jsonify({"token": token, "perfil": usuario["perfil"], "nome": usuario["nome"]}), 200

#  necessidade de teste
@auth_bp.get("/auth/me")
def me():
	token = request.headers.get("Authorization", "").replace("Bearer ", "")
	if not token.startswith("token-"):
		return jsonify({"erro": "Token inválido"}), 401

	partes = token.split("-", 2)
	if len(partes) != 3:
		return jsonify({"erro": "Token inválido"}), 401

	return jsonify({"perfil": partes[1], "email": partes[2]}), 200
