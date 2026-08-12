import hashlib
import hmac
import secrets
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from banco import (
    contar_operadores_ativos,
    cadastrar_operador,
    buscar_operador_por_usuario,
)

COR_FUNDO = "#0B1220"
COR_TOPO = "#111D30"
COR_CARTAO = "#17263A"
COR_BORDA = "#253B56"
COR_CAMPO = "#0F1B2D"
COR_BOTAO = "#1B2D45"
COR_BOTAO_HOVER = "#274463"
COR_SUCESSO = "#2E7D32"
COR_SUCESSO_HOVER = "#256428"
COR_TEXTO = "#F5F7FA"
COR_TEXTO_2 = "#A9B7C6"
COR_DESTAQUE = "#D32F2F"

FONTE = "Segoe UI"
ITERACOES_HASH = 200_000


def gerar_hash_senha(senha, salt_hex=None):

    if salt_hex is None:
        salt = secrets.token_bytes(16)
        salt_hex = salt.hex()
    else:
        salt = bytes.fromhex(salt_hex)

    senha_hash = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt,
        ITERACOES_HASH,
    )

    return senha_hash.hex(), salt_hex


def senha_confere(
    senha_digitada,
    hash_salvo,
    salt_salvo
):

    hash_digitado, _ = gerar_hash_senha(
        senha_digitada,
        salt_salvo,
    )

    return hmac.compare_digest(
        hash_digitado,
        hash_salvo,
    )


def centralizar(
    janela,
    largura,
    altura
):

    janela.update_idletasks()

    x = max(
        (janela.winfo_screenwidth() - largura) // 2,
        0,
    )

    y = max(
        (janela.winfo_screenheight() - altura) // 2,
        0,
    )

    janela.geometry(
        f"{largura}x{altura}+{x}+{y}"
    )


def criar_entry(
    parent,
    mostrar=None
):

    return tk.Entry(
        parent,
        show=mostrar,
        font=(FONTE, 11),
        bg=COR_CAMPO,
        fg=COR_TEXTO,
        insertbackground=COR_TEXTO,
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground=COR_BORDA,
        highlightcolor="#4C78A8",
    )


def criar_botao(
    parent,
    texto,
    comando,
    principal=False
):

    normal = (
        COR_SUCESSO
        if principal
        else COR_BOTAO
    )

    hover = (
        COR_SUCESSO_HOVER
        if principal
        else COR_BOTAO_HOVER
    )

    botao = tk.Button(
        parent,
        text=texto,
        command=comando,
        font=(FONTE, 10, "bold"),
        bg=normal,
        fg=COR_TEXTO,
        activebackground=hover,
        activeforeground=COR_TEXTO,
        relief="flat",
        bd=0,
        padx=18,
        pady=10,
        cursor="hand2",
    )

    botao.bind(
        "<Enter>",
        lambda _evento: botao.config(bg=hover)
    )

    botao.bind(
        "<Leave>",
        lambda _evento: botao.config(bg=normal)
    )

    return botao


