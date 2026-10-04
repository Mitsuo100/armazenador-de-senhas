import os

from dotenv import load_dotenv
from flask import Flask, request, render_template, flash, redirect, url_for, session
from tabela import criar_table, verificar_credenciais, registrar_password, buscar_passwords
from werkzeug.security import generate_password_hash
from cryptography.fernet import Fernet

load_dotenv()

def criar_site():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.secret_key = os.getenv('FLASK_SECRET_KEY')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/cadastro', methods=['POST'])
    def cadastrar():
        login = request.form['login']
        senha = request.form['senha']

        senha_hash = generate_password_hash(senha)

        criado = criar_table(login, senha_hash)

        if not criado:
            flash('Esse login já está cadastrado.', 'erro')
            return redirect(url_for('index'))

        key = Fernet.generate_key().decode()

        flash('Guarde sua key: ' + key, 'sucesso')

        return redirect(url_for('index'))

    @app.route('/login', methods=['POST'])
    def login():
        login = request.form['login']
        senha = request.form['senha']

        usuario = verificar_credenciais(login, senha)

        if usuario:
            session['usuario_id'] = usuario[0]
            return redirect(url_for('senhas'))

        flash('Credenciais inválidas!', 'erro')

        return redirect(url_for('index'))

    @app.route('/senhas')
    def senhas():
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'erro')
            return redirect(url_for('index'))

        usuario_id = session['usuario_id']

        passwords = buscar_passwords(usuario_id)

        return render_template(
            'senhas.html',
            passwords=passwords
        )

    @app.route('/registrar-password', methods=['POST'])
    def registra_password():
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para registrar uma senha.', 'erro')
            return redirect(url_for('index'))

        servico = request.form['servico']
        key = request.form['key']
        senha = request.form['password']

        try:
            cipher = Fernet(key)

            senha_criptografada = cipher.encrypt(
                senha.encode()
            ).decode()

        except Exception:
            flash('Key de criptografia inválida.', 'erro')
            return redirect(url_for('senhas'))

        usuario_id = session['usuario_id']

        registrar_password(
            usuario_id,
            servico,
            senha_criptografada
        )

        flash('Senha salva com sucesso!', 'sucesso')

        return redirect(url_for('senhas'))

    @app.route('/descriptografar', methods=['POST'])
    def descriptografar():
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'erro')
            return redirect(url_for('index'))

        key = request.form['key']

        try:
            cipher = Fernet(key)
        except Exception:
            flash('Key de criptografia inválida.', 'erro')
            return redirect(url_for('senhas'))

        usuario_id = session['usuario_id']

        passwords = buscar_passwords(usuario_id)

        senhas_descriptografadas = []

        try:
            for password in passwords:
                senha_original = cipher.decrypt(
                    password[2].encode()
                ).decode()

                senhas_descriptografadas.append(
                    (
                        password[0],
                        password[1],
                        senha_original
                    )
                )

        except Exception:
            flash('A key não corresponde às senhas armazenadas.', 'erro')
            return redirect(url_for('senhas'))

        return render_template(
            'senhas.html',
            passwords=passwords,
            senhas_descriptografadas=senhas_descriptografadas
        )

    return app