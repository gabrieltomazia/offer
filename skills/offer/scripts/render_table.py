#!/usr/bin/env python3
"""Gera offers-table.md e offers-table.html a partir de offers.csv.

Uso:
  python render_table.py offer-out/<nome>/offers.csv

Os dois arquivos saem na mesma pasta do CSV. O HTML é um arquivo único, sem
scripts e sem recursos externos: abre direto no navegador.

No CSV, escreva só o nome do negócio: o script acrescenta "(VOCÊ)" na linha do usuário.
"""
import argparse
import datetime
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _lib  # noqa: E402

COLS = [
    ("negocio", "Negócio"),
    ("servico", "Serviço"),
    ("pacote", "Pacote"),
    ("preco_texto", "Preço (texto da fonte)"),
    ("unidade", "Unidade"),
    ("inclui", "Inclui"),
    ("garantia_texto", "Garantia (texto da fonte)"),
    ("bonus", "Bônus"),
    ("prova", "Prova"),
    ("observacoes", "Observações"),
    ("fonte_url", "Fonte"),
]
ROTULO_TIPO = {"usuario": "VOCÊ", "concorrente": "", "guia": "guia de preço"}
ORDEM_TIPO = {"usuario": 0, "concorrente": 1, "guia": 2}
MARCA_RE = re.compile(r"\s*\(voc[eê]\)\s*", re.I)


def url_segura(u):
    return u if re.match(r"^https?://", u or "", re.I) else ""


def md_cel(texto):
    return (texto or "").replace("|", "/").replace("\n", " ").strip() or "-"


def ordenar(linhas):
    """Serviços do usuário primeiro; dentro do serviço, o usuário no topo."""
    meus = {l.get("servico", "") for l in linhas if l.get("tipo") == "usuario"}
    return sorted(linhas, key=lambda l: (l.get("servico", "") not in meus, l.get("servico", ""),
                                         ORDEM_TIPO.get(l.get("tipo"), 9), l.get("negocio", "")))


def nome_de(l):
    return MARCA_RE.sub(" ", l.get("negocio", "")).strip()


def sufixo_preco(l):
    tipo = l.get("preco_tipo")
    texto = _lib.chave(l.get("preco_texto", ""))
    if tipo == "a_partir_de" and "a partir" not in texto:
        return "a partir de"
    if tipo == "faixa":
        return "faixa"
    return ""


def resumo(linhas):
    conc = {l["negocio"] for l in linhas if l.get("tipo") == "concorrente"}
    com = {l["negocio"] for l in linhas if l.get("tipo") == "concorrente"
           and l.get("preco_tipo") not in ("", _lib.DESCONHECIDO)}
    return len(conc), len(com)


def montar_md(linhas):
    n, com = resumo(linhas)
    out = ["# Tabela de ofertas", ""]
    out.append(f"{n} concorrentes encontrados nesta rodada (não são todos os que existem). "
               f"{com} publicam preço, {n - com} não publicam.")
    out.append("")
    out.append("`desconhecido` significa que a página não publica preço. Nenhum valor foi estimado.")
    out.append("")
    out.append("| " + " | ".join(r for _, r in COLS) + " |")
    out.append("|" + "---|" * len(COLS))
    for l in ordenar(linhas):
        cels = []
        for chave, _ in COLS:
            v = l.get(chave, "")
            if chave == "negocio":
                marca = ROTULO_TIPO.get(l.get("tipo"), "")
                v = nome_de(l)
                v = f"**{v} ({marca})**" if l.get("tipo") == "usuario" else (f"{v} ({marca})" if marca else v)
            elif chave == "fonte_url":
                u = url_segura(v)
                if u:
                    v = f"[link]({u})"
                elif l.get("evidencia_tipo") == "informado_pelo_dono":
                    v = "informado pelo dono"
                else:
                    v = ""
            elif chave == "preco_texto" and sufixo_preco(l):
                v = f"{v} ({sufixo_preco(l)})"
            elif chave == "inclui":
                v = "; ".join(x.strip() for x in v.split("|") if x.strip())
            cels.append(md_cel(v))
        out.append("| " + " | ".join(cels) + " |")
    out.append("")
    return "\n".join(out)


