---
id: interlude1
chapter: "Interlúdio: Vinte anos de blog num fim de semana"
sources:
  - {post: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo, sha256: "247ad116f3c45c935f8a59156a72b8852733e259c70b65044f19fb56c6d32f3b"}
refs_projects: []
blog_commit: "cc8b467dd4d6d3b5c57fad6bb6fae70ec5839a01"
---

# Interlúdio: Vinte anos de blog num fim de semana {#sec-interlude1 .unnumbered}

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Segunda-feira, 6 de abril de 2026, umas seis e meia da tarde. Na véspera, meu blog tinha completado vinte anos, e eu ainda não tinha escrito o texto de aniversário. Abri o Claude Code dentro da pasta onde mora o blog inteiro e digitei, mais ou menos, isto: traduza tudo pro inglês.

Foi só isso. Depois fui cuidar da vida.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
O blog nasceu em 2006, no Blogspot do Google, como quase todo blog da época. Mudou de casa várias vezes: um sistema pronto feito em Ruby on Rails, depois outro, depois um motor que eu mesmo escrevi em 2012 e fui arrastando por anos de atualizações, até chegar, em setembro de 2025, num gerador de site estático chamado Hugo. Vinte anos carregando os mesmos textos de um formato pro outro, jogando fora o lixo pelo caminho.

E vinte anos com a mesma dívida.

## A promessa que nunca saiu do papel

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Quase tudo ali estava em português. Fazia anos que eu recebia mensagens de leitores brasileiros morando em Portugal, nos Estados Unidos, no Japão, na Alemanha, no Canadá, sempre com o mesmo pedido: uma versão em inglês, pra mostrar pros colegas de trabalho. "Eu mostraria esse texto pro meu time, mas só tá em português."

Eu sempre respondia que um dia traduzia. E nunca traduzi.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
A conta não fechava. Eram 727 textos em português. Traduzir à mão, um por um, levaria semanas, talvez meses de trabalho dedicado, e eu nunca ia ter fôlego pra isso. Pior: a cada ano, mais textos entravam na fila.

Tinha até uma ironia no meio. Alguns textos nasceram em inglês, como uma série de entrevistas de 2008 com programadores conhecidos lá fora, e uns posts de 2017 e 2018, quando eu tentei escrever primeiro em inglês. Esses estavam parados do outro lado, sem versão em português.

## Dormindo enquanto o agente trabalha

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Deixei o [agente]{.gls} rodando e fui dormir. Acordei na terça e ele continuava. Dormi de novo. Na quarta de manhã cedo, tinha terminado.

Do primeiro commit de tradução ao último foram umas 39 horas, contando as noites, os almoços e uma roda de café no meio. O título deste interlúdio é uma licença poética: na prática, foi um fim de semana estendido que caiu no meio da semana.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
O histórico do projeto mostra a cadência: um lote de posts de uma conferência de 2008, outro de uma conferência de 2009, um de 2011 sobre Objective-C, o ano de 2012 inteiro, a série de 2015 sobre Elixir. Foram mais de 80 commits, organizados por ano e por série.

No fim havia 354 textos em inglês ao lado dos 727 originais. Quase metade do blog, de uma vez.

Pra cada texto, o agente lia o original, escrevia a tradução e depois passava por cima uma revisão de estilo, pra tirar os vícios de texto de máquina. Centenas de vezes seguidas.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
E a qualidade me surpreendeu. Uns noventa por cento ficaram bons, naturais e fiéis ao meu jeito de escrever. Eu não esperava que funcionasse tão bem. Com boas instruções de tom e estilo, o agente respeitou o original e não tentou "corrigir" nenhuma ideia técnica minha.

No pior caso, eu revisava alguns parágrafos. No melhor, a versão em inglês parecia escrita direto na outra língua.

> Um trabalho que eu adiei por quase vinte anos, por ser grande e chato demais, virou um problema de fim de semana.

## A conta

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Teve preço. Eu assinava o plano de uso pesado da Anthropic, o Max 20x, feito pra quem usa o Claude Code o dia inteiro. Nunca tinha batido no teto dele, nem nas sessões mais longas da maratona do capítulo anterior.

