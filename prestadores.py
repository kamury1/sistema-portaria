import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from banco import cadastrar_prestador
from banco import listar_prestadores
from banco import pesquisar_prestadores
from banco import atualizar_prestador
from banco import excluir_prestador


# ==========================================================
# CADASTRO DE PRESTADORES
# ==========================================================

def abrir_prestadores(janela_principal):

    janela_prestadores = tk.Toplevel(janela_principal)
    janela_prestadores.title("Cadastro de Prestadores")
    janela_prestadores.geometry("600x500")
    janela_prestadores.resizable(False, False)

    titulo = tk.Label(
        janela_prestadores,
        text="Cadastro de Prestadores",
        font=("Arial", 20)
    )

    titulo.pack(pady=20)

    formulario = tk.Frame(janela_prestadores)
    formulario.pack(pady=10)

    # Nome
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

    # Documento
    tk.Label(
        formulario,
        text="Documento:",
        font=("Arial", 12)
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    entrada_documento = tk.Entry(
        formulario,
        width=35,
        font=("Arial", 12)
    )

    entrada_documento.grid(
        row=1,
        column=1,
        pady=10
    )

    # Empresa
    tk.Label(
        formulario,
        text="Empresa:",
        font=("Arial", 12)
    ).grid(
        row=2,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    entrada_empresa = tk.Entry(
        formulario,
        width=35,
        font=("Arial", 12)
    )

    entrada_empresa.grid(
        row=2,
        column=1,
        pady=10
    )

    # Telefone
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
    # SALVAR PRESTADOR
    # ======================================================

    def salvar():

        nome = entrada_nome.get().strip()
        documento = entrada_documento.get().strip()
        empresa = entrada_empresa.get().strip()
        telefone = entrada_telefone.get().strip()

        if nome == "":
            messagebox.showwarning(
                "Atenção",
                "Informe o nome do prestador."
            )
            return

        if documento == "":
            messagebox.showwarning(
                "Atenção",
                "Informe o documento do prestador."
            )
            return

        cadastrar_prestador(
            nome,
            documento,
            empresa,
            telefone
        )

        messagebox.showinfo(
            "Sucesso",
            "Prestador cadastrado com sucesso!"
        )

        entrada_nome.delete(0, tk.END)
        entrada_documento.delete(0, tk.END)
        entrada_empresa.delete(0, tk.END)
        entrada_telefone.delete(0, tk.END)

        entrada_nome.focus()

    botao_salvar = tk.Button(
        janela_prestadores,
        text="Salvar Prestador",
        font=("Arial", 13),
        width=20,
        command=salvar
    )

    botao_salvar.pack(pady=25)

    entrada_nome.focus()


# ==========================================================
# PRESTADORES CADASTRADOS
# ==========================================================

def abrir_lista_prestadores(janela_principal):

    janela_lista = tk.Toplevel(janela_principal)
    janela_lista.title("Prestadores Cadastrados")
    janela_lista.geometry("1050x620")

    titulo = tk.Label(
        janela_lista,
        text="Prestadores Cadastrados",
        font=("Arial", 20)
    )

    titulo.pack(pady=15)

    # ======================================================
    # PESQUISA
    # ======================================================

    frame_pesquisa = tk.Frame(janela_lista)
    frame_pesquisa.pack(pady=10)

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

    frame_tabela = tk.Frame(janela_lista)

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
            "telefone"
        ),
        show="headings"
    )

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome")
    tabela.heading("documento", text="Documento")
    tabela.heading("empresa", text="Empresa")
    tabela.heading("telefone", text="Telefone")

    tabela.column(
        "id",
        width=50,
        anchor="center"
    )

    tabela.column(
        "nome",
        width=250
    )

    tabela.column(
        "documento",
        width=170
    )

    tabela.column(
        "empresa",
        width=220
    )

    tabela.column(
        "telefone",
        width=150
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
    # CARREGAR PRESTADORES
    # ======================================================

    def carregar():

        for item in tabela.get_children():
            tabela.delete(item)

        prestadores = listar_prestadores()

        for prestador in prestadores:

            tabela.insert(
                "",
                tk.END,
                values=prestador
            )

    # ======================================================
    # PESQUISAR PRESTADOR
    # ======================================================

    def pesquisar():

        nome = entrada_pesquisa.get().strip()

        for item in tabela.get_children():
            tabela.delete(item)

        prestadores = pesquisar_prestadores(nome)

        for prestador in prestadores:

            tabela.insert(
                "",
                tk.END,
                values=prestador
            )

    # ======================================================
    # EDITAR PRESTADOR
    # ======================================================

    def editar():

        item_selecionado = tabela.selection()

        if not item_selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um prestador para editar."
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

        janela_editar = tk.Toplevel(janela_lista)
        janela_editar.title("Editar Prestador")
        janela_editar.geometry("550x450")
        janela_editar.resizable(False, False)

        titulo_editar = tk.Label(
            janela_editar,
            text="Editar Prestador",
            font=("Arial", 20)
        )

        titulo_editar.pack(pady=20)

        formulario_editar = tk.Frame(
            janela_editar
        )

        formulario_editar.pack(pady=10)

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

        # Documento
        tk.Label(
            formulario_editar,
            text="Documento:",
            font=("Arial", 12)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        entrada_documento = tk.Entry(
            formulario_editar,
            width=30,
            font=("Arial", 12)
        )

        entrada_documento.grid(
            row=1,
            column=1,
            pady=10
        )

        entrada_documento.insert(
            0,
            documento_atual
        )

        # Empresa
        tk.Label(
            formulario_editar,
            text="Empresa:",
            font=("Arial", 12)
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        entrada_empresa = tk.Entry(
            formulario_editar,
            width=30,
            font=("Arial", 12)
        )

        entrada_empresa.grid(
            row=2,
            column=1,
            pady=10
        )

        entrada_empresa.insert(
            0,
            empresa_atual
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

        # ==================================================
        # SALVAR ALTERAÇÕES
        # ==================================================

        def salvar_alteracoes():

            nome = entrada_nome.get().strip()
            documento = entrada_documento.get().strip()
            empresa = entrada_empresa.get().strip()
            telefone = entrada_telefone.get().strip()

            if nome == "":

                messagebox.showwarning(
                    "Atenção",
                    "Informe o nome do prestador."
                )

                return

            if documento == "":

                messagebox.showwarning(
                    "Atenção",
                    "Informe o documento do prestador."
                )

                return

            atualizar_prestador(
                id_prestador,
                nome,
                documento,
                empresa,
                telefone
            )

            messagebox.showinfo(
                "Sucesso",
                "Prestador atualizado com sucesso!"
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
    # EXCLUIR PRESTADOR
    # ======================================================

    def excluir():

        item_selecionado = tabela.selection()

        if not item_selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um prestador para excluir."
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
            f"Documento: {documento_prestador}"
        )

        if not confirmar:
            return

        excluir_prestador(
            id_prestador
        )

        messagebox.showinfo(
            "Sucesso",
            "Prestador excluído com sucesso!"
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
        text="Editar Prestador",
        width=15,
        command=editar
    )

    botao_editar.pack(
        side="left",
        padx=5
    )

    botao_excluir = tk.Button(
        frame_botoes,
        text="Excluir Prestador",
        width=15,
        command=excluir
    )

    botao_excluir.pack(
        side="left",
        padx=5
    )

    # Pesquisar apertando Enter
    entrada_pesquisa.bind(
        "<Return>",
        lambda event: pesquisar()
    )

    # Editar dando dois cliques
    tabela.bind(
        "<Double-1>",
        lambda event: editar()
    )

    # Carrega os dados ao abrir a tela
    carregar()