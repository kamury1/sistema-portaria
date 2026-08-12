import tkinter as tk
from tkinter import messagebox, ttk

from banco import (
    cadastrar_prestador,
    listar_prestadores,
    pesquisar_prestadores,
    atualizar_prestador,
    excluir_prestador,
)


# ==========================================================
# IDENTIDADE VISUAL
# ==========================================================

COR_FUNDO = "#0B1220"
COR_TOPO = "#111D30"
COR_CARTAO = "#17263A"
COR_CARTAO_BORDA = "#253B56"
COR_CAMPO = "#0F1B2D"
COR_BOTAO = "#1B2D45"
COR_BOTAO_HOVER = "#274463"
COR_SUCESSO = "#2E7D32"
COR_SUCESSO_HOVER = "#256428"
COR_PERIGO = "#C62828"
COR_PERIGO_HOVER = "#A51F1F"
COR_TEXTO = "#F5F7FA"
COR_TEXTO_2 = "#A9B7C6"
COR_TABELA = "#FFFFFF"
COR_TABELA_ALT = "#F3F6FA"
COR_TABELA_TEXTO = "#17202A"
COR_SELECAO = "#D9E8F6"

FONTE = "Segoe UI"


# ==========================================================
# FUNÇÕES VISUAIS AUXILIARES
# ==========================================================

