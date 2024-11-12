import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Rota principal que serve o arquivo index.html
@app.route('/')
def index():
    return render_template('index.html')

# Rota para salvar o email no arquivo JSON
@app.route('/save-email', methods=['POST'])
def save_email():
    data = request.get_json()
    email = data.get('email')

    if email:
        try:
            # Se o arquivo não existir, cria com uma lista vazia
            if not os.path.exists('email.json'):
                with open('email.json', 'w') as file:
                    json.dump([], file)

            # Lê o conteúdo atual do arquivo JSON
            with open('email.json', 'r') as file:
                try:
                    emails = json.load(file)
                except json.JSONDecodeError:
                    emails = []  # Caso o arquivo esteja vazio ou corrompido

            # Adiciona o novo email à lista
            emails.append(email)

            # Salva a lista atualizada no arquivo
            with open('email.json', 'w') as file:
                json.dump(emails, file, indent=4)

            return jsonify({'status': 'success'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'error', 'message': 'No email provided'}), 400

# Rota para a página /dados
@app.route('/dados')
def dados():
    # Verifica se o arquivo existe e está em formato JSON válido
    if os.path.exists('email.json'):
        with open('email.json', 'r') as file:
            try:
                emails = json.load(file)
            except json.JSONDecodeError:
                emails = []  # Inicializa como lista vazia caso esteja corrompido
    else:
        emails = []

    # Passa os emails para o template dados.html
    return render_template('dados.html', emails=emails)

if __name__ == '__main__':
    app.run(debug=True)
