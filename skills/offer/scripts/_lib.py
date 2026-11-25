"""Funcoes compartilhadas pelos scripts da skill oferta-irresistivel.

So biblioteca padrao. Nada aqui acessa a rede.
"""
import csv
import json
import re
import sys
import unicodedata

DESCONHECIDO = "desconhecido"

COLUNAS = [
    "id",            # u01 para o usuario, c01, c02... para concorrentes, g01... para guias de preco
    "negocio",       # nome do negocio
    "tipo",          # usuario | concorrente | guia
    "servico",       # nome padronizado do servico (igual entre linhas comparaveis)
    "pacote",        # nome do pacote/plano como o negocio chama
    "preco_texto",   # texto exato da fonte, ou "desconhecido"
    "preco_tipo",    # fixo | a_partir_de | faixa | desconhecido
    "preco_valor",   # numero (ex.: 1500.00) ou "min-max" para faixa; vazio se desconhecido
    "unidade",       # mensal | anual | por_sessao | por_hora | por_procedimento | por_unidade | unico | outro:<texto>
    "inclui",        # o que o pacote inclui, itens separados por " | "
    "garantia_texto",  # texto exato da fonte, ou "nenhuma publicada"
    "bonus",
    "prova",         # prova social publica (numeros, depoimentos, anos), resumida
    "fonte_url",     # pagina onde o preco/garantia aparece
    "fonte_arquivo", # captura(s) em sources/, separadas por ";"
    "evidencia_tipo",  # site | checkout | diretorio | avaliacao | guia | informado_pelo_dono
    "coletado_em",   # AAAA-MM-DD
    "observacoes",
]

TIPOS = {"usuario", "concorrente", "guia"}
PRECO_TIPOS = {"fixo", "a_partir_de", "faixa", DESCONHECIDO}
UNIDADES = {
    "mensal", "anual", "por_sessao", "por_hora", "por_procedimento",
    "por_unidade", "unico",
}
EVIDENCIAS = {"site", "checkout", "diretorio", "avaliacao", "guia", "informado_pelo_dono"}

NUM_RE = re.compile(r"\d[\d.,]*\d|\d")


def setup_stdout():
    """Windows costuma usar cp1252 no terminal; forca UTF-8 para nao quebrar acentos."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def ler_ofertas(caminho):
    """Le offers.csv e devolve (linhas, erros_de_estrutura)."""
    erros = []
    with open(caminho, "r", encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f)
        cabecalho = leitor.fieldnames or []
        faltando = [c for c in COLUNAS if c not in cabecalho]
        if faltando:
            erros.append("colunas ausentes no CSV: " + ", ".join(faltando))
        linhas = []
        for n, bruta in enumerate(leitor, start=2):
            if bruta.get(None):
                erros.append(f"linha {n} tem mais colunas que o cabecalho. Quase sempre e uma virgula "
                             "dentro de um campo (ex.: nota 4,8): ponha o campo entre aspas duplas")
            linha = {k: (v or "").strip() for k, v in bruta.items() if k}
            if not any(linha.values()):
                continue
            linha["_linha"] = n
            linhas.append(linha)
    return linhas, erros


def ler_json(caminho):
    with open(caminho, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def sem_acento(texto):
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def chave(texto):
    """Minusculas, sem acento, espacos simples. Para comparar nomes e frases."""
    return re.sub(r"\s+", " ", sem_acento(texto).casefold()).strip()


def compacto(texto):
    """Forma usada para conferir citacao palavra por palavra.

    Mantem todas as letras, numeros e pontuacao na ordem original. Ignora so
    diferencas que o HTML introduz: maiusculas, tipo de espaco e quebras.
    """
    texto = unicodedata.normalize("NFKC", texto)
    return re.sub(r"\s+", "", texto).casefold()


def parse_numero(token):
    """Converte '1.500,00', '1,500.00', '29,90', '1.500' ou '97' em float."""
    t = token.strip().strip(".,")
    if not t:
        return None
    if "." in t and "," in t:
        if t.rfind(",") > t.rfind("."):
            t = t.replace(".", "").replace(",", ".")
        else:
            t = t.replace(",", "")
    elif "," in t:
        if re.fullmatch(r"\d{1,3}(,\d{3})+", t):
            t = t.replace(",", "")
        else:
            t = t.replace(",", ".")
    elif "." in t:
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", t):
            t = t.replace(".", "")
    try:
        return float(t)
    except ValueError:
        return None


def numeros_em(texto):
    """Lista de floats presentes em um texto."""
    achados = []
    for m in NUM_RE.finditer(texto):
        v = parse_numero(m.group(0))
        if v is not None:
            achados.append(v)
    return achados


def igual(a, b):
    return abs(a - b) < 0.005


def contem_valor(valor, lista):
    return any(igual(valor, x) for x in lista)


def fmt_brl(valor):
    inteiro, frac = f"{valor:,.2f}".split(".")
    return "R$ " + inteiro.replace(",", ".") + "," + frac


def valor_da_linha(linha):
    """Devolve (minimo, maximo) numericos da linha, ou None se nao ha preco."""
    bruto = linha.get("preco_valor", "")
    if not bruto or linha.get("preco_tipo") == DESCONHECIDO:
        return None
    if linha.get("preco_tipo") == "faixa":
        partes = re.split(r"\s*-\s*", bruto)
        if len(partes) != 2:
            return None
        try:
            a, b = float(partes[0]), float(partes[1])
        except ValueError:
            return None
        return (min(a, b), max(a, b))
    try:
        v = float(bruto)
    except ValueError:
        return None
    return (v, v)
