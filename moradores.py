import tkinter as tk
from tkinter import messagebox, ttk

from banco import (
    cadastrar_morador,
    listar_moradores,
    pesquisar_moradores,
    atualizar_morador,
    excluir_morador,
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
COR_DESTAQUE = "#D32F2F"
COR_DESTAQUE_HOVER = "#B71C1C"
COR_SUCESSO = "#2E7D32"
COR_SUCESSO_HOVER = "#256428"
COR_PERIGO = "#C62828"
COR_PERIGO_HOVER = "#A51F1F"
COR_TEXTO = "#F5F7FA"
COR_TEXTO_2 = "#A9B7C6"
COR_LINHA = "#263A50"
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


def criar_botao(parent, texto, comando, cor=COR_BOTAO, hover=COR_BOTAO_HOVER, largura=None):
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
    ).grid(row=row, column=0, sticky="w", padx=(0, 14), pady=8)


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
    entrada.grid(row=row, column=1, sticky="ew", ipady=8, pady=8)
    return entrada


def configurar_estilo_tabela():
    estilo = ttk.Style()

    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    estilo.configure(
        "Moradores.Treeview",
        background=COR_TABELA,
        fieldbackground=COR_TABELA,
        foreground=COR_TABELA_TEXTO,
        rowheight=34,
        borderwidth=0,
        relief="flat",
        font=(FONTE, 10),
    )
    estilo.map(
        "Moradores.Treeview",
        background=[("selected", COR_SELECAO)],
        foreground=[("selected", COR_TABELA_TEXTO)],
    )
    estilo.configure(
        "Moradores.Treeview.Heading",
        background=COR_TOPO,
        foreground=COR_TEXTO,
        relief="flat",
        padding=(8, 10),
        font=(FONTE, 10, "bold"),
    )
    estilo.map(
        "Moradores.Treeview.Heading",
        background=[("active", COR_BOTAO_HOVER)],
    )


# ==========================================================
# CADASTRAR MORADOR
# ==========================================================