Aquela tradução foi a primeira vez. Na quinta de manhã, o painel da minha conta mostrava 91% da cota semanal consumida e uns 280 reais, perto de 50 dólares, de uso extra cobrado por cima da mensalidade. E o agente começou a receber, cada vez mais, um erro avisando que eu estava mandando pedidos demais.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Faz sentido: ler um texto inteiro, traduzir, revisar o estilo, e repetir isso centenas de vezes seguidas, consome uma montanha de [tokens]{.gls key=token}, aqueles pedacinhos de texto em que o modelo lê e escreve (@sec-ch01). Achei justo. É o preço de usar a ferramenta pesado justamente quando ela fazia diferença.

## Os seis que disseram não

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Nem tudo passou, porém.

Meia dúzia de textos antigos se recusaram a ser traduzidos. Tanto o Claude quanto o GPT, chamados direto pela [API]{.gls key=api}, devolviam um erro com uma mensagem sobre política de conteúdo. Tentei várias vezes, em sessões novas, com o contexto limpo. Nada.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Olhando a lista, dava pra adivinhar o que tinha disparado o alarme:

- um texto de 2009 sobre o discurso de Steve Jobs na formatura de Stanford, em 2005, que fala de câncer porque Jobs contava ali do diagnóstico que tinha recebido [@jobs2005stanford];
- dois capítulos de Ayn Rand que eu tinha traduzido anos antes, sobre os direitos do homem e sobre argumentação;
- um post sobre o discurso do dinheiro de *A Revolta de Atlas*, também da Ayn Rand;
- um post contra o nazismo, barrado, ao que tudo indica, só porque a palavra "nazi" aparecia nele, apesar de o texto inteiro ser uma crítica;
- um ensaio sobre democracia e ética que travava em toda tentativa.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Nenhum desses textos tem nada de perigoso. Um fala de doença, outro de filosofia política, outro critica os nazistas. Pelo jeito, o filtro automático das empresas mede com uma régua grossa: esbarrou num tema sensível, recusa, sem pesar o contexto.

A saída veio de casa. Carreguei no meu próprio computador o Qwen 3.5 35B, um [modelo aberto]{.gls key=modelo-aberto} da chinesa Alibaba, desses que qualquer um pode baixar e rodar sem pedir licença a ninguém (@sec-ch13 conta o que isso exige) [@qwen2026qwen35]. Sem filtro corporativo no meio, o modelo leu, entendeu o contexto e traduziu tudo sem drama.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Ou seja: um modelo chinês traduziu os textos que os modelos ocidentais recusaram, inclusive um contra o nazismo. Eu não consigo deixar de achar isso levemente hilário.

Por trás da piada tem uma lição prática. Os modelos comerciais sempre vão carregar a política da empresa que os vende, e essa política é aplicada de forma preventiva. Pra quem usa em produção, é uma troca real: você ganha fluência e capacidade, e perde o controle no dia em que o seu assunto resvala no que a empresa decidiu que é sensível.

> O único muro de verdade naquele fim de semana foi o filtro de conteúdo das empresas, e quem pulou o muro foi um modelo rodando em casa.

## O caminho de volta

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Já que eu estava com a mão na massa, aproveitei pra resolver o lado contrário. As entrevistas de 2008 e os textos de 2017 e 2018 que nasceram em inglês ganharam versão em português, pelo mesmo caminho, só que invertido. O agente também ajustou o programinha que monta o índice do blog, pra gerar uma lista em cada língua.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Em 9 de abril, quando enfim publiquei o texto de aniversário, metade do blog era bilíngue. O que faltava eram, na maior parte, dicas velhas de versões de software que nem existem mais, coisas que fazia mais sentido apagar do que traduzir.

A barreira pra alcançar leitores fora do Brasil, que eu carreguei por duas décadas, tinha ficado barata o suficiente pra eu não ter mais desculpa.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
O Qwen que salvou aqueles seis textos eu conhecia de outro lugar. Naquelas mesmas semanas, eu vinha colocando modelos pra competir num teste de programação que eu mesmo tinha montado, tentando descobrir qual era melhor. Parecia uma pergunta simples, com resposta numa tabela. Nos meses seguintes eu descobri que medir modelo de IA é bem mais traiçoeiro do que traduzir vinte anos de blog.
