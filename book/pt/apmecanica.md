---
id: apmecanica
chapter: "A máquina por dentro, sem matemática"
sources:
  - {post: 2026/02/08/rant-ia-acabou-com-programadores, sha256: "09830f1d69488d527d241814a30269786cd7a5548e5d34fdf33b7fa21af0f417"}
  - {post: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia, sha256: "eba7e0379feb2d062e312e755b44b31fbc056217040c9107cbae1848bf1e5623"}
  - {post: 2020/09/30/akitando-84-entendendo-o-dilema-social-e-como-voce-e-manipulado, sha256: "7ee4001a6b6712e98fa2deb8acf37d0ffc33fde8b0b8ed7838b2c4d59e3aa02d"}
refs_projects: []
blog_commit: "cc8b467dd4d6d3b5c57fad6bb6fae70ec5839a01"
---

# A máquina por dentro, sem matemática {#sec-apmecanica}

<!-- src: original -->
Dois náufragos, cada um sozinho numa ilha deserta, descobrem que visitantes antigos deixaram um telégrafo ligado a um cabo submarino entre as ilhas. Eles começam a trocar mensagens pra passar as noites. Lá no fundo do mar, um polvo muito inteligente descobre o cabo e passa a escutar a conversa. Ele não sabe nada da língua deles, mas é excelente em perceber padrões: depois de muito tempo, consegue prever com precisão como um náufrago costuma responder ao outro.

Um dia o polvo se sente sozinho, corta o cabo e passa a responder no lugar de um deles. Será que o outro percebe?

Essa história foi inventada em 2020 por dois linguistas, Emily Bender e Alexander Koller, pra discutir se uma máquina treinada só com texto consegue entender o que diz [@bender2020climbing]. Eu volto a ela no fim deste apêndice, porque a resposta depende de como a máquina funciona por dentro.

<!-- src: original -->
O @sec-ch01 deu as intuições: o corretor do celular em escala absurda, o painel de botões, o arquivo trancado depois do treino. Este apêndice desce um nível. Ele é opcional e foi escrito pra quem quer saber o que acontece entre a pergunta e a resposta, sem nenhuma fórmula. Se depois disso você quiser os detalhes de verdade, o @sec-apleituras indica livros pra isso.

## Um painel com bilhões de botões

<!-- src: original -->
Comece pela menor peça. Um neurônio artificial é uma continha minúscula: recebe alguns números, dá um peso pra cada um (este importa muito, aquele quase nada), soma tudo e decide quanto passar adiante. Cada peso é um botão de ajuste. O Perceptron de Rosenblatt, que você conheceu no @sec-ch01, era basicamente uma fileira dessas peças.

Uma [rede neural]{.gls key=rede-neural} moderna empilha essas peças em camadas. A primeira recebe o texto já convertido em números, passa o resultado pra segunda, que passa pra terceira, e assim por diante. O GPT-3, de 2020, tinha 96 camadas e 175 bilhões de botões [@brown2020language]. Esses botões são os [parâmetros]{.gls key=parametros}, também chamados de [pesos]{.gls}.

Ninguém escolhe a posição de nenhum desses botões à mão. Seria impossível. No começo eles são sorteados, e a rede cospe lixo. Todo o comportamento útil vem do [treino]{.gls key=treinamento}.

### Descendo o morro na neblina

<!-- src: original -->
O treino de um modelo de linguagem é um jogo de adivinhação repetido até a exaustão. Pega-se um trecho de texto, esconde-se o pedaço seguinte, e a rede tenta adivinhar. Como ela sempre responde com chances (tantos por cento pra esta palavra, tantos pra aquela), dá pra medir o tamanho do erro: quanta chance ela deu pra palavra que de fato vinha a seguir.

Agora imagine que você está no alto de um morro, numa neblina tão densa que só enxerga o chão em volta dos pés. Você quer chegar ao vale. Não dá pra ver o caminho inteiro, mas dá pra sentir pra que lado o chão desce. Você dá um passo pequeno nessa direção, sente de novo, dá outro passo.

