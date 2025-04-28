from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import date
import sqlite3
from sqlite3 import Error

app: Flask = Flask(__name__)

def get_connection():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('./database/db-veiculos.db')
    conn.row_factory = sqlite3.Row  # Permite acessar os dados por nome das colunas
    return conn
@app.route('/')
def index():
    return render_template('index.html')  # Agora Flask vai procurar em templates/index.html

# Rota para listar todos os veículos
@app.route('/veiculos/listar', methods=['GET'])
def listar_veiculos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM veiculos')
        veiculos = cursor.fetchall()
        # lista_veiculos = [dict(veiculo) for veiculo in veiculos]
        # return jsonify(lista_veiculos), 200
        return render_template('listar.html',regs=veiculos)
    except Error as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()


# Rota para cadastrar um novo veículo

@app.route('/veiculos/cadastrar', methods=['GET','POST'])
def cadastrar_veiculo():
    if request.method == 'POST':
        modelo = request.form.get('modelo')
        marca = request.form.get('marca')
        ano = request.form.get('ano')
        placa = request.form.get('placa')
        datacriacao = date.today().isoformat()

        if not all([modelo, marca, ano, placa]):
            return jsonify({'erro': 'Dados incompletos'}), 400

        try:
            ano = int(ano)
        except ValueError:
            return jsonify({'erro': 'Ano deve ser um número inteiro'}), 400

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO veiculos (modelo, marca, ano, placa, datacriacao)
                           VALUES (?, ?, ?, ?, ?)''', (modelo, marca, ano, placa, datacriacao))
            conn.commit()
            mensagem = 'Veículo cadastrado com sucesso!'
            return render_template('cadastrar.html', mensagem=mensagem)
        except Error as e:
            return jsonify({'erro': str(e)}), 500
        finally:
            conn.close()

    return render_template('cadastrar.html')

# Rota para atualizar os dados de um veículo
@app.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
def atualizar_veiculo(id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Buscar dados do veículo para preencher o formulário
        cursor.execute('SELECT * FROM veiculos WHERE idveiculo = ?', (id,))
        veiculo = cursor.fetchone()
        conn.close()

        if veiculo is None:
            return jsonify({'erro': 'Veículo não encontrado'}), 404

        return render_template('editar.html', veiculo=veiculo)

    if request.method == 'POST':
        # Atualizar os dados recebidos do formulário
        modelo = request.form.get('modelo')
        marca = request.form.get('marca')
        ano = request.form.get('ano')
        placa = request.form.get('placa')

        if not all([modelo, marca, ano, placa]):
            return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

        try:
            ano = int(ano)
        except ValueError:
            return jsonify({'erro': 'Ano deve ser um número inteiro'}), 400

        try:
            cursor.execute('''UPDATE veiculos
                              SET modelo = ?, marca = ?, ano = ?, placa = ?
                              WHERE idveiculo = ?''', (modelo, marca, ano, placa, id))
            conn.commit()
            return redirect(url_for('listar_veiculos'))  # Redireciona para a página de listagem de veículos
        except Error as e:
            return jsonify({'erro': str(e)}), 500
        finally:
            conn.close()


# Rota para excluir um veículo
@app.route('/veiculos/deletar/<int:id>', methods=['GET', 'POST'])
def excluir_veiculo(id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Busca o veículo para confirmar a exclusão
        cursor.execute('SELECT * FROM veiculos WHERE idveiculo = ?', (id,))
        veiculo = cursor.fetchone()
        conn.close()

        if veiculo is None:
            return jsonify({'erro': 'Veículo não encontrado'}), 404

        return render_template('excluir.html', veiculo=veiculo)

    if request.method == 'POST':
        try:
            cursor.execute('SELECT * FROM veiculos WHERE idveiculo = ?', (id,))
            veiculo = cursor.fetchone()

            if veiculo is None:
                return jsonify({'erro': 'Veículo não encontrado'}), 404

            cursor.execute('DELETE FROM veiculos WHERE idveiculo = ?', (id,))
            conn.commit()
            return redirect(url_for('listar_veiculos'))  # Redireciona para a página de listagem de veículos
        except Error as e:
            return jsonify({'erro': str(e)}), 500
        finally:
            conn.close()
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

# Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True)
