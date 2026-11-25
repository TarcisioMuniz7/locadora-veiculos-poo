
import hashlib
import hmac
import os

from banco.conexao import conectar

USUARIO_PADRAO = "admin"
SENHA_PADRAO = "admin123"


def gerar_hash(senha, sal):
    return hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), sal, 100_000
    ).hex()


class UsuarioDAO:

    def cadastrar(self, usuario, senha):
        sal = os.urandom(16)

        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO usuarios (usuario, senha_hash, sal)
                VALUES (?, ?, ?)
            """, (usuario, gerar_hash(senha, sal), sal.hex()))

            return cursor.lastrowid

    def autenticar(self, usuario, senha):
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT senha_hash, sal
                FROM usuarios
                WHERE usuario = ?
            """, (usuario,))

            linha = cursor.fetchone()

        if linha is None:
            return False

        senha_hash, sal = linha
        return hmac.compare_digest(
            senha_hash, gerar_hash(senha, bytes.fromhex(sal))
        )

    def criar_admin_padrao(self):
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            total = cursor.fetchone()[0]

        if total == 0:
            self.cadastrar(USUARIO_PADRAO, SENHA_PADRAO)
