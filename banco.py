import sqlite3
import os
import sys


# ==========================================================
# LOCAL DO BANCO DE DADOS
# ==========================================================

def caminho_do_programa():

    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    return os.path.dirname(os.path.abspath(__file__))


CAMINHO_BANCO = os.path.join(
    caminho_do_programa(),
    "portaria.db"
)


# ==========================================================
# CONEXÃO COM O BANCO
# ==========================================================

conexao = sqlite3.connect(CAMINHO_BANCO)
cursor = conexao.cursor()


# ==========================================================
# CRIAR TABELAS
# ==========================================================

def criar_tabelas():

    # ------------------------------------------------------
    # MORADORES
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            apartamento TEXT NOT NULL,
            telefone TEXT,
            tipo TEXT
        )
    """)

    # ------------------------------------------------------
    # PRESTADORES
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prestadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            documento TEXT NOT NULL,
            empresa TEXT,
            telefone TEXT
        )
    """)

    # ------------------------------------------------------
    # VISITANTES
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            documento TEXT NOT NULL,
            telefone TEXT
        )
    """)

    # ------------------------------------------------------
    # ACESSOS DE PRESTADORES
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS acessos_prestadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prestador_id INTEGER NOT NULL,
            apartamento TEXT NOT NULL,
            data_entrada TEXT NOT NULL,
            hora_entrada TEXT NOT NULL,
            data_saida TEXT,
            hora_saida TEXT,
            status TEXT NOT NULL DEFAULT 'ATIVO',
            FOREIGN KEY (prestador_id)
                REFERENCES prestadores(id)
        )
    """)


    # ------------------------------------------------------
    # OPERADORES
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            senha_salt TEXT NOT NULL,
            ativo INTEGER NOT NULL DEFAULT 1,
            criado_em TEXT NOT NULL
        )
    """)

    conexao.commit()

    # ======================================================
    # ATUALIZAÇÃO AUTOMÁTICA DA TABELA MORADORES
    # ======================================================
    # Verifica se a coluna "vagas" já existe.
    # Se não existir, cria sem apagar os moradores atuais.

    cursor.execute("""
        PRAGMA table_info(moradores)
    """)

    colunas = cursor.fetchall()

    nomes_colunas = [
        coluna[1]
        for coluna in colunas
    ]

    if "vagas" not in nomes_colunas:

        cursor.execute("""
            ALTER TABLE moradores
            ADD COLUMN vagas TEXT
        """)

        conexao.commit()

    # ======================================================
    # ATUALIZAÇÃO AUTOMÁTICA DA TABELA DE ACESSOS
    # ======================================================
    # Acrescenta os operadores responsáveis pela entrada e
    # pela saída sem apagar os acessos que já existem.

    cursor.execute("""
        PRAGMA table_info(acessos_prestadores)
    """)

    colunas_acessos = cursor.fetchall()

    nomes_colunas_acessos = [
        coluna[1]
        for coluna in colunas_acessos
    ]

    if "operador_entrada_id" not in nomes_colunas_acessos:

        cursor.execute("""
            ALTER TABLE acessos_prestadores
            ADD COLUMN operador_entrada_id INTEGER
        """)

        conexao.commit()

    if "operador_saida_id" not in nomes_colunas_acessos:

        cursor.execute("""
            ALTER TABLE acessos_prestadores
            ADD COLUMN operador_saida_id INTEGER
        """)

        conexao.commit()


# ==========================================================
# CADASTRAR MORADOR
# ==========================================================

def cadastrar_morador(
    nome,
    apartamento,
    vagas,
    telefone,
    tipo
):

    cursor.execute("""
        INSERT INTO moradores
        (
            nome,
            apartamento,
            vagas,
            telefone,
            tipo
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        nome,
        apartamento,
        vagas,
        telefone,
        tipo
    ))

    conexao.commit()


# ==========================================================
# LISTAR MORADORES
# ==========================================================

def listar_moradores():

    cursor.execute("""
        SELECT
            id,
            nome,
            apartamento,
            vagas,
            telefone,
            tipo
        FROM moradores
        ORDER BY nome
    """)

    return cursor.fetchall()


# ==========================================================
# PESQUISAR MORADORES
# ==========================================================

def pesquisar_moradores(nome):

    cursor.execute("""
        SELECT
            id,
            nome,
            apartamento,
            vagas,
            telefone,
            tipo
        FROM moradores
        WHERE nome LIKE ?
        ORDER BY nome
    """, (
        f"%{nome}%",
    ))

    return cursor.fetchall()


