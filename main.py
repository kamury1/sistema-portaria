import os
import tkinter as tk
from datetime import datetime

from banco import (
    criar_tabelas,
    listar_moradores,
    listar_visitantes,
    listar_prestadores,
    listar_acessos_ativos,
)

from moradores import abrir_moradores, abrir_lista_moradores
from visitantes import abrir_visitantes, abrir_lista_visitantes
from prestadores import abrir_prestadores, abrir_lista_prestadores
from acessos import abrir_registro_entrada, abrir_acessos_ativos, abrir_historico_acessos
from importador import importar_planilha
from backup import fazer_backup_banco
from busca_global import abrir_busca_global
from login import solicitar_login


# ==========================================================
# CORES / IDENTIDADE VISUAL
# ==========================================================

COR_FUNDO = "#0B1220"
COR_SIDEBAR = "#0F1B2D"
COR_TOPO = "#111D30"
COR_CARTAO = "#17263A"
COR_CARTAO_BORDA = "#253B56"
COR_BOTAO = "#1B2D45"
COR_BOTAO_HOVER = "#274463"
COR_DESTAQUE = "#D32F2F"
COR_SUCESSO = "#2E7D32"
COR_TEXTO = "#F5F7FA"
COR_TEXTO_2 = "#A9B7C6"
COR_LINHA = "#263A50"

FONTE = "Segoe UI"


# ==========================================================
# BANCO
# ==========================================================

criar_tabelas()


# ==========================================================
# JANELA PRINCIPAL
# ==========================================================

janela = tk.Tk()
janela.withdraw()
janela.title("Sistema de Portaria - Edifício Oxygen | Veper")
janela.configure(bg=COR_FUNDO)
janela.minsize(1100, 680)

try:
    janela.state("zoomed")
except tk.TclError:
    janela.geometry("1366x768")

# Ícone do programa, se estiver disponível na pasta do projeto
try:
    caminho_icone = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icone_portaria.ico")
    if os.path.exists(caminho_icone):
        janela.iconbitmap(caminho_icone)
except Exception:
    pass


# ==========================================================
# LOGIN DO OPERADOR
# ==========================================================

operador_atual = solicitar_login(janela)

if operador_atual is None:
    janela.destroy()
    raise SystemExit

janela.deiconify()

try:
    janela.state("zoomed")
except tk.TclError:
    pass


# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def adicionar_hover(botao, normal=COR_BOTAO, hover=COR_BOTAO_HOVER):
    botao.bind("<Enter>", lambda _evento: botao.config(bg=hover))
    botao.bind("<Leave>", lambda _evento: botao.config(bg=normal))


def criar_botao_menu(parent, texto, comando, destaque=False):
    cor_normal = COR_DESTAQUE if destaque else COR_BOTAO
    cor_hover = "#B71C1C" if destaque else COR_BOTAO_HOVER

    botao = tk.Button(
        parent,
        text=texto,
        command=comando,
        anchor="w",
        padx=18,
        pady=11,
        font=(FONTE, 10, "bold"),
        bg=cor_normal,
        fg=COR_TEXTO,
        activebackground=cor_hover,
        activeforeground=COR_TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
    )
    botao.pack(fill="x", padx=14, pady=3)
    adicionar_hover(botao, cor_normal, cor_hover)
    return botao


def criar_titulo_secao(parent, texto):
    tk.Label(
        parent,
        text=texto.upper(),
        font=(FONTE, 8, "bold"),
        bg=COR_SIDEBAR,
        fg=COR_TEXTO_2,
        anchor="w",
    ).pack(fill="x", padx=20, pady=(18, 5))


def abrir_e_atualizar(funcao):
    funcao(janela)
    janela.after(300, atualizar_dashboard)


# ==========================================================
# LAYOUT BASE
# ==========================================================

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(1, weight=1)

# ----------------------------------------------------------
# MENU LATERAL
# ----------------------------------------------------------

sidebar = tk.Frame(janela, bg=COR_SIDEBAR, width=270)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)

