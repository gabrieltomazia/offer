#!/usr/bin/env python3
"""Valida as notas do placar e monta o ranking das ofertas.

Uso:
  python scorecard.py offer-out/<nome>/scores.json
  python scorecard.py offer-out/<nome>/scores.json --out offer-out/<nome>/placar.md

Formato de scores.json:
{
  "ofertas": [
    {
      "id": "u01", "nome": "Clareamento a laser", "tipo": "atual",
      "notas": {
        "resultado":   {"nota": 1, "motivo": "promete 'sorriso novo', sem dizer em quanto tempo"},
        "prova":       {"nota": 0, "motivo": ""},
        ...
      }
    }
  ]
}
tipo: atual | nova | concorrente. Uma nota por concorrente (use o pacote principal dele).
Em "nome", escreva só o nome: o script acrescenta "(você hoje)" e "(oferta nova)".
Os 8 critérios estão em references/criterios-do-placar.md.

Regras: nota inteira de 0 a 3; toda nota acima de 0 exige um motivo curto vindo da
evidência coletada. Sem motivo, o script recusa.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _lib  # noqa: E402

CRITERIOS = [
    ("resultado", "Resultado claro"),
    ("prova", "Prova"),
    ("velocidade", "Velocidade"),
    ("facilidade", "Facilidade"),
    ("risco", "Risco tirado do comprador"),
    ("bonus", "Bônus"),
    ("urgencia", "Urgência honesta"),
    ("clareza", "Clareza de nome, preço e conteúdo"),
]
MAXIMO = 3 * len(CRITERIOS)
MOTIVO_MIN = 8
TIPOS = {"atual", "nova", "concorrente"}
AVISO = ("Este placar é um julgamento com motivos escritos, feito a partir do que está publicado. "
         "Não é uma medição de vendas nem uma previsão de resultado.")
ROTULO_RE = re.compile(r"\s*\((?:voc[eê] hoje|oferta nova|oferta atual)\)\s*", re.I)


def validar(dados):
    erros = []
    ofertas = dados.get("ofertas")
    if not isinstance(ofertas, list) or not ofertas:
        return ["scores.json precisa de uma lista 'ofertas' com pelo menos uma oferta"]
    vistos = set()
    for o in ofertas:
        ident = o.get("id") or o.get("nome") or "?"
        if ident in vistos:
            erros.append(f"{ident}: id repetido")
        vistos.add(ident)
        if o.get("tipo") not in TIPOS:
            erros.append(f"{ident}: tipo inválido '{o.get('tipo')}' (atual, nova ou concorrente)")
        notas = o.get("notas") or {}
        for chave, rotulo in CRITERIOS:
            item = notas.get(chave)
            if not isinstance(item, dict):
                erros.append(f"{ident}: falta o critério '{chave}' ({rotulo})")
                continue
            nota = item.get("nota")
            if not isinstance(nota, int) or isinstance(nota, bool) or not 0 <= nota <= 3:
                erros.append(f"{ident}: nota de '{chave}' deve ser inteiro de 0 a 3 (veio {nota!r})")
                continue
            motivo = (item.get("motivo") or "").strip()
            if nota > 0 and len(motivo) < MOTIVO_MIN:
                erros.append(f"{ident}: nota {nota} em '{chave}' sem motivo. "
                             "Escreva o que na evidência justifica a nota, ou dê 0")
        extras = set(notas) - {c for c, _ in CRITERIOS}
        if extras:
            erros.append(f"{ident}: critérios desconhecidos: {', '.join(sorted(extras))}")
    for tipo in ("atual", "nova"):
        if sum(1 for o in ofertas if o.get("tipo") == tipo) > 1:
            erros.append(f"há mais de uma oferta do tipo '{tipo}'")
    return erros


def total(oferta):
    return sum(oferta["notas"][c]["nota"] for c, _ in CRITERIOS)


def posicao(alvo, outros):
    """Ranking de competição: empate divide a mesma posição."""
    return sum(1 for o in outros if total(o) > total(alvo)) + 1


def nome_de(o):
    return ROTULO_RE.sub(" ", str(o.get("nome") or o.get("id") or "?")).strip()


def montar_md(dados):
    ofertas = dados["ofertas"]
    conc = [o for o in ofertas if o["tipo"] == "concorrente"]
    atual = next((o for o in ofertas if o["tipo"] == "atual"), None)
    nova = next((o for o in ofertas if o["tipo"] == "nova"), None)
    campo = len(conc) + 1

    out = ["# Placar das ofertas", "", AVISO, ""]
    frases = []
    if atual:
        frases.append(f"hoje você é {posicao(atual, conc)}º de {campo}")
    if nova:
        frases.append(f"a oferta nova seria {posicao(nova, conc)}º de {campo}")
    if frases:
        out.append("**Ranking:** " + ", ".join(frases) + f" ({len(conc)} concorrente(s) avaliado(s), mais você).")
        out.append("")
    if conc and max(total(o) for o in conc) <= MAXIMO // 4:
        out.append("Atenção: os concorrentes avaliados publicam muito pouco (nenhum passa de "
                   f"{MAXIMO // 4} pontos). Ficar à frente deles no placar é fácil e diz pouco. "
                   "Compare a oferta nova com o máximo possível, não só com eles.")
        out.append("")

    ordenadas = sorted(ofertas, key=lambda o: (-total(o), o["tipo"] != "nova", nome_de(o)))
    out.append("| Posição | Oferta | " + " | ".join(r for _, r in CRITERIOS) + f" | Total (de {MAXIMO}) |")
    out.append("|" + "---|" * (len(CRITERIOS) + 3))
    for o in ordenadas:
        if o["tipo"] == "concorrente":
            pos = f"{posicao(o, [x for x in conc if x is not o] + ([atual] if atual else []))}º"
            nome = nome_de(o)
        else:
            pos = f"{posicao(o, conc)}º de {campo}"
            marca = "você hoje" if o["tipo"] == "atual" else "oferta nova"
            nome = f"**{nome_de(o)} ({marca})**"
        notas = " | ".join(str(o["notas"][c]["nota"]) for c, _ in CRITERIOS)
        out.append(f"| {pos} | {nome} | {notas} | {total(o)} |")
    out.append("")
    out.append("Como ler a coluna Posição: os concorrentes estão ordenados no cenário de hoje (eles e a sua "
               "oferta atual). A oferta nova mostra em que lugar ficaria se entrasse no lugar da atual.")
    out.append("")
    out.append("## Motivos de cada nota")
    out.append("")
    for o in ordenadas:
        out.append(f"### {nome_de(o)} ({total(o)}/{MAXIMO})")
        out.append("")
        for chave, rotulo in CRITERIOS:
            item = o["notas"][chave]
            motivo = (item.get("motivo") or "").strip() or "nada publicado que sustente nota"
            out.append(f"- {rotulo}: **{item['nota']}**. {motivo}")
        out.append("")
    return "\n".join(out)


def main():
    _lib.setup_stdout()
    ap = argparse.ArgumentParser(description="Valida notas e gera o ranking das ofertas.")
    ap.add_argument("scores")
    ap.add_argument("--out", help="salva o placar em Markdown neste caminho")
    args = ap.parse_args()

    dados = _lib.ler_json(args.scores)
    erros = validar(dados)
    if erros:
        print("PLACAR RECUSADO:")
        for e in erros:
            print("  - " + e)
        return 1
    md = montar_md(dados)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Salvo em {args.out}\n")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
