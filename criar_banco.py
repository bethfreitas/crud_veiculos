import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('db-veiculos.db')

# Criar um cursor
cursor = conn.cursor()

# Consultar as tabelas do banco de dados
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

# Verificar se a tabela 'veiculos' existe
if ('veiculos',) in tabelas:
    print("Tabela 'veiculos' encontrada!")
else:
    print("Tabela 'veiculos' não encontrada!")

# Fechar a conexão
conn.close()