logo_area = tk.Frame(sidebar, bg=COR_SIDEBAR, height=105)
logo_area.pack(fill="x")
logo_area.pack_propagate(False)

logo = tk.Label(
    logo_area,
    text="PORTARIA",
    font=(FONTE, 22, "bold"),
    bg=COR_SIDEBAR,
    fg=COR_TEXTO,
)
logo.pack(anchor="w", padx=20, pady=(20, 0))

sublogo = tk.Label(
    logo_area,
    text="EDIFÍCIO OXYGEN  •  VEPER",
    font=(FONTE, 8, "bold"),
    bg=COR_SIDEBAR,
    fg=COR_DESTAQUE,
)
sublogo.pack(anchor="w", padx=21, pady=(2, 10))

separator = tk.Frame(sidebar, bg=COR_LINHA, height=1)
separator.pack(fill="x", padx=14)

criar_titulo_secao(sidebar, "Cadastros")
criar_botao_menu(sidebar, "+  Cadastrar morador", lambda: abrir_e_atualizar(abrir_moradores))
criar_botao_menu(sidebar, "   Moradores cadastrados", lambda: abrir_e_atualizar(abrir_lista_moradores))
criar_botao_menu(sidebar, "+  Cadastrar visitante", lambda: abrir_e_atualizar(abrir_visitantes))
criar_botao_menu(sidebar, "   Visitantes cadastrados", lambda: abrir_e_atualizar(abrir_lista_visitantes))
criar_botao_menu(sidebar, "+  Cadastrar prestador", lambda: abrir_e_atualizar(abrir_prestadores))
criar_botao_menu(sidebar, "   Prestadores cadastrados", lambda: abrir_e_atualizar(abrir_lista_prestadores))

criar_titulo_secao(sidebar, "Controle de acesso")
criar_botao_menu(
    sidebar,
    "→  Registrar entrada",
    lambda: (
        abrir_registro_entrada(janela, operador_atual),
        janela.after(300, atualizar_dashboard)
    ),
    destaque=True
)
criar_botao_menu(
    sidebar,
    "●  Acessos ativos",
    lambda: (
        abrir_acessos_ativos(janela, operador_atual),
        janela.after(300, atualizar_dashboard)
    )
)
criar_botao_menu(sidebar, "≡  Histórico de acessos", lambda: abrir_e_atualizar(abrir_historico_acessos))

criar_titulo_secao(sidebar, "Ferramentas")
criar_botao_menu(sidebar, "↑  Importar planilha", lambda: importar_planilha(janela))
criar_botao_menu(sidebar, "▣  Fazer backup", lambda: fazer_backup_banco(janela))

# Informações no rodapé do menu
rodape_sidebar = tk.Frame(sidebar, bg=COR_SIDEBAR)
rodape_sidebar.pack(side="bottom", fill="x", padx=18, pady=18)

tk.Frame(rodape_sidebar, bg=COR_LINHA, height=1).pack(fill="x", pady=(0, 12))

tk.Label(
    rodape_sidebar,
    text="OPERADOR",
    font=(FONTE, 8, "bold"),
    bg=COR_SIDEBAR,
    fg=COR_TEXTO_2,
).pack(anchor="w")

tk.Label(
    rodape_sidebar,
    text=operador_atual["nome"],
    font=(FONTE, 11, "bold"),
    bg=COR_SIDEBAR,
    fg=COR_TEXTO,
).pack(anchor="w", pady=(2, 0))

tk.Label(
    rodape_sidebar,
    text=f'@{operador_atual["usuario"]}',
    font=(FONTE, 8),
    bg=COR_SIDEBAR,
    fg=COR_TEXTO_2,
).pack(anchor="w", pady=(1, 0))


# ----------------------------------------------------------
# CONTEÚDO PRINCIPAL
# ----------------------------------------------------------

conteudo = tk.Frame(janela, bg=COR_FUNDO)
conteudo.grid(row=0, column=1, sticky="nsew")
conteudo.grid_rowconfigure(1, weight=1)
conteudo.grid_columnconfigure(0, weight=1)