def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    x = max((largura_tela - largura) // 2, 0)
    y = max((altura_tela - altura) // 2, 0)

    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def adicionar_hover(botao, normal, hover):
    botao.bind("<Enter>", lambda _evento: botao.config(bg=hover))
    botao.bind("<Leave>", lambda _evento: botao.config(bg=normal))


def criar_botao(
    parent,
    texto,
    comando,
    cor=COR_BOTAO,
    hover=COR_BOTAO_HOVER,
    largura=None,
):
    botao = tk.Button(
        parent,
        text=texto,
        command=comando,
        font=(FONTE, 10, "bold"),
        bg=cor,
        fg=COR_TEXTO,
        activebackground=hover,
        activeforeground=COR_TEXTO,
        relief="flat",
        bd=0,
        padx=18,
        pady=9,
        cursor="hand2",
        width=largura,
    )

    adicionar_hover(botao, cor, hover)
    return botao


def criar_label_campo(parent, texto, row):
    tk.Label(
        parent,
        text=texto,
        font=(FONTE, 10, "bold"),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
        anchor="w",
    ).grid(
        row=row,
        column=0,
        sticky="w",
        padx=(0, 14),
        pady=8,
    )


def criar_entry(parent, row):
    entrada = tk.Entry(
        parent,
        font=(FONTE, 11),
        bg=COR_CAMPO,
        fg=COR_TEXTO,
        insertbackground=COR_TEXTO,
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground=COR_CARTAO_BORDA,
        highlightcolor="#4C78A8",
    )

    entrada.grid(
        row=row,
        column=1,
        sticky="ew",
        ipady=8,
        pady=8,
    )

    return entrada


def configurar_estilo_tabela():
    estilo = ttk.Style()

    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    estilo.configure(
        "Prestadores.Treeview",
        background=COR_TABELA,
        fieldbackground=COR_TABELA,
        foreground=COR_TABELA_TEXTO,
        rowheight=34,
        borderwidth=0,
        relief="flat",
        font=(FONTE, 10),
    )

    estilo.map(
        "Prestadores.Treeview",
        background=[("selected", COR_SELECAO)],
        foreground=[("selected", COR_TABELA_TEXTO)],
    )

    estilo.configure(
        "Prestadores.Treeview.Heading",
        background=COR_TOPO,
        foreground=COR_TEXTO,
        relief="flat",
        padding=(8, 10),
        font=(FONTE, 10, "bold"),
    )

    estilo.map(
        "Prestadores.Treeview.Heading",
        background=[("active", COR_BOTAO_HOVER)],
    )


# ==========================================================
# CADASTRO DE PRESTADORES
# ==========================================================

def abrir_prestadores(janela_principal):
    janela_prestadores = tk.Toplevel(janela_principal)
    janela_prestadores.title("Cadastro de Prestador")
    janela_prestadores.configure(bg=COR_FUNDO)
    janela_prestadores.resizable(False, False)
    centralizar_janela(janela_prestadores, 740, 570)
    janela_prestadores.transient(janela_principal)

    topo = tk.Frame(
        janela_prestadores,
        bg=COR_TOPO,
        height=92,
    )
    topo.pack(fill="x")
    topo.pack_propagate(False)

    tk.Label(
        topo,
        text="Cadastrar Prestador",
        font=(FONTE, 20, "bold"),
        bg=COR_TOPO,
        fg=COR_TEXTO,
    ).pack(
        anchor="w",
        padx=30,
        pady=(18, 0),
    )

    tk.Label(
        topo,
        text="Registre os dados do prestador de serviço.",
        font=(FONTE, 9),
        bg=COR_TOPO,
        fg=COR_TEXTO_2,
    ).pack(
        anchor="w",
        padx=31,
        pady=(3, 0),
    )

    cartao = tk.Frame(
        janela_prestadores,
        bg=COR_CARTAO,
        highlightthickness=1,
        highlightbackground=COR_CARTAO_BORDA,
    )
    cartao.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=26,
    )

    formulario = tk.Frame(
        cartao,
        bg=COR_CARTAO,
    )
    formulario.pack(
        fill="x",
        padx=32,
        pady=(28, 10),
    )
    formulario.grid_columnconfigure(1, weight=1)

    criar_label_campo(formulario, "Nome *", 0)
    entrada_nome = criar_entry(formulario, 0)

    criar_label_campo(formulario, "Documento *", 1)
    entrada_documento = criar_entry(formulario, 1)

    criar_label_campo(formulario, "Empresa", 2)
    entrada_empresa = criar_entry(formulario, 2)

    criar_label_campo(formulario, "Telefone", 3)
    entrada_telefone = criar_entry(formulario, 3)

    tk.Label(
        cartao,
        text="* Campos obrigatórios",
        font=(FONTE, 8),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
    ).pack(
        anchor="w",
        padx=32,
        pady=(0, 8),
    )

    def limpar_campos():
        entrada_nome.delete(0, tk.END)
        entrada_documento.delete(0, tk.END)
        entrada_empresa.delete(0, tk.END)
        entrada_telefone.delete(0, tk.END)
        entrada_nome.focus_set()

    def salvar():
        nome = entrada_nome.get().strip()
        documento = entrada_documento.get().strip()
        empresa = entrada_empresa.get().strip()
        telefone = entrada_telefone.get().strip()

        if not nome:
            messagebox.showwarning(
                "Atenção",
                "Informe o nome do prestador.",
                parent=janela_prestadores,
            )
            entrada_nome.focus_set()
            return

        if not documento:
            messagebox.showwarning(
                "Atenção",
                "Informe o documento do prestador.",
                parent=janela_prestadores,
            )
            entrada_documento.focus_set()
            return

        try:
            cadastrar_prestador(
                nome,
                documento,
                empresa,
                telefone,
            )
        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível cadastrar o prestador.\n\n{erro}",
                parent=janela_prestadores,
            )
            return

        messagebox.showinfo(
            "Cadastro concluído",
            f"Prestador {nome} cadastrado com sucesso!",
            parent=janela_prestadores,
        )

        limpar_campos()

    botoes = tk.Frame(
        cartao,
        bg=COR_CARTAO,
    )
    botoes.pack(
        fill="x",
        padx=32,
        pady=(10, 26),
    )

    criar_botao(
        botoes,
        "Salvar prestador",
        salvar,
        cor=COR_SUCESSO,
        hover=COR_SUCESSO_HOVER,
    ).pack(side="right")

    criar_botao(
        botoes,
        "Limpar",
        limpar_campos,
    ).pack(
        side="right",
        padx=(0, 10),
    )

    entrada_nome.bind(
        "<Return>",
        lambda _evento: entrada_documento.focus_set(),
    )
    entrada_documento.bind(
        "<Return>",
        lambda _evento: entrada_empresa.focus_set(),
    )
    entrada_empresa.bind(
        "<Return>",
        lambda _evento: entrada_telefone.focus_set(),
    )
    entrada_telefone.bind(
        "<Return>",
        lambda _evento: salvar(),
    )

    entrada_nome.focus_set()


# ==========================================================
# PRESTADORES CADASTRADOS
# ==========================================================

