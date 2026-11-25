<!--
Template do relatorio final. Este arquivo cita concorrentes e numeros da pesquisa,
entao NAO passa pelo check_copy.py. Os numeros daqui vem de offers.csv,
price-position.md e placar.md.
-->

# Relatório: {{nome do negócio}}

> RASCUNHO. Nada foi publicado, nenhum preço foi alterado e ninguém foi contatado. Você decide o que aplicar.

Data: {{AAAA-MM-DD}}

## 1. O negócio em duas linhas

{{resumo aprovado no diagnóstico}}

## 2. O que foi pesquisado

- Concorrentes encontrados nesta rodada: {{N}} (não são todos os que existem, são os que a busca mostrou)
- Buscas usadas: {{lista}}
- Publicam preço: {{N}}. Não publicam: {{N}}
- Páginas que não abriram: {{lista ou "nenhuma"}}
- Preços conferidos em captura manual (abra o link para confirmar): {{lista ou "nenhum"}}

## 3. Tabela de ofertas

Veja `offers-table.html` (abre no navegador) ou `offers-table.md`.

Destaques:

- {{destaque}}
- {{destaque}}

## 4. Posição de preço

{{resumo de price-position.md: por serviço e unidade, mínimo, mediana, máximo e onde você está. Se a base for insuficiente, diga aqui}}

Lembretes: o preço acompanha o valor. Se for subir, teste com clientes novos por um período. Ser o mais barato é uma escolha com custo.

## 5. O que os clientes do mercado elogiam e reclamam

| Elogiam | Reclamam |
|---|---|
| {{tema}} | {{tema}} |

## 6. Oferta nova

Veja `offer-novo.md`. Em resumo:

- Nome: {{...}}
- Preço: {{...}}
- Garantia: {{...}}
- O que mudou: {{...}}

## 7. Placar

{{ranking: "hoje você é Xº de N, a oferta nova seria Yº"}}

Isto é um julgamento com motivos escritos, não uma medição de vendas. Detalhes em `placar.md`.

## 8. Arquivos entregues

- `offer-novo.md`
- `pagina-de-oferta.md`
- `pitch.txt`
- `offers.csv`, `offers-table.md`, `offers-table.html`
- `price-position.md`, `placar.md`, `scores.json`, `reviews.md`, `competitors.md`, `facts.json`
- `instagram.md` (se foi pedido)
- `sources/` (capturas das páginas; evidência local, não compartilhe)

## 9. O que ficou em aberto

- {{preços que ninguém publica}}
- {{decisões pendentes do dono}}
- {{o que conferir com conselho profissional ou advogado antes de publicar}}

## 10. Próximos passos sugeridos

1. Revisar `facts.json` mais uma vez: tudo que a página promete, você terá que cumprir.
2. Testar a oferta nova com clientes novos por um período definido.
3. Refazer a pesquisa em alguns meses: preços e ofertas mudam.

---

Ferramenta independente, não é feita, apoiada ou afiliada a Alex Hormozi ou à Acquisition.com.
