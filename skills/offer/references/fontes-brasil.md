# Onde achar oferta e preço públicos no Brasil

Guia para as Etapas 1 e 2. A regra é a mesma em todas as fontes: só o que qualquer pessoa vê sem login, sem contornar bloqueio e sem contatar o concorrente.

## Sumário

1. Buscas que funcionam
2. Fontes por tipo de negócio
3. Onde o preço costuma estar (e onde não está)
4. Avaliações
5. Guias de preço
6. O que não é concorrente
7. Quando a fonte não abre
8. Modo com ferramenta paga (opcional)

## 1. Buscas que funcionam

Monte de 6 a 10 buscas e pare quando os nomes começarem a se repetir.

| Intenção | Modelo de busca |
|---|---|
| Quem atende na região | `<serviço> em <cidade>` / `<serviço> <bairro> <cidade>` |
| Quem publica preço | `<serviço> <cidade> preço` / `<serviço> valor` / `quanto custa <serviço> <cidade>` |
| Quem vende em pacote | `<serviço> pacotes` / `<serviço> planos` / `<serviço> mensalidade` |
| Quem vende online | `<serviço> online` / `curso de <tema>` / `<serviço> para <nicho>` |
| Página de planos direta | `<serviço> <cidade> "planos"` / `"a partir de" <serviço> <cidade>` |
| Reclamações | `<nome do concorrente> reclame aqui` / `<nome> avaliações` |

Dicas:

- Use o nome que o cliente usa, não o termo técnico ("aparelho invisível" além de "alinhador ortodôntico").
- Para cidade média, inclua cidades vizinhas se o dono disse que disputa cliente com elas.
- Anote de qual busca cada concorrente veio. Ajuda o usuário a entender a amostra.

## 2. Fontes por tipo de negócio

### Negócio local (clínica, salão, academia, pet shop, oficina, escola)

- **Site próprio:** páginas "Serviços", "Tratamentos", "Planos", "Preços", "Promoções", "Convênios".
- **Google Maps / Perfil da Empresa:** nome, categoria, serviços listados, nota e avaliações. Preço aparece às vezes na aba de serviços ou nas avaliações. Use quando a página abrir sem login.
- **Instagram:** bio, destaques ("Preços", "Planos", "Valores") e legendas fixadas. Só o que abre sem login; se pedir login, registre "não foi possível ler".
- **Plataformas de agendamento:** Doctoralia, BoaConsulta (saúde); Booksy, Trinks (beleza); Gympass/Wellhub, TotalPass (academias). Costumam mostrar valor de consulta ou serviço. Para clínicas, a listagem por tratamento e cidade dessas plataformas costuma render mais do que a busca aberta, que devolve artigos e diretórios. O perfil que o profissional mantém ali vale como página dele (`evidencia_tipo=diretorio`).
- **Marketplaces de serviço:** GetNinjas, Habitissimo. Úteis como guia de faixa, não como concorrente.

### Agência, gestor de tráfego, consultor, freelancer

- **Site próprio:** "Planos", "Investimento", "Como funciona", "Contrate". Muitos não publicam e pedem diagnóstico: registre `desconhecido`.
- **Páginas de venda de pacotes fechados:** alguns vendem "gestão de tráfego" como produto com preço em checkout.
- **Links de pagamento públicos:** Asaas, Mercado Pago, PagBank e similares. Muito prestador de serviço cobra por um link aberto que mostra nome do plano, valor e periodicidade. O link mostra pouco: procure a página do mesmo vendedor para saber o que o plano inclui. Link desativado não é preço publicado.
- **Marketplaces de freelancers:** Workana, 99Freelas, Fiverr, GetNinjas. Bons para faixa, com a ressalva de que o perfil de cliente é diferente.
- **LinkedIn e Instagram:** raramente têm preço. Servem para pacote, nicho e prova.

### Infoproduto, curso, mentoria, comunidade

- **Página de venda:** o preço costuma estar no fim, perto do botão, e é comum aparecer parcelado ("12x de R$ ...") com o valor à vista em letra menor. Havendo os dois, registre o à vista e anote o parcelamento em `observacoes`: o total parcelado costuma ter acréscimo e inflaria a comparação. Só parcelado: texto exato e, em `preco_valor`, o total.
- **Checkout público:** Hotmart, Kiwify, Eduzz, Monetizze, Ticto, Braip, Kirvano, Cakto. A página de pagamento mostra preço e parcelas sem login. Leia, não preencha nada e não avance no formulário.
- **Vitrines:** marketplace da Hotmart, Udemy, Domestika. Preço público, geralmente com promoção rotativa: registre o preço mostrado e a data. Essas páginas montam preço e garantia por JavaScript, então a captura automática costuma vir sem valor nenhum (o script avisa). Aí o caminho é ler por outra via pública e gravar captura manual, sabendo que o validador passa a conferir um texto digitado por você: avise o usuário e peça para ele abrir os links. A vitrine mostra nota e número de avaliações, mas raramente o texto delas.
- **Mercado Livre:** cursos e produtos físicos, com preço e avaliações públicas.
- **Instagram:** link da bio leva à página de venda. A oferta está lá, não no perfil.

### Produto físico e e-commerce

