#!/usr/bin/env python3
"""Mostra onde o preço do usuário fica entre os preços publicados dos concorrentes.

Uso:
  python price_position.py offer-out/<nome>/offers.csv
  python price_position.py offer-out/<nome>/offers.csv --out offer-out/<nome>/price-position.md

Regras embutidas:
  - Só compara preços do mesmo serviço e da mesma unidade (mensal com mensal).
  - Preço "desconhecido" nunca entra na conta, mas é sempre contado e mostrado.
  - Faixas ficam listadas à parte, com a fonte, e não entram em mínimo/mediana/máximo.
  - Com menos de 3 concorrentes publicando preço na mesma unidade, o script não
    calcula mediana nem posição: lista os preços e diz que não há base.

Rode check_prices.py antes: este script confia que os preços já foram conferidos.
"""
import argparse
import os
import statistics
import sys
from collections import OrderedDict, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _lib  # noqa: E402

MINIMO_PARA_SUGERIR = 3

LEMBRETES = [
    "O preço acompanha o valor: antes de mexer no número, fortaleça o que a oferta entrega e prova.",
    "Se for subir, teste com clientes novos por um período definido em vez de dar um salto para todos.",
    "Ser o mais barato é uma escolha, e ela tem custo: margem menor, menos folga para entregar bem e clientes que trocam por qualquer desconto.",
    "Esta tabela só enxerga preço publicado. Quem negocia por orçamento ou WhatsApp está fora da conta.",
    "Pacotes com escopo diferente (mais ou menos itens, promoção, preço \"a partir de\") estão na mesma conta. Olhe a tabela antes de tirar conclusão do número.",
]


def analisar(linhas):
    por_servico = OrderedDict()
    for l in linhas:
        por_servico.setdefault(l.get("servico", ""), []).append(l)

    blocos = []
    for servico, grupo in por_servico.items():
        conc = [l for l in grupo if l.get("tipo") == "concorrente"]
        meus = [l for l in grupo if l.get("tipo") == "usuario"]
        guias = [l for l in grupo if l.get("tipo") == "guia"]

        negocios = OrderedDict((l["negocio"], None) for l in conc)
        com_preco = OrderedDict((l["negocio"], None) for l in conc
                                if l.get("preco_tipo") in ("fixo", "a_partir_de", "faixa"))
        sem_preco = [n for n in negocios if n not in com_preco]

        por_unidade = defaultdict(list)
        faixas = []
        for l in conc:
            par = _lib.valor_da_linha(l)
            if par is None:
                continue
            if l.get("preco_tipo") == "faixa":
                faixas.append(l)
            else:
                por_unidade[l.get("unidade", "")].append((par[0], l))

        unidades = []
        for unidade, itens in por_unidade.items():
            itens = sorted(itens, key=lambda x: x[0])
            valores = [v for v, _ in itens]
            quem = OrderedDict((l["negocio"], None) for _, l in itens)
            info = {
                "unidade": unidade,
                "itens": itens,
                "n_precos": len(valores),
                "n_negocios": len(quem),
                "n_a_partir_de": sum(1 for _, l in itens if l.get("preco_tipo") == "a_partir_de"),
                "min": valores[0],
                "mediana": statistics.median(valores),
                "max": valores[-1],
                "base_suficiente": len(quem) >= MINIMO_PARA_SUGERIR,
                "usuario": [],
            }
            for m in meus:
                par = _lib.valor_da_linha(m)
                if par is None or m.get("unidade") != unidade or m.get("preco_tipo") == "faixa":
                    continue
                meu = par[0]
                mais_baratos = sum(1 for v in valores if v < meu and not _lib.igual(v, meu))
                dif = (meu - info["mediana"]) / info["mediana"] * 100 if info["mediana"] else 0.0
                info["usuario"].append({
                    "pacote": m.get("pacote") or m.get("negocio"),
                    "valor": meu,
                    "posicao": mais_baratos + 1,
                    "de": len(valores) + 1,
                    "dif_mediana_pct": dif,
                    "abaixo_do_min": meu < valores[0] and not _lib.igual(meu, valores[0]),
                    "acima_do_max": meu > valores[-1] and not _lib.igual(meu, valores[-1]),
                })
            unidades.append(info)

        unidades_com_dado = {u["unidade"] for u in unidades}
        nao_comparaveis = []
        for m in meus:
            par = _lib.valor_da_linha(m)
            if par is None:
                nao_comparaveis.append((m, "seu preço não foi informado"))
            elif unidades_com_dado and m.get("unidade") not in unidades_com_dado:
                outras = ", ".join(sorted(unidades_com_dado))
                nao_comparaveis.append((m, f"seu preço é '{m.get('unidade')}', e os concorrentes "
                                           f"publicam em: {outras}. Unidades diferentes não se comparam"))

        blocos.append({
            "servico": servico,
            "n_concorrentes": len(negocios),
            "n_publicam": len(com_preco),
            "sem_preco": sem_preco,
            "unidades": unidades,
            "faixas": faixas,
            "guias": guias,
            "nao_comparaveis": nao_comparaveis,
            "meus": meus,
        })
    return blocos


