# Critérios do placar (Etapa 6)

Oito perguntas, nota de 0 a 3 em cada, total de 0 a 24. A mesma régua vale para a oferta atual do usuário, para a oferta nova e para cada concorrente.

O placar é um julgamento organizado, não uma medição. Ele serve para comparar ofertas lado a lado com motivos escritos, e não prevê vendas. Diga isso ao usuário sempre que mostrar o ranking.

## Regras de nota

- Nota 0 é o padrão. Sobe só com evidência.
- Toda nota acima de 0 leva um motivo curto que aponta para algo observável: uma frase da página, uma linha da tabela, um item de `facts.json`.
- Julgue o que está **publicado**. Um concorrente pode ter uma garantia ótima que só conta no WhatsApp; se não está na página, a nota é 0, e o motivo diz "nada publicado".
- A oferta atual do usuário é julgada pelo que as páginas públicas dele mostram hoje (site, Instagram, página do produto, perfil no Google), não pelo que ele contou no diagnóstico. Se ele não tem nada público, julgue pela descrição que deu, com a mesma régua, e avise que a nota vem do relato e não de uma página. A oferta nova é julgada pelo `offer-novo.md`.
- Uma nota por concorrente, pelo pacote principal. Concorrente cuja página não foi lida fica fora do placar, e você diz quantos ficaram fora.
- Em mercados onde quase ninguém publica nada (perfis de diretório, "consultar valores"), os concorrentes ficam todos perto de zero e a oferta nova vira primeira por construção. Diga isso com clareza: o ranking, nesse caso, vale menos que a comparação da oferta nova com a nota máxima.
- Na dúvida entre duas notas, dê a menor. Um placar generoso com o usuário tira o sentido do ranking.
- Não dê nota pela qualidade do negócio em si (você não tem como saber), só pela oferta como está escrita.

## As oito perguntas

### 1. Resultado claro (`resultado`)
A oferta diz o que o cliente consegue, em palavras que ele usaria?

| Nota | Quando |
|---|---|
| 0 | Só descreve o serviço ou a empresa ("soluções completas em...") |
| 1 | Menciona um benefício genérico ("mais clientes", "sorriso bonito") |
| 2 | Resultado específico para um público definido |
| 3 | Resultado específico, para quem, e com medida ou marco observável |

### 2. Prova (`prova`)
Há evidência de que funciona para gente como o comprador?

| Nota | Quando |
|---|---|
| 0 | Nenhuma prova publicada |
| 1 | Afirmação solta ("centenas de clientes", "anos de experiência") sem como conferir |
| 2 | Prova conferível: depoimentos identificáveis, nota e número de avaliações, casos |
| 3 | Prova conferível, com números e próxima do perfil do cliente ideal |

### 3. Velocidade (`velocidade`)
A oferta diz quanto tempo até o primeiro resultado, e o prazo é curto para a categoria?

| Nota | Quando |
|---|---|
| 0 | Nenhum prazo mencionado |
| 1 | Prazo vago ("rápido", "em pouco tempo") |
| 2 | Prazo definido para entrega ou primeiro resultado |
| 3 | Prazo definido, curto para a categoria, e uma primeira vitória logo no início |

### 4. Facilidade (`facilidade`)
A oferta reduz o trabalho, a dúvida e o sacrifício do comprador?

| Nota | Quando |
|---|---|
| 0 | Não fala do que o cliente precisa fazer, ou exige muito sem ajuda |
| 1 | Menciona suporte ou atendimento de forma genérica |
| 2 | Tira tarefas concretas da mão do cliente ou explica o passo a passo |
| 3 | Faz pelo cliente a parte difícil e deixa claro o pouco que sobra para ele |

### 5. Risco tirado do comprador (`risco`)
Se der errado, quem perde?

| Nota | Quando |
|---|---|
| 0 | Nenhuma garantia nem redutor de risco publicado |
| 1 | Só repete direito legal, ou oferece algo leve (primeira conversa gratuita) |
| 2 | Garantia própria com prazo e condições claras |
| 3 | Garantia forte e clara (incondicional ampla ou por resultado), com como acionar |

### 6. Bônus (`bonus`)
Há extras que resolvem o problema seguinte do cliente?

| Nota | Quando |
|---|---|
| 0 | Nenhum bônus |
| 1 | Brinde genérico sem ligação com o resultado |
| 2 | Bônus ligado ao resultado ou ao próximo passo |
| 3 | Bônus que resolvem obstáculos concretos, explicados um a um |

### 7. Urgência honesta (`urgencia`)
Existe um motivo verdadeiro para decidir agora?

| Nota | Quando |
|---|---|
| 0 | Nenhuma urgência, ou urgência sem motivo aparente (contador que reinicia, "últimas vagas" permanente) |
| 1 | Promoção com data, sem explicação |
| 2 | Limite ou data com motivo plausível (turma, agenda) |
| 3 | Limite real explicado e coerente com a capacidade do negócio |

Urgência com cara de falsa vale 0 e o motivo registra o que foi visto. Você não tem como provar que é falsa: descreva o fato ("o contador volta ao início quando a página recarrega"), sem acusar.

### 8. Clareza de nome, preço e conteúdo (`clareza`)
Dá para entender o que é, quanto custa e o que vem junto sem falar com ninguém?

| Nota | Quando |
|---|---|
| 0 | Sem nome de oferta, sem preço, sem lista do que inclui |
| 1 | Um dos três está claro |
| 2 | Dois dos três estão claros |
| 3 | Nome específico, preço publicado e lista do que inclui |

## Formato de scores.json

```json
{
  "ofertas": [
    {
      "id": "u01",
      "nome": "Sua oferta hoje",
      "tipo": "atual",
      "notas": {
        "resultado":  {"nota": 1, "motivo": "home promete 'mais vendas', sem público nem medida"},
        "prova":      {"nota": 2, "motivo": "3 depoimentos com nome e empresa na home"},
        "velocidade": {"nota": 0, "motivo": ""},
        "facilidade": {"nota": 1, "motivo": "cita 'suporte por WhatsApp' sem detalhar"},
        "risco":      {"nota": 0, "motivo": ""},
        "bonus":      {"nota": 0, "motivo": ""},
        "urgencia":   {"nota": 0, "motivo": ""},
        "clareza":    {"nota": 1, "motivo": "lista o que inclui; sem nome de pacote e sem preço"}
      }
    }
  ]
}
```

`tipo`: `atual`, `nova` ou `concorrente`. Uma `atual` e uma `nova` no máximo.

## Como ler o ranking

- A posição da oferta atual e a da nova são calculadas, cada uma, contra os concorrentes. "Hoje você é 14º de 38, a nova seria 2º" quer dizer 37 concorrentes mais o usuário.
- Empates dividem a mesma posição.
- Diferença de 1 ou 2 pontos é ruído. Não venda como vitória.
- O mais útil do placar são as colunas: onde todos os concorrentes têm 0, há espaço livre. Onde o usuário tem 0 e os líderes têm 3, há uma lacuna para fechar.
- Se a oferta nova não ficar no topo, diga isso e mostre o que falta. Não ajuste notas para melhorar a posição.