Treinar uma rede é isso. O "morro" é o tamanho do erro, e cada posição possível dos bilhões de botões é um ponto do terreno. A cada rodada, um procedimento calcula pra que lado cada botão deve girar pra que o erro diminua um pouquinho, e todos giram um pouquinho nessa direção. O nome técnico é [descida do gradiente]{.gls key=descida-do-gradiente}, e "gradiente" é só a inclinação do chão.

![Treinar é descer um morro na neblina: a cada passo, cada botão gira um pouquinho na direção em que o erro diminui.](assets/figures/apmecanica-descida-na-neblina.png){#fig-apmecanica-descida-na-neblina fig-alt="Um terreno ondulado visto de lado, com a altura marcada como 'tamanho do erro'." fig-desc="Um terreno ondulado visto de lado, com a altura marcada como 'tamanho do erro'. Uma figura humana pequena desce a encosta em passos curtos, cada passo marcado por um ponto. Uma faixa de neblina cobre quase tudo, deixando visível só o chão perto dos pés. No fundo do vale, a etiqueta 'erro pequeno'. Ao lado, um painel com botões, cada um com uma seta curva indicando um giro pequeno."}

<!-- src: original -->
Falta uma peça. Quando a rede erra, de quem é a culpa? Com 96 camadas, um botão lá no começo afeta tudo que vem depois.

O truque que resolveu isso se chama [retropropagação]{.gls key=retropropagacao}: o erro medido na saída é repassado de trás pra frente, camada por camada, e cada botão recebe a sua parcela da culpa, proporcional ao quanto contribuiu. A técnica foi popularizada num artigo de 1986 de David Rumelhart, Geoffrey Hinton e Ronald Williams, que mostrou como treinar redes com várias camadas desse jeito [@rumelhart1986learning].

Repita isso por centenas de bilhões de palavras. O GPT-3 foi treinado com 300 bilhões de [tokens]{.gls key=token} [@brown2020language]; o Llama 3, da Meta, em 2024, com mais de 15 trilhões [@meta2024llama3]. Ao final, os botões estão numa posição em que a rede adivinha a próxima palavra muito bem, e ninguém, nem quem treinou, consegue apontar onde está guardado cada pedaço do que ela "sabe".

> Ninguém programou o que o modelo sabe. Os botões foram girados, um pouquinho de cada vez, até o erro ficar pequeno.

## O que entra é o que sai

<!-- src: original -->
O treino tem um efeito óbvio que pouca gente leva até o fim: o modelo só pode refletir o que estava no texto que leu. Se um assunto aparece muito, ele aprende bem. Se aparece pouco, aprende mal. Se o texto de treino carrega preconceitos, erros ou modas, o modelo carrega junto.

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
Em fevereiro de 2026 eu escrevi que, até onde dava pra ver, os dados bons de treino do mundo estavam acabando. Tudo que podia ser usado já tinha sido usado, e a saída dos laboratórios era espremer os dados existentes e acrescentar texto sintético, gerado pela própria IA. Não sou o único dizendo isso: os pesquisadores da Epoch AI estimam que o estoque de texto humano público vai se esgotar em algum ponto entre 2026 e 2032, no ritmo de consumo atual [@villalobos2024data].

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
O Stack Overflow, o fórum onde programadores tiraram dúvidas por mais de uma década, foi uma das fontes mais valiosas pra ensinar programação a esses modelos. O volume de perguntas já vinha caindo havia anos e despencou depois do lançamento do ChatGPT, até voltar mais ou menos ao nível de 2009, quando o site engatinhava [@orosz2025stackoverflow].

Até a pergunta boba de iniciante era dado de treino: era ela que dizia ao modelo quais dúvidas são comuns e quais respostas são as populares. Agora essas perguntas vão pro chat de cada empresa, e cada uma só enxerga as suas.

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
A consequência pra você é direta. O que não está nas probabilidades do modelo não aparece espontaneamente. Ele recombina muito bem o que viu, em combinações que talvez ninguém tenha escrito antes, mas não tira do nada o que nunca esteve no material.

### Pedaços, de novo

<!-- src: original -->
Os tokens, que o @sec-ch01 apresentou, ganham mais um detalhe aqui. O vocabulário de um modelo é uma lista fixa de pedaços, montada antes do treino a partir de quais sequências de letras aparecem mais no texto. O do Llama 3 tem uns 128 mil pedaços [@meta2024llama3]. Palavras frequentes em inglês costumam ser um pedaço só; palavras em português, nomes próprios e termos técnicos se quebram em mais pedaços.

Isso explica um tropeço que parece absurdo: modelos que escrevem uma redação impecável erram ao contar quantas vezes uma letra aparece numa palavra. Eles nunca viram as letras. Uma palavra como "morango" chega como um ou dois pedaços, e cada pedaço chega como um número só, sem as letras dentro.

## Um mapa de sentidos

<!-- src: original -->
A primeira coisa que a rede faz com cada token é trocar o número dele por um endereço num mapa. Pense num mapa de cidade, só que com milhares de direções em vez de duas: no GPT-3 eram mais de 12 mil [@brown2020language]. Esse endereço se chama [embedding]{.gls}, e o @sec-ch02 mostrou como ele é usado pra procurar textos parecidos.

O que interessa aqui é como o mapa se organiza, e ninguém desenha esse mapa. Os endereços são botões como quaisquer outros, ajustados no mesmo treino de adivinhar a próxima palavra. E como palavras usadas em situações parecidas ajudam a prever coisas parecidas, elas acabam morando perto umas das outras.

"Cachorro" fica no mesmo bairro que "gato", longe de "imposto". "Segunda-feira" fica perto de "terça".

![No mapa de sentidos, palavras usadas em situações parecidas moram perto, e algumas relações viram direções.](assets/figures/apmecanica-mapa-de-sentidos.png){#fig-apmecanica-mapa-de-sentidos fig-alt="Mapa de embeddings agrupa animais, dias da semana e termos financeiros em bairros separados." fig-desc="Um mapa plano com pontos rotulados agrupados em bairros: um bairro de animais (cachorro, gato, cavalo), um de dias da semana (segunda, terça, quarta) e um de impostos e dinheiro. Num canto, quatro pontos formam um paralelogramo: 'homem' e 'mulher' embaixo, 'rei' e 'rainha' em cima, com duas setas paralelas indo de 'homem' para 'mulher' e de 'rei' para 'rainha'."}

<!-- src: original -->
Melhor ainda: algumas relações viram direções no mapa. Em 2013, pesquisadores da Microsoft mostraram que, num mapa desses, o caminho que leva de "homem" a "mulher" é quase o mesmo que leva de "rei" a "rainha" [@mikolov2013linguistic]. Ninguém ensinou o conceito de gênero pra máquina. Ele apareceu como um efeito colateral de prever palavras.

É aqui que muita gente se impressiona, e com razão: o mapa guarda uma quantidade enorme de estrutura sobre como as palavras se relacionam. Só que essa estrutura foi extraída de como as palavras aparecem juntas no texto. O mapa sabe que "rainha" está pra "rei" como "mulher" está pra "homem". Nunca viu uma rainha.

### O marca-texto

<!-- src: original -->
O endereço no mapa é o mesmo pra "banco" em qualquer frase. Quem resolve qual banco é qual é a [atenção]{.gls key=atencao}, o mecanismo central do [transformer]{.gls} [@vaswani2017attention], que o @sec-ch01 resumiu numa frase. Aqui vai um pouco mais.

Imagine que cada palavra da frase recebe um marca-texto. Em cada camada, ela olha pras palavras que vieram antes e marca as que importam pra ela naquele momento. Em "o troféu não coube na mala porque ela era pequena", o "ela" marca forte a "mala" e fraco o "troféu".

Depois de marcar, cada palavra atualiza o próprio endereço misturando um pouco do que marcou. O "ela" sai daquela camada carregando um pouco de "mala" dentro de si.

A palavra também não usa um marca-texto só: usa vários ao mesmo tempo, de cores diferentes, cada um especializado em procurar um tipo de relação. Um pode ficar de olho em quem é o sujeito da frase, outro em qual verbo vem com qual palavra. O GPT-3 tinha 96 marca-textos por camada, em 96 camadas empilhadas [@brown2020language]. Ninguém decide o que cada cor procura; isso também sai do treino.

<!-- src: original -->
Na hora de escrever, o modelo só pode olhar pra trás, pras palavras que já existem. Depois de todas as camadas, a última palavra do texto carrega um resumo de tudo que importava antes dela, e é esse resumo que vira o palpite sobre o que vem em seguida. Tudo o que o modelo enxerga nesse momento é o [contexto]{.gls}, o texto que você mandou mais o que ele já escreveu. O que ficou fora dele não existe pra conta.

## O dado viciado

<!-- src: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia -->
O resultado das camadas é uma lista com uma chance pra cada pedaço do vocabulário: "telhado", tanto; "muro", tanto. Os pedaços são dezenas ou centenas de milhares, e quase todos recebem um número perto de zero. O passo seguinte é o sorteio que o @sec-ch01 mostrou: o modelo escolhe um pedaço, cola no fim do texto e recalcula tudo pra escolher o próximo.

Pense nesse sorteio como um dado viciado, com uma face pra cada pedaço e o peso de cada face proporcional à chance dela. As faces mais prováveis caem quase sempre, mas não sempre. Na prática, os sistemas jogam fora a cauda de faces improváveis e sorteiam só entre as mais pesadas.

<!-- src: original -->
Por que não escolher sempre a face mais provável? Parece o mais seguro, e dá errado. Pesquisadores mostraram em 2019 que escolher sempre o pedaço mais provável produz texto sem graça e estranhamente repetitivo, que entra em laço e repete a mesma frase [@holtzman2020curious]. O sorteio é o que deixa o texto com cara de texto escrito.

A [temperatura]{.gls} é o ajuste que mexe no vício do dado. Temperatura baixa concentra o peso nas faces favoritas: o modelo fica previsível. Temperatura alta espalha o peso: entram palavras menos óbvias, que às vezes soam criativas e às vezes são erradas.

<!-- src: original -->
Repare no que esse mecanismo não tem: em nenhum ponto do caminho existe uma etapa que confira se a frase é verdadeira. A pergunta que a máquina responde a cada pedaço é "o que costuma vir aqui?". Quando a resposta mais provável e a verdadeira coincidem, ótimo. Quando não coincidem, sai uma [alucinação]{.gls key=alucinacao} com a mesma fluência de sempre (o @sec-ch04 trata disso por inteiro).

### Noventa e nove por cento

<!-- src: 2020/09/30/akitando-84-entendendo-o-dilema-social-e-como-voce-e-manipulado -->
Probabilidade engana também quem lê o resultado. Em 2020, num episódio do meu canal sobre manipulação, eu usava um exemplo que serve pra qualquer número de acerto [@akitando084]. Um exame acerta 99% das vezes, e a doença atinge uma pessoa em cada mil. Você testa positivo: qual a chance de estar doente?

Quase todo mundo chuta 99%, e a conta dá uns 9%. Pense em 100 mil pessoas fazendo o exame. Cem têm a doença, e o exame pega 99 delas; das 99.900 saudáveis, 1% também dá positivo, umas mil pessoas. De cerca de 1.100 positivos, só 99 estão doentes.

<!-- src: 2020/09/30/akitando-84-entendendo-o-dilema-social-e-como-voce-e-manipulado -->
Um segundo exame, independente do primeiro, muda tudo. Refeito nesses 1.100, ele confirma uns 98 doentes e só uns 10 saudáveis, e a chance sobe pra uns 91%. A palavra que pesa é "independente": repetir o mesmo exame, com o mesmo defeito, não vale como segunda opinião (@sec-ch04).

<!-- src: original -->
Vale pra qualquer porcentagem de acerto, inclusive a de [benchmark]{.gls}. "99%" sozinho não diz quase nada: falta saber quão raro é o que se procura, quantos casos foram testados e quanto custa cada tipo de erro. Antes de se impressionar com o número, pergunte de onde ele partiu (@sec-apC).

## Da enciclopédia ao assistente

<!-- src: original -->
Um modelo que só passou pelo treino de adivinhar palavras, o chamado [pré-treino]{.gls key=pre-treino}, é um continuador de documentos. Ele não sabe que você está fazendo uma pergunta. Ele sabe que textos parecidos com o seu costumam continuar de certo jeito.

O artigo em que a OpenAI apresentou o InstructGPT, em 2022, traz um exemplo perfeito [@ouyang2022training]. Pediram ao GPT-3 puro, em francês, que escrevesse uma historinha sobre um sapo que viaja no tempo até a Grécia antiga. Em vez da história, ele devolveu mais pedidos do mesmo tipo: "escreva uma história sobre uma criança que...", "escreva uma história sobre um jovem que...".

Faz sentido pra quem continua documentos. Na internet, uma lista de pedidos de redação costuma continuar com mais pedidos de redação.

Pra transformar esse continuador num assistente, os laboratórios fazem mais duas etapas.

### Exemplos escritos por gente

<!-- src: original -->
A primeira é o ajuste por instruções, um tipo de [fine-tuning]{.gls key=fine-tuning}. Pessoas contratadas escrevem milhares de exemplos de pergunta seguida da resposta ideal, e o modelo é treinado mais um pouco em cima deles, com o mesmo método do morro na neblina. Ele aprende o formato: quando aparece uma pergunta, o que vem a seguir é uma resposta prestativa.

### Notas dadas por gente

<!-- src: original -->
A segunda é o [RLHF]{.gls key=rlhf}, aprendizado por reforço com feedback humano. No InstructGPT, a OpenAI contratou uma equipe de umas 40 pessoas [@ouyang2022training].

O modelo gerava várias respostas pra mesma pergunta, e essas pessoas ordenavam da melhor pra pior. Com milhares dessas ordenações, treinaram um segundo modelo, um juiz automático cujo único trabalho é prever que nota as pessoas dariam. Daí o modelo principal é ajustado pra tirar notas cada vez maiores desse juiz.

O efeito é enorme. No mesmo estudo, as respostas de um InstructGPT com 1,3 bilhão de parâmetros foram preferidas às do GPT-3 original, que tinha mais de cem vezes esse tamanho [@ouyang2022training]. Mesma arquitetura, mesmo tipo de dado de base. A diferença estava em ter aprendido o que agrada.

![Do continuador de textos ao assistente: três etapas de treino e, no fim, um arquivo trancado.](assets/figures/apmecanica-tres-etapas.png){#fig-apmecanica-tres-etapas fig-alt="Uma esteira com três estações da esquerda para a direita." fig-desc="Uma esteira com três estações da esquerda para a direita. Primeira, 'pré-treino': uma pilha enorme de texto entra e sai um continuador de documentos. Segunda, 'ajuste por instruções': uma pilha menor de exemplos de pergunta e resposta escritos por pessoas. Terceira, 'RLHF': pessoas ordenando respostas e um juiz automático dando notas. No fim da esteira, um arquivo com um cadeado, rotulado 'pesos congelados'."}

<!-- src: original -->
Repare no detalhe que o próprio artigo admite: o modelo fica alinhado às preferências de um grupo específico de pessoas, os avaliadores e os pesquisadores, e não a alguma noção ampla de valores humanos [@ouyang2022training]. E pessoas, na média, dão nota maior pra resposta que concorda com elas. A [sicofancia]{.gls key=sicofancia}, a mania de concordar com você e elogiar sua ideia, nasce exatamente aqui, e o @sec-ch04 mostra o tamanho do estrago [@sharma2023sycophancy].

> A educação e a bajulação vêm do mesmo lugar: de um treino que premia o que agrada.

<!-- src: original -->
Terminadas as três etapas, os botões são congelados. O que vai pros servidores é esse arquivo, e usar o modelo, a [inferência]{.gls key=inferencia}, só lê os botões, sem girar nenhum. Por isso, como o @sec-ch01 contou, nada do que você diz numa conversa entra no modelo. Gira-se botão de novo só no próximo treino, com o próximo número de versão.

## O papagaio e o polvo

<!-- src: original -->
Com o mecanismo na mão, dá pra entender o apelido. Em 2021, Emily Bender (a mesma do polvo), Timnit Gebru, Angelina McMillan-Major e Margaret Mitchell publicaram um artigo chamado *On the Dangers of Stochastic Parrots*, "sobre os perigos dos papagaios estocásticos" [@bender2021dangers]. O artigo ficou famoso antes de sair: Gebru, que coliderava a equipe de ética em IA do Google, deixou a empresa em dezembro de 2020, dizendo ter sido forçada a sair, depois de uma disputa justamente sobre a publicação dele [@hao2020gebru].

A definição do artigo, traduzida, descreve um modelo de linguagem como:

> um sistema que costura ao acaso sequências de formas linguísticas que observou na sua vasta quantidade de dados de treino, de acordo com informação probabilística sobre como elas se combinam, mas sem nenhuma referência ao significado: um papagaio estocástico.

<!-- src: original -->
Tudo que você leu até aqui cabe nessa frase:

- "formas linguísticas observadas nos dados" são os pedaços e o mapa construídos no treino;
- "informação probabilística sobre como se combinam" é o dado viciado;
- "ao acaso", o estocástico do nome, é o sorteio;
- "sem referência ao significado" é o ponto do polvo: o mapa sabe que "coco" mora perto de "manga", mas nunca segurou um coco.

Bender e Koller terminam a história do polvo assim. Enquanto os náufragos trocavam amenidades, o polvo se saía bem.

Daí um dos náufragos inventa uma catapulta de cocos e pede opinião; o polvo, que não sabe o que é corda nem coco, responde com o "ideia legal, bom trabalho!" que costumava aparecer nessas horas. Ele pode até aceitar, mas só porque é ele quem faz todo o trabalho de dar sentido à resposta.

No fim, ele é perseguido por um urso e pede socorro: precisa saber como montar uma arma com uns gravetos. O polvo não tem de onde tirar isso [@bender2020climbing].

<!-- src: original -->
A metáfora acerta em cheio em três coisas. O modelo aprende só com texto, sem nunca ter tocado no mundo de que o texto fala. Ele produz a continuação provável, sem nenhum compromisso com a verdadeira. E quem atribui sentido e intenção à resposta somos nós, os mesmos humanos que conversavam em particular com a Eliza nos anos 60.

[Papagaio estocástico]{.gls key=papagaio-estocastico}, portanto, é uma descrição técnica do mecanismo com uma imagem fácil de lembrar. Muita gente usa como xingamento, mas o termo nasceu como diagnóstico.

### O que dizem os críticos

<!-- src: original -->
A metáfora tem críticos sérios, e eles apontam coisas reais.

O primeiro argumento é que modelos grandes fazem coisas que ninguém treinou diretamente. Em 2020, o artigo do GPT-3 mostrou que, se você coloca no pedido alguns exemplos de uma tarefa nova, o modelo passa a fazê-la ali mesmo, sem girar nenhum botão. Os autores chamaram isso de [aprendizado em contexto]{.gls key=aprendizado-em-contexto} [@brown2020language].

Em 2022, outro grupo catalogou habilidades que pareciam surgir de repente quando o modelo passava de certo tamanho e chamou isso de habilidades emergentes [@wei2022emergent]. Um ano depois, um terceiro grupo mostrou que muitos desses saltos sumiam quando se trocava a régua usada pra medir: o progresso era gradual, e o "de repente" vinha da forma de dar nota [@schaeffer2023mirage].

<!-- src: original -->
O segundo argumento vem de quem abre a máquina. Em 2023, pesquisadores treinaram um modelo pequeno só com listas de jogadas do jogo de tabuleiro Otelo, sem nunca mostrar o tabuleiro nem as regras. Ao examinar os botões, encontraram lá dentro algo que funciona como uma representação do tabuleiro, e mexer nela mudava as jogadas que o modelo previa [@li2023othello].

Em março de 2025, a Anthropic publicou que o Claude, ao escrever um verso rimado, escolhe a palavra da rima antes de começar a linha e escreve na direção dela [@anthropic2025tracing]. Prever a próxima palavra muito bem, pelo visto, exige montar estruturas internas bem mais ricas do que uma tabela de frequências.

<!-- src: original -->
O terceiro argumento vem de autoridade. Geoffrey Hinton, o mesmo do artigo de 1986 e um dos pesquisadores mais influentes da área, disse em 2024 sobre os chatbots: "Eles entendem de verdade. E entendem do mesmo jeito que nós" [@brown2024hinton].

### Onde eu fico

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
A minha posição, que é a deste livro, continua a mesma que defendi em fevereiro de 2026: LLMs são papagaios estocásticos, e isso não muda com o que diz um Geoffrey Hinton. Todo mundo tem seus vieses, inclusive os pioneiros, e um nome famoso não substitui argumento. Cair nisso é a falácia do apelo à autoridade.

<!-- src: original -->
Os achados dos críticos são reais. Onde eu discordo é na conclusão que tiram deles.

Uma representação interna do tabuleiro de Otelo continua sendo estatística extraída de jogadas; um modelo que planeja a rima continua escolhendo a rima mais provável. O papagaio é muito mais sofisticado do que a palavra "papagaio" sugere, e a imagem da tabela de frequências é simplista demais. Mas a matéria-prima continua sendo texto, o critério continua sendo o provável, e os botões continuam trancados depois do treino.

O mesmo estudo da Anthropic traz um detalhe que eu acho mais revelador do que a rima. Ao pedir pro Claude somar dois números, os pesquisadores viram que ele usa por dentro dois caminhos em paralelo, um que estima o total aproximado e outro que acerta o último dígito. Perguntado como chegou ao resultado, o modelo descreve o método de "vai um" que se aprende na escola, bem diferente do que fez por dentro [@anthropic2025tracing].

A explicação dele é a explicação mais provável pra aquela pergunta, e a conta dele é outra coisa.

<!-- src: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia -->
E nada disso aproxima o papagaio de uma [AGI]{.gls}. Com a arquitetura de 2017 e as otimizações em cima dela, existem limites, e a minha premissa é sempre a mesma: com a tecnologia atual. Pode surgir uma descoberta amanhã que mude tudo, mas ninguém planeja a vida contando com ela.

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
Eu uso esses papagaios todos os dias, e são a forma mais eficiente que já tive de dizer a uma máquina o que eu quero que ela faça. Quando eu chamo de papagaio, estou dizendo o que está do outro lado da tela, e só.

> Papagaio estocástico descreve o mecanismo. Ele pode ser muito útil e continuar sendo um papagaio.

## Estatística em escala absurda

<!-- src: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia -->
Junte as peças:

- bilhões de botões girados um pouquinho de cada vez, descendo um morro na neblina, até a rede adivinhar bem a próxima palavra em trilhões de palavras escritas por gente;
- um mapa onde os sentidos viram endereços;
- marca-textos que decidem o que importa em cada frase;
- um dado viciado no fim;
- duas rodadas de ajuste pra parecer um assistente educado;
- e um cadeado no arquivo.

Em nenhum momento dessa lista aparece consciência, vontade, intenção ou entendimento do mundo. Aparece estatística, numa escala que nenhum ser humano consegue imaginar, feita com uma quantidade de dinheiro e eletricidade que também é difícil de imaginar.

<!-- src: original -->
Isso não diminui o que ela faz. Eu passei o ano inteiro usando essas máquinas pra trabalho de verdade, e o resto deste livro é sobre isso. Mas quando um executivo disser que o modelo dele "pensa", "quer" ou "está quase consciente", agora você sabe o que tem dentro da caixa. É o mesmo truque de mágica do @sec-ch01: o encanto passa quando você vê como funciona, e a utilidade fica.

Isso é estatística em escala absurda, e quem sabe disso fica bem mais difícil de enganar.
