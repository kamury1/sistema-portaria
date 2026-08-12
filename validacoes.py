import re


def normalizar_texto(valor):
    """Remove espaços duplicados e espaços no início/fim."""
    return " ".join(str(valor or "").strip().split())


def normalizar_documento(valor):
    """
    Mantém a forma digitada para exibição, mas permite comparar
    documentos ignorando pontos, traços, barras, espaços e maiúsculas.
    """
    return normalizar_texto(valor)


def chave_documento(valor):
    return re.sub(r"[^0-9A-Za-z]", "", str(valor or "")).upper()


def validar_nome(nome):
    nome = normalizar_texto(nome)

    if not nome:
        return False, "Informe o nome."

    if len(nome) < 2:
        return False, "O nome está muito curto."

    if len(nome) > 100:
        return False, "O nome está muito longo."

    return True, nome


def validar_apartamento(apartamento):
    apartamento = normalizar_texto(apartamento)

    if not apartamento:
        return False, "Informe o apartamento."

    if len(apartamento) > 20:
        return False, "O apartamento informado está muito longo."

    return True, apartamento


def validar_vagas(vagas):
    vagas = normalizar_texto(vagas)

    if not vagas:
        return True, ""

    # Aceita formatos simples usados no dia a dia: 12, 12/13, A12, G2-15 etc.
    if len(vagas) > 30:
        return False, "O campo de vaga está muito longo."

    if not re.fullmatch(r"[0-9A-Za-zÀ-ÿ /.,#_-]+", vagas):
        return False, "A vaga contém caracteres inválidos."

    return True, vagas


def validar_documento(documento):
    documento = normalizar_documento(documento)
    chave = chave_documento(documento)

    if not documento:
        return False, "Informe o documento."

    if len(chave) < 4:
        return False, "O documento informado está muito curto."

    if len(documento) > 40:
        return False, "O documento informado está muito longo."

    return True, documento


def validar_telefone(telefone):
    telefone = normalizar_texto(telefone)

    if not telefone:
        return True, ""

    numeros = re.sub(r"\D", "", telefone)

    # Validação propositalmente flexível: aceita telefone fixo/celular
    # com ou sem DDD, sem bloquear formatos usuais da portaria.
    if len(numeros) < 8 or len(numeros) > 13:
        return False, "Informe um telefone válido (8 a 13 números)."

    if len(telefone) > 30:
        return False, "O telefone informado está muito longo."

    return True, telefone


def documento_duplicado(documento, registros, indice_documento, id_ignorar=None):
    """
    registros: lista de tuplas vindas do banco.
    indice_documento: posição do documento na tupla.
    id_ignorar: usado na edição para não comparar o registro com ele mesmo.
    """
    chave = chave_documento(documento)

    if not chave:
        return False

    for registro in registros:
        if id_ignorar is not None and registro[0] == id_ignorar:
            continue

        if chave_documento(registro[indice_documento]) == chave:
            return True

    return False
