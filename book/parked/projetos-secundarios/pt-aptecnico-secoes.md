<!-- Parked 2026-10-14: sections cut from book/pt/aptecnico.md (author: Frank projects are footnote-worthy). -->

## Frank Investigator: como os três modelos votam {#sec-aptecnico-investigator}

<!-- src: original -->
Em @sec-ch04 eu conto o Frank Investigator, um programa que fiz em março de 2026 pra examinar notícias: ele quebra a matéria em afirmações, pede a três modelos de empresas diferentes que avaliem cada uma e deixa uma fonte primária passar por cima de todos eles. O capítulo fica na ideia. Aqui vai a conta de como os votos viram um veredito, e por que a confiança que cada modelo declara entra nela mesmo assim.

![Três modelos votam com pesos diferentes; uma fonte primária contrária derruba o resultado.](assets/figures/ch04-tres-juizes.png){#fig-ch04-tres-juizes fig-alt="Três caixas representando modelos de empresas diferentes: modelo A e modelo B votam 'sustentado 40%', modelo C vota 'misto 95%'. Os votos vão para uma balança que pende para 'misto'. Ao lado, um documento marcado 'fonte primária' com um carimbo 'veto: no máximo 60%' trava o resultado em 'misto, no máximo 60%'. Embaixo, cinco jornais do mesmo grupo viram um só ('mesmo grupo = uma voz'), e três jornais ligados por setas em círculo representam a citação circular."}

### O voto ponderado

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
Naquele março, os três juízes eram o Claude Sonnet 4.6, o GPT-5.4 e o Gemini 3.1 Pro. Cada um devolve, pra cada afirmação, um veredito e uma confiança. A votação é ponderada por essa confiança, em vez de contar maioria simples: as confianças somam por veredito. Se dois modelos dizem "sustentado" com 40% de confiança cada e um diz "misto" com 95%, o "misto" vence, porque 95 pesa mais do que 80.

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
Quanto mais distantes as opiniões, mais a confiança final cai. E se um modelo começa a dar respostas inconsistentes, ele vai pra quarentena e os outros dois seguem sozinhos.

### Por que a confiança declarada ainda entra

<!-- src: original -->
O próprio @sec-ch04 mostra que o tom seguro de um modelo não diz nada sobre a veracidade, e a confiança que ele declara é um sinal fraco pelo mesmo motivo. Dentro do programa, ela só faz um trabalho: decidir o veredito quando os três discordam, sem fingir que dois votos fracos valem mais do que um forte. Ela nunca decide sozinha o que é verdade, porque duas regras ficam acima dela: o veto da fonte primária e o desconto das fontes repetidas.

### O veto e o teto de 60%

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
Se uma fonte primária (o dado oficial, a decisão judicial, o estudo original) contradiz uma afirmação, a confiança fica travada em no máximo 60% e o veredito é forçado pra "misto", mesmo que os três modelos digam "sustentado". Se cinco matérias "confirmam" a afirmação mas todas pertencem ao mesmo grupo de comunicação, o sistema conta uma voz só e reduz o peso.


## Frank Sherlock: o teste dos modelos de visão e a publicação em três sistemas {#sec-aptecnico-sherlock}

<!-- src: original -->
Em @sec-ch07 eu conto o Frank Sherlock, um programa que fiz em fevereiro de 2026 pra catalogar fotos e documentos por conteúdo, com um modelo de visão rodando na minha própria placa de vídeo. O capítulo guarda a lição, meça antes de escolher. Aqui ficam os números do teste que fiz antes de escrever o aplicativo, a conta de custo e o que deu trabalho pra publicar o programa em Linux, Mac e Windows.

### Os modelos de visão, medidos

<!-- src: 2026/02/23/vibe-code-fiz-um-indexador-inteligente-de-imagens-com-ia-em-2-dias -->
Antes de escrever uma linha do aplicativo, separei imagens com a classificação correta registrada e comparei os candidatos no mesmo terreno. Um modelo de visão aberto de 7 bilhões de [parâmetros]{.gls key=parametros}, o Qwen2.5-VL 7B, ganhou em todas as medidas do LLaVA 13B, quase duas vezes maior, e ainda foi três vezes mais rápido.

A versão gigante do mesmo modelo, com 32 bilhões, acertou uma imagem a mais num grupo de 16 e levou 29 vezes mais tempo. Pra quem vai processar centenas de milhares de arquivos, isso transforma um trabalho de seis horas num trabalho de uma semana.

<!-- src: 2026/02/23/vibe-code-fiz-um-indexador-inteligente-de-imagens-com-ia-em-2-dias -->
Os modelos mais novos da mesma família, o Qwen3-VL de 8 bilhões e o de 30 bilhões, testados com três repetições cada, foram piores na minha tarefa: acertaram o tipo de arquivo bem menos vezes do que o 7B e devolviam respostas truncadas.

### A conta de padeiro

<!-- src: 2026/02/23/vibe-code-fiz-um-indexador-inteligente-de-imagens-com-ia-em-2-dias -->
Classificar meio milhão de arquivos na minha [GPU]{.gls key=gpu} levaria quase um mês ligado e custaria uns 34 dólares de energia. Pela API de visão de uma empresa de nuvem, a um centavo de dólar por imagem, seriam uns 5 mil dólares. É conta feita no papel de pão, mas a ordem de grandeza decide sozinha.

### Do índice ao reconhecimento de rostos, versão por versão

<!-- src: 2026/03/01/software-nunca-esta-pronto-4-projetos-a-vida-pos-deploy-e-por-que-one-shot-prompt-e-mito -->
A primeira versão pública foi a 0.1. Nos quatro dias seguintes, 53 commits levaram o programa da versão 0.3 à 0.7: detecção de fotos duplicadas, depois vídeos em onze formatos, e na 0.7 a detecção de rostos, com agrupamento dos parecidos e nome pra cada pessoa. Foram sete versões publicadas em sete dias.

### Três sistemas, três jeitos de quebrar

<!-- src: 2026/03/01/software-nunca-esta-pronto-4-projetos-a-vida-pos-deploy-e-por-que-one-shot-prompt-e-mito -->
No começo de março, o projeto tinha 103 commits, umas 28 mil linhas de código e 621 testes. Dezessete daqueles commits foram só pra fazer o programa compilar e ser publicado direito nos três sistemas. O Windows escreve caminhos de arquivo de um jeito que quebra comparações de texto; o Mac exige que o programa seja assinado e registrado junto à Apple antes de abrir sem alarme.

