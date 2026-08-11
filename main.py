import tkinter as tk
from datetime import datetime

from banco import criar_tabelas

from moradores import abrir_moradores
from moradores import abrir_lista_moradores

from visitantes import abrir_visitantes
from visitantes import abrir_lista_visitantes

from prestadores import abrir_prestadores
from prestadores import abrir_lista_prestadores

from acessos import abrir_registro_entrada
from acessos import abrir_acessos_ativos
from acessos import abrir_historico_acessos


# ==========================================================
# CORES DO SISTEMA
# ==========================================================

COR_FUNDO = "#0B1F33"          # Azul-marinho
COR_CABECALHO = "#081724"      # Azul mais escuro
COR_CARTAO = "#132A40"         # Azul dos blocos
COR_BOTAO = "#1F3B57"         # Botão normal
COR_BOTAO_ATIVO = "#294E70"   # Botão ao passar/clicar
COR_TEXTO = "#FFFFFF"         # Branco
COR_TEXTO_SECUNDARIO = "#D9E2EC"
COR_DESTAQUE = "#C62828"       # Vermelho
COR_BORDA = "#274B6D"


# ==========================================================
# CRIAR TABELAS
# ==========================================================

criar_tabelas()


# ==========================================================
# JANELA PRINCIPAL
# ==========================================================

janela = tk.Tk()

janela.title(
    "Sistema de Portaria - Edifício Oxygen | Veper"
)

janela.state("zoomed")

janela.configure(
    bg=COR_FUNDO
)


# ==========================================================
# CABEÇALHO
# ==========================================================

frame_cabecalho = tk.Frame(
    janela,
    bg=COR_CABECALHO,
    height=120
)

frame_cabecalho.pack(
    fill="x"
)

frame_cabecalho.pack_propagate(
    False
)


titulo = tk.Label(
    frame_cabecalho,
    text="SISTEMA DE PORTARIA",
    font=("Arial", 27, "bold"),
    bg=COR_CABECALHO,
    fg=COR_TEXTO
)

titulo.pack(
    pady=(18, 3)
)


subtitulo = tk.Label(
    frame_cabecalho,
    text="Edifício Oxygen  •  Veper",
    font=("Arial", 15, "bold"),
    bg=COR_CABECALHO,
    fg=COR_DESTAQUE
)

subtitulo.pack()


# ==========================================================
# ÁREA PRINCIPAL
# ==========================================================

frame_principal = tk.Frame(
    janela,
    bg=COR_FUNDO
)

frame_principal.pack(
    expand=True
)


# ==========================================================
# FUNÇÃO PARA CRIAR BOTÕES
# ==========================================================

def criar_botao(
    frame,
    texto,
    comando
):

    botao = tk.Button(
        frame,
        text=texto,
        font=("Arial", 12, "bold"),
        width=23,
        height=2,

        bg=COR_BOTAO,
        fg=COR_TEXTO,

        activebackground=COR_BOTAO_ATIVO,
        activeforeground=COR_TEXTO,

        relief="flat",
        borderwidth=0,

        cursor="hand2",

        command=comando
    )

    botao.pack(
        pady=8
    )

    return botao


# ==========================================================
# MORADORES
# ==========================================================

frame_moradores = tk.LabelFrame(
    frame_principal,
    text="  MORADORES  ",
    font=("Arial", 14, "bold"),

    bg=COR_CARTAO,
    fg=COR_TEXTO,

    width=350,
    height=230,

    padx=25,
    pady=20,

    bd=2,
    relief="groove"
)

frame_moradores.grid(
    row=0,
    column=0,
    padx=22,
    pady=18
)

frame_moradores.grid_propagate(
    False
)


criar_botao(
    frame_moradores,
    "Cadastrar Morador",
    lambda: abrir_moradores(janela)
)


criar_botao(
    frame_moradores,
    "Moradores Cadastrados",
    lambda: abrir_lista_moradores(janela)
)


# ==========================================================
# VISITANTES
# ==========================================================

frame_visitantes = tk.LabelFrame(
    frame_principal,
    text="  VISITANTES  ",
    font=("Arial", 14, "bold"),

    bg=COR_CARTAO,
    fg=COR_TEXTO,

    width=350,
    height=230,

    padx=25,
    pady=20,

    bd=2,
    relief="groove"
)

frame_visitantes.grid(
    row=0,
    column=1,
    padx=22,
    pady=18
)

frame_visitantes.grid_propagate(
    False
)


criar_botao(
    frame_visitantes,
    "Cadastrar Visitante",
    lambda: abrir_visitantes(janela)
)


criar_botao(
    frame_visitantes,
    "Visitantes Cadastrados",
    lambda: abrir_lista_visitantes(janela)
)


# ==========================================================
# PRESTADORES
# ==========================================================

frame_prestadores = tk.LabelFrame(
    frame_principal,
    text="  PRESTADORES  ",
    font=("Arial", 14, "bold"),

    bg=COR_CARTAO,
    fg=COR_TEXTO,

    width=350,
    height=260,

    padx=25,
    pady=20,

    bd=2,
    relief="groove"
)

frame_prestadores.grid(
    row=1,
    column=0,
    padx=22,
    pady=18
)

frame_prestadores.grid_propagate(
    False
)


criar_botao(
    frame_prestadores,
    "Cadastrar Prestador",
    lambda: abrir_prestadores(janela)
)


criar_botao(
    frame_prestadores,
    "Prestadores Cadastrados",
    lambda: abrir_lista_prestadores(janela)
)


# ==========================================================
# CONTROLE DE ACESSO
# ==========================================================

frame_acessos = tk.LabelFrame(
    frame_principal,
    text="  CONTROLE DE ACESSO  ",
    font=("Arial", 14, "bold"),

    bg=COR_CARTAO,
    fg=COR_TEXTO,

    width=350,
    height=260,

    padx=25,
    pady=15,

    bd=2,
    relief="groove"
)

frame_acessos.grid(
    row=1,
    column=1,
    padx=22,
    pady=18
)

frame_acessos.grid_propagate(
    False
)


criar_botao(
    frame_acessos,
    "Registrar Entrada",
    lambda: abrir_registro_entrada(janela)
)


criar_botao(
    frame_acessos,
    "Acessos Ativos",
    lambda: abrir_acessos_ativos(janela)
)


criar_botao(
    frame_acessos,
    "Histórico de Acessos",
    lambda: abrir_historico_acessos(janela)
)


# ==========================================================
# RODAPÉ
# ==========================================================

frame_rodape = tk.Frame(
    janela,
    bg=COR_CABECALHO,
    height=70
)

frame_rodape.pack(
    fill="x",
    side="bottom"
)

frame_rodape.pack_propagate(
    False
)


operador = tk.Label(
    frame_rodape,
    text="Operador: Cristiano",
    font=("Arial", 11, "bold"),
    bg=COR_CABECALHO,
    fg=COR_TEXTO
)

operador.pack(
    pady=(8, 2)
)


relogio = tk.Label(
    frame_rodape,
    text="",
    font=("Arial", 11),
    bg=COR_CABECALHO,
    fg=COR_TEXTO_SECUNDARIO
)

relogio.pack()


# ==========================================================
# RELÓGIO AUTOMÁTICO
# ==========================================================

def atualizar_relogio():

    agora = datetime.now()

    texto = agora.strftime(
        "%d/%m/%Y  •  %H:%M:%S"
    )

    relogio.config(
        text=texto
    )

    janela.after(
        1000,
        atualizar_relogio
    )


atualizar_relogio()


# ==========================================================
# INICIAR SISTEMA
# ==========================================================

janela.mainloop()