def criar_primeiro_operador(
    janela_pai
):

    resultado = {
        "criado": False
    }

    janela = tk.Toplevel(
        janela_pai
    )

    janela.title(
        "Primeiro acesso"
    )

    janela.configure(
        bg=COR_FUNDO
    )

    janela.resizable(
        False,
        False
    )

    centralizar(
        janela,
        620,
        530
    )

    janela.transient(
        janela_pai
    )

    janela.grab_set()

    topo = tk.Frame(
        janela,
        bg=COR_TOPO,
        height=105,
    )

    topo.pack(
        fill="x"
    )

    topo.pack_propagate(
        False
    )

    tk.Label(
        topo,
        text="Configuração inicial",
        font=(FONTE, 20, "bold"),
        bg=COR_TOPO,
        fg=COR_TEXTO,
    ).pack(
        anchor="w",
        padx=30,
        pady=(20, 0),
    )

    tk.Label(
        topo,
        text="Crie o primeiro operador do Sistema de Portaria.",
        font=(FONTE, 9),
        bg=COR_TOPO,
        fg=COR_TEXTO_2,
    ).pack(
        anchor="w",
        padx=31,
        pady=(3, 0),
    )

    card = tk.Frame(
        janela,
        bg=COR_CARTAO,
        highlightthickness=1,
        highlightbackground=COR_BORDA,
    )

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=26,
    )

    form = tk.Frame(
        card,
        bg=COR_CARTAO,
    )

    form.pack(
        fill="x",
        padx=30,
        pady=(26, 10),
    )

    form.grid_columnconfigure(
        1,
        weight=1,
    )

    campos = [
        ("Nome completo", None),
        ("Usuário", None),
        ("Senha", "•"),
        ("Confirmar senha", "•"),
    ]

    entradas = []

    for linha, (
        rotulo,
        mostrar
    ) in enumerate(campos):

        tk.Label(
            form,
            text=rotulo,
            font=(FONTE, 10, "bold"),
            bg=COR_CARTAO,
            fg=COR_TEXTO_2,
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=9,
        )

        campo = criar_entry(
            form,
            mostrar
        )

        campo.grid(
            row=linha,
            column=1,
            sticky="ew",
            ipady=8,
            pady=9,
        )

        entradas.append(
            campo
        )

    nome, usuario, senha, confirmar = entradas

    tk.Label(
        card,
        text="A senha será protegida por hash e não ficará salva em texto puro.",
        font=(FONTE, 8),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
    ).pack(
        anchor="w",
        padx=30,
        pady=(0, 5),
    )

    def salvar():

        nome_txt = (
            nome.get().strip()
        )

        usuario_txt = (
            usuario.get().strip()
        )

        senha_txt = senha.get()
        confirmar_txt = confirmar.get()

        if (
            not nome_txt
            or not usuario_txt
            or not senha_txt
        ):

            messagebox.showwarning(
                "Atenção",
                "Preencha nome, usuário e senha.",
                parent=janela,
            )

            return

        if len(usuario_txt) < 3:

            messagebox.showwarning(
                "Atenção",
                "O usuário deve ter pelo menos 3 caracteres.",
                parent=janela,
            )

            return

        if len(senha_txt) < 6:

            messagebox.showwarning(
                "Atenção",
                "A senha deve ter pelo menos 6 caracteres.",
                parent=janela,
            )

            return

        if senha_txt != confirmar_txt:

            messagebox.showwarning(
                "Atenção",
                "As senhas não conferem.",
                parent=janela,
            )

            return

        senha_hash, senha_salt = (
            gerar_hash_senha(
                senha_txt
            )
        )

        try:

            cadastrar_operador(
                nome_txt,
                usuario_txt,
                senha_hash,
                senha_salt,
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),
            )

        except Exception as erro:

            mensagem = str(erro)

            if "UNIQUE" in mensagem.upper():

                mensagem = (
                    "Esse nome de usuário "
                    "já está cadastrado."
                )

            messagebox.showerror(
                "Erro",
                "Não foi possível criar "
                "o operador.\n\n"
                f"{mensagem}",
                parent=janela,
            )

            return

        resultado["criado"] = True

        messagebox.showinfo(
            "Operador criado",
            "Primeiro operador criado com sucesso.\n\n"
            "Agora faça login para entrar no sistema.",
            parent=janela,
        )

        janela.destroy()

    botoes = tk.Frame(
        card,
        bg=COR_CARTAO,
    )

    botoes.pack(
        fill="x",
        padx=30,
        pady=(14, 26),
    )

    criar_botao(
        botoes,
        "Criar operador",
        salvar,
        principal=True,
    ).pack(
        side="right"
    )

    nome.bind(
        "<Return>",
        lambda _evento: usuario.focus_set()
    )

    usuario.bind(
        "<Return>",
        lambda _evento: senha.focus_set()
    )

    senha.bind(
        "<Return>",
        lambda _evento: confirmar.focus_set()
    )

    confirmar.bind(
        "<Return>",
        lambda _evento: salvar()
    )

    nome.focus_set()

    janela_pai.wait_window(
        janela
    )

    return resultado["criado"]


