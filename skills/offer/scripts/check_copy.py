#!/usr/bin/env python3
"""Recusa copy que promete algo que o dono nao aprovou.

Uso:
  python check_copy.py --facts offer-out/<nome>/facts.json --offers offer-out/<nome>/offers.csv \
      offer-out/<nome>/offer-novo.md offer-out/<nome>/pagina-de-oferta.md offer-out/<nome>/pitch.txt

O que reprova:
  NUMERO      numero (preco, prazo, percentual, quantidade) que nao esta em facts.json,
              ou que esta la com outro sentido ("60 dias" no fato, "60 clinicas" na copy)
  GARANTIA    linguagem de garantia sem garantia aprovada; promessa de devolucao ou de
              resultado garantido que o texto aprovado da garantia nao contem
  URGENCIA    escassez ou prazo que nao corresponde a urgencia real registrada
  SUPERLATIVO "o melhor", "numero 1", "lider" etc. sem comprovacao registrada
  CONCORRENTE nome de concorrente citado na copy
  PENDENTE    marcador de template que ficou sem preencher

Codigos de saida: 0 limpo, 1 com reprovacoes, 2 facts.json ainda nao aprovado pelo dono.

Quando reprovar: reescreva a frase ou pergunte ao dono. Nunca acrescente um fato
a facts.json so para o script passar.

Limite conhecido: o script confere se o fato existe e se o numero aparece perto da
mesma palavra. Ele nao entende a frase. Promessa vaga sem numero ("resultados em
poucos dias") passa. Sempre releia a copy com facts.json ao lado.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _lib  # noqa: E402

CHAVES_IGNORADAS = {"aprovado_em", "site", "instagram", "checkout", "origem", "fonte", "idioma"}

UNIDADES_NUM = {
    "um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "quatro": 4, "cinco": 5,
    "seis": 6, "sete": 7, "oito": 8, "nove": 9,
}
DEZENAS_NUM = {
    "vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50, "sessenta": 60,
    "setenta": 70, "oitenta": 80, "noventa": 90,
}
PALAVRAS_NUMERO = dict(UNIDADES_NUM)
PALAVRAS_NUMERO.update(DEZENAS_NUM)
PALAVRAS_NUMERO.update({
    "dez": 10, "onze": 11, "doze": 12, "treze": 13, "quatorze": 14, "catorze": 14,
    "quinze": 15, "cem": 100, "duzentos": 200, "duzentas": 200, "quinhentos": 500,
    "quinhentas": 500, "mil": 1000,
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "twelve": 12, "fourteen": 14, "fifteen": 15,
    "twenty": 20, "thirty": 30, "sixty": 60, "ninety": 90, "hundred": 100, "thousand": 1000,
})
ARTIGOS = {"um", "uma", "one"}
UNID_TEMPO = r"dias?|semanas?|mes(?:es)?|anos?|horas?|minutos?|days?|weeks?|months?|years?|hours?"
UNID_OUTRAS = (r"vagas?|clientes?|alunos?|alunas?|pacientes?|pessoas?|empresas?|clinicas?|vezes|parcelas?|"
               r"por cento|sessoes|sessao|aulas?|modulos?|encontros?|bonus|pedidos?|avaliacoes|avaliacao|"
               r"leads?|vendas?|contatos?|reais|spots?|clients?|students?|sessions?|lessons?|times|"
               r"orders?|reviews?|sales")
_ALT_NUM = "|".join(sorted(PALAVRAS_NUMERO, key=len, reverse=True))
PALAVRA_RE = re.compile(
    r"\b(" + _ALT_NUM + r")\s+(?:primeir[oa]s?\s+|proxim[oa]s?\s+|nov[oa]s?\s+)?("
    + UNID_TEMPO + "|" + UNID_OUTRAS + r")\b")
COMPOSTO_RE = re.compile(r"\b(" + "|".join(DEZENAS_NUM) + r") e (" + "|".join(UNIDADES_NUM) + r")\b")
TEMPO_RE = re.compile(r"^(?:" + UNID_TEMPO + r")$")

MULTIPLICADORES = ["dobro", "dobrar", "dobre", "triplo", "triplicar", "triplique", "metade",
                   "double", "triple", "half the"]

GARANTIA_RE = re.compile(
    r"\bgarant\w*|\breembols\w*|dinheiro de volta|"
    r"\bdevolv\w+ (?:\w+ ){0,3}(?:dinheiro|valor|investimento|pagamento)|"
    r"risco zero|\bsem risco\b|\bpor (?:minha|nossa) conta\b|\bnao (?:paga|cobr\w+)\b|"
    r"\b(?:trabalh\w+|continu\w+) (?:\w+ ){0,3}(?:de graca|sem cobrar|sem custo)\b|"
    r"\bguarantee\w*|\brefund\w*|money[- ]back|risk[- ]free|\bon (?:me|us)\b")
# Promessas especificas: so passam se o texto aprovado da garantia tiver a mesma ideia.
FAMILIAS_GARANTIA = [
    ("devolucao de dinheiro", re.compile(r"reembols|dinheiro de volta|devolv|refund|money[- ]back")),
    ("ausencia de risco", re.compile(r"risco zero|sem risco|risk[- ]free")),
    ("satisfacao garantida", re.compile(r"satisfacao garantida|satisfaction guaranteed")),
    ("trabalho sem cobrar", re.compile(r"por (?:minha|nossa) conta|nao (?:paga|cobr)|de graca|sem cobrar|sem custo|on (?:me|us)")),
]
RESULTADO_GARANTIDO_RE = re.compile(
    r"resultados? garantidos?|garantia de resultados?|garantimos (?:\w+ ){0,2}resultados?|"
    r"guaranteed results?|results? guaranteed")
URGENCIA_RE = re.compile(
    r"\bultim[oa]s? (?:vagas?|unidades?|dias?|horas?|chances?|turmas?)|vagas? limitadas?|"
    r"\b(?:so|somente|apenas) hoje\b|tempo limitado|\bacaba (?:hoje|amanha|em|logo)\b|"
    r"\bencerra\w*\b|enquanto durar\w*|\brestam\b|\bcorra\b|nao perca|\bantes que acabe\b|"
    r"\boferta relampago\b|\b(?:so|apenas|somente) \w+ vagas?\b|"
    r"\bvagas? (?:\w+ ){0,2}por (?:mes|semana|turma)\b|only \w+ (?:spots?|seats?)|"
    r"last (?:spots?|chance|seats?)|limited[- ]time|limited spots?|"
    r"\bends (?:today|soon|tonight)\b|\bhurry\b|only \w+ left|don'?t miss")
_LUGAR = r"(?:brasil|mercado|cidade|regiao|mundo|pais|estado)"
SUPERLATIVO_RE = re.compile(
    r"\b[oa]s? melhor(?:es)?\b|\bmelhor(?:es)? (?:\w+ ){1,6}d[oae]s? " + _LUGAR + r"\b|"
    r"\bnumero (?:1|um)\b|\bn[o.]? ?1\b|#\s?1\b|\blider(?:es)?\b|"
    r"\b[oa]s? maior(?:es)?\b|\b[oa]s? unic[oa]s?\b|\bimbative\w*|\bincompara\w*|\bsem igual\b|"
    r"\binsuperave\w*|\b[oa]s? mais \w+ d[oae]s? " + _LUGAR + r"\b|"
    r"\bthe best\b|\bbest (?:\w+ ){1,4}in (?:the )?(?:world|country|city|market|town)\b|"
    r"\bnumber one\b|\bworld[- ]class\b|\bunbeatable\b|\bunmatched\b|"
    r"\bthe (?:leading|only|top|largest|biggest)\b")
PENDENTE_RE = re.compile(
    r"\{\{[^}]*\}\}|\[PREENCHER[^\]]*\]|\bTODO\b|\bXX+\b|\ba (?:definir|confirmar|combinar)\b", re.I)
NEGACAO_RE = re.compile(r"\b(?:nao|sem|nem|nunca|not|no|never|without)\b[^.;!?]{0,30}$")

URL_RE = re.compile(r"https?://\S+|www\.\S+")
# marcas de tempo de roteiro ("[0-3s]") e a duracao do formato ("Reels de 30s") nao sao promessa
TEMPO_ROTEIRO_RE = re.compile(
    r"\[\s*\d+(?:\s*[-a]\s*\d+)?\s*s\s*\]|\b(?:reels?|video|roteiro|stories?)\s+de\s+\d+\s?(?:s|seg|segundos)\b",
    re.I)
ITEM_LISTA_RE = re.compile(r"^(\s*)\d+[.)]\s")
COMENTARIO_RE = re.compile(r"<!--.*?-->", re.S)

# numero + ate tres palavras seguintes, para saber "numero de que"
NUM_CTX_RE = re.compile(
    r"(r\$\s*)?(\d[\d.,]*\d|\d)\s*(%)?((?:\s*[^\W\d_]+){0,3})", re.I)
VAZIAS = {"de", "da", "do", "das", "dos", "em", "na", "no", "nas", "nos", "por", "para", "pra",
          "com", "sem", "que", "ate", "ou", "a", "o", "e", "as", "os", "ao", "um", "uma", "se",
          "the", "of", "in", "on", "for", "to", "and", "or", "per", "at", "with",
          "primeiro", "primeira", "primeiros", "primeiras", "proximo", "proxima", "proximos",
          "proximas", "novo", "nova", "novos", "novas", "mais", "menos", "cada", "sua", "seu"}


def contexto_do_numero(m):
    """Devolve (valor, radical_da_palavra_seguinte, e_moeda)."""
    valor = _lib.parse_numero(m.group(2))
    if m.group(3):
        return valor, "%", bool(m.group(1))
    radical = ""
    for w in (m.group(4) or "").split():
        if w in VAZIAS or len(w) < 3:
            if w == "x":
                radical = "x"
                break
            continue
        radical = w[:4]
        break
    return valor, radical, bool(m.group(1))


class Fatos:
    """Indice do que o dono aprovou: numeros, em que frase aparecem e textos."""

    def __init__(self):
        self.numeros = []        # todos os valores numericos
        self.moedas = []         # valores que aparecem como R$
        self.frases = []         # (valores_da_frase, texto_normalizado)
        self.soltos = []         # valores vindos de campos numericos (sem frase)
        self.textos = []

    def carregar(self, no):
        if isinstance(no, dict):
            for k, v in no.items():
                if str(k).startswith("_") or k in CHAVES_IGNORADAS:
                    continue
                self.carregar(v)
        elif isinstance(no, list):
            for v in no:
                self.carregar(v)
        elif isinstance(no, bool) or no is None:
            return
        elif isinstance(no, (int, float)):
            self.numeros.append(float(no))
            self.soltos.append(float(no))
        elif isinstance(no, str):
            norm = _lib.chave(no)
            vals = []
            for m in NUM_CTX_RE.finditer(norm):
                v, _, moeda = contexto_do_numero(m)
                if v is None:
                    continue
                vals.append(v)
                if moeda:
                    self.moedas.append(v)
            for m in PALAVRA_RE.finditer(norm):
                vals.append(float(PALAVRAS_NUMERO[m.group(1)]))
            for m in COMPOSTO_RE.finditer(norm):
                vals.append(float(DEZENAS_NUM[m.group(1)] + UNIDADES_NUM[m.group(2)]))
            self.numeros.extend(vals)
            self.frases.append((vals, norm))
            self.textos.append(norm)

    def tem(self, valor):
        return _lib.contem_valor(valor, self.numeros)

    def tem_com_sentido(self, valor, radical):
        if _lib.contem_valor(valor, self.soltos):
            return True
        for vals, texto in self.frases:
            if _lib.contem_valor(valor, vals):
                if radical == "%":
                    if re.search(r"\d\s*%", texto):
                        return True
                elif re.search(r"(?<![^\W\d_])" + re.escape(radical), texto):
                    return True
        return False

    def onde(self, valor):
        for vals, texto in self.frases:
            if _lib.contem_valor(valor, vals):
                return texto[:70]
        return ""


def nomes_de_concorrentes(caminho_csv, fatos):
    nomes = set()
    if caminho_csv and os.path.isfile(caminho_csv):
        linhas, _ = _lib.ler_ofertas(caminho_csv)
        for l in linhas:
            if l.get("tipo") == "concorrente" and l.get("negocio"):
                nomes.add(l["negocio"])
    for extra in fatos.get("concorrentes", []) or []:
        if isinstance(extra, str):
            nomes.add(extra)
    alvos = set()
    for n in nomes:
        k = _lib.chave(n)
        if len(k) >= 4:
            alvos.add((n, k))
        # apelido com digito costuma ser a marca ("V4" em "V4 Company")
        primeira = k.split(" ")[0] if k else ""
        if len(primeira) >= 2 and re.search(r"\d", primeira) and re.search(r"[a-z]", primeira):
            alvos.add((n, primeira))
    return sorted(alvos)


def limpar(texto):
    """Tira comentarios HTML (o comprador nao le), preservando a contagem de linhas."""
    return COMENTARIO_RE.sub(lambda m: "\n" * m.group(0).count("\n"), texto)


def conferir_arquivo(caminho, idx, fatos, concorrentes):
    with open(caminho, "r", encoding="utf-8-sig") as f:
        bruto = limpar(f.read())
    achados = []
    garantia = fatos.get("garantia") or {}
    garantia_ok = garantia.get("aprovada") is True
    por_resultado = _lib.chave(str(garantia.get("tipo", ""))) in ("por_resultado", "por resultado")
    texto_garantia = _lib.chave(" ".join(str(garantia.get(k, "")) for k in ("texto", "condicoes", "como_acionar")))
    urgencia = fatos.get("urgencia") or {}
    urgencia_ok = urgencia.get("real") is True
    texto_urgencia = _lib.chave(" ".join([
        str(urgencia.get("texto", "")), str(urgencia.get("motivo", "")),
        str((fatos.get("capacidade") or {}).get("limite_real", ""))]))
    superl_ok = []
    for s in fatos.get("superlativos_comprovados", []) or []:
        superl_ok.append(_lib.chave(s.get("texto", "") if isinstance(s, dict) else str(s)))
    blob = " \n ".join(idx.textos)

    for n, original in enumerate(bruto.splitlines(), start=1):
        linha = URL_RE.sub(" ", original)
        linha = TEMPO_ROTEIRO_RE.sub(" ", linha)
        linha = ITEM_LISTA_RE.sub(r"\1", linha)
        if not linha.strip():
            continue
        norm = _lib.chave(linha)

        for m in PENDENTE_RE.finditer(linha):
            achados.append((n, "PENDENTE", m.group(0), "marcador de template sem preencher"))

        for m in NUM_CTX_RE.finditer(norm):
            valor, radical, moeda = contexto_do_numero(m)
            if valor is None:
                continue
            trecho = m.group(0).strip()
            if not idx.tem(valor):
                achados.append((n, "NUMERO", trecho, "este numero nao esta em facts.json"))
            elif moeda and not (_lib.contem_valor(valor, idx.moedas) or _lib.contem_valor(valor, idx.soltos)):
                achados.append((n, "NUMERO", trecho,
                                "valor em reais que nao aparece como valor em reais em facts.json"))
            elif radical and not moeda and not idx.tem_com_sentido(valor, radical):
                achados.append((n, "NUMERO", trecho,
                                f"o numero existe em facts.json, mas com outro sentido (la: \"{idx.onde(valor)}\")"))
        for m in COMPOSTO_RE.finditer(norm):
            v = float(DEZENAS_NUM[m.group(1)] + UNIDADES_NUM[m.group(2)])
            if not idx.tem(v):
                achados.append((n, "NUMERO", m.group(0), "numero por extenso que nao esta em facts.json"))
        for m in PALAVRA_RE.finditer(norm):
            palavra, unidade = m.group(1), m.group(2)
            if palavra in ARTIGOS and not TEMPO_RE.match(unidade):
                continue
            v = float(PALAVRAS_NUMERO[palavra])
            if not idx.tem(v):
                achados.append((n, "NUMERO", m.group(0),
                                "quantidade ou prazo por extenso que nao esta em facts.json"))
            elif not idx.tem_com_sentido(v, unidade[:4]):
                achados.append((n, "NUMERO", m.group(0),
                                f"o numero existe em facts.json, mas com outro sentido (la: \"{idx.onde(v)}\")"))
        for termo in MULTIPLICADORES:
            if re.search(r"\b" + re.escape(termo) + r"\b", norm) and termo not in blob:
                achados.append((n, "NUMERO", termo, "promessa de proporcao que nao esta em facts.json"))

        for m in GARANTIA_RE.finditer(norm):
            if not garantia_ok:
                achados.append((n, "GARANTIA", m.group(0),
                                "o dono nao aprovou nenhuma garantia (facts.json: garantia.aprovada)"))
                continue
            for nome, familia in FAMILIAS_GARANTIA:
                if familia.search(m.group(0)) and not familia.search(texto_garantia):
                    achados.append((n, "GARANTIA", m.group(0),
                                    f"promete {nome}, e o texto aprovado da garantia nao diz isso"))
        if garantia_ok and not por_resultado:
            for m in RESULTADO_GARANTIDO_RE.finditer(norm):
                if NEGACAO_RE.search(norm[:m.start()]):
                    continue  # "nao e garantia de resultado" e esclarecimento, nao promessa
                achados.append((n, "GARANTIA", m.group(0),
                                "a garantia aprovada nao e por resultado; nao prometa resultado garantido"))

        for m in URGENCIA_RE.finditer(norm):
            if not urgencia_ok:
                achados.append((n, "URGENCIA", m.group(0),
                                "nao ha limite ou data real registrada (facts.json: urgencia.real)"))
            elif m.group(0) not in texto_urgencia:
                achados.append((n, "URGENCIA", m.group(0),
                                "esta frase de escassez nao esta no texto de urgencia aprovado; "
                                "use as palavras de facts.json (urgencia.texto)"))

        for m in SUPERLATIVO_RE.finditer(norm):
            if not any(m.group(0) in ok for ok in superl_ok):
                achados.append((n, "SUPERLATIVO", m.group(0),
                                "superlativo sem comprovacao em facts.json (superlativos_comprovados)"))

        for nome, alvo in concorrentes:
            if re.search(r"(?<!\w)" + re.escape(alvo) + r"(?!\w)", norm):
                achados.append((n, "CONCORRENTE", nome, "a copy nao cita concorrentes pelo nome"))
    # uma ocorrencia por (linha, tipo, trecho)
    vistos, unicos = set(), []
    for a in achados:
        if a[:3] not in vistos:
            vistos.add(a[:3])
            unicos.append(a)
    return unicos


def main():
    _lib.setup_stdout()
    ap = argparse.ArgumentParser(description="Confere a copy contra os fatos aprovados pelo dono.")
    ap.add_argument("arquivos", nargs="+", help="arquivos de copy (.md, .txt)")
    ap.add_argument("--facts", required=True, help="facts.json aprovado pelo dono")
    ap.add_argument("--offers", help="offers.csv, para saber os nomes dos concorrentes")
    args = ap.parse_args()

    fatos = _lib.ler_json(args.facts)
    if fatos.get("aprovado_pelo_dono") is not True:
        print("PARADO: facts.json ainda nao foi aprovado pelo dono (aprovado_pelo_dono: true).")
        print("Mostre os fatos ao dono, corrija o que ele pedir e so entao marque como aprovado.")
        return 2

    # Garantia nao aprovada e urgencia nao real nao contam como fato: o que estiver
    # rascunhado nesses campos nao libera numero nem frase na copy.
    validos = dict(fatos)
    garantia = fatos.get("garantia") or {}
    if garantia.get("aprovada") is not True:
        validos.pop("garantia", None)
    elif not str(garantia.get("como_acionar", "")).strip():
        print("aviso: a garantia foi aprovada sem 'como_acionar'. Pergunte ao dono como o cliente pede.")
    if (fatos.get("urgencia") or {}).get("real") is not True:
        validos.pop("urgencia", None)
    idx = Fatos()
    idx.carregar(validos)
    concorrentes = nomes_de_concorrentes(args.offers, fatos)
    if not args.offers:
        print("aviso: sem --offers, o script nao sabe os nomes dos concorrentes.")

    total = 0
    for caminho in args.arquivos:
        if not os.path.isfile(caminho):
            print(f"REPROVADO {caminho}: arquivo nao encontrado")
            total += 1
            continue
        achados = conferir_arquivo(caminho, idx, fatos, concorrentes)
        if not achados:
            print(f"LIMPO     {caminho}")
            continue
        print(f"REPROVADO {caminho}: {len(achados)} problema(s)")
        for n, tipo, trecho, motivo in achados:
            print(f"    linha {n} [{tipo}] \"{trecho}\": {motivo}")
        total += len(achados)

    print()
    if total:
        print(f"{total} problema(s). Reescreva a frase sem a promessa, ou pergunte ao dono se o fato e "
              "verdadeiro e ele aprova. Nao acrescente nada a facts.json por conta propria.")
        return 1
    print("Copy limpa: todo numero, garantia, prazo e limite esta em facts.json; "
          "nenhum superlativo sem prova; nenhum concorrente citado.")
    print("Lembrete: o script nao entende a frase. Promessa vaga sem numero passa. "
          "Releia a copy com facts.json ao lado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
