import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

# erro na busca
from routes.administracao import administracao_bp
from routes.auth import auth_bp
from routes.consultas import consultas_bp
from routes.pacientes import pacientes_bp
from routes.prescricoes import prescricoes_bp
from routes.profissionais import profissionais_bp
from routes.prontuarios import prontuarios_bp
from routes.telemedicina import telemedicina_bp


load_dotenv()


def create_app():
	app = Flask(__name__)
 
	app.config["API_KEY"] = os.getenv("API_KEY", "")

	app.register_blueprint(auth_bp)
	app.register_blueprint(pacientes_bp)
 
	# Api fora (verificar def)
	app.register_blueprint(profissionais_bp)
 
	app.register_blueprint(consultas_bp)
	app.register_blueprint(prontuarios_bp)
	app.register_blueprint(prescricoes_bp)
	app.register_blueprint(telemedicina_bp)
	app.register_blueprint(administracao_bp)

	@app.before_request
	def validar_api_key():
		# Healthcheck fica livre para monitoramento simples.
		if request.path == "/health":
			return None

		api_key_esperada = app.config.get("API_KEY", "")
		api_key_recebida = request.headers.get("X-API-KEY", "")

		if not api_key_esperada:
			return jsonify({"erro": "API_KEY nao configurada no servidor"}), 500

		if api_key_recebida != api_key_esperada:
			return jsonify({"erro": "Nao autorizado. X-API-KEY invalida"}), 401

		return None



	@app.get("/health")
	def health_check():
		return jsonify({"status": "ok"}), 200

	return app


app = create_app()

# Run app.py para funcionar
if __name__ == "__main__":
	app.run(debug=False)