# ==========================================================
# ATUALIZAR MORADOR
# ==========================================================

def atualizar_morador(
    id_morador,
    nome,
    apartamento,
    vagas,
    telefone,
    tipo
):

    cursor.execute("""
        UPDATE moradores

        SET
            nome = ?,
            apartamento = ?,
            vagas = ?,
            telefone = ?,
            tipo = ?

        WHERE id = ?
    """, (
        nome,
        apartamento,
        vagas,
        telefone,
        tipo,
        id_morador
    ))

    conexao.commit()


# ==========================================================
# EXCLUIR MORADOR
# ==========================================================

def excluir_morador(id_morador):

    cursor.execute("""
        DELETE FROM moradores
        WHERE id = ?
    """, (
        id_morador,
    ))

    conexao.commit()


# ==========================================================
# CADASTRAR PRESTADOR
# ==========================================================

def cadastrar_prestador(
    nome,
    documento,
    empresa,
    telefone
):

    cursor.execute("""
        INSERT INTO prestadores
        (
            nome,
            documento,
            empresa,
            telefone
        )
        VALUES (?, ?, ?, ?)
    """, (
        nome,
        documento,
        empresa,
        telefone
    ))

    conexao.commit()


# ==========================================================
# LISTAR PRESTADORES
# ==========================================================

def listar_prestadores():

    cursor.execute("""
        SELECT
            id,
            nome,
            documento,
            empresa,
            telefone
        FROM prestadores
        ORDER BY nome
    """)

    return cursor.fetchall()


# ==========================================================
# PESQUISAR PRESTADORES
# ==========================================================

def pesquisar_prestadores(nome):

    cursor.execute("""
        SELECT
            id,
            nome,
            documento,
            empresa,
            telefone
        FROM prestadores
        WHERE nome LIKE ?
        ORDER BY nome
    """, (
        f"%{nome}%",
    ))

    return cursor.fetchall()


# ==========================================================
# ATUALIZAR PRESTADOR
# ==========================================================

def atualizar_prestador(
    id_prestador,
    nome,
    documento,
    empresa,
    telefone
):

    cursor.execute("""
        UPDATE prestadores

        SET
            nome = ?,
            documento = ?,
            empresa = ?,
            telefone = ?

        WHERE id = ?
    """, (
        nome,
        documento,
        empresa,
        telefone,
        id_prestador
    ))

    conexao.commit()


# ==========================================================
# EXCLUIR PRESTADOR
# ==========================================================

def excluir_prestador(id_prestador):

    cursor.execute("""
        DELETE FROM prestadores
        WHERE id = ?
    """, (
        id_prestador,
    ))

    conexao.commit()


# ==========================================================
# REGISTRAR ENTRADA DE PRESTADOR
# ==========================================================

def registrar_entrada_prestador(
    prestador_id,
    apartamento,
    data_entrada,
    hora_entrada,
    operador_entrada_id
):

    cursor.execute("""
        INSERT INTO acessos_prestadores (
            prestador_id,
            apartamento,
            data_entrada,
            hora_entrada,
            status,
            operador_entrada_id
        )
        VALUES (?, ?, ?, ?, 'ATIVO', ?)
    """, (
        prestador_id,
        apartamento,
        data_entrada,
        hora_entrada,
        operador_entrada_id
    ))

    conexao.commit()


# ==========================================================
# LISTAR ACESSOS ATIVOS
# ==========================================================

def listar_acessos_ativos():

    cursor.execute("""
        SELECT
            acessos_prestadores.id,
            prestadores.nome,
            prestadores.documento,
            prestadores.empresa,
            acessos_prestadores.apartamento,
            acessos_prestadores.data_entrada,
            acessos_prestadores.hora_entrada

        FROM acessos_prestadores

        INNER JOIN prestadores
        ON prestadores.id =
           acessos_prestadores.prestador_id

        WHERE acessos_prestadores.status = 'ATIVO'

        ORDER BY acessos_prestadores.id DESC
    """)

    return cursor.fetchall()


# ==========================================================
# REGISTRAR SAÍDA DE PRESTADOR
# ==========================================================