def abrir_lista_prestadores(janela_principal):
    janela_lista = tk.Toplevel(janela_principal)
    janela_lista.title("Prestadores Cadastrados")
    janela_lista.configure(bg=COR_FUNDO)
    janela_lista.minsize(1060, 650)
    centralizar_janela(janela_lista, 1220, 740)
    janela_lista.transient(janela_principal)

    configurar_estilo_tabela()

    topo = tk.Frame(
        janela_lista,
        bg=COR_TOPO,
        height=96,
    )
    topo.pack(fill="x")
    topo.pack_propagate(False)

    bloco_titulo = tk.Frame(
        topo,
        bg=COR_TOPO,
    )
    bloco_titulo.pack(
        side="left",
        padx=30,
        pady=18,
    )

    tk.Label(
        bloco_titulo,
        text="Prestadores Cadastrados",
        font=(FONTE, 20, "bold"),
        bg=COR_TOPO,
        fg=COR_TEXTO,
    ).pack(anchor="w")

    label_total = tk.Label(
        bloco_titulo,
        text="0 prestador(es) cadastrado(s)",
        font=(FONTE, 9),
        bg=COR_TOPO,
        fg=COR_TEXTO_2,
    )
    label_total.pack(
        anchor="w",
        pady=(3, 0),
    )

    conteudo = tk.Frame(
        janela_lista,
        bg=COR_FUNDO,
    )
    conteudo.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=24,
    )

    # ------------------------------------------------------
    # BUSCA
    # ------------------------------------------------------

    barra_busca = tk.Frame(
        conteudo,
        bg=COR_CARTAO,
        highlightthickness=1,
        highlightbackground=COR_CARTAO_BORDA,
    )
    barra_busca.pack(
        fill="x",
        pady=(0, 16),
    )

    tk.Label(
        barra_busca,
        text="Pesquisar por nome",
        font=(FONTE, 9, "bold"),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
    ).pack(
        side="left",
        padx=(18, 10),
        pady=14,
    )

    entrada_pesquisa = tk.Entry(
        barra_busca,
        font=(FONTE, 10),
        bg=COR_CAMPO,
        fg=COR_TEXTO,
        insertbackground=COR_TEXTO,
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground=COR_CARTAO_BORDA,
        highlightcolor="#4C78A8",
    )
    entrada_pesquisa.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=7,
        pady=11,
    )

    # ------------------------------------------------------
    # TABELA
    # ------------------------------------------------------

    frame_tabela = tk.Frame(
        conteudo,
        bg=COR_CARTAO,
        highlightthickness=1,
        highlightbackground=COR_CARTAO_BORDA,
    )
    frame_tabela.pack(
        fill="both",
        expand=True,
    )

    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)

    colunas = (
        "id",
        "nome",
        "documento",
        "empresa",
        "telefone",
    )

    tabela = ttk.Treeview(
        frame_tabela,
        columns=colunas,
        show="headings",
        style="Prestadores.Treeview",
        selectmode="browse",
    )

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome")
    tabela.heading("documento", text="Documento")
    tabela.heading("empresa", text="Empresa")
    tabela.heading("telefone", text="Telefone")

    tabela.column(
        "id",
        width=70,
        minwidth=60,
        anchor="center",
        stretch=False,
    )
    tabela.column(
        "nome",
        width=330,
        minwidth=220,
        anchor="w",
    )
    tabela.column(
        "documento",
        width=210,
        minwidth=160,
        anchor="w",
    )
    tabela.column(
        "empresa",
        width=300,
        minwidth=180,
        anchor="w",
    )
    tabela.column(
        "telefone",
        width=210,
        minwidth=150,
        anchor="w",
    )

    barra_vertical = ttk.Scrollbar(
        frame_tabela,
        orient="vertical",
        command=tabela.yview,
    )
    barra_horizontal = ttk.Scrollbar(
        frame_tabela,
        orient="horizontal",
        command=tabela.xview,
    )

    tabela.configure(
        yscrollcommand=barra_vertical.set,
        xscrollcommand=barra_horizontal.set,
    )

    tabela.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(1, 0),
        pady=(1, 0),
    )
    barra_vertical.grid(
        row=0,
        column=1,
        sticky="ns",
    )
    barra_horizontal.grid(
        row=1,
        column=0,
        sticky="ew",
    )

    tabela.tag_configure(
        "par",
        background=COR_TABELA,
    )
    tabela.tag_configure(
        "impar",
        background=COR_TABELA_ALT,
    )

    # ------------------------------------------------------
    # FUNÇÕES DA LISTA
    # ------------------------------------------------------

    def preencher_tabela(prestadores):
        prestadores = list(prestadores)

        for item in tabela.get_children():
            tabela.delete(item)

        for indice, prestador in enumerate(prestadores):
            tag = "par" if indice % 2 == 0 else "impar"

            tabela.insert(
                "",
                tk.END,
                values=prestador,
                tags=(tag,),
            )

        label_total.config(
            text=f"{len(prestadores)} prestador(es) exibido(s)"
        )

    def carregar():
        try:
            preencher_tabela(
                listar_prestadores()
            )
        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível carregar os prestadores.\n\n{erro}",
                parent=janela_lista,
            )

    def pesquisar():
        nome = entrada_pesquisa.get().strip()

        try:
            if nome:
                preencher_tabela(
                    pesquisar_prestadores(nome)
                )
            else:
                carregar()
        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível realizar a pesquisa.\n\n{erro}",
                parent=janela_lista,
            )

    def mostrar_todos():
        entrada_pesquisa.delete(0, tk.END)
        carregar()
        entrada_pesquisa.focus_set()

    # ------------------------------------------------------
    # EDITAR
    # ------------------------------------------------------

    def editar():
        item_selecionado = tabela.selection()

        if not item_selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione um prestador para editar.",
                parent=janela_lista,
            )
            return

        dados = tabela.item(
            item_selecionado[0]
        )["values"]

        id_prestador = dados[0]
        nome_atual = dados[1]
        documento_atual = dados[2]
        empresa_atual = dados[3]
        telefone_atual = dados[4]

        janela_editar = tk.Toplevel(
            janela_lista
        )
        janela_editar.title(
            "Editar Prestador"
        )
        janela_editar.configure(
            bg=COR_FUNDO
        )
        janela_editar.resizable(
            False,
            False,
        )
        centralizar_janela(
            janela_editar,
            700,
            550,
        )
        janela_editar.transient(
            janela_lista
        )
        janela_editar.grab_set()

        topo_editar = tk.Frame(
            janela_editar,
            bg=COR_TOPO,
            height=88,
        )
        topo_editar.pack(fill="x")
        topo_editar.pack_propagate(False)

        tk.Label(
            topo_editar,
            text="Editar Prestador",
            font=(FONTE, 19, "bold"),
            bg=COR_TOPO,
            fg=COR_TEXTO,
        ).pack(
            anchor="w",
            padx=30,
            pady=(17, 0),
        )

        tk.Label(
            topo_editar,
            text=f"Registro #{id_prestador}",
            font=(FONTE, 9),
            bg=COR_TOPO,
            fg=COR_TEXTO_2,
        ).pack(
            anchor="w",
            padx=31,
            pady=(2, 0),
        )

        cartao_editar = tk.Frame(
            janela_editar,
            bg=COR_CARTAO,
            highlightthickness=1,
            highlightbackground=COR_CARTAO_BORDA,
        )
        cartao_editar.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=24,
        )

        formulario_editar = tk.Frame(
            cartao_editar,
            bg=COR_CARTAO,
        )
        formulario_editar.pack(
            fill="x",
            padx=30,
            pady=(26, 10),
        )
        formulario_editar.grid_columnconfigure(
            1,
            weight=1,
        )

        criar_label_campo(
            formulario_editar,
            "Nome *",
            0,
        )
        entrada_nome = criar_entry(
            formulario_editar,
            0,
        )
        entrada_nome.insert(
            0,
            nome_atual,
        )

        criar_label_campo(
            formulario_editar,
            "Documento *",
            1,
        )
        entrada_documento = criar_entry(
            formulario_editar,
            1,
        )
        entrada_documento.insert(
            0,
            documento_atual,
        )

        criar_label_campo(
            formulario_editar,
            "Empresa",
            2,
        )
        entrada_empresa = criar_entry(
            formulario_editar,
            2,
        )
        entrada_empresa.insert(
            0,
            empresa_atual,
        )

        criar_label_campo(
            formulario_editar,
            "Telefone",
            3,
        )
        entrada_telefone = criar_entry(
            formulario_editar,
            3,
        )
        entrada_telefone.insert(
            0,
            telefone_atual,
        )

        def salvar_alteracoes():
            nome = entrada_nome.get().strip()
            documento = entrada_documento.get().strip()
            empresa = entrada_empresa.get().strip()
            telefone = entrada_telefone.get().strip()

            if not nome:
                messagebox.showwarning(
                    "Atenção",
                    "Informe o nome do prestador.",
                    parent=janela_editar,
                )
                entrada_nome.focus_set()
                return

            if not documento:
                messagebox.showwarning(
                    "Atenção",
                    "Informe o documento do prestador.",
                    parent=janela_editar,
                )
                entrada_documento.focus_set()
                return

            try:
                atualizar_prestador(
                    id_prestador,
                    nome,
                    documento,
                    empresa,
                    telefone,
                )
            except Exception as erro:
                messagebox.showerror(
                    "Erro",
                    f"Não foi possível atualizar o prestador.\n\n{erro}",
                    parent=janela_editar,
                )
                return

            messagebox.showinfo(
                "Alteração concluída",
                "Prestador atualizado com sucesso!",
                parent=janela_editar,
            )

            janela_editar.destroy()
            carregar()

        frame_botoes_editar = tk.Frame(
            cartao_editar,
            bg=COR_CARTAO,
        )
        frame_botoes_editar.pack(
            fill="x",
            padx=30,
            pady=(8, 24),
        )

        criar_botao(
            frame_botoes_editar,
            "Salvar alterações",
            salvar_alteracoes,
            cor=COR_SUCESSO,
            hover=COR_SUCESSO_HOVER,
        ).pack(side="right")

        criar_botao(
            frame_botoes_editar,
            "Cancelar",
            janela_editar.destroy,
        ).pack(
            side="right",
            padx=(0, 10),
        )

        entrada_nome.bind(
            "<Return>",
            lambda _evento: entrada_documento.focus_set(),
        )
        entrada_documento.bind(
            "<Return>",
            lambda _evento: entrada_empresa.focus_set(),
        )
        entrada_empresa.bind(
            "<Return>",
            lambda _evento: entrada_telefone.focus_set(),
        )
        entrada_telefone.bind(
            "<Return>",
            lambda _evento: salvar_alteracoes(),
        )

        entrada_nome.focus_set()

    # ------------------------------------------------------
    # EXCLUIR
    # ------------------------------------------------------

    def excluir():
        item_selecionado = tabela.selection()

        if not item_selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione um prestador para excluir.",
                parent=janela_lista,
            )
            return

        dados = tabela.item(
            item_selecionado[0]
        )["values"]

        id_prestador = dados[0]
        nome_prestador = dados[1]
        documento_prestador = dados[2]

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir este prestador?\n\n"
            f"Nome: {nome_prestador}\n"
            f"Documento: {documento_prestador}",
            parent=janela_lista,
        )

        if not confirmar:
            return

        try:
            excluir_prestador(
                id_prestador
            )
        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível excluir o prestador.\n\n{erro}",
                parent=janela_lista,
            )
            return

        messagebox.showinfo(
            "Exclusão concluída",
            "Prestador excluído com sucesso!",
            parent=janela_lista,
        )

        carregar()

    # ------------------------------------------------------
    # BOTÕES
    # ------------------------------------------------------

    criar_botao(
        barra_busca,
        "Pesquisar",
        pesquisar,
    ).pack(
        side="left",
        padx=10,
    )

    criar_botao(
        barra_busca,
        "Mostrar todos",
        mostrar_todos,
    ).pack(
        side="left",
        padx=(0, 14),
    )

    acoes = tk.Frame(
        conteudo,
        bg=COR_FUNDO,
    )
    acoes.pack(
        fill="x",
        pady=(16, 0),
    )

    criar_botao(
        acoes,
        "Excluir prestador",
        excluir,
        cor=COR_PERIGO,
        hover=COR_PERIGO_HOVER,
    ).pack(side="right")

    criar_botao(
        acoes,
        "Editar prestador",
        editar,
    ).pack(
        side="right",
        padx=(0, 10),
    )

    # ------------------------------------------------------
    # ATALHOS
    # ------------------------------------------------------

    entrada_pesquisa.bind(
        "<Return>",
        lambda _evento: pesquisar(),
    )

    entrada_pesquisa.bind(
        "<Escape>",
        lambda _evento: mostrar_todos(),
    )

    tabela.bind(
        "<Double-1>",
        lambda _evento: editar(),
    )

    janela_lista.bind(
        "<F5>",
        lambda _evento: carregar(),
    )

    carregar()
    entrada_pesquisa.focus_set()