# Topo
frame_topo = tk.Frame(conteudo, bg=COR_TOPO, height=88)
frame_topo.grid(row=0, column=0, sticky="ew")
frame_topo.grid_propagate(False)
frame_topo.grid_columnconfigure(0, weight=1)

bloco_titulo = tk.Frame(frame_topo, bg=COR_TOPO)
bloco_titulo.grid(row=0, column=0, sticky="w", padx=34, pady=17)

lbl_titulo = tk.Label(
    bloco_titulo,
    text="Painel de Controle",
    font=(FONTE, 22, "bold"),
    bg=COR_TOPO,
    fg=COR_TEXTO,
)
lbl_titulo.pack(anchor="w")

lbl_subtitulo = tk.Label(
    bloco_titulo,
    text="Visão geral da portaria e acessos do condomínio",
    font=(FONTE, 10),
    bg=COR_TOPO,
    fg=COR_TEXTO_2,
)
lbl_subtitulo.pack(anchor="w", pady=(2, 0))

bloco_relogio = tk.Frame(frame_topo, bg=COR_TOPO)
bloco_relogio.grid(row=0, column=1, sticky="e", padx=34)

lbl_data = tk.Label(
    bloco_relogio,
    text="",
    font=(FONTE, 9),
    bg=COR_TOPO,
    fg=COR_TEXTO_2,
)
lbl_data.pack(anchor="e")

lbl_hora = tk.Label(
    bloco_relogio,
    text="",
    font=(FONTE, 17, "bold"),
    bg=COR_TOPO,
    fg=COR_TEXTO,
)
lbl_hora.pack(anchor="e")


# Área do dashboard
painel = tk.Frame(conteudo, bg=COR_FUNDO)
painel.grid(row=1, column=0, sticky="nsew", padx=34, pady=28)
painel.grid_columnconfigure(0, weight=1)
painel.grid_columnconfigure(1, weight=1)
painel.grid_columnconfigure(2, weight=1)
painel.grid_columnconfigure(3, weight=1)

# Cabeçalho da seção
secao_topo = tk.Frame(painel, bg=COR_FUNDO)
secao_topo.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 16))
secao_topo.grid_columnconfigure(0, weight=1)

tk.Label(
    secao_topo,
    text="Resumo do sistema",
    font=(FONTE, 14, "bold"),
    bg=COR_FUNDO,
    fg=COR_TEXTO,
).grid(row=0, column=0, sticky="w")

btn_atualizar = tk.Button(
    secao_topo,
    text="Atualizar painel",
    command=lambda: atualizar_dashboard(),
    font=(FONTE, 9, "bold"),
    bg=COR_BOTAO,
    fg=COR_TEXTO,
    activebackground=COR_BOTAO_HOVER,
    activeforeground=COR_TEXTO,
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=14,
    pady=7,
)
btn_atualizar.grid(row=0, column=1, sticky="e")
adicionar_hover(btn_atualizar)


# ==========================================================
# CARDS DO DASHBOARD
# ==========================================================

labels_contadores = {}


def criar_card(coluna, titulo, descricao, chave, cor_indicador):
    card = tk.Frame(
        painel,
        bg=COR_CARTAO,
        highlightthickness=1,
        highlightbackground=COR_CARTAO_BORDA,
        height=150,
    )
    card.grid(row=1, column=coluna, sticky="nsew", padx=(0 if coluna == 0 else 7, 0 if coluna == 3 else 7))
    card.grid_propagate(False)

    indicador = tk.Frame(card, bg=cor_indicador, width=5)
    indicador.pack(side="left", fill="y")

    interno = tk.Frame(card, bg=COR_CARTAO)
    interno.pack(fill="both", expand=True, padx=18, pady=17)

    tk.Label(
        interno,
        text=titulo,
        font=(FONTE, 10, "bold"),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
    ).pack(anchor="w")

    numero = tk.Label(
        interno,
        text="0",
        font=(FONTE, 29, "bold"),
        bg=COR_CARTAO,
        fg=COR_TEXTO,
    )
    numero.pack(anchor="w", pady=(5, 0))

    tk.Label(
        interno,
        text=descricao,
        font=(FONTE, 9),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
    ).pack(anchor="w")

    labels_contadores[chave] = numero


