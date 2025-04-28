from flask import Flask, request, jsonify, render_template
from datetime import date
import sqlite3
from sqlite3 import Error

app: Flask = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Agora Flask vai procurar em templates/index.html

# if __name__ == '__main__':
#     app.run(debug=True)

def get_connection():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('db-veiculos.db')
    conn.row_factory = sqlite3.Row  # Permite acessar os dados por nome das colunas
    return conn


# Rota para listar todos os veículos
@app.route('/veiculos', methods=['GET'])
def listar_veiculos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM veiculos')
        veiculos = cursor.fetchall()
        lista_veiculos = [dict(veiculo) for veiculo in veiculos]
        return jsonify(lista_veiculos), 200
    except Error as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()


# Rota para cadastrar um novo veículo
@app.route('/veiculos', methods=['POST'])
def cadastrar_veiculo():
    data = request.get_json()  # Recebe os dados no formato JSON
    modelo = data.get('modelo')
    marca = data.get('marca')
    ano = data.get('ano')
    placa = data.get('placa')
    datacriacao = date.today().isoformat()  # Data de criação do veículo

    if not all([modelo, marca, ano, placa]):
        return jsonify({'erro': 'Dados incompletos'}), 400

    try:
        ano = int(ano)  # Garantir que o ano seja um número inteiro
    except ValueError:
        return jsonify({'erro': 'Ano deve ser um número inteiro'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO veiculos (modelo, marca, ano, placa, datacriacao)
                       VALUES (?, ?, ?, ?, ?)''', (modelo, marca, ano, placa, datacriacao))
        conn.commit()
        return jsonify({'mensagem': 'Veículo cadastrado com sucesso'}), 201
    except Error as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()


# Rota para atualizar os dados de um veículo
@app.route('/veiculos/<int:id>', methods=['PUT'])
def atualizar_veiculo(id):
    data = request.get_json()  # Recebe os dados no formato JSON
    modelo = data.get('modelo')
    marca = data.get('marca')
    ano = data.get('ano')
    placa = data.get('placa')

    if not any([modelo, marca, ano, placa]):
        return jsonify({'erro': 'Dados para atualização não fornecidos'}), 400

    try:
        ano = int(ano)  # Garantir que o ano seja um número inteiro
    except ValueError:
        return jsonify({'erro': 'Ano deve ser um número inteiro'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM veiculos WHERE idveiculo = ?', (id,))
        veiculo = cursor.fetchone()
        if veiculo is None:
            return jsonify({'erro': 'Veículo não encontrado'}), 404

        campos = []
        valores = []

        if modelo:
            campos.append('modelo = ?')
            valores.append(modelo)
        if marca:
            campos.append('marca = ?')
            valores.append(marca)
        if ano:
            campos.append('ano = ?')
            valores.append(ano)
        if placa:
            campos.append('placa = ?')
            valores.append(placa)

        valores.append(id)
        sql = f'UPDATE veiculos SET {", ".join(campos)} WHERE idveiculo = ?'
        cursor.execute(sql, valores)
        conn.commit()
        return jsonify({'mensagem': 'Veículo atualizado com sucesso'}), 200
    except Error as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()


# Rota para excluir um veículo
@app.route('/veiculos/<int:id>', methods=['DELETE'])
def excluir_veiculo(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM veiculos WHERE idveiculo = ?', (id,))
        veiculo = cursor.fetchone()
        if veiculo is None:
            return jsonify({'erro': 'Veículo não encontrado'}), 404

        cursor.execute('DELETE FROM veiculos WHERE idveiculo = ?', (id,))
        conn.commit()
        return jsonify({'mensagem': 'Veículo excluído com sucesso'}), 200
    except Error as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()


# Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True)