- Loja própria, Mercado Livre, Shopee, Amazon, Magalu. Compare o mesmo tipo e tamanho de produto, e registre frete separado se a página mostrar.

## 3. Onde o preço costuma estar (e onde não está)

| Tipo | Publica preço? | Observação |
|---|---|---|
| Curso e infoproduto | Quase sempre | Atenção a parcelado versus à vista |
| Academia, coworking, escola de idiomas | Frequente | Costuma ser "a partir de" |
| Salão, estética, barbearia | Frequente em agendadores | Menos no site |
| SaaS e assinatura | Quase sempre | Mensal versus anual: unidades diferentes |
| Agência, consultoria | Raro | A maioria pede reunião |
| Clínica médica e odontológica | Raro | Regras de conselho restringem; consulta aparece em agendadores |
| Advocacia, contabilidade | Raro | Contabilidade online é exceção e publica planos |
| Obra, reforma, serviço sob medida | Quase nunca | Orçamento caso a caso |

"Solicite um orçamento", "fale com um consultor", "chame no WhatsApp" e "consulte valores" significam `desconhecido`. Não é falha da pesquisa, é informação: mostra que o mercado negocia no privado, e isso entra no relatório ("11 não publicam preço").

Armadilhas de unidade:

- "R$ 99 por mês no plano anual" é preço mensal com compromisso anual. Anote isso em `observacoes`.
- "A partir de" é piso. Use `preco_tipo=a_partir_de`.
- "De R$ 997 por R$ 497": o preço é o atual (R$ 497). O valor riscado não entra em `preco_valor`.
- Taxa de adesão, matrícula e investimento em mídia são separados do preço do serviço. Anote em `observacoes`.

## 4. Avaliações

- **Google (Perfil da Empresa):** a fonte mais comum para negócio local.
- **Reclame Aqui:** reclamações com resposta da empresa. Forte para infoproduto, e-commerce e serviços online.
- **Comentários públicos:** em posts abertos e páginas de produto (Mercado Livre, Udemy).
- **Doctoralia, Booksy, Trustpilot:** conforme o setor.

Como registrar em `reviews.md`:

```
## c03 Nome do concorrente
Fonte: <url> (lido em AAAA-MM-DD, N avaliações visíveis)

Elogiam:
- Atendimento rápido: "responderam no mesmo dia"
- ...

Reclamam:
- Atraso na entrega: "prometeram 15 dias e levou 40"
- ...
```

Regras: temas, não pessoas. Frases curtas (até umas 15 palavras), sem nome, apelido, foto ou qualquer dado de quem escreveu. Se uma avaliação contar algo íntimo (saúde, dívida), resuma o tema e não cite. Se houver poucas avaliações, diga quantas viu em vez de generalizar.

## 5. Guias de preço

Matérias e tabelas do tipo "quanto custa um implante em 2026" ou tabelas de referência de sindicatos e associações podem ser usadas como fonte de faixa:

- Linha com `tipo=guia`, `preco_tipo=faixa`, texto exato, URL e data.
- Não entram em mínimo, mediana e máximo. Aparecem à parte como referência.
- Diga de onde vem e de quando é. Guia antigo ou sem metodologia vale pouco, e isso deve ser dito.

## 6. O que não é concorrente

Ignore, a menos que o usuário peça para incluir:

- Diretórios e listas ("as 10 melhores clínicas de...").
- Portais de notícia, blogs e fóruns.
- Franqueadoras vendendo franquia (o concorrente é a unidade local).
- Fornecedores e fabricantes do setor.
- Vagas de emprego e cursos sobre a profissão.
- Negócios de outra região que não atendem a do usuário (para negócio local).

## 7. Quando a fonte não abre

- Página exige login: não entre. Registre "exige login" e siga.
- Captcha, bloqueio de robô ou HTTP 403/429: não insista nem troque de técnica para contornar. Registre e siga.
- robots.txt proíbe: o script já respeita. Não leia por outro caminho.
- Página montada por JavaScript e a captura veio vazia: tente a leitura normal de páginas do Claude Code. Se conseguir o texto, salve como captura manual. Se não, `desconhecido`.
- Sempre liste no relatório final as páginas que não abriram. O usuário pode abrir no navegador dele e te passar o que viu.

## 8. Modo com ferramenta paga (opcional)

O modo Básico (zero custo) dá conta de 10 a 20 concorrentes por rodada. Um coletor pago, como um ator de Google Maps no Apify, só faz sentido para levantar mais de 100 locais de uma vez.

Antes de usar:

1. Diga o que a ferramenta faria que o modo Básico não faz.
2. Mostre o custo estimado com a conta (preço por mil resultados da tabela pública da ferramenta, vezes a quantidade) e o link da página de preços. Se não souber o preço atual, diga que não sabe e peça para o usuário conferir.
3. Espere um sim explícito.
4. O token vai em variável de ambiente ou arquivo local fora do repositório (por exemplo `~/.config/oferta-irresistivel/.env`), criado pelo próprio usuário. Nunca peça para colar no chat, nunca imprima o token e nunca grave em `offer-out/`.
5. As mesmas regras continuam valendo: só dados públicos, sem dados pessoais de avaliadores, sem contato.