def registrar_saida_prestador(
    id_acesso,
    data_saida,
    hora_saida,
    operador_saida_id
):

    cursor.execute("""
        UPDATE acessos_prestadores

        SET
            data_saida = ?,
            hora_saida = ?,
            status = 'FINALIZADO',
            operador_saida_id = ?

        WHERE id = ?
    """, (
        data_saida,
        hora_saida,
        operador_saida_id,
        id_acesso
    ))

    conexao.commit()


# ==========================================================
# HISTÓRICO DE ACESSOS
# ==========================================================

def listar_historico_acessos():

    cursor.execute("""
        SELECT
            acessos_prestadores.id,
            prestadores.nome,
            prestadores.documento,
            prestadores.empresa,
            acessos_prestadores.apartamento,
            acessos_prestadores.data_entrada,
            acessos_prestadores.hora_entrada,
            acessos_prestadores.data_saida,
            acessos_prestadores.hora_saida,
            acessos_prestadores.status,
            COALESCE(operador_entrada.nome, '-'),
            COALESCE(operador_saida.nome, '-')

        FROM acessos_prestadores

        INNER JOIN prestadores
        ON prestadores.id =
           acessos_prestadores.prestador_id

        LEFT JOIN operadores AS operador_entrada
        ON operador_entrada.id =
           acessos_prestadores.operador_entrada_id

        LEFT JOIN operadores AS operador_saida
        ON operador_saida.id =
           acessos_prestadores.operador_saida_id

        ORDER BY acessos_prestadores.id DESC
    """)

    return cursor.fetchall()


# ==========================================================
# CADASTRAR VISITANTE
# ==========================================================

def cadastrar_visitante(
    nome,
    documento,
    telefone
):

    cursor.execute("""
        INSERT INTO visitantes
        (
            nome,
            documento,
            telefone
        )
        VALUES (?, ?, ?)
    """, (
        nome,
        documento,
        telefone
    ))

    conexao.commit()


# ==========================================================
# LISTAR VISITANTES
# ==========================================================

def listar_visitantes():

    cursor.execute("""
        SELECT
            id,
            nome,
            documento,
            telefone
        FROM visitantes
        ORDER BY nome
    """)

    return cursor.fetchall()


# ==========================================================
# PESQUISAR VISITANTES
# ==========================================================

def pesquisar_visitantes(nome):

    cursor.execute("""
        SELECT
            id,
            nome,
            documento,
            telefone
        FROM visitantes
        WHERE nome LIKE ?
        ORDER BY nome
    """, (
        f"%{nome}%",
    ))

    return cursor.fetchall()


# ==========================================================
# ATUALIZAR VISITANTE
# ==========================================================

def atualizar_visitante(
    id_visitante,
    nome,
    documento,
    telefone
):

    cursor.execute("""
        UPDATE visitantes

        SET
            nome = ?,
            documento = ?,
            telefone = ?

        WHERE id = ?
    """, (
        nome,
        documento,
        telefone,
        id_visitante
    ))

    conexao.commit()


# ==========================================================
# EXCLUIR VISITANTE
# ==========================================================

def excluir_visitante(id_visitante):

    cursor.execute("""
        DELETE FROM visitantes
        WHERE id = ?
    """, (
        id_visitante,
    ))

    conexao.commit()

# ==========================================================
# OPERADORES
# ==========================================================

def contar_operadores_ativos():

    cursor.execute("""
        SELECT COUNT(*)
        FROM operadores
        WHERE ativo = 1
    """)

    return cursor.fetchone()[0]


def cadastrar_operador(
    nome,
    usuario,
    senha_hash,
    senha_salt,
    criado_em
):

    cursor.execute("""
        INSERT INTO operadores
        (
            nome,
            usuario,
            senha_hash,
            senha_salt,
            ativo,
            criado_em
        )
        VALUES (?, ?, ?, ?, 1, ?)
    """, (
        nome,
        usuario,
        senha_hash,
        senha_salt,
        criado_em
    ))

    conexao.commit()


def buscar_operador_por_usuario(usuario):

    cursor.execute("""
        SELECT
            id,
            nome,
            usuario,
            senha_hash,
            senha_salt,
            ativo
        FROM operadores
        WHERE lower(usuario) = lower(?)
        LIMIT 1
    """, (
        usuario,
    ))

    return cursor.fetchone()


def listar_operadores():

    cursor.execute("""
        SELECT
            id,
            nome,
            usuario,
            ativo,
            criado_em
        FROM operadores
        ORDER BY nome
    """)

    return cursor.fetchall()