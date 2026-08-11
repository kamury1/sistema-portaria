import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from banco import cadastrar_morador
from banco import listar_moradores
from banco import pesquisar_moradores
from banco import atualizar_morador
from banco import excluir_morador


# ==========================================================
# CADASTRAR MORADOR
# ==========================================================

def abrir_moradores(janela_principal):

    janela_moradores = tk.Toplevel(
        janela_principal
    )

    janela_moradores.title(
        "Cadastro de Moradores"
    )

    janela_moradores.geometry(
        "600x550"
    )

    janela_moradores.resizable(
        False,
        False
    )

    titulo = tk.Label(
        janela_moradores,
        text="Cadastro de Moradores",
        font=("Arial", 20)
    )

    titulo.pack(
        pady=20
    )

    formulario = tk.Frame(
        janela_moradores
    )

    formulario.pack(
        pady=10
    )

    # ======================================================
    # NOME
    # ======================================================

    tk.Label(
        formulario,
        text="Nome:",
        font=("Arial", 12)
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    entrada_nome = tk.Entry(
        formulario,
        width=35,
        font=("Arial", 12)
    )

    entrada_nome.grid(
        row=0,
        column=1,
        pady=10
    )

    # ======================================================
    # APARTAMENTO
    # ======================================================

    tk.Label(
        formulario,
        text="Apartamento:",
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
        width=35,
        font=("Arial", 12)
    )

    entrada_apartamento.grid(
        row=1,
        column=1,
        pady=10
    )

    # ======================================================
    # VAGAS
    # ======================================================

    tk.Label(
        formulario,
        text="Vaga(s):",
        font=("Arial", 12)
    ).grid(
        row=2,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    entrada_vagas = tk.Entry(
        formulario,
        width=35,
        font=("Arial", 12)
    )

    entrada_vagas.grid(
        row=2,
        column=1,
        pady=10
    )

    # ======================================================
    # TELEFONE
    # ======================================================

    tk.Label(
        formulario,
        text="Telefone:",
        font=("Arial", 12)
    ).grid(
        row=3,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    entrada_telefone = tk.Entry(
        formulario,
        width=35,
        font=("Arial", 12)
    )

    entrada_telefone.grid(
        row=3,
        column=1,
        pady=10
    )

    # ======================================================
    # TIPO
    # ======================================================

    tk.Label(
        formulario,
        text="Tipo:",
        font=("Arial", 12)
    ).grid(
        row=4,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    tipo_morador = tk.StringVar(
        value="Proprietário"
    )

    opcoes_tipo = tk.OptionMenu(
        formulario,
        tipo_morador,
        "Proprietário",
        "Inquilino",
        "Familiar",
        "Outro"
    )

    opcoes_tipo.config(
        width=28,
        font=("Arial", 11)
    )

    opcoes_tipo.grid(
        row=4,
        column=1,
        pady=10
    )

    # ======================================================
    # SALVAR
    # ======================================================

    def salvar():

        nome = entrada_nome.get().strip()

        apartamento = (
            entrada_apartamento
            .get()
            .strip()
        )

        vagas = (
            entrada_vagas
            .get()
            .strip()
        )

        telefone = (
            entrada_telefone
            .get()
            .strip()
        )

        tipo = tipo_morador.get()

        if nome == "":

            messagebox.showwarning(
                "Atenção",
                "Informe o nome do morador."
            )

            return

        if apartamento == "":

            messagebox.showwarning(
                "Atenção",
                "Informe o apartamento."
            )

            return

        cadastrar_morador(
            nome,
            apartamento,
            vagas,
            telefone,
            tipo
        )

        messagebox.showinfo(
            "Sucesso",
            "Morador cadastrado com sucesso!"
        )

        entrada_nome.delete(
            0,
            tk.END
        )

        entrada_apartamento.delete(
            0,
            tk.END
        )

        entrada_vagas.delete(
            0,
            tk.END
        )

        entrada_telefone.delete(
            0,
            tk.END
        )

        tipo_morador.set(
            "Proprietário"
        )

        entrada_nome.focus()

    botao_salvar = tk.Button(
        janela_moradores,
        text="Salvar Morador",
        font=("Arial", 13),
        width=20,
        command=salvar
    )

    botao_salvar.pack(
        pady=25
    )

    entrada_nome.focus()


# ==========================================================
# MORADORES CADASTRADOS
# ==========================================================

def abrir_lista_moradores(janela_principal):

    janela_lista = tk.Toplevel(
        janela_principal
    )

    janela_lista.title(
        "Moradores Cadastrados"
    )

    janela_lista.geometry(
        "1100x600"
    )

    titulo = tk.Label(
        janela_lista,
        text="Moradores Cadastrados",
        font=("Arial", 20)
    )

    titulo.pack(
        pady=15
    )

    # ======================================================
    # PESQUISA
    # ======================================================

    frame_pesquisa = tk.Frame(
        janela_lista
    )

    frame_pesquisa.pack(
        pady=10
    )

    tk.Label(
        frame_pesquisa,
        text="Pesquisar por nome:",
        font=("Arial", 12)
    ).pack(
        side="left",
        padx=5
    )

    entrada_pesquisa = tk.Entry(
        frame_pesquisa,
        width=30,
        font=("Arial", 12)
    )

    entrada_pesquisa.pack(
        side="left",
        padx=5
    )

    # ======================================================
    # TABELA
    # ======================================================

    frame_tabela = tk.Frame(
        janela_lista
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
            "apartamento",
            "vagas",
            "telefone",
            "tipo"
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
        "apartamento",
        text="Apartamento"
    )

    tabela.heading(
        "vagas",
        text="Vaga(s)"
    )

    tabela.heading(
        "telefone",
        text="Telefone"
    )

    tabela.heading(
        "tipo",
        text="Tipo"
    )

    tabela.column(
        "id",
        width=50,
        anchor="center"
    )

    tabela.column(
        "nome",
        width=280
    )

    tabela.column(
        "apartamento",
        width=120,
        anchor="center"
    )

    tabela.column(
        "vagas",
        width=130,
        anchor="center"
    )

    tabela.column(
        "telefone",
        width=170,
        anchor="center"
    )

    tabela.column(
        "tipo",
        width=150,
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
    # CARREGAR MORADORES
    # ======================================================

    def carregar():

        for item in tabela.get_children():
            tabela.delete(item)

        moradores = listar_moradores()

        for morador in moradores:

            tabela.insert(
                "",
                tk.END,
                values=morador
            )

    # ======================================================
    # PESQUISAR
    # ======================================================

    def pesquisar():

        nome = (
            entrada_pesquisa
            .get()
            .strip()
        )

        for item in tabela.get_children():
            tabela.delete(item)

        moradores = pesquisar_moradores(
            nome
        )

        for morador in moradores:

            tabela.insert(
                "",
                tk.END,
                values=morador
            )

    # ======================================================
    # EDITAR MORADOR
    # ======================================================

    def editar():

        item_selecionado = (
            tabela.selection()
        )

        if not item_selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um morador para editar."
            )

            return

        dados = tabela.item(
            item_selecionado[0]
        )["values"]

        id_morador = dados[0]
        nome_atual = dados[1]
        apartamento_atual = dados[2]
        vagas_atual = dados[3]
        telefone_atual = dados[4]
        tipo_atual = dados[5]

        janela_editar = tk.Toplevel(
            janela_lista
        )

        janela_editar.title(
            "Editar Morador"
        )

        janela_editar.geometry(
            "550x500"
        )

        janela_editar.resizable(
            False,
            False
        )

        titulo_editar = tk.Label(
            janela_editar,
            text="Editar Morador",
            font=("Arial", 20)
        )

        titulo_editar.pack(
            pady=20
        )

        formulario_editar = tk.Frame(
            janela_editar
        )

        formulario_editar.pack(
            pady=10
        )

        # Nome
        tk.Label(
            formulario_editar,
            text="Nome:",
            font=("Arial", 12)
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        entrada_nome = tk.Entry(
            formulario_editar,
            width=30,
            font=("Arial", 12)
        )

        entrada_nome.grid(
            row=0,
            column=1,
            pady=10
        )

        entrada_nome.insert(
            0,
            nome_atual
        )

        # Apartamento
        tk.Label(
            formulario_editar,
            text="Apartamento:",
            font=("Arial", 12)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        entrada_apartamento = tk.Entry(
            formulario_editar,
            width=30,
            font=("Arial", 12)
        )

        entrada_apartamento.grid(
            row=1,
            column=1,
            pady=10
        )

        entrada_apartamento.insert(
            0,
            apartamento_atual
        )

        # Vagas
        tk.Label(
            formulario_editar,
            text="Vaga(s):",
            font=("Arial", 12)
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        entrada_vagas = tk.Entry(
            formulario_editar,
            width=30,
            font=("Arial", 12)
        )

        entrada_vagas.grid(
            row=2,
            column=1,
            pady=10
        )

        entrada_vagas.insert(
            0,
            vagas_atual
        )

        # Telefone
        tk.Label(
            formulario_editar,
            text="Telefone:",
            font=("Arial", 12)
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        entrada_telefone = tk.Entry(
            formulario_editar,
            width=30,
            font=("Arial", 12)
        )

        entrada_telefone.grid(
            row=3,
            column=1,
            pady=10
        )

        entrada_telefone.insert(
            0,
            telefone_atual
        )

        # Tipo
        tk.Label(
            formulario_editar,
            text="Tipo:",
            font=("Arial", 12)
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        tipo_morador = tk.StringVar(
            value=tipo_atual
        )

        opcoes_tipo = tk.OptionMenu(
            formulario_editar,
            tipo_morador,
            "Proprietário",
            "Inquilino",
            "Familiar",
            "Outro"
        )

        opcoes_tipo.config(
            width=23,
            font=("Arial", 11)
        )

        opcoes_tipo.grid(
            row=4,
            column=1,
            pady=10
        )

        # ==================================================
        # SALVAR ALTERAÇÕES
        # ==================================================

        def salvar_alteracoes():

            nome = (
                entrada_nome
                .get()
                .strip()
            )

            apartamento = (
                entrada_apartamento
                .get()
                .strip()
            )

            vagas = (
                entrada_vagas
                .get()
                .strip()
            )

            telefone = (
                entrada_telefone
                .get()
                .strip()
            )

            tipo = tipo_morador.get()

            if nome == "" or apartamento == "":

                messagebox.showwarning(
                    "Atenção",
                    "Nome e apartamento são obrigatórios."
                )

                return

            atualizar_morador(
                id_morador,
                nome,
                apartamento,
                vagas,
                telefone,
                tipo
            )

            messagebox.showinfo(
                "Sucesso",
                "Morador atualizado com sucesso!"
            )

            janela_editar.destroy()

            carregar()

        botao_salvar = tk.Button(
            janela_editar,
            text="Salvar Alterações",
            font=("Arial", 12),
            width=20,
            command=salvar_alteracoes
        )

        botao_salvar.pack(
            pady=20
        )

        entrada_nome.focus()

    # ======================================================
    # EXCLUIR MORADOR
    # ======================================================

    def excluir():

        item_selecionado = (
            tabela.selection()
        )

        if not item_selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um morador para excluir."
            )

            return

        dados = tabela.item(
            item_selecionado[0]
        )["values"]

        id_morador = dados[0]
        nome_morador = dados[1]
        apartamento = dados[2]

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir este morador?\n\n"
            f"Nome: {nome_morador}\n"
            f"Apartamento: {apartamento}"
        )

        if not confirmar:
            return

        excluir_morador(
            id_morador
        )

        messagebox.showinfo(
            "Sucesso",
            "Morador excluído com sucesso!"
        )

        carregar()

    # ======================================================
    # BOTÕES
    # ======================================================

    frame_botoes = tk.Frame(
        janela_lista
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

    botao_editar = tk.Button(
        frame_botoes,
        text="Editar Morador",
        width=15,
        command=editar
    )

    botao_editar.pack(
        side="left",
        padx=5
    )

    botao_excluir = tk.Button(
        frame_botoes,
        text="Excluir Morador",
        width=15,
        command=excluir
    )

    botao_excluir.pack(
        side="left",
        padx=5
    )

    # Pesquisar pressionando Enter
    entrada_pesquisa.bind(
        "<Return>",
        lambda event: pesquisar()
    )

    # Editar dando dois cliques
    tabela.bind(
        "<Double-1>",
        lambda event: editar()
    )

    carregar()