CSS = """
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:24px;color:#1c1c1c;background:#fafaf8}
h1{font-size:22px;margin:0 0 6px}
p{margin:4px 0 14px;color:#555;max-width:80ch}
.wrap{overflow-x:auto;border:1px solid #ddd;border-radius:8px;background:#fff}
table{border-collapse:collapse;width:100%;font-size:14px;min-width:1250px}
th,td{padding:9px 11px;border-bottom:1px solid #eee;text-align:left;vertical-align:top}
th{background:#f1efe9;position:sticky;top:0;font-weight:600}
tr.usuario td{background:#fff7df;font-weight:600}
tr.guia td{color:#666;font-style:italic}
td.desconhecido{color:#999}
td.preco{white-space:nowrap}
td.obs{color:#666;font-size:13px}
a{color:#0b57a4}
small{color:#777}
"""


def montar_html(linhas):
    n, com = resumo(linhas)
    e = html.escape
    hoje = datetime.date.today().isoformat()
    p = ["<!doctype html>", '<html lang="pt-BR"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         "<title>Tabela de ofertas</title>", f"<style>{CSS}</style></head><body>",
         "<h1>Tabela de ofertas</h1>",
         f"<p>{n} concorrentes encontrados nesta rodada (não são todos os que existem). "
         f"{com} publicam preço, {n - com} não publicam. "
         "<strong>desconhecido</strong> significa que a página não publica preço. "
         f"Nenhum valor foi estimado. <small>Gerado em {hoje}. Rascunho para conferência.</small></p>",
         '<div class="wrap"><table><thead><tr>']
    p.extend(f"<th>{e(r)}</th>" for _, r in COLS)
    p.append("</tr></thead><tbody>")
    for l in ordenar(linhas):
        tipo = l.get("tipo", "")
        classe = tipo if tipo in ("usuario", "guia") else ""
        p.append(f'<tr class="{classe}">')
        for chave, _ in COLS:
            v = l.get(chave, "")
            cls = ""
            if chave == "negocio":
                marca = ROTULO_TIPO.get(tipo, "")
                conteudo = e(nome_de(l)) + (f" <small>({e(marca)})</small>" if marca else "")
            elif chave == "fonte_url":
                u = url_segura(v)
                if u:
                    conteudo = f'<a href="{e(u, quote=True)}" rel="noopener noreferrer nofollow">abrir fonte</a>'
                elif l.get("evidencia_tipo") == "informado_pelo_dono":
                    conteudo = "informado pelo dono"
                else:
                    conteudo = "-"
            elif chave == "preco_texto":
                cls = "preco desconhecido" if v.casefold() == _lib.DESCONHECIDO else "preco"
                conteudo = e(v)
                if sufixo_preco(l):
                    conteudo += f" <small>({e(sufixo_preco(l))})</small>"
            elif chave == "inclui":
                conteudo = "<br>".join(e(x.strip()) for x in v.split("|") if x.strip()) or "-"
            elif chave == "observacoes":
                cls = "obs"
                conteudo = e(v) or "-"
            else:
                conteudo = e(v) or "-"
            p.append(f'<td class="{cls}">{conteudo}</td>' if cls else f"<td>{conteudo}</td>")
        p.append("</tr>")
    p.append("</tbody></table></div></body></html>")
    return "\n".join(p)


def main():
    _lib.setup_stdout()
    ap = argparse.ArgumentParser(description="Gera a tabela de ofertas em Markdown e HTML.")
    ap.add_argument("csv")
    args = ap.parse_args()

    linhas, erros = _lib.ler_ofertas(args.csv)
    if erros:
        for er in erros:
            print("ERRO DE ESTRUTURA: " + er)
        return 1
    pasta = os.path.dirname(os.path.abspath(args.csv))
    md, ht = os.path.join(pasta, "offers-table.md"), os.path.join(pasta, "offers-table.html")
    with open(md, "w", encoding="utf-8") as f:
        f.write(montar_md(linhas))
    with open(ht, "w", encoding="utf-8") as f:
        f.write(montar_html(linhas))
    n, com = resumo(linhas)
    print(f"Gerados: {md} e {ht}")
    print(f"{n} concorrentes, {com} com preço publicado, {n - com} sem preço (desconhecido).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