criar_card(0, "MORADORES", "Cadastros no sistema", "moradores", "#1976D2")
criar_card(1, "VISITANTES", "Cadastros no sistema", "visitantes", "#7B1FA2")
criar_card(2, "PRESTADORES", "Cadastros no sistema", "prestadores", "#EF6C00")
criar_card(3, "ACESSOS ATIVOS", "Pessoas com entrada ativa", "acessos", COR_SUCESSO)



# ==========================================================
# BUSCA RÁPIDA
# ==========================================================

frame_busca = tk.Frame(
    painel,
    bg=COR_CARTAO,
    highlightthickness=1,
    highlightbackground=COR_CARTAO_BORDA,
)
frame_busca.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(22, 0))
frame_busca.grid_columnconfigure(1, weight=1)

tk.Label(
    frame_busca,
    text="Busca rápida",
    font=(FONTE, 11, "bold"),
    bg=COR_CARTAO,
    fg=COR_TEXTO,
).grid(row=0, column=0, padx=(22, 14), pady=18, sticky="w")

entrada_busca_global = tk.Entry(
    frame_busca,
    font=(FONTE, 11),
    bg=COR_SIDEBAR,
    fg=COR_TEXTO,
    insertbackground=COR_TEXTO,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=COR_CARTAO_BORDA,
    highlightcolor="#4C78A8",
)
entrada_busca_global.grid(row=0, column=1, sticky="ew", ipady=8, pady=12)

def executar_busca_global():
    termo = entrada_busca_global.get().strip()
    abrir_busca_global(janela, termo)

btn_busca_global = tk.Button(
    frame_busca,
    text="Pesquisar",
    command=executar_busca_global,
    font=(FONTE, 9, "bold"),
    bg=COR_BOTAO,
    fg=COR_TEXTO,
    activebackground=COR_BOTAO_HOVER,
    activeforeground=COR_TEXTO,
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=16,
    pady=8,
)
btn_busca_global.grid(row=0, column=2, padx=(12, 22), pady=12)
adicionar_hover(btn_busca_global)

entrada_busca_global.bind("<Return>", lambda _evento: executar_busca_global())

tk.Label(
    frame_busca,
    text="Pesquise por nome, apartamento, documento, empresa ou telefone.",
    font=(FONTE, 8),
    bg=COR_CARTAO,
    fg=COR_TEXTO_2,
).grid(row=1, column=1, columnspan=2, sticky="w", pady=(0, 12))


# ==========================================================
# AÇÕES RÁPIDAS
# ==========================================================

frame_acoes = tk.Frame(
    painel,
    bg=COR_CARTAO,
    highlightthickness=1,
    highlightbackground=COR_CARTAO_BORDA,
)
frame_acoes.grid(row=3, column=0, columnspan=4, sticky="nsew", pady=(22, 0))
frame_acoes.grid_columnconfigure(0, weight=1)
frame_acoes.grid_columnconfigure(1, weight=1)
frame_acoes.grid_columnconfigure(2, weight=1)

cab_acoes = tk.Frame(frame_acoes, bg=COR_CARTAO)
cab_acoes.grid(row=0, column=0, columnspan=3, sticky="ew", padx=22, pady=(20, 10))

tk.Label(
    cab_acoes,
    text="Ações rápidas",
    font=(FONTE, 14, "bold"),
    bg=COR_CARTAO,
    fg=COR_TEXTO,
).pack(anchor="w")

tk.Label(
    cab_acoes,
    text="Atalhos para as tarefas mais usadas durante o atendimento.",
    font=(FONTE, 9),
    bg=COR_CARTAO,
    fg=COR_TEXTO_2,
).pack(anchor="w", pady=(3, 0))