def abrir_moradores(janela_principal):
    janela_moradores = tk.Toplevel(janela_principal)
    janela_moradores.title("Cadastro de Morador")
    janela_moradores.configure(bg=COR_FUNDO)
    janela_moradores.resizable(False, False)
    centralizar_janela(janela_moradores, 720, 610)
    janela_moradores.transient(janela_principal)

    # Cabeçalho
    topo = tk.Frame(janela_moradores, bg=COR_TOPO, height=92)
    topo.pack(fill="x")
    topo.pack_propagate(False)

    tk.Label(
        topo,
        text="Cadastrar Morador",
        font=(FONTE, 20, "bold"),
        bg=COR_TOPO,
        fg=COR_TEXTO,
    ).pack(anchor="w", padx=30, pady=(18, 0))

    tk.Label(
        topo,
        text="Preencha os dados abaixo para adicionar um novo morador.",
        font=(FONTE, 9),
        bg=COR_TOPO,
        fg=COR_TEXTO_2,
    ).pack(anchor="w", padx=31, pady=(3, 0))

    # Cartão do formulário
    cartao = tk.Frame(
        janela_moradores,
        bg=COR_CARTAO,
        highlightthickness=1,
        highlightbackground=COR_CARTAO_BORDA,
    )
    cartao.pack(fill="both", expand=True, padx=30, pady=26)

    formulario = tk.Frame(cartao, bg=COR_CARTAO)
    formulario.pack(fill="x", padx=32, pady=(28, 10))
    formulario.grid_columnconfigure(1, weight=1)

    criar_label_campo(formulario, "Nome *", 0)
    entrada_nome = criar_entry(formulario, 0)

    criar_label_campo(formulario, "Apartamento *", 1)
    entrada_apartamento = criar_entry(formulario, 1)

    criar_label_campo(formulario, "Vaga(s)", 2)
    entrada_vagas = criar_entry(formulario, 2)

    criar_label_campo(formulario, "Telefone", 3)
    entrada_telefone = criar_entry(formulario, 3)

    criar_label_campo(formulario, "Tipo", 4)
    tipo_morador = tk.StringVar(value="Proprietário")

    combo_tipo = ttk.Combobox(
        formulario,
        textvariable=tipo_morador,
        values=("Proprietário", "Inquilino", "Familiar", "Outro"),
        state="readonly",
        font=(FONTE, 10),
    )
    combo_tipo.grid(row=4, column=1, sticky="ew", ipady=5, pady=8)

    tk.Label(
        cartao,
        text="* Campos obrigatórios",
        font=(FONTE, 8),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
    ).pack(anchor="w", padx=32, pady=(0, 8))

    def limpar_campos():
        for entrada in (entrada_nome, entrada_apartamento, entrada_vagas, entrada_telefone):
            entrada.delete(0, tk.END)
        tipo_morador.set("Proprietário")
        entrada_nome.focus_set()

    def salvar():
        nome = entrada_nome.get().strip()
        apartamento = entrada_apartamento.get().strip()
        vagas = entrada_vagas.get().strip()
        telefone = entrada_telefone.get().strip()
        tipo = tipo_morador.get()

        if not nome:
            messagebox.showwarning("Atenção", "Informe o nome do morador.", parent=janela_moradores)
            entrada_nome.focus_set()
            return

        if not apartamento:
            messagebox.showwarning("Atenção", "Informe o apartamento.", parent=janela_moradores)
            entrada_apartamento.focus_set()
            return

        try:
            cadastrar_morador(nome, apartamento, vagas, telefone, tipo)
        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível cadastrar o morador.\n\n{erro}",
                parent=janela_moradores,
            )
            return

        messagebox.showinfo(
            "Cadastro concluído",
            f"Morador {nome} cadastrado com sucesso!",
            parent=janela_moradores,
        )
        limpar_campos()

    botoes = tk.Frame(cartao, bg=COR_CARTAO)
    botoes.pack(fill="x", padx=32, pady=(10, 26))

    criar_botao(
        botoes,
        "Salvar morador",
        salvar,
        cor=COR_SUCESSO,
        hover=COR_SUCESSO_HOVER,
    ).pack(side="right")

    criar_botao(
        botoes,
        "Limpar",
        limpar_campos,
    ).pack(side="right", padx=(0, 10))

    entrada_nome.bind("<Return>", lambda _evento: entrada_apartamento.focus_set())
    entrada_apartamento.bind("<Return>", lambda _evento: entrada_vagas.focus_set())
    entrada_vagas.bind("<Return>", lambda _evento: entrada_telefone.focus_set())
    entrada_telefone.bind("<Return>", lambda _evento: salvar())

    entrada_nome.focus_set()


# ==========================================================
# MORADORES CADASTRADOS
# ==========================================================

