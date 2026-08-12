import os
import sqlite3
from datetime import datetime
from tkinter import messagebox

from banco import CAMINHO_BANCO, caminho_do_programa


def pasta_backups():
    """Retorna a pasta onde os backups locais serão armazenados."""
    pasta = os.path.join(caminho_do_programa(), "backups")
    os.makedirs(pasta, exist_ok=True)
    return pasta


def fazer_backup_banco(janela=None):
    """
    Cria uma cópia consistente do banco SQLite usando a API de backup do próprio SQLite.
    O arquivo é salvo na pasta 'backups' com data e hora no nome.
    """
    if not os.path.exists(CAMINHO_BANCO):
        messagebox.showwarning(
            "Backup",
            "O banco de dados ainda não foi encontrado.",
            parent=janela,
        )
        return None

    agora = datetime.now()
    nome_arquivo = agora.strftime("portaria_backup_%Y-%m-%d_%H-%M-%S.db")
    destino = os.path.join(pasta_backups(), nome_arquivo)

    origem_conexao = None
    destino_conexao = None

    try:
        origem_conexao = sqlite3.connect(CAMINHO_BANCO)
        destino_conexao = sqlite3.connect(destino)

        origem_conexao.backup(destino_conexao)

        messagebox.showinfo(
            "Backup concluído",
            "Backup criado com sucesso!\n\n"
            f"Arquivo:\n{destino}",
            parent=janela,
        )

        return destino

    except Exception as erro:
        # Se uma tentativa incompleta tiver criado um arquivo vazio/parcial,
        # removemos para não confundir com um backup válido.
        try:
            if os.path.exists(destino):
                os.remove(destino)
        except OSError:
            pass

        messagebox.showerror(
            "Erro no backup",
            f"Não foi possível criar o backup.\n\n{erro}",
            parent=janela,
        )
        return None

    finally:
        if destino_conexao is not None:
            destino_conexao.close()

        if origem_conexao is not None:
            origem_conexao.close()