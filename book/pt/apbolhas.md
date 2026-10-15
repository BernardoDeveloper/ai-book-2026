---
id: apbolhas
chapter: "Três bolhas"
sources:
  - {post: 2018/12/26/akitando-34-voce-nao-sabe-nada-de-enterprise-conhecendo-a-sap, sha256: "46691d1aa6f8602ea97cfb27c0610c79945c18d19fdf844aed3011108f5150fb"}
  - {post: 2019/06/11/akitando-50-a-bolha-de-startups-vai-estourar-winter-is-coming, sha256: "ef99201b54eac4d40fa676dd8c2b21cba025e15843c437512218e253bc570a94"}
  - {post: 2021/06/22/akitando-100-mercado-financeiro-pos-pandemia-a-tempestade-perfeita, sha256: "04d2af19a6d40c3915c19ae146e71b3806843b736d6c932abd86444429784740"}
  - {post: 2022/11/22/akitando-132-rant-a-bolha-de-startups-estourou, sha256: "0ab9f5cdffe6b1d0ce41ca3642c8c17c3369c25f7e244e99e4384ae46d183fc7"}
  - {post: 2023/02/14/akitando-138-meu-comeco-de-carreira-durante-a-bolha-1997-a-2002-bug-do-milenio-crash, sha256: "79a02c73df595ddf8952c7bfbbd8023f51a3297b259610afa65901112dfe4160"}
refs_projects: []
blog_commit: "b54f14bf348a68cd8529004a4743d35dbbc5590d"
---

# Três bolhas {#sec-apbolhas}

<!-- src: original -->
Uma pergunta voltou o ano inteiro em 2026: a carreira acaba? Eu não tenho bola de cristal, mas tenho uma coisa que ajuda mais: já vi o ciclo de perto três vezes, de dentro do mercado de tecnologia, e as três deixaram números.

Este apêndice põe as três lado a lado. Pra cada uma, o que aconteceu, o que ficou depois e o que eu fiz no meio dela. A história da segunda, a bolha da programação, está contada no @sec-ch18; aqui ela aparece ao lado das outras duas, que é onde o padrão fica visível.