def montar_md(blocos):
    out = ["# Posição de preço", ""]
    out.append("Leitura dos preços **publicados**. Nada aqui é estimado.")
    out.append("")
    for b in blocos:
        out.append(f"## {b['servico'] or '(serviço sem nome)'}")
        out.append("")
        n, p = b["n_concorrentes"], b["n_publicam"]
        out.append(f"- Concorrentes nesta rodada: **{n}**")
        out.append(f"- Publicam algum preço: **{p}**")
        out.append(f"- Não publicam preço: **{n - p}**"
                   + (f" ({', '.join(b['sem_preco'])})" if b["sem_preco"] else ""))
        out.append("")
        if not b["unidades"]:
            out.append("Nenhum concorrente publica preço fixo para este serviço. "
                       "**Não há base para sugerir movimento de preço.**")
            out.append("")
        for u in b["unidades"]:
            out.append(f"### Unidade: {u['unidade']}")
            out.append("")
            if not u["base_suficiente"]:
                out.append(f"**Base insuficiente:** só {u['n_negocios']} concorrente(s) publica(m) preço nesta "
                           f"unidade (o mínimo é {MINIMO_PARA_SUGERIR}). **Não sugira movimento de preço** "
                           "com esta amostra: um ou dois preços não representam o mercado. "
                           "Por isso não há mediana nem posição aqui, só a lista do que foi visto:")
                out.append("")
                for v, l in u["itens"]:
                    out.append(f"- {l['negocio']} ({l.get('pacote') or 'sem nome de pacote'}): "
                               f"\"{l['preco_texto']}\"")
                for m in b["meus"]:
                    par = _lib.valor_da_linha(m)
                    if par and m.get("unidade") == u["unidade"]:
                        out.append(f"- **Você ({m.get('pacote') or m.get('negocio')}): {_lib.fmt_brl(par[0])}**")
                out.append("")
                continue
            out.append("| Preços | Concorrentes | Mínimo | Mediana | Máximo |")
            out.append("|---|---|---|---|---|")
            out.append(f"| {u['n_precos']} | {u['n_negocios']} | {_lib.fmt_brl(u['min'])} | "
                       f"{_lib.fmt_brl(u['mediana'])} | {_lib.fmt_brl(u['max'])} |")
            out.append("")
            if u["n_precos"] > u["n_negocios"]:
                out.append(f"- São {u['n_precos']} preços de {u['n_negocios']} concorrentes: "
                           "quem publica mais de um pacote pesa mais na mediana.")
            if u["n_a_partir_de"]:
                out.append(f"- Preços do tipo \"a partir de\" nesta conta: {u['n_a_partir_de']}. "
                           "O valor real pode ser maior.")
            for me in u["usuario"]:
                base = (f"- **Você ({me['pacote']}): {_lib.fmt_brl(me['valor'])}**, "
                        f"{me['posicao']}º mais barato entre {me['de']} preços (os {u['n_precos']} publicados e o seu), ")
                if _lib.igual(me["dif_mediana_pct"], 0):
                    linha = base + "na mediana."
                else:
                    sinal = "acima" if me["dif_mediana_pct"] > 0 else "abaixo"
                    linha = base + f"{abs(me['dif_mediana_pct']):.0f}% {sinal} da mediana."
                if me["abaixo_do_min"]:
                    linha += " Você está abaixo do menor preço publicado."
                if me["acima_do_max"]:
                    linha += " Você está acima do maior preço publicado."
                out.append(linha)
            if not u["usuario"] and b["meus"]:
                out.append("- Seu preço não está nesta unidade, então não entra nesta comparação.")
            out.append(f"- Base: {u['n_negocios']} concorrentes publicam nesta unidade. "
                       "Dá para discutir posicionamento, com os lembretes abaixo.")
            out.append("")
        for m, motivo in b["nao_comparaveis"]:
            out.append(f"- Não comparável ({m.get('pacote') or m.get('negocio')}): {motivo}.")
        if b["nao_comparaveis"]:
            out.append("")
        if b["faixas"]:
            out.append("**Faixas com evidência (fora da mediana):**")
            out.append("")
            for l in b["faixas"]:
                out.append(f"- {l['negocio']}: \"{l['preco_texto']}\" ({l.get('unidade')}), "
                           f"fonte: {l.get('fonte_url')}")
            out.append("")
        if b["guias"]:
            out.append("**Guias de preço consultados (referência, não são concorrentes; "
                       "confira se a unidade é a mesma da sua):**")
            out.append("")
            for l in b["guias"]:
                out.append(f"- {l['negocio']}: \"{l['preco_texto']}\" ({l.get('unidade')}), "
                           f"fonte: {l.get('fonte_url')}")
            out.append("")
    out.append("## Antes de decidir qualquer preço")
    out.append("")
    for item in LEMBRETES:
        out.append(f"- {item}")
    out.append("")
    return "\n".join(out)


def main():
    _lib.setup_stdout()
    ap = argparse.ArgumentParser(description="Posição de preço por serviço e unidade.")
    ap.add_argument("csv")
    ap.add_argument("--out", help="salva o resultado em Markdown neste caminho")
    args = ap.parse_args()

    linhas, erros = _lib.ler_ofertas(args.csv)
    if erros:
        for e in erros:
            print("ERRO DE ESTRUTURA: " + e)
        return 1
    md = montar_md(analisar(linhas))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Salvo em {args.out}\n")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
