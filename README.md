# /offer: o Claude pesquisa os seus concorrentes e monta uma oferta irresistível

Uma skill pro Claude Code que faz três trabalhos pro dono de negócio:

| Parte | O que faz |
| --- | --- |
| **Pesquisa** | Procura os concorrentes que vendem o mesmo que você (na sua cidade ou online), lê a página de cada um e anota o serviço, o preço e a garantia, sempre com a fonte. |
| **Preço** | Monta a tabela e mostra onde o seu preço fica: mínimo, mediana e máximo do mercado. Dá nota pra cada oferta e te coloca num ranking contra elas. |
| **Oferta** | Reconstrói a sua oferta em sete passos inspirados no livro *$100M Offers* (Ofertas de 100 Milhões) e entrega a oferta nova, o texto da página e um pitch de uma frase. |

Nada é inventado: preço sem fonte não entra na tabela, e nenhuma promessa
(garantia, prazo, bônus, número) vai pro texto sem você aprovar. Nada é
publicado: tudo sai como arquivo pra você revisar.

Funciona no **Claude Code** (terminal ou aba **Code** do app do Claude no
computador). Precisa da assinatura paga do Claude (Pro ou Max) e de
**Python 3** no computador.

## Instalar

Abra o Claude Code e cole:

```text
Instala a skill desse repositório na minha pasta de skills do usuário
(.claude/skills): https://github.com/gabrieltomazia/offer
A pasta skills/offer tem que ficar direto em .claude/skills/offer.
No fim, me mostra o que tem dentro de .claude/skills/offer.
```

Tem Node? Também dá com um comando:

```bash
npx skills add gabrieltomazia/offer -g -a claude-code
```

Ou na mão: baixe o repositório (botão **Code → Download ZIP**) e copie a
pasta `skills/offer` para `.claude/skills/` dentro da sua pasta de usuário.
O `SKILL.md` tem que ficar direto dentro da pasta:

```text
.claude/skills/offer/SKILL.md
```

Depois abra uma conversa **nova** e digite `/offer`: tem que aparecer.

## Usar

Crie uma pasta pro seu negócio, abra o Claude Code nela e digite:

```text
/offer meu site é [SEU SITE]. Pesquisa os meus concorrentes e monta uma
oferta que o meu cliente ideal não consiga recusar.
```

Ele vai te fazer algumas perguntas (o que você vende, pra quem, por quanto,
qual garantia você consegue cumprir) e para pra você aprovar em cada etapa.
Os arquivos ficam em `offer-out/` dentro da sua pasta.

## Aviso

Ferramenta independente. Não é feita, apoiada nem afiliada a Alex Hormozi ou
à Acquisition.com. As ideias de oferta foram inspiradas pela leitura do livro
*$100M Offers* e estão explicadas com palavras próprias. A skill não dá
aconselhamento jurídico: para garantia e publicidade, confirme com um
profissional.
