"""
Servidor Flask para o Agente Auditor de Documentos

Disponibiliza um endpoint REST para enviar um PDF e as categorias desejadas,
executa o fluxo do Agente Auditor e retorna o Relatório Final em JSON.
"""

import os
import json
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from .agent.auditor import AgenteAuditor
from .models.contratos import EntradaRequest

app = Flask(__name__)

# Configurações de Upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB

# Instanciar o Agente
agente = AgenteAuditor()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/auditar', methods=['POST'])
def auditar_documento():
    """
    Endpoint principal para auditoria.
    Recebe multipart/form-data com:
    - file: Arquivo PDF
    - categorias: String JSON com a lista de categorias (ex: '["estrutura", "ortografia"]')
    """
    if 'file' not in request.files:
        return jsonify({
            "status_final": "erro",
            "validacao": False,
            "motivo": "Nenhum arquivo enviado na requisição."
        }), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "status_final": "erro",
            "validacao": False,
            "motivo": "Nenhum arquivo selecionado."
        }), 400
        
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({
            "status_final": "erro",
            "validacao": False,
            "motivo": "O arquivo deve ser obrigatoriamente um PDF."
        }), 400

    # Processar categorias
    categorias_str = request.form.get('categorias', '["estrutura", "referencias", "ortografia"]')
    try:
        categorias = json.loads(categorias_str)
        if not isinstance(categorias, list) or len(categorias) == 0:
            raise ValueError
    except Exception:
        return jsonify({
            "status_final": "erro",
            "validacao": False,
            "motivo": "Formato inválido para as categorias. Envie um JSON Array válido."
        }), 400

    # Salvar o arquivo temporariamente
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file.save(filepath)
        
        # Montar a requisição e chamar o agente
        req = EntradaRequest(
            arquivo=filepath,
            categorias=categorias
        )
        
        resultado = agente.executar_auditoria(req)
        
        # Opcional: Remover o arquivo após processamento para não lotar o servidor
        try:
            os.remove(filepath)
        except OSError:
            pass
            
        # Determinar status HTTP baseado na validação
        status_code = 200 if resultado.get("validacao") else 207  # 207 Multi-Status
        if resultado.get("status_final") == "erro":
            status_code = 400
            
        return jsonify(resultado), status_code
        
    except Exception as e:
        return jsonify({
            "status_final": "erro",
            "validacao": False,
            "motivo": f"Erro interno do servidor: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Rota simples para verificar se a API está no ar."""
    return jsonify({"status": "Agente Auditor Operacional"}), 200

if __name__ == '__main__':
    print(f"🚀 Iniciando Agente Auditor API...")
    print(f"📂 Diretório de uploads: {app.config['UPLOAD_FOLDER']}")
    app.run(host='0.0.0.0', port=5000, debug=True)
