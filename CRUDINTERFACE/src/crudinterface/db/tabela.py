from CRUDINTERFACE.src.crudinterface.db.funcoes import conexao

def Tabela():
    conection = conexao()
    cursor = conection.cursor()

    command_SQL =  """
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT UNIQUE NOT NULL,
            endereco TEXT NOT NULL
        )
        """
    cursor.execute(command_SQL)
    conection.close()