![Três bolhas numa linha só, de 1995 a 2026, com a minha trajetória embaixo.](assets/figures/apbolhas-linha.png){#fig-apbolhas-linha fig-alt="Linha do tempo de 1995 a 2026 com três faixas." fig-desc="Linha do tempo de 1995 a 2026 com três faixas. A internet, de 1995 a 2002: pico da Nasdaq em 10 de março de 2000 e fundo em 9 de outubro de 2002, 78% abaixo. O dinheiro de graça, de 2010 a 2022, com dois trechos hachurados de juro perto de zero, de dezembro de 2008 a dezembro de 2015 e de março de 2020 a março de 2022, e as demissões no setor logo depois: cerca de 165 mil em 2022 e 263 mil em 2023. A IA, a partir do ChatGPT em 30 de novembro de 2022, ainda em aberto. Embaixo, a minha linha: primeiro emprego em 1996, a pontocom fecha e eu vou pro SAP em 2001, Rails em 2007, Codeminer 42 em 2011, o Akitando de 2018 a 2023 e este livro em 2026."}

## A internet, 1995 a 2002

<!-- src: 2023/02/14/akitando-138-meu-comeco-de-carreira-durante-a-bolha-1997-a-2002-bug-do-milenio-crash -->
O índice Nasdaq, que concentra as empresas de tecnologia da bolsa americana, fechou no pico em 10 de março de 2000. Caiu daí até 9 de outubro de 2002 e perdeu uns 78% no caminho [@fred2026nasdaq]. Só voltou ao valor do pico em 2015. No meio disso, centenas de pontocom fecharam as portas.

<!-- src: 2019/06/11/akitando-50-a-bolha-de-startups-vai-estourar-winter-is-coming -->
O que ficou foi a infraestrutura. Na euforia, as empresas enterraram tanta fibra óptica que boa parte dela ficou anos sem uso, e foi esse excesso que barateou a internet da década seguinte [@wikipedia2026darkfibre]. A internet não parou: o Google e a Amazon viraram gigantes justamente nos anos secos que vieram depois do estouro.

<!-- src: 2023/02/14/akitando-138-meu-comeco-de-carreira-durante-a-bolha-1997-a-2002-bug-do-milenio-crash -->
Eu atravessei essa bolha por dentro. Entre 1996 e 2001 passei por agência, provedor e pontocom, e em 2001 a pontocom onde eu trabalhava fechou. Uma semana depois eu estava numa consultoria pequena que trabalhava com SAP; o @sec-ch18 conta essa semana [@akitando138].

<!-- src: 2018/12/26/akitando-34-voce-nao-sabe-nada-de-enterprise-conhecendo-a-sap -->
Fiquei uns cinco anos lá, integrando sistemas em empresas grandes. Foi onde aprendi que regra de negócio de empresa grande não se adivinha de fora, lição que volta no @sec-ch20.

<!-- src: 2023/02/14/akitando-138-meu-comeco-de-carreira-durante-a-bolha-1997-a-2002-bug-do-milenio-crash -->
Em 2023, olhando pra trás, eu resumi assim o que me fez atravessar aquela época sem grandes estragos:

> Eu nunca me defini como "programador ASP" ou "programador Java" ou "administrador de SQL Server". Minha especialidade não era nenhuma dessas ferramentas.

## O dinheiro de graça, 2010 a 2022

<!-- src: 2021/06/22/akitando-100-mercado-financeiro-pos-pandemia-a-tempestade-perfeita -->
Depois da crise de 2008, o banco central americano deixou os juros entre zero e 0,25% de dezembro de 2008 a dezembro de 2015, e voltou a eles de março de 2020 a março de 2022 [@fed2026openmarket]. Com a renda fixa rendendo quase nada, o dinheiro foi atrás de risco: ações de tecnologia, fundos de investimento em startups e o que mais prometesse crescer. A partir de 2010, mais ou menos, o mercado de programação viveu uma década de contratação fácil.

O sintoma mais claro veio no fim. As empresas de fachada criadas só pra comprar outra empresa e levá-la à bolsa sem o escrutínio normal, as SPACs, foram 59 em 2019, 248 em 2020 e 613 em 2021 [@spacinsider2026stats].

<!-- src: 2022/11/22/akitando-132-rant-a-bolha-de-startups-estourou -->
Aí a inflação voltou, e os juros subiram de quase zero pra 4,25% a 4,50% só em 2022 [@fed2026openmarket]. O dinheiro voltou pra renda fixa e as empresas de tecnologia demitiram: cerca de 165 mil pessoas em 2022 e mais de 260 mil em 2023, pelas contas do layoffs.fyi, que acompanha as demissões no setor no mundo todo [@layoffsfyi2026tracker].

O que essa bolha deixou foi uma geração inteira de programadores, parte deles formada às pressas em curso de semanas, e empresas acostumadas a resolver tudo contratando mais gente. O @sec-ch18 conta o que aconteceu com o volume sem valor quando o dinheiro secou.

<!-- src: 2019/06/11/akitando-50-a-bolha-de-startups-vai-estourar-winter-is-coming -->
Nessa eu fiz outra coisa: avisei. O Akitando, meu canal de 2018 a 2023, nasceu pra ensinar o que sobrevive às bolhas, e os avisos, de junho de 2019 a novembro de 2022, estão contados com data no @sec-ch18.

<!-- src: 2021/06/22/akitando-100-mercado-financeiro-pos-pandemia-a-tempestade-perfeita -->
Os sinais de empresa engordando pra vender, que descrevi no canal em 2021, voltam no @sec-ch14 pra ler os prospectos de 2026.

<!-- src: 2022/11/22/akitando-132-rant-a-bolha-de-startups-estourou -->
E errei o calendário duas vezes. A virada que eu chutei pra 2021 veio em 2022, empurrada pela pandemia. E a segunda perna da queda, que eu esperava pra 2023, não veio: a Nasdaq subiu uns 43% naquele ano, puxada pelas grandes empresas e pela onda da IA, enquanto o emprego no setor continuava fraco [@fred2026nasdaq; @layoffsfyi2026tracker]. Aviso serve pra se preparar; calendário, ninguém acerta.

## A IA, desde novembro de 2022

<!-- src: original -->
O ChatGPT saiu em 30 de novembro de 2022 [@openai2022chatgpt], oito dias depois de eu publicar o episódio sobre o estouro. O dinheiro que tinha fugido das startups voltou correndo, agora pra quem vende modelo, placa de vídeo e data center. O @sec-ch14 mostra quanto dinheiro é e quem ganha com a pressa.

Essa terceira ainda não terminou, e eu não sei dizer se ela vai estourar como as outras, nem quando. Sei o que ela já deixou: modelos que funcionam, vários deles abertos e rodando numa máquina em casa (@sec-ch13). Se os data centers vão ser a fibra óptica desta vez, sobrando baratos depois de um estouro, é pergunta em aberto.

<!-- src: original -->
O que eu fiz nesta é o livro que você está lendo. Em janeiro de 2023 eu disse no canal que a empolgação com IA é inversamente proporcional ao conhecimento sobre IA (@sec-ch01). Em 2026 fui medir: passei o ano usando, testando e quebrando essas ferramentas em trabalho de verdade, e anotei onde elas rendem e onde enganam.

## A carreira acaba?

<!-- src: original -->
Três ciclos não fazem uma lei, e eu não vou fingir que fazem. Mas eles repetem um padrão que dá pra conferir em cada um.

As empresas que viviam da bolha morreram, e a tecnologia ficou: a internet depois de 2002, os aplicativos e a nuvem depois de 2022. O trabalho que só tinha volume sumiu, seja o catalogador de sites, seja o programador que só montava formulário. E quem se definia pela ferramenta da moda sofreu mais do que quem se definia pelo problema que sabia resolver.

<!-- src: original -->
O padrão não garante nada pra ninguém em particular. Gente boa também perdeu o emprego nos dois estouros, e eu tive sorte de receber uma ligação na semana certa. O que os ciclos mostram é qual lado da transição costuma atravessar.

> Pelo que eu vi três vezes, a bolha acaba com o atalho. A profissão tem continuado, mudando de ferramenta, nas mãos de quem aprende a resolver o problema por baixo dela.