def criar_acao_rapida(coluna, titulo, descricao, comando, principal=False):
    cor = COR_DESTAQUE if principal else COR_BOTAO
    hover = "#B71C1C" if principal else COR_BOTAO_HOVER

    caixa = tk.Frame(frame_acoes, bg=COR_CARTAO)
    caixa.grid(row=1, column=coluna, sticky="nsew", padx=22, pady=(8, 24))

    botao = tk.Button(
        caixa,
        text=titulo,
        command=comando,
        font=(FONTE, 11, "bold"),
        bg=cor,
        fg=COR_TEXTO,
        activebackground=hover,
        activeforeground=COR_TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        pady=13,
    )
    botao.pack(fill="x")
    adicionar_hover(botao, cor, hover)

    tk.Label(
        caixa,
        text=descricao,
        font=(FONTE, 9),
        bg=COR_CARTAO,
        fg=COR_TEXTO_2,
        justify="left",
        wraplength=260,
    ).pack(anchor="w", pady=(8, 0))


criar_acao_rapida(
    0,
    "+  Novo morador",
    "Cadastre rapidamente um novo morador ou residente.",
    lambda: abrir_e_atualizar(abrir_moradores),
)

criar_acao_rapida(
    1,
    "+  Novo prestador",
    "Registre os dados de um prestador antes de liberar o acesso.",
    lambda: abrir_e_atualizar(abrir_prestadores),
)

criar_acao_rapida(
    2,
    "→  Registrar entrada",
    "Registre uma entrada e acompanhe os acessos ativos.",
    lambda: (
        abrir_registro_entrada(janela, operador_atual),
        janela.after(300, atualizar_dashboard)
    ),
    principal=True,
)


# ==========================================================
# STATUS DO SISTEMA
# ==========================================================

frame_status = tk.Frame(painel, bg=COR_FUNDO)
frame_status.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(18, 0))
frame_status.grid_columnconfigure(0, weight=1)

lbl_status = tk.Label(
    frame_status,
    text="● Sistema operacional",
    font=(FONTE, 9, "bold"),
    bg=COR_FUNDO,
    fg="#66BB6A",
)
lbl_status.grid(row=0, column=0, sticky="w")

lbl_ultima_atualizacao = tk.Label(
    frame_status,
    text="",
    font=(FONTE, 9),
    bg=COR_FUNDO,
    fg=COR_TEXTO_2,
)
lbl_ultima_atualizacao.grid(row=0, column=1, sticky="e")


# ==========================================================
# ATUALIZAÇÃO DO PAINEL
# ==========================================================

def atualizar_dashboard():
    try:
        totais = {
            "moradores": len(listar_moradores()),
            "visitantes": len(listar_visitantes()),
            "prestadores": len(listar_prestadores()),
            "acessos": len(listar_acessos_ativos()),
        }

        for chave, valor in totais.items():
            labels_contadores[chave].config(text=str(valor))

        lbl_status.config(text="● Sistema operacional", fg="#66BB6A")
        lbl_ultima_atualizacao.config(
            text=f"Atualizado às {datetime.now().strftime('%H:%M:%S')}"
        )

    except Exception as erro:
        lbl_status.config(text="● Falha ao atualizar painel", fg="#EF5350")
        lbl_ultima_atualizacao.config(text=str(erro)[:70])


def atualizar_relogio():
    agora = datetime.now()
    lbl_data.config(text=agora.strftime("%d/%m/%Y"))
    lbl_hora.config(text=agora.strftime("%H:%M:%S"))
    janela.after(1000, atualizar_relogio)


def atualizacao_automatica():
    atualizar_dashboard()
    janela.after(5000, atualizacao_automatica)


# ==========================================================
# INICIAR SISTEMA
# ==========================================================

atualizar_relogio()
atualizar_dashboard()
janela.after(5000, atualizacao_automatica)
janela.mainloop()