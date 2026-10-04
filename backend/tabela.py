import sqlite3
from werkzeug.security import check_password_hash


def criar_table(login, senha):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id FROM usuarios WHERE login = ?",
        (login,)
    )

    usuario = cursor.fetchone()

    if usuario:
        conexao.close()
        return False

    cursor.execute(
        "INSERT INTO usuarios (login, senha) VALUES (?, ?)",
        (login, senha)
    )

    conexao.commit()
    conexao.close()

    return True


def verificar_credenciais(login, senha):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE login = ?",
        (login,)
    )

    usuario = cursor.fetchone()

    conexao.close()

    if usuario is None:
        return None

    if check_password_hash(usuario[2], senha):
        return usuario

    return None


def registrar_password(usuario_id, servico, senha):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO senhas (usuario_id, servico, senha) VALUES (?, ?, ?)",
        (usuario_id, servico, senha)
    )

    conexao.commit()
    conexao.close()


def buscar_passwords(usuario_id):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, servico, senha FROM senhas WHERE usuario_id = ?",
        (usuario_id,)
    )

    senhas = cursor.fetchall()

    conexao.close()

    return senhas