# Ideias de oferta (Etapa 5)

Este arquivo explica, com palavras próprias, o raciocínio usado para reconstruir uma oferta. A leitura de referência é o livro *$100M Offers*, de Alex Hormozi, que vale ser lido inteiro. Nada aqui é citação do livro, e esta skill não fala em nome do autor.

Ferramenta independente, não é feita, apoiada ou afiliada a Alex Hormozi ou à Acquisition.com.

## Sumário

1. As quatro alavancas do valor percebido
2. Os sete passos
3. Regras de honestidade ao reconstruir
4. Erros comuns

## 1. As quatro alavancas do valor percebido

Quem compra não compara preços, compara o que acha que vai receber pelo preço. Esse "acho que vou receber" depende de quatro coisas:

| Alavanca | Pergunta do comprador | Direção |
|---|---|---|
| Tamanho do resultado | "O que eu ganho com isso, e quanto isso importa para mim?" | Quanto maior, mais valor |
| Confiança | "Vai funcionar para alguém como eu?" | Quanto maior, mais valor |
| Tempo | "Quanto demora até eu ver resultado?" | Quanto menor, mais valor |
| Esforço e sacrifício | "O que eu preciso fazer, aprender ou abrir mão?" | Quanto menor, mais valor |

Duas subir, duas descer. Uma oferta fraca quase sempre trabalha só a primeira (promete um resultado grande) e esquece as outras três. Na prática, as duas de baixo costumam ser as mais baratas de melhorar: responder mais rápido, entregar a primeira vitória na primeira semana, tirar uma tarefa chata da mão do cliente.

Use a tabela de concorrentes para enxergar onde ninguém está trabalhando. Se todos prometem o mesmo resultado e nenhum fala de prazo, a alavanca do tempo está livre.

## 2. Os sete passos

### Passo 1. Resultado nas palavras do cliente

Escreva o que o cliente quer do jeito que ele diria para um amigo, não do jeito que o dono descreve o serviço.

- Serviço descrito pelo dono: "gestão de tráfego pago".
- Resultado dito pelo cliente: "quero o telefone tocando com gente que já sabe o preço".

Fontes: a resposta da pergunta 7 do diagnóstico, os elogios das avaliações (o que as pessoas agradecem) e os depoimentos do próprio dono. Não invente a fala do cliente. Se não houver material, pergunte ao dono o que os clientes costumam dizer na primeira conversa.

### Passo 2. Lista de obstáculos

Liste tudo que pode impedir o comprador de chegar ao resultado ou de comprar. Pense em quatro momentos: antes de comprar, logo depois de comprar, durante o uso e depois que termina.

A melhor pista está em `reviews.md`: cada reclamação recorrente sobre um concorrente é um obstáculo real que o mercado ainda não resolveu. "Demoraram três dias para responder", "não explicaram o que estava incluso", "tive que voltar quatro vezes".

Para cada obstáculo, anote a qual alavanca ele pertence (confiança, tempo ou esforço). Isso mostra onde a oferta nova ganha.

### Passo 3. Cada obstáculo vira uma entrega

Para cada obstáculo, escreva o que o dono pode entregar para resolvê-lo. Depois passe cada entrega por um filtro com o dono:

- Você consegue fazer isso para todo cliente, todo mês?
- Quanto custa para você em tempo ou dinheiro?
- O cliente dá muito valor a isso?

Fique com as entregas de alto valor para o cliente e custo suportável para o dono. Descarte o resto sem dó: uma entrega que o dono não sustenta vira reclamação no mês seguinte.

Só entra na oferta o que o dono confirmou. Registre em `facts.json` em `oferta_nova.inclui`.

### Passo 4. Empacotar e dar nome

Junte as entregas em um pacote com começo, meio e fim, na ordem em que o cliente vai vivê-las. Dê um nome que diga para quem é e o que resolve.

O nome precisa ser específico e verdadeiro:

- Específico: "Implante em Etapas para Quem Tem Medo de Dentista" diz mais que "Plano Premium".
- Verdadeiro: se o nome contém um prazo ou um número, esse número tem que estar em `facts.json`. "Agenda Cheia em 30 Dias" só existe se o dono aprovar e conseguir cumprir.

### Passo 5. Tirar o risco do comprador

O medo de errar a compra trava mais venda que o preço. A garantia transfere parte desse risco para o vendedor.

Apresente as famílias ao dono, com o custo de cada uma, e deixe ele escolher (há também a garantia de serviço, descrita em `garantias-e-cdc.md`, para quem não pode prometer resultado):

- **Incondicional:** devolve se o cliente não gostar, sem perguntas, dentro de um prazo. Mais forte para vender, mais exposta a abuso.
- **Condicional:** devolve se o cliente fez a parte dele (compareceu, aplicou, enviou o material) e mesmo assim não ficou satisfeito. Protege o dono e ainda incentiva o cliente a agir.
- **Por resultado:** o dono continua trabalhando sem cobrar, ou devolve, se um resultado definido não acontecer em um prazo. A mais forte e a mais arriscada; só para quem controla o resultado.

Regras:

- A garantia é decisão do dono. Sem escolha explícita, a oferta sai sem garantia, e tudo bem.
- Garantia não substitui os direitos que o consumidor já tem por lei. Leia `garantias-e-cdc.md` antes dessa conversa.
- Algumas profissões têm regras que restringem promessa de resultado (saúde, direito, finanças). O arquivo de garantias explica.
- Registre em `facts.json` o tipo, o texto exato e as condições. A copy só pode usar esse texto.

### Passo 6. Bônus que resolvem o próximo problema

Um bom bônus responde à pergunta "e depois?". Quando o cliente consegue o resultado principal, qual é o problema seguinte?

- Clareou os dentes: como manter a cor.
- Começou a receber contatos: como responder e fechar.
- Terminou o curso: como conseguir o primeiro cliente.

Cada bônus tem que ser algo que o dono já tem ou consegue produzir, e precisa estar em `facts.json`. Não atribua valor em reais a um bônus a menos que ele seja vendido separadamente por esse preço e o dono confirme. "Bônus no valor de R$ 2.000" sem venda real é número inventado.

### Passo 7. Urgência só se for real

Existem dois tipos honestos de urgência:

- **Limite de capacidade:** o dono só consegue atender X clientes novos por mês. Vem da pergunta 10 do diagnóstico.
- **Data de verdade:** a turma começa em um dia, o preço muda em um dia que o dono vai cumprir.

Se nenhum dos dois existir, a oferta sai sem urgência nenhuma. Contador falso, "últimas vagas" permanentes e promoção que nunca acaba são fáceis de descobrir, queimam a confiança que a oferta inteira tentou construir e podem configurar publicidade enganosa.

Registre em `facts.json` em `urgencia` (`real: true`, o texto e o motivo). Com `real: false`, o `check_copy.py` recusa qualquer frase de escassez.

## 3. Regras de honestidade ao reconstruir

- A oferta nova é montada com o que o dono tem e consegue fazer. O papel da skill é organizar e deixar visível, não inflar.
- Toda promessa da oferta nova tem uma linha correspondente em `facts.json`.
- Se a pesquisa mostrar que a oferta atual já é forte, diga isso. Nem toda oferta precisa ser refeita; às vezes o problema é só clareza de nome e preço.
- Se o dono quiser prometer algo arriscado, explique o risco uma vez, com clareza, e respeite a decisão dele. A decisão é dele, o registro em `facts.json` também.
- Não derrube concorrentes na copy. A oferta se sustenta pelo que entrega, e citar concorrente pelo nome traz risco jurídico.

## 4. Erros comuns

- **Empilhar item sem critério.** Dez itens fracos confundem mais do que três fortes. Cada item precisa resolver um obstáculo da lista.
- **Subir preço sem mexer em nada.** O preço acompanha o valor percebido. Primeiro a oferta, depois o número.
- **Prometer velocidade que depende do cliente.** Se o prazo depende de o cliente enviar material, diga isso no texto.
- **Copiar a garantia do concorrente.** O que um concorrente consegue bancar não diz nada sobre o que este dono consegue.
- **Tratar a oferta nova como certeza.** É uma hipótese bem fundamentada. O teste real é oferecer a clientes novos por um período e observar.
