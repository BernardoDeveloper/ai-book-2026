---
id: antes
chapter: "Antes de começar: o que este livro não explica"
sources: []
refs_projects: ["docs/research/FURTHER-READING.md"]
blog_commit: "cc8b467dd4d6d3b5c57fad6bb6fae70ec5839a01"
---

# Antes de começar: o que este livro não explica {#sec-antes .unnumbered}

<!-- src: original -->
Este livro dá intuições sobre como essas máquinas funcionam, e para por aí. O @sec-ch01 explica o que é um modelo de linguagem, por que ele trabalha com pedaços de palavras, a diferença entre treinar um modelo e usá-lo, e por que ele não aprende nada com você depois de pronto. São imagens do dia a dia, sem conta nenhuma, e bastam pra acompanhar a história.

O que eu deixei de fora de propósito é a mecânica por dentro:

- como uma [rede neural]{.gls key=rede-neural} aprende, com [descida do gradiente]{.gls key=descida-do-gradiente} e [retropropagação]{.gls key=retropropagacao};
- o que são [embeddings]{.gls key=embedding}, as listas de números que representam o sentido de um texto;
- como um [transformer]{.gls}, a arquitetura por trás de todos esses modelos, e o seu mecanismo de [atenção]{.gls key=atencao} funcionam;
- como o [pré-treino]{.gls key=pre-treino} e o [RLHF]{.gls} (aprendizado por reforço com feedback humano) transformam um amontoado de texto num assistente educado.

<!-- src: original -->
Cada um desses assuntos pede um livro inteiro, e esses livros existem, escritos por gente que pesquisa ou constrói essas coisas. Um livro de narrativa que tentasse fazer o mesmo viraria apostila na página dez.

## Por que vale a pena saber

<!-- src: original -->
Ainda assim, este livro fica melhor se você entender esses mecanismos antes. Várias afirmações das Partes I e III se apoiam neles. Quando eu digo que o modelo não aprende com a sua conversa, que ele concorda com você porque foi treinado pra agradar, ou que cada geração nova custa muito mais pra melhorar muito menos, estou resumindo consequências de como o treino funciona.

<!-- src: original -->
Quem conhece a mecânica lê essas frases como conclusão. Quem não conhece precisa confiar em mim, e o livro inteiro é um pedido pra você não confiar cegamente em ninguém, inclusive em mim.

<!-- src: original -->
Dito isso, ninguém precisa fazer lição de casa antes de virar a página. O livro foi escrito pra ser lido sem nada disso, e a história se sustenta sozinha.

> Você não precisa saber como o motor funciona pra entender por que o carro bateu. Mas, se um dia quiser abrir o capô, as indicações estão aqui.

<!-- src: original -->
Se quiser um meio-termo, existe um apêndice opcional, *A máquina por dentro, sem matemática* (@sec-apmecanica). Em poucas páginas e sem nenhuma fórmula, ele mostra o painel de botões, a descida do morro na neblina, o mapa de sentidos e o marca-texto da atenção. E termina explicando de onde veio o apelido [papagaio estocástico]{.gls key=papagaio-estocastico}, o que ele captura bem e por que eu concordo com ele. Dá pra ler agora, no meio do caminho ou no fim.

## Pra quem quiser ir mais fundo

<!-- src: ref:docs/research/FURTHER-READING.md -->
A lista abaixo é curta de propósito e vai do mais fácil ao mais técnico. Conferi cada item em outubro de 2026: autor, editora, se existe em português e se dá pra ler de graça, legalmente. A maior parte está só em inglês, e eu aviso quando não está.

### Para qualquer pessoa

- Timothy B. Lee e Sean Trott, *Grandes modelos de linguagem, explicados com o mínimo de matemática e jargão*: o caminho mais curto, gratuito e com tradução oficial em português do Brasil [@lee2024modelos].
- Stephen Wolfram, *What Is ChatGPT Doing ... and Why Does It Work?*: da próxima palavra até o transformer, com figuras; o ensaio completo é gratuito no site do autor, e há edição de Portugal, *O Que Faz o ChatGPT e Como Funciona* [@wolfram2023chatgpt].
- Melanie Mitchell, *Artificial Intelligence: A Guide for Thinking Humans*: uma pesquisadora explica como as redes aprendem e onde falham, contra o hype; é anterior ao ChatGPT [@mitchell2019guide].
- John D. Kelleher, *Deep Learning*: livro de bolso que já explica descida do gradiente e retropropagação, ponte pro nível seguinte [@kelleher2019deep].

### Com um pouco de matemática

- Michael Nielsen, *Neural Networks and Deep Learning*: o clássico mais gentil sobre redes neurais e retropropagação, gratuito online; para antes dos transformers [@nielsen2015neural].
- François Fleuret, *The Little Book of Deep Learning*: menos de 200 páginas do tamanho de uma tela de celular, do treino ao transformer; PDF gratuito [@fleuret2023little].
- Simon J. D. Prince, *Understanding Deep Learning*: livro-texto moderno e muito bem ilustrado, pra consultar depois dos dois anteriores; PDF gratuito [@prince2023understanding].

### Mão na massa (com Python)

- Sebastian Raschka, *Build a Large Language Model (From Scratch)*: constrói um modelo no estilo do GPT, peça por peça; o livro é pago, o código é gratuito [@raschka2024build].
- Jay Alammar e Maarten Grootendorst, *Hands-On Large Language Models*: quase 300 ilustrações originais; tem uma tradução feita com auxílio de IA, *Modelos de linguagem grandes e práticos*, só na plataforma por assinatura da O'Reilly [@alammar2024handson].

### Vídeos gratuitos

- Grant Sanderson (3Blue1Brown), série *Neural networks*: a explicação visual mais clara de neurônios, gradiente, retropropagação e atenção; parte dela tem dublagem ou legendas em português do Brasil [@sanderson2017neural].
- Andrej Karpathy, *Intro to Large Language Models* e *Deep Dive into LLMs like ChatGPT*: pré-treino, ajuste fino e RLHF explicados pro público geral; em inglês, só com legendas automáticas [@karpathy2023intro; @karpathy2025deepdive].
- Andrej Karpathy, *Neural Networks: Zero to Hero*: escreve a retropropagação e um GPT pequeno ao vivo; exige Python firme [@karpathy2022zerotohero].
- Jay Alammar, *The Illustrated Transformer*: os diagramas com que muita gente aprendeu transformers; texto gratuito, sem tradução pro português [@alammar2018illustrated].

<!-- src: original -->
Se você não tem tempo pra nada disso, comece pelo texto de Lee e Trott ou pelos primeiros vídeos do 3Blue1Brown. E se nem isso, tudo bem: vire a página. A história começa em fevereiro de 2026, com uma frase que eu nunca disse circulando pela internet com o meu nome.