def abrir_lista_moradores(janela_principal):
    janela_lista = tk.Toplevel(janela_principal)
    janela_lista.title("Moradores Cadastrados")
    janela_lista.configure(bg=COR_FUNDO)
    janela_lista.minsize(1120, 680)
    centralizar_janela(janela_lista, 1280, 760)
    janela_lista.transient(janela_principal)

    configurar_estilo_tabela()

    # ------------------------------------------------------
    # CABEÇALHO
    # ------------------------------------------------------
    topo = tk.Frame(janela_lista, bg=COR_TOPO, height=96)
    topo.pack(fill="x")
    topo.pack_propagate(False)

    bloco_titulo = tk.Frame(topo, bg=COR_TOPO)
    bloco_titulo.pack(side="left", padx=30, pady=18)

    tk.Label(
        bloco_titulo,
        text="Moradores Cadastrados",
        font=(FONTE, 20, "bold"),
        bg=COR_TOPO,
        fg=COR_TEXTO,
    ).pack(anchor="w")

    tk.Label(
        bloco_titulo,
        text="Consulte, pesquise e gerencie os moradores do condomínio.",
        font=(FONTE, 9),
        bg=COR_TOPO,
        fg=COR_TEXTO_2,
    ).pack(anchor="w", pady=(3, 0))

    contador_var = tk.StringVar(value="0 moradores")
    tk.Label(
        topo,
        textvariable=contador_var,
        font=(FONTE, 10, "bold"),
        bg=COR_TOPO,
        fg=COR_TEXTO_2,
    ).pack(side="right", padx=30)

    # ------------------------------------------------------
    # CONTEÚDO
    # ------------------------------------------------------
    conteudo = tk.Frame(janela_lista, bg=COR_FUNDO)
    conteudo.pack(fill="both", expand=True, padx=28, pady=18)

    # Barra de busca
    barra = tk.Frame(
        conteudo,
        bg=COR_CARTAO,
        highlightthickness=1,
        highlightbackground=COR_CARTAO_BORDA,
    )
    barra.pack(fill="x", pady=(0, 16))

    bloco_busca = tk.Frame(barra, bg=COR_CARTAO)
    bloco_busca.pack(fill="x", padx=18, pady=14)

    tk.Label(
        bloco_busca,
        text="Pesquisar",
        font=(FONTE, 9, "bold"),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
    ).pack(side="left", padx=(0, 10))

    entrada_pesquisa = tk.Entry(
        bloco_busca,
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
    entrada_pesquisa.pack(side="left", fill="x", expand=True, ipady=8)

    # ------------------------------------------------------
    # TABELA
    # ------------------------------------------------------
    frame_tabela = tk.Frame(
        conteudo,
        bg=COR_CARTAO,
        highlightthickness=1,
        highlightbackground=COR_CARTAO_BORDA,
    )
    frame_tabela.pack(fill="both", expand=True)

    tabela_container = tk.Frame(frame_tabela, bg=COR_CARTAO)
    tabela_container.pack(fill="both", expand=True, padx=14, pady=12)
    tabela_container.grid_rowconfigure(0, weight=1)
    tabela_container.grid_columnconfigure(0, weight=1)

    colunas = ("id", "nome", "apartamento", "vagas", "telefone", "tipo")

    tabela = ttk.Treeview(
        tabela_container,
        columns=colunas,
        show="headings",
        style="Moradores.Treeview",
        selectmode="browse",
    )

    cabecalhos = {
        "id": "ID",
        "nome": "Nome",
        "apartamento": "Apartamento",
        "vagas": "Vaga(s)",
        "telefone": "Telefone",
        "tipo": "Tipo",
    }

    for coluna, texto in cabecalhos.items():
        tabela.heading(coluna, text=texto)

    tabela.column("id", width=55, minwidth=45, anchor="center", stretch=False)
    tabela.column("nome", width=310, minwidth=220, anchor="w")
    tabela.column("apartamento", width=120, minwidth=100, anchor="center", stretch=False)
    tabela.column("vagas", width=120, minwidth=90, anchor="center", stretch=False)
    tabela.column("telefone", width=180, minwidth=140, anchor="center")
    tabela.column("tipo", width=150, minwidth=120, anchor="center")

    scroll_y = ttk.Scrollbar(tabela_container, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_container, orient="horizontal", command=tabela.xview)
    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    tabela.tag_configure("par", background=COR_TABELA)
    tabela.tag_configure("impar", background=COR_TABELA_ALT)

    # ------------------------------------------------------
    # FUNÇÕES DA LISTA
    # ------------------------------------------------------
    def preencher_tabela(moradores):
        for item in tabela.get_children():
            tabela.delete(item)

        for indice, morador in enumerate(moradores):
            tag = "par" if indice % 2 == 0 else "impar"
            tabela.insert("", tk.END, values=morador, tags=(tag,))

        total = len(moradores)
        contador_var.set(f"{total} morador" if total == 1 else f"{total} moradores")

    def carregar():
        try:
            moradores = listar_moradores()
            preencher_tabela(moradores)
        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível carregar os moradores.\n\n{erro}",
                parent=janela_lista,
            )

    def pesquisar():
        nome = entrada_pesquisa.get().strip()

        try:
            moradores = pesquisar_moradores(nome) if nome else listar_moradores()
            preencher_tabela(moradores)
        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível realizar a pesquisa.\n\n{erro}",
                parent=janela_lista,
            )

    def limpar_pesquisa():
        entrada_pesquisa.delete(0, tk.END)
        carregar()
        entrada_pesquisa.focus_set()

    def obter_selecionado():
        selecionados = tabela.selection()
        if not selecionados:
            messagebox.showwarning(
                "Atenção",
                "Selecione um morador na tabela.",
                parent=janela_lista,
            )
            return None
        return tabela.item(selecionados[0])["values"]

    # ------------------------------------------------------
    # EDITAR
    # ------------------------------------------------------
    def editar():
        dados = obter_selecionado()
        if not dados:
            return

        id_morador, nome_atual, apartamento_atual, vagas_atual, telefone_atual, tipo_atual = dados

        janela_editar = tk.Toplevel(janela_lista)
        janela_editar.title("Editar Morador")
        janela_editar.configure(bg=COR_FUNDO)
        janela_editar.resizable(False, False)
        centralizar_janela(janela_editar, 700, 600)
        janela_editar.transient(janela_lista)
        janela_editar.grab_set()

        topo_editar = tk.Frame(janela_editar, bg=COR_TOPO, height=88)
        topo_editar.pack(fill="x")
        topo_editar.pack_propagate(False)

        tk.Label(
            topo_editar,
            text="Editar Morador",
            font=(FONTE, 19, "bold"),
            bg=COR_TOPO,
            fg=COR_TEXTO,
        ).pack(anchor="w", padx=28, pady=(17, 0))

        tk.Label(
            topo_editar,
            text=f"Registro #{id_morador}",
            font=(FONTE, 9),
            bg=COR_TOPO,
            fg=COR_TEXTO_2,
        ).pack(anchor="w", padx=29, pady=(2, 0))

        cartao_editar = tk.Frame(
            janela_editar,
            bg=COR_CARTAO,
            highlightthickness=1,
            highlightbackground=COR_CARTAO_BORDA,
        )
        cartao_editar.pack(fill="both", expand=True, padx=28, pady=24)

        formulario = tk.Frame(cartao_editar, bg=COR_CARTAO)
        formulario.pack(fill="x", padx=30, pady=(26, 10))
        formulario.grid_columnconfigure(1, weight=1)

        criar_label_campo(formulario, "Nome *", 0)
        entrada_nome = criar_entry(formulario, 0)
        entrada_nome.insert(0, nome_atual)

        criar_label_campo(formulario, "Apartamento *", 1)
        entrada_apartamento = criar_entry(formulario, 1)
        entrada_apartamento.insert(0, apartamento_atual)

        criar_label_campo(formulario, "Vaga(s)", 2)
        entrada_vagas = criar_entry(formulario, 2)
        entrada_vagas.insert(0, "" if vagas_atual is None else vagas_atual)

        criar_label_campo(formulario, "Telefone", 3)
        entrada_telefone = criar_entry(formulario, 3)
        entrada_telefone.insert(0, "" if telefone_atual is None else telefone_atual)

        criar_label_campo(formulario, "Tipo", 4)
        tipo_morador = tk.StringVar(value=tipo_atual or "Proprietário")
        combo_tipo = ttk.Combobox(
            formulario,
            textvariable=tipo_morador,
            values=("Proprietário", "Inquilino", "Familiar", "Outro"),
            state="readonly",
            font=(FONTE, 10),
        )
        combo_tipo.grid(row=4, column=1, sticky="ew", ipady=5, pady=8)

        def salvar_alteracoes():
            nome = entrada_nome.get().strip()
            apartamento = entrada_apartamento.get().strip()
            vagas = entrada_vagas.get().strip()
            telefone = entrada_telefone.get().strip()
            tipo = tipo_morador.get()

            if not nome or not apartamento:
                messagebox.showwarning(
                    "Atenção",
                    "Nome e apartamento são obrigatórios.",
                    parent=janela_editar,
                )
                return

            try:
                atualizar_morador(id_morador, nome, apartamento, vagas, telefone, tipo)
            except Exception as erro:
                messagebox.showerror(
                    "Erro",
                    f"Não foi possível atualizar o morador.\n\n{erro}",
                    parent=janela_editar,
                )
                return

            messagebox.showinfo(
                "Atualização concluída",
                "Morador atualizado com sucesso!",
                parent=janela_editar,
            )
            janela_editar.destroy()
            carregar()

        botoes_editar = tk.Frame(cartao_editar, bg=COR_CARTAO)
        botoes_editar.pack(fill="x", padx=30, pady=(10, 24))

        criar_botao(
            botoes_editar,
            "Salvar alterações",
            salvar_alteracoes,
            cor=COR_SUCESSO,
            hover=COR_SUCESSO_HOVER,
        ).pack(side="right")

        criar_botao(
            botoes_editar,
            "Cancelar",
            janela_editar.destroy,
        ).pack(side="right", padx=(0, 10))

        entrada_nome.focus_set()

    # ------------------------------------------------------
    # EXCLUIR
    # ------------------------------------------------------
    def excluir():
        dados = obter_selecionado()
        if not dados:
            return

        id_morador = dados[0]
        nome_morador = dados[1]
        apartamento = dados[2]

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir este morador?\n\n"
            f"Nome: {nome_morador}\n"
            f"Apartamento: {apartamento}\n\n"
            "Esta ação não poderá ser desfeita.",
            parent=janela_lista,
        )

        if not confirmar:
            return

        try:
            excluir_morador(id_morador)
        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível excluir o morador.\n\n{erro}",
                parent=janela_lista,
            )
            return

        messagebox.showinfo(
            "Exclusão concluída",
            "Morador excluído com sucesso!",
            parent=janela_lista,
        )
        carregar()

    # ------------------------------------------------------
    # BOTÕES DA BARRA
    # ------------------------------------------------------
    criar_botao(bloco_busca, "Pesquisar", pesquisar).pack(side="left", padx=(10, 0))
    criar_botao(bloco_busca, "Limpar", limpar_pesquisa).pack(side="left", padx=(8, 0))

    # Barra de ações inferior
    acoes = tk.Frame(conteudo, bg=COR_FUNDO)
    acoes.pack(fill="x", pady=(10, 2))

    tk.Label(
        acoes,
        text="Dica: dê dois cliques em um morador para editar.",
        font=(FONTE, 8),
        bg=COR_FUNDO,
        fg=COR_TEXTO_2,
    ).pack(side="left")

    criar_botao(
        acoes,
        "Excluir morador",
        excluir,
        cor=COR_PERIGO,
        hover=COR_PERIGO_HOVER,
    ).pack(side="right")

    criar_botao(
        acoes,
        "Editar morador",
        editar,
    ).pack(side="right", padx=(0, 10))

    criar_botao(
        acoes,
        "Atualizar lista",
        carregar,
    ).pack(side="right", padx=(0, 10))

    entrada_pesquisa.bind("<Return>", lambda _evento: pesquisar())
    entrada_pesquisa.bind("<Escape>", lambda _evento: limpar_pesquisa())
    tabela.bind("<Double-1>", lambda _evento: editar())
    janela_lista.bind("<F5>", lambda _evento: carregar())

    carregar()
    entrada_pesquisa.focus_set()