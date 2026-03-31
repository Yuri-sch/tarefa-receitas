import sqlite3
from datetime import date

conexao = sqlite3.connect('db.sqlite3')
cursor = conexao.cursor()

hoje = date.today().strftime('%Y-%m-%d')

print("Inserindo usuário...")
# Alterado para a tabela exata 'usuario' e situacao como texto
cursor.execute("""
    INSERT INTO usuario (nome, login, senha, situacao) 
    VALUES ('Administrador', 'admin', 'senha123', 'Ativo');
""")

print("Inserindo 10 receitas...")
# Alterado para a tabela exata 'receita' e custo como INT
receitas = [
    ('Bolo de Cenoura', 'Bolo fofinho com cobertura de chocolate.', hoje, 15, 'doce'),
    ('Coxinha de Frango', 'Massa de batata com recheio cremoso.', hoje, 5, 'salgada'),
    ('Brigadeiro', 'Docinho tradicional de leite condensado.', hoje, 2, 'doce'),
    ('Torta de Frango', 'Torta salgada de liquidificador.', hoje, 25, 'salgada'),
    ('Pudim de Leite', 'Pudim sem furinhos com calda.', hoje, 12, 'doce'),
    ('Empadão de Palmito', 'Massa podre que derrete na boca.', hoje, 30, 'salgada'),
    ('Beijinho', 'Docinho de coco ralado e cravo.', hoje, 2, 'doce'),
    ('Kibe Frito', 'Kibe tradicional temperado com hortelã.', hoje, 6, 'salgada'),
    ('Torta de Limão', 'Massa com creme de limão e merengue.', hoje, 22, 'doce'),
    ('Esfiha de Carne', 'Massa macia com carne moída.', hoje, 4, 'salgada')
]

cursor.executemany("""
    INSERT INTO receita (nome, descricao, data_registro, custo, tipo_receita) 
    VALUES (?, ?, ?, ?, ?);
""", receitas)

conexao.commit()
conexao.close()

print("Script de insert executado com sucesso! Banco populado.")