import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "CRUD.db"

def conexao():
    try:
        conection = sqlite3.connect(DB_FILE)
    
    except Exception as e:
        print(f"Houve uma falha ao conectar com o banco. Error : {e}")
        
    return conection


# Insert data
def insert_Data(nome, telefone, endereco):
    conection = conexao()
    cursor = conection.cursor()
    command_SQL = """INSERT INTO usuarios(nome, telefone, endereco) VALUES (?, ?, ?)"""
    try:
        cursor.execute(command_SQL, (nome, telefone, endereco))
        conection.commit()
        
    except sqlite3.IntegrityError as error:
        conection.rollback()
        raise error
    
    except Exception as e:
        conection.rollback()
        raise e
    
    finally:
        cursor.close()
        conection.close()
    

# List data
def List_Data():
    conection = conexao()
    cursor = conection.cursor()
    command_SQL = """SELECT * FROM usuarios"""
    cursor.execute(command_SQL)
    users = cursor.fetchall()
    cursor.close()
    conection.close()
    
    return users

# Find data
def Find_Data(id_user):
    conection = conexao()
    cursor = conection.cursor()
    command_SQL = """SELECT * FROM usuarios WHERE id = ?"""
    try:
        cursor.execute(command_SQL, (id_user,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conection.close()

# Delete data
def Delete_Data(id_user):
    conection = conexao()
    cursor = conection.cursor()
    command_SQL = """DELETE FROM usuarios WHERE id = ?"""
    cursor.execute(command_SQL, (id_user,))
    conection.commit()
    cursor.close()
    conection.close()
    

# Update data
def Update_Data(endereco, id_user):
    conection = conexao()
    cursor = conection.cursor()
    command_SQL = """UPDATE usuarios SET endereco = ? WHERE id = ?"""
    cursor.execute(command_SQL, (endereco, id_user))
    conection.commit()
    cursor.close()
    conection.close()
    
# Limpeza no banco
def Clean_Data():
    conection = conexao()
    cursor = conection.cursor()
    
    try:
        command_SQL = """DELETE FROM usuarios 
        WHERE nome IS NULL OR TRIM(nome) = ''
        OR telefone IS NULL OR TRIM(telefone) = '' 
        OR endereco IS NULL OR TRIM(endereco) = '' """
        
        cursor.execute(command_SQL)
        conection.commit()
        return cursor.rowcount #devolve quantos dados foram apagados
    
    except Exception as e:
        conection.rollback() #Desfaz qualquer alteração quando der erro
        raise e # envia o erro para o streamlit
    
    finally:
        cursor.close()
        conection.close()
        
# Zona de Perigo (Reiniciar o banco de dados)
def Reset_Table():
    conection = conexao()
    try:
        cursor = conection.cursor()
        # 1- Apaga todos os dados da tabela usuários do banco de dados
        cursor.execute("DELETE FROM usuarios")
        # 2- Reinicia o contador do ID (AUTOINCREMENT) para voltar ao 1
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='usuarios'")
        conection.commit()
    except Exception as e:
        conection.rollback()
        raise e
    finally:
        cursor.close()
        conection.close()