def solicitar_login(
    janela_pai
):

    if contar_operadores_ativos() == 0:

        criado = criar_primeiro_operador(
            janela_pai
        )

        if not criado:
            return None

    resultado = {
        "operador": None
    }

    janela = tk.Toplevel(
        janela_pai
    )

    janela.title(
        "Login - Sistema de Portaria"
    )

    janela.configure(
        bg=COR_FUNDO
    )

    janela.resizable(
        False,
        False
    )

    centralizar(
        janela,
        580,
        440
    )

    janela.transient(
        janela_pai
    )

    janela.grab_set()

    topo = tk.Frame(
        janela,
        bg=COR_TOPO,
        height=115,
    )

    topo.pack(
        fill="x"
    )

    topo.pack_propagate(
        False
    )

    tk.Label(
        topo,
        text="SISTEMA DE PORTARIA",
        font=(FONTE, 21, "bold"),
        bg=COR_TOPO,
        fg=COR_TEXTO,
    ).pack(
        anchor="w",
        padx=30,
        pady=(22, 0),
    )

    tk.Label(
        topo,
        text="Edifício Oxygen  •  Veper",
        font=(FONTE, 9, "bold"),
        bg=COR_TOPO,
        fg=COR_DESTAQUE,
    ).pack(
        anchor="w",
        padx=31,
        pady=(3, 0),
    )

    card = tk.Frame(
        janela,
        bg=COR_CARTAO,
        highlightthickness=1,
        highlightbackground=COR_BORDA,
    )

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=26,
    )

    tk.Label(
        card,
        text="Acesso do operador",
        font=(FONTE, 16, "bold"),
        bg=COR_CARTAO,
        fg=COR_TEXTO,
    ).pack(
        anchor="w",
        padx=30,
        pady=(24, 4),
    )

    tk.Label(
        card,
        text="Entre com seu usuário e senha.",
        font=(FONTE, 9),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
    ).pack(
        anchor="w",
        padx=30,
        pady=(0, 16),
    )

    form = tk.Frame(
        card,
        bg=COR_CARTAO,
    )

    form.pack(
        fill="x",
        padx=30,
    )

    form.grid_columnconfigure(
        1,
        weight=1,
    )

    tk.Label(
        form,
        text="Usuário",
        font=(FONTE, 10, "bold"),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=(0, 14),
        pady=8,
    )

    usuario = criar_entry(
        form
    )

    usuario.grid(
        row=0,
        column=1,
        sticky="ew",
        ipady=8,
        pady=8,
    )

    tk.Label(
        form,
        text="Senha",
        font=(FONTE, 10, "bold"),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=(0, 14),
        pady=8,
    )

    senha = criar_entry(
        form,
        "•"
    )

    senha.grid(
        row=1,
        column=1,
        sticky="ew",
        ipady=8,
        pady=8,
    )

    def entrar():

        usuario_txt = (
            usuario.get().strip()
        )

        senha_txt = senha.get()

        if (
            not usuario_txt
            or not senha_txt
        ):

            messagebox.showwarning(
                "Atenção",
                "Informe usuário e senha.",
                parent=janela,
            )

            return

        operador = (
            buscar_operador_por_usuario(
                usuario_txt
            )
        )

        if (
            operador is None
            or operador[5] != 1
        ):

            messagebox.showerror(
                "Acesso negado",
                "Usuário ou senha incorretos.",
                parent=janela,
            )

            senha.delete(
                0,
                tk.END
            )

            senha.focus_set()
            return

        if not senha_confere(
            senha_txt,
            operador[3],
            operador[4],
        ):

            messagebox.showerror(
                "Acesso negado",
                "Usuário ou senha incorretos.",
                parent=janela,
            )

            senha.delete(
                0,
                tk.END
            )

            senha.focus_set()
            return

        resultado["operador"] = {
            "id": operador[0],
            "nome": operador[1],
            "usuario": operador[2],
        }

        janela.destroy()

    botoes = tk.Frame(
        card,
        bg=COR_CARTAO,
    )

    botoes.pack(
        fill="x",
        padx=30,
        pady=(18, 24),
    )

    criar_botao(
        botoes,
        "Entrar",
        entrar,
        principal=True,
    ).pack(
        side="right"
    )

    usuario.bind(
        "<Return>",
        lambda _evento: senha.focus_set()
    )

    senha.bind(
        "<Return>",
        lambda _evento: entrar()
    )

    def fechar():

        resultado["operador"] = None
        janela.destroy()

    janela.protocol(
        "WM_DELETE_WINDOW",
        fechar
    )

    usuario.focus_set()

    janela_pai.wait_window(
        janela
    )

    return resultado["operador"]