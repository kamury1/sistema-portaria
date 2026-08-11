import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from banco import cadastrar_visitante
from banco import listar_visitantes
from banco import pesquisar_visitantes
from banco import atualizar_visitante
from banco import excluir_visitante


# ==========================================================
# CADASTRO DE VISITANTES
# ==========================================================

def abrir_visitantes(janela_principal):

    janela_visitantes = tk.Toplevel(janela_principal)
    janela_visitantes.title("Cadastro de Visitantes")
    janela_visitantes.geometry("600x500")
    janela_visitantes.resizable(False, False)

    titulo = tk.Label(
        janela_visitantes,
        text="Cadastro de Visitantes",
        font=("Arial", 20)
    )

    titulo.pack(pady=20)

    formulario = tk.Frame(janela_visitantes)
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

    # Telefone
    tk.Label(
        formulario,
        text="Telefone:",
        font=("Arial", 12)
    ).grid(
        row=2,
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
        row=2,
        column=1,
        pady=10
    )

    # ======================================================
    # SALVAR VISITANTE
    # ======================================================

    def salvar():

        nome = entrada_nome.get().strip()
        documento = entrada_documento.get().strip()
        telefone = entrada_telefone.get().strip()

        if nome == "":
            messagebox.showwarning(
                "Atenção",
                "Informe o nome do visitante."
            )
            return

        if documento == "":
            messagebox.showwarning(
                "Atenção",
                "Informe o documento do visitante."
            )
            return

        cadastrar_visitante(
            nome,
            documento,
            telefone
        )

        messagebox.showinfo(
            "Sucesso",
            "Visitante cadastrado com sucesso!"
        )

        entrada_nome.delete(0, tk.END)
        entrada_documento.delete(0, tk.END)
        entrada_telefone.delete(0, tk.END)

        entrada_nome.focus()

    botao_salvar = tk.Button(
        janela_visitantes,
        text="Salvar Visitante",
        font=("Arial", 13),
        width=20,
        command=salvar
    )

    botao_salvar.pack(pady=25)

    entrada_nome.focus()


# ==========================================================
# VISITANTES CADASTRADOS
# ==========================================================

def abrir_lista_visitantes(janela_principal):

    janela_lista = tk.Toplevel(janela_principal)
    janela_lista.title("Visitantes Cadastrados")
    janela_lista.geometry("950x600")

    titulo = tk.Label(
        janela_lista,
        text="Visitantes Cadastrados",
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
            "telefone"
        ),
        show="headings"
    )

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome")
    tabela.heading("documento", text="Documento")
    tabela.heading("telefone", text="Telefone")

    tabela.column(
        "id",
        width=50,
        anchor="center"
    )

    tabela.column(
        "nome",
        width=300
    )

    tabela.column(
        "documento",
        width=200
    )

    tabela.column(
        "telefone",
        width=180
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
    # CARREGAR VISITANTES
    # ======================================================

    def carregar():

        for item in tabela.get_children():
            tabela.delete(item)

        visitantes = listar_visitantes()

        for visitante in visitantes:

            tabela.insert(
                "",
                tk.END,
                values=visitante
            )

    # ======================================================
    # PESQUISAR VISITANTE
    # ======================================================

    def pesquisar():

        nome = entrada_pesquisa.get().strip()

        for item in tabela.get_children():
            tabela.delete(item)

        visitantes = pesquisar_visitantes(nome)

        for visitante in visitantes:

            tabela.insert(
                "",
                tk.END,
                values=visitante
            )

    # ======================================================
    # EDITAR VISITANTE
    # ======================================================

    def editar():

        item_selecionado = tabela.selection()

        if not item_selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um visitante para editar."
            )

            return

        dados = tabela.item(
            item_selecionado[0]
        )["values"]

        id_visitante = dados[0]
        nome_atual = dados[1]
        documento_atual = dados[2]
        telefone_atual = dados[3]

        janela_editar = tk.Toplevel(janela_lista)
        janela_editar.title("Editar Visitante")
        janela_editar.geometry("550x400")
        janela_editar.resizable(False, False)

        titulo_editar = tk.Label(
            janela_editar,
            text="Editar Visitante",
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

        # Telefone
        tk.Label(
            formulario_editar,
            text="Telefone:",
            font=("Arial", 12)
        ).grid(
            row=2,
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
            row=2,
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
            telefone = entrada_telefone.get().strip()

            if nome == "":

                messagebox.showwarning(
                    "Atenção",
                    "Informe o nome do visitante."
                )

                return

            if documento == "":

                messagebox.showwarning(
                    "Atenção",
                    "Informe o documento do visitante."
                )

                return

            atualizar_visitante(
                id_visitante,
                nome,
                documento,
                telefone
            )

            messagebox.showinfo(
                "Sucesso",
                "Visitante atualizado com sucesso!"
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
    # EXCLUIR VISITANTE
    # ======================================================

    def excluir():

        item_selecionado = tabela.selection()

        if not item_selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um visitante para excluir."
            )

            return

        dados = tabela.item(
            item_selecionado[0]
        )["values"]

        id_visitante = dados[0]
        nome_visitante = dados[1]
        documento_visitante = dados[2]

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir este visitante?\n\n"
            f"Nome: {nome_visitante}\n"
            f"Documento: {documento_visitante}"
        )

        if not confirmar:
            return

        excluir_visitante(
            id_visitante
        )

        messagebox.showinfo(
            "Sucesso",
            "Visitante excluído com sucesso!"
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
        text="Editar Visitante",
        width=15,
        command=editar
    )

    botao_editar.pack(
        side="left",
        padx=5
    )

    botao_excluir = tk.Button(
        frame_botoes,
        text="Excluir Visitante",
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

    # Carrega os visitantes ao abrir
    carregar()