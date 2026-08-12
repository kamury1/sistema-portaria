import tkinter as tk
from tkinter import ttk

from banco import listar_moradores, listar_visitantes, listar_prestadores

COR_FUNDO = "#0B1220"
COR_TOPO = "#111D30"
COR_CARTAO = "#17263A"
COR_BORDA = "#253B56"
COR_CAMPO = "#0F1B2D"
COR_BOTAO = "#1B2D45"
COR_BOTAO_HOVER = "#274463"
COR_TEXTO = "#F5F7FA"
COR_TEXTO_2 = "#A9B7C6"
COR_TABELA = "#FFFFFF"
COR_TABELA_ALT = "#F3F6FA"
COR_TABELA_TEXTO = "#17202A"
COR_SELECAO = "#D9E8F6"
FONTE = "Segoe UI"


def centralizar(janela, largura, altura):
    janela.update_idletasks()
    x = max((janela.winfo_screenwidth() - largura) // 2, 0)
    y = max((janela.winfo_screenheight() - altura) // 2, 0)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def configurar_tabela():
    estilo = ttk.Style()
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    estilo.configure(
        "Busca.Treeview",
        background=COR_TABELA,
        fieldbackground=COR_TABELA,
        foreground=COR_TABELA_TEXTO,
        rowheight=34,
        borderwidth=0,
        font=(FONTE, 10),
    )
    estilo.map(
        "Busca.Treeview",
        background=[("selected", COR_SELECAO)],
        foreground=[("selected", COR_TABELA_TEXTO)],
    )
    estilo.configure(
        "Busca.Treeview.Heading",
        background=COR_TOPO,
        foreground=COR_TEXTO,
        relief="flat",
        padding=(8, 10),
        font=(FONTE, 10, "bold"),
    )


def buscar_pessoas(termo):
    """
    Busca em moradores, visitantes e prestadores.
    Retorna linhas padronizadas:
    (tipo, nome, detalhe_1, detalhe_2, telefone)
    """
    termo = termo.strip().lower()
    resultados = []

    if not termo:
        return resultados

    for morador in listar_moradores():
        # id, nome, apartamento, vagas, telefone, tipo
        campos = [str(valor or "").lower() for valor in morador[1:]]
        if any(termo in campo for campo in campos):
            resultados.append((
                "Morador",
                morador[1],
                f"Apto {morador[2]}",
                f"{morador[5]} • Vaga(s): {morador[3]}",
                morador[4] or "",
            ))

    for visitante in listar_visitantes():
        # id, nome, documento, telefone
        campos = [str(valor or "").lower() for valor in visitante[1:]]
        if any(termo in campo for campo in campos):
            resultados.append((
                "Visitante",
                visitante[1],
                f"Documento: {visitante[2]}",
                "Cadastro de visitante",
                visitante[3] or "",
            ))

    for prestador in listar_prestadores():
        # id, nome, documento, empresa, telefone
        campos = [str(valor or "").lower() for valor in prestador[1:]]
        if any(termo in campo for campo in campos):
            resultados.append((
                "Prestador",
                prestador[1],
                f"Empresa: {prestador[3] or '-'}",
                f"Documento: {prestador[2]}",
                prestador[4] or "",
            ))

    resultados.sort(key=lambda item: (item[0], str(item[1]).lower()))
    return resultados


def abrir_busca_global(janela_principal, termo_inicial=""):
    janela = tk.Toplevel(janela_principal)
    janela.title("Busca Rápida")
    janela.configure(bg=COR_FUNDO)
    janela.minsize(950, 600)
    centralizar(janela, 1120, 680)
    janela.transient(janela_principal)

    configurar_tabela()

    topo = tk.Frame(janela, bg=COR_TOPO, height=96)
    topo.pack(fill="x")
    topo.pack_propagate(False)

    tk.Label(
        topo,
        text="Busca Rápida",
        font=(FONTE, 20, "bold"),
        bg=COR_TOPO,
        fg=COR_TEXTO,
    ).pack(anchor="w", padx=30, pady=(18, 0))

    tk.Label(
        topo,
        text="Pesquise moradores, visitantes e prestadores em um só lugar.",
        font=(FONTE, 9),
        bg=COR_TOPO,
        fg=COR_TEXTO_2,
    ).pack(anchor="w", padx=31, pady=(3, 0))

    conteudo = tk.Frame(janela, bg=COR_FUNDO)
    conteudo.pack(fill="both", expand=True, padx=30, pady=24)

    barra = tk.Frame(
        conteudo,
        bg=COR_CARTAO,
        highlightthickness=1,
        highlightbackground=COR_BORDA,
    )
    barra.pack(fill="x", pady=(0, 16))

    tk.Label(
        barra,
        text="Buscar",
        font=(FONTE, 9, "bold"),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
    ).pack(side="left", padx=(18, 10), pady=14)

    entrada = tk.Entry(
        barra,
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
    entrada.pack(side="left", fill="x", expand=True, ipady=7, pady=11)

    quadro = tk.Frame(
        conteudo,
        bg=COR_CARTAO,
        highlightthickness=1,
        highlightbackground=COR_BORDA,
    )
    quadro.pack(fill="both", expand=True)
    quadro.grid_rowconfigure(0, weight=1)
    quadro.grid_columnconfigure(0, weight=1)

    colunas = ("tipo", "nome", "detalhe1", "detalhe2", "telefone")
    tabela = ttk.Treeview(
        quadro,
        columns=colunas,
        show="headings",
        style="Busca.Treeview",
        selectmode="browse",
    )

    tabela.heading("tipo", text="Tipo")
    tabela.heading("nome", text="Nome")
    tabela.heading("detalhe1", text="Informação")
    tabela.heading("detalhe2", text="Detalhes")
    tabela.heading("telefone", text="Telefone")

    tabela.column("tipo", width=115, minwidth=100, anchor="center", stretch=False)
    tabela.column("nome", width=280, minwidth=180)
    tabela.column("detalhe1", width=230, minwidth=150)
    tabela.column("detalhe2", width=270, minwidth=170)
    tabela.column("telefone", width=170, minwidth=130)

    sv = ttk.Scrollbar(quadro, orient="vertical", command=tabela.yview)
    sh = ttk.Scrollbar(quadro, orient="horizontal", command=tabela.xview)
    tabela.configure(yscrollcommand=sv.set, xscrollcommand=sh.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    sv.grid(row=0, column=1, sticky="ns")
    sh.grid(row=1, column=0, sticky="ew")

    tabela.tag_configure("par", background=COR_TABELA)
    tabela.tag_configure("impar", background=COR_TABELA_ALT)

    rodape = tk.Frame(conteudo, bg=COR_FUNDO)
    rodape.pack(fill="x", pady=(12, 0))

    status = tk.Label(
        rodape,
        text="Digite algo para pesquisar.",
        font=(FONTE, 9),
        bg=COR_FUNDO,
        fg=COR_TEXTO_2,
    )
    status.pack(side="left")

    def executar_busca():
        termo = entrada.get().strip()

        for item in tabela.get_children():
            tabela.delete(item)

        if not termo:
            status.config(text="Digite um nome, apartamento, documento, empresa ou telefone.")
            return

        try:
            resultados = buscar_pessoas(termo)
        except Exception as erro:
            status.config(text=f"Erro ao pesquisar: {erro}")
            return

        for indice, linha in enumerate(resultados):
            tabela.insert(
                "",
                tk.END,
                values=linha,
                tags=("par" if indice % 2 == 0 else "impar",),
            )

        if resultados:
            status.config(text=f"{len(resultados)} resultado(s) encontrado(s).")
        else:
            status.config(text=f'Nenhum resultado para "{termo}".')

    def limpar():
        entrada.delete(0, tk.END)
        for item in tabela.get_children():
            tabela.delete(item)
        status.config(text="Digite algo para pesquisar.")
        entrada.focus_set()

    def criar_botao(texto, comando):
        botao = tk.Button(
            barra,
            text=texto,
            command=comando,
            font=(FONTE, 9, "bold"),
            bg=COR_BOTAO,
            fg=COR_TEXTO,
            activebackground=COR_BOTAO_HOVER,
            activeforeground=COR_TEXTO,
            relief="flat",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
        )
        botao.bind("<Enter>", lambda e: botao.config(bg=COR_BOTAO_HOVER))
        botao.bind("<Leave>", lambda e: botao.config(bg=COR_BOTAO))
        return botao

    criar_botao("Pesquisar", executar_busca).pack(side="left", padx=10)
    criar_botao("Limpar", limpar).pack(side="left", padx=(0, 14))

    entrada.bind("<Return>", lambda e: executar_busca())
    entrada.bind("<Escape>", lambda e: limpar())

    entrada.insert(0, termo_inicial)
    entrada.focus_set()

    if termo_inicial.strip():
        janela.after(80, executar_busca)