import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

from banco import listar_prestadores
from banco import registrar_entrada_prestador
from banco import listar_acessos_ativos
from banco import registrar_saida_prestador
from banco import listar_historico_acessos


# ==========================================================
# REGISTRAR ENTRADA DE PRESTADOR
# ==========================================================

def abrir_registro_entrada(janela_principal):

    janela_acesso = tk.Toplevel(janela_principal)
    janela_acesso.title("Registrar Entrada de Prestador")
    janela_acesso.geometry("700x500")
    janela_acesso.resizable(False, False)

    titulo = tk.Label(
        janela_acesso,
        text="Registrar Entrada de Prestador",
        font=("Arial", 20)
    )

    titulo.pack(pady=20)

    formulario = tk.Frame(janela_acesso)
    formulario.pack(pady=10)

    # Prestador
    tk.Label(
        formulario,
        text="Prestador:",
        font=("Arial", 12)
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    combo_prestador = ttk.Combobox(
        formulario,
        width=40,
        font=("Arial", 12),
        state="readonly"
    )

    combo_prestador.grid(
        row=0,
        column=1,
        pady=10
    )

    # Apartamento
    tk.Label(
        formulario,
        text="Apartamento de destino:",
        font=("Arial", 12)
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    entrada_apartamento = tk.Entry(
        formulario,
        width=42,
        font=("Arial", 12)
    )

    entrada_apartamento.grid(
        row=1,
        column=1,
        pady=10
    )

    # ======================================================
    # CARREGAR PRESTADORES
    # ======================================================

    prestadores = listar_prestadores()

    mapa_prestadores = {}
    nomes_combo = []

    for prestador in prestadores:

        id_prestador = prestador[0]
        nome = prestador[1]
        documento = prestador[2]
        empresa = prestador[3]

        texto = f"{nome} | {documento} | {empresa}"

        nomes_combo.append(texto)

        mapa_prestadores[texto] = id_prestador

    combo_prestador["values"] = nomes_combo

    # ======================================================
    # REGISTRAR ENTRADA
    # ======================================================

    def registrar():

        prestador_selecionado = combo_prestador.get()
        apartamento = entrada_apartamento.get().strip()

        if prestador_selecionado == "":

            messagebox.showwarning(
                "Atenção",
                "Selecione um prestador."
            )

            return

        if apartamento == "":

            messagebox.showwarning(
                "Atenção",
                "Informe o apartamento de destino."
            )

            return

        prestador_id = mapa_prestadores[
            prestador_selecionado
        ]

        agora = datetime.now()

        data_entrada = agora.strftime("%d/%m/%Y")
        hora_entrada = agora.strftime("%H:%M:%S")

        registrar_entrada_prestador(
            prestador_id,
            apartamento,
            data_entrada,
            hora_entrada
        )

        messagebox.showinfo(
            "Entrada registrada",
            f"Entrada registrada com sucesso!\n\n"
            f"Data: {data_entrada}\n"
            f"Hora: {hora_entrada}"
        )

        combo_prestador.set("")
        entrada_apartamento.delete(0, tk.END)

    botao_registrar = tk.Button(
        janela_acesso,
        text="Registrar Entrada",
        font=("Arial", 14),
        width=22,
        command=registrar
    )

    botao_registrar.pack(pady=30)


# ==========================================================
# ACESSOS ATIVOS
# ==========================================================

def abrir_acessos_ativos(janela_principal):

    janela_ativos = tk.Toplevel(janela_principal)
    janela_ativos.title("Acessos Ativos")
    janela_ativos.geometry("1100x600")

    titulo = tk.Label(
        janela_ativos,
        text="Prestadores no Condomínio",
        font=("Arial", 20)
    )

    titulo.pack(pady=15)

    frame_tabela = tk.Frame(janela_ativos)

    frame_tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    tabela = ttk.Treeview(
        frame_tabela,
        columns=(
            "id",
            "nome",
            "documento",
            "empresa",
            "apartamento",
            "data",
            "hora"
        ),
        show="headings"
    )

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome")
    tabela.heading("documento", text="Documento")
    tabela.heading("empresa", text="Empresa")
    tabela.heading("apartamento", text="Apartamento")
    tabela.heading("data", text="Data Entrada")
    tabela.heading("hora", text="Hora Entrada")

    tabela.column(
        "id",
        width=50,
        anchor="center"
    )

    tabela.column(
        "nome",
        width=220
    )

    tabela.column(
        "documento",
        width=150
    )

    tabela.column(
        "empresa",
        width=180
    )

    tabela.column(
        "apartamento",
        width=100,
        anchor="center"
    )

    tabela.column(
        "data",
        width=110,
        anchor="center"
    )

    tabela.column(
        "hora",
        width=100,
        anchor="center"
    )

    barra_rolagem = ttk.Scrollbar(
        frame_tabela,
        orient="vertical",
        command=tabela.yview
    )

    tabela.configure(
        yscrollcommand=barra_rolagem.set
    )

    barra_rolagem.pack(
        side="right",
        fill="y"
    )

    tabela.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ======================================================
    # CARREGAR ACESSOS ATIVOS
    # ======================================================

    def carregar():

        for item in tabela.get_children():
            tabela.delete(item)

        acessos = listar_acessos_ativos()

        for acesso in acessos:

            tabela.insert(
                "",
                tk.END,
                values=acesso
            )

    # ======================================================
    # REGISTRAR SAÍDA
    # ======================================================

    def registrar_saida():

        item_selecionado = tabela.selection()

        if not item_selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um prestador."
            )

            return

        dados = tabela.item(
            item_selecionado[0]
        )["values"]

        id_acesso = dados[0]
        nome = dados[1]
        apartamento = dados[4]

        confirmar = messagebox.askyesno(
            "Confirmar saída",
            f"Registrar saída deste prestador?\n\n"
            f"Nome: {nome}\n"
            f"Apartamento: {apartamento}"
        )

        if not confirmar:
            return

        agora = datetime.now()

        data_saida = agora.strftime("%d/%m/%Y")
        hora_saida = agora.strftime("%H:%M:%S")

        registrar_saida_prestador(
            id_acesso,
            data_saida,
            hora_saida
        )

        messagebox.showinfo(
            "Saída registrada",
            f"Saída registrada com sucesso!\n\n"
            f"Data: {data_saida}\n"
            f"Hora: {hora_saida}"
        )

        carregar()

    # ======================================================
    # BOTÕES
    # ======================================================

    frame_botoes = tk.Frame(
        janela_ativos
    )

    frame_botoes.pack(
        pady=10
    )

    botao_atualizar = tk.Button(
        frame_botoes,
        text="Atualizar Lista",
        width=18,
        command=carregar
    )

    botao_atualizar.pack(
        side="left",
        padx=5
    )

    botao_saida = tk.Button(
        frame_botoes,
        text="Registrar Saída",
        width=18,
        command=registrar_saida
    )

    botao_saida.pack(
        side="left",
        padx=5
    )

    carregar()


# ==========================================================
# HISTÓRICO DE ACESSOS
# ==========================================================

def abrir_historico_acessos(janela_principal):

    janela_historico = tk.Toplevel(janela_principal)
    janela_historico.title("Histórico de Acessos")
    janela_historico.geometry("1250x650")

    titulo = tk.Label(
        janela_historico,
        text="Histórico de Acessos de Prestadores",
        font=("Arial", 20)
    )

    titulo.pack(pady=15)

    # ======================================================
    # FILTROS DE PESQUISA
    # ======================================================

    frame_pesquisa = tk.Frame(
        janela_historico
    )

    frame_pesquisa.pack(
        pady=10
    )

    # Nome
    tk.Label(
        frame_pesquisa,
        text="Nome:",
        font=("Arial", 11)
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    entrada_nome = tk.Entry(
        frame_pesquisa,
        width=22,
        font=("Arial", 11)
    )

    entrada_nome.grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )

    # Apartamento
    tk.Label(
        frame_pesquisa,
        text="Apartamento:",
        font=("Arial", 11)
    ).grid(
        row=0,
        column=2,
        padx=5,
        pady=5
    )

    entrada_apartamento = tk.Entry(
        frame_pesquisa,
        width=12,
        font=("Arial", 11)
    )

    entrada_apartamento.grid(
        row=0,
        column=3,
        padx=5,
        pady=5
    )

    # Data
    tk.Label(
        frame_pesquisa,
        text="Data:",
        font=("Arial", 11)
    ).grid(
        row=0,
        column=4,
        padx=5,
        pady=5
    )

    entrada_data = tk.Entry(
        frame_pesquisa,
        width=12,
        font=("Arial", 11)
    )

    entrada_data.grid(
        row=0,
        column=5,
        padx=5,
        pady=5
    )

    tk.Label(
        frame_pesquisa,
        text="dd/mm/aaaa",
        font=("Arial", 9)
    ).grid(
        row=1,
        column=5
    )

    # ======================================================
    # TABELA
    # ======================================================

    frame_tabela = tk.Frame(
        janela_historico
    )

    frame_tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    tabela = ttk.Treeview(
        frame_tabela,
        columns=(
            "id",
            "nome",
            "documento",
            "empresa",
            "apartamento",
            "data_entrada",
            "hora_entrada",
            "data_saida",
            "hora_saida",
            "status"
        ),
        show="headings"
    )

    tabela.heading(
        "id",
        text="ID"
    )

    tabela.heading(
        "nome",
        text="Nome"
    )

    tabela.heading(
        "documento",
        text="Documento"
    )

    tabela.heading(
        "empresa",
        text="Empresa"
    )

    tabela.heading(
        "apartamento",
        text="Apartamento"
    )

    tabela.heading(
        "data_entrada",
        text="Data Entrada"
    )

    tabela.heading(
        "hora_entrada",
        text="Hora Entrada"
    )

    tabela.heading(
        "data_saida",
        text="Data Saída"
    )

    tabela.heading(
        "hora_saida",
        text="Hora Saída"
    )

    tabela.heading(
        "status",
        text="Status"
    )

    tabela.column(
        "id",
        width=50,
        anchor="center"
    )

    tabela.column(
        "nome",
        width=180
    )

    tabela.column(
        "documento",
        width=120
    )

    tabela.column(
        "empresa",
        width=150
    )

    tabela.column(
        "apartamento",
        width=100,
        anchor="center"
    )

    tabela.column(
        "data_entrada",
        width=100,
        anchor="center"
    )

    tabela.column(
        "hora_entrada",
        width=90,
        anchor="center"
    )

    tabela.column(
        "data_saida",
        width=100,
        anchor="center"
    )

    tabela.column(
        "hora_saida",
        width=90,
        anchor="center"
    )

    tabela.column(
        "status",
        width=100,
        anchor="center"
    )

    # Barras de rolagem
    barra_vertical = ttk.Scrollbar(
        frame_tabela,
        orient="vertical",
        command=tabela.yview
    )

    barra_horizontal = ttk.Scrollbar(
        frame_tabela,
        orient="horizontal",
        command=tabela.xview
    )

    tabela.configure(
        yscrollcommand=barra_vertical.set,
        xscrollcommand=barra_horizontal.set
    )

    barra_vertical.pack(
        side="right",
        fill="y"
    )

    barra_horizontal.pack(
        side="bottom",
        fill="x"
    )

    tabela.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ======================================================
    # CARREGAR HISTÓRICO
    # ======================================================

    def carregar():

        for item in tabela.get_children():
            tabela.delete(item)

        registros = listar_historico_acessos()

        for registro in registros:

            tabela.insert(
                "",
                tk.END,
                values=registro
            )

    # ======================================================
    # PESQUISAR HISTÓRICO
    # ======================================================

    def pesquisar():

        nome_pesquisa = (
            entrada_nome
            .get()
            .strip()
            .lower()
        )

        apartamento_pesquisa = (
            entrada_apartamento
            .get()
            .strip()
            .lower()
        )

        data_pesquisa = (
            entrada_data
            .get()
            .strip()
            .lower()
        )

        for item in tabela.get_children():
            tabela.delete(item)

        registros = listar_historico_acessos()

        for registro in registros:

            nome = str(
                registro[1]
            ).lower()

            apartamento = str(
                registro[4]
            ).lower()

            data_entrada = str(
                registro[5]
            ).lower()

            data_saida = str(
                registro[7]
            ).lower()

            encontrou_nome = (
                nome_pesquisa == ""
                or nome_pesquisa in nome
            )

            encontrou_apartamento = (
                apartamento_pesquisa == ""
                or apartamento_pesquisa
                in apartamento
            )

            encontrou_data = (
                data_pesquisa == ""
                or data_pesquisa
                in data_entrada
                or data_pesquisa
                in data_saida
            )

            if (
                encontrou_nome
                and encontrou_apartamento
                and encontrou_data
            ):

                tabela.insert(
                    "",
                    tk.END,
                    values=registro
                )

    # ======================================================
    # LIMPAR FILTROS
    # ======================================================

    def limpar_filtros():

        entrada_nome.delete(
            0,
            tk.END
        )

        entrada_apartamento.delete(
            0,
            tk.END
        )

        entrada_data.delete(
            0,
            tk.END
        )

        carregar()

    # ======================================================
    # BOTÕES
    # ======================================================

    frame_botoes = tk.Frame(
        janela_historico
    )

    frame_botoes.pack(
        pady=10
    )

    botao_pesquisar = tk.Button(
        frame_botoes,
        text="Pesquisar",
        width=15,
        command=pesquisar
    )

    botao_pesquisar.pack(
        side="left",
        padx=5
    )

    botao_todos = tk.Button(
        frame_botoes,
        text="Mostrar Todos",
        width=15,
        command=carregar
    )

    botao_todos.pack(
        side="left",
        padx=5
    )

    botao_limpar = tk.Button(
        frame_botoes,
        text="Limpar Filtros",
        width=15,
        command=limpar_filtros
    )

    botao_limpar.pack(
        side="left",
        padx=5
    )

    # Pressionar Enter pesquisa
    entrada_nome.bind(
        "<Return>",
        lambda event: pesquisar()
    )

    entrada_apartamento.bind(
        "<Return>",
        lambda event: pesquisar()
    )

    entrada_data.bind(
        "<Return>",
        lambda event: pesquisar()
    )

    # Carrega tudo quando abre
    carregar()