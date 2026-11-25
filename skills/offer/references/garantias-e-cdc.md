# Garantias e Código de Defesa do Consumidor

Leia antes de qualquer conversa sobre garantia. Isto é um resumo de orientação, não aconselhamento jurídico. Os artigos citados são da Lei 8.078/1990 (CDC). Leis e normas de conselhos mudam: diga ao dono para confirmar o texto vigente com um advogado ou com o conselho da profissão antes de publicar.

## O que o cliente já tem por lei (não é "sua garantia")

Estes direitos existem com ou sem oferta. Apresentá-los como se fossem um diferencial exclusivo engana o comprador.

| Direito | O que é | Onde está |
|---|---|---|
| Arrependimento | Em compra feita fora do estabelecimento (internet, telefone, porta a porta), o consumidor pode desistir em 7 dias a contar da assinatura ou do recebimento, com devolução do que pagou | CDC, art. 49 |
| Garantia legal | Prazo para reclamar de vício aparente: 30 dias para serviço ou produto não durável, 90 dias para durável | CDC, art. 26 |
| Oferta obriga | Tudo que for anunciado com precisão suficiente obriga quem anunciou e passa a fazer parte do contrato | CDC, art. 30 |
| Cumprimento forçado | Se o fornecedor não cumprir a oferta, o consumidor pode exigir o cumprimento, aceitar equivalente ou desfazer com devolução | CDC, art. 35 |
| Publicidade enganosa | É proibida a publicidade que induz a erro, inclusive por omissão | CDC, art. 37 |
| Garantia contratual | A garantia que o vendedor oferece soma à legal e deve ser dada por escrito, dizendo o que cobre, por quanto tempo e como acionar | CDC, art. 50 |

Consequências práticas para a oferta:

- Curso online vendido pela internet já tem os 7 dias de arrependimento. Dá para lembrar o comprador desse direito, mas escreva como direito dele ("você tem 7 dias para desistir, como a lei prevê"), não como bondade exclusiva. Um prazo maior que 7 dias é, aí sim, garantia do dono.
- O que a página promete, o dono terá que cumprir. Por isso toda promessa passa pelo `facts.json` aprovado.
- Toda garantia do dono precisa dizer três coisas: o que cobre, por quanto tempo, e como o cliente aciona.

## As famílias de garantia

Apresente ao dono com o custo de cada uma. A escolha é dele.

### Incondicional
"Se não gostar em X dias, devolvo o valor." Sem exigir motivo.

- Força: a mais simples de entender, derruba a objeção de risco.
- Custo: alguns pedidos de devolução de quem usou e não devia. Funciona melhor quando a entrega é boa e o custo por cliente é baixo.
- Pergunte: "se 1 em cada 10 clientes pedisse o dinheiro de volta, seu caixa aguentaria?"

### Condicional
"Se você fizer A, B e C e não ficar satisfeito, devolvo."

- Força: protege o dono e empurra o cliente a fazer a parte dele, o que aumenta a chance de resultado.
- Custo: as condições precisam ser claras, verificáveis e razoáveis. Condição escondida ou impossível vira reclamação e pode ser considerada abusiva.
- Pergunte: "quais são as duas ou três coisas que o cliente precisa fazer para dar certo?"

### Por resultado
"Se não chegar a X em Y dias, continuo trabalhando sem cobrar" ou "devolvo".

- Força: a mais convincente, porque amarra o pagamento ao resultado.
- Custo: o dono assume um risco que depende de coisas fora do controle dele. Só serve quando ele controla a maior parte do resultado e mede esse resultado de forma objetiva.
- Pergunte: "em quantos dos seus últimos 10 clientes esse resultado aconteceu nesse prazo?" Se a resposta não for quase todos, não é a garantia certa.

### De serviço
"Se precisar de ajuste, o retorno em até X dias é sem custo." Cobre o atendimento, não o resultado.

- Força: é a saída para profissões que não podem prometer resultado, como as de saúde.
- Custo: o tempo de refazer ou ajustar.
- Em `facts.json`, use `tipo: de_servico`. Na copy, pode esclarecer que não é garantia de resultado.

### Sem garantia
É uma opção legítima. A oferta ainda pode reduzir risco de outras formas: primeira conversa sem compromisso, contrato sem multa, pagamento em etapas, amostra do trabalho. Só entram se o dono confirmar.

## Profissões com regras próprias

Alguns conselhos e órgãos restringem promessa de resultado e certos tipos de publicidade. Quando o negócio for de uma dessas áreas, avise o dono e não proponha garantia de resultado:

- **Saúde (medicina, odontologia, psicologia, nutrição, fisioterapia e outras):** os conselhos profissionais têm códigos de ética e resoluções de publicidade. Em geral, é vedado garantir resultado de tratamento, e há restrições sobre divulgar preço, promoções e imagens de antes e depois. As regras variam por conselho e mudam com o tempo. Uma garantia possível nessa área costuma ser sobre o serviço (retorno, ajuste, atendimento), não sobre o resultado clínico.
- **Advocacia:** a publicidade é regulada pela OAB e não admite promessa de resultado.
- **Investimentos e finanças:** não se promete rentabilidade. Há regras da CVM e do Banco Central conforme a atividade.
- **Emagrecimento, estética, suplementos:** promessa de resultado em prazo é o tipo de alegação que mais gera autuação e reclamação.

Isto explica também por que, na tabela, clínicas e escritórios quase nunca publicam preço: muitas vezes não podem. `desconhecido` é o registro correto.

Diga ao dono: "sua profissão tem regras de publicidade; confirme com seu conselho antes de publicar esta página."

## Infoproduto e promessa de ganho

- Promessa de renda ("fature R$ 10 mil em 30 dias") é alegação de resultado financeiro. Só entra se for um resultado típico, comprovável e aprovado pelo dono, e mesmo assim prefira descrever o que o aluno aprende e faz.
- Resultado de um aluno excepcional precisa ser apresentado como caso individual, não como o que todos conseguem.
- As plataformas de checkout têm políticas próprias de reembolso que se somam à lei. O dono deve conhecer a da plataforma dele.

## Como registrar em facts.json

```json
"garantia": {
  "aprovada": true,
  "tipo": "condicional",
  "texto": "Se você comparecer às 4 sessões e não notar diferença, devolvemos o valor em até 10 dias.",
  "condicoes": "Comparecer às 4 sessões agendadas. Pedido por e-mail em até 30 dias após a última sessão.",
  "como_acionar": "E-mail para o endereço informado no contrato."
}
```

- `aprovada: false` significa que nenhuma frase de garantia entra na copy. O `check_copy.py` recusa.
- `como_acionar` vazio gera aviso no script: pergunte ao dono o canal e o prazo.
- Promessa de devolução de dinheiro só passa se o texto aprovado falar em devolução.
- Para lembrar um direito legal (os 7 dias de arrependimento), registre a frase em `direitos_legais`. Sem isso, o número é recusado na copy.
- `tipo` diferente de `por_resultado` faz o script recusar "resultado garantido".
- A copy usa o `texto` aprovado. Reescrever com outras palavras pode mudar o que foi prometido.

## Garantia de concorrente

Na tabela, a garantia do concorrente entra com o texto exato da página, validado pelo `check_prices.py`, ou `nenhuma publicada`. Não interprete ("parece que devolvem") e não use a garantia de um concorrente como argumento de que o dono deveria oferecer a mesma.
