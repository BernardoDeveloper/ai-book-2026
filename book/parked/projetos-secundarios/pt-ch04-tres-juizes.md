<!-- Parked 2026-10-14: the full section as it stood before the trim (book/pt/ch04.md). -->

## Três juízes e um veto

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
O Frank Investigator foi desenhado em cima desses dois defeitos. Nada nele torna o sistema perfeito, mas cada decisão ataca um deles. Vale a pena olhar as decisões uma por uma, porque quase todas dá pra copiar quando você mesmo usa um chatbot.

### Ninguém dá opinião

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
A primeira decisão foi que nenhum ser humano formula a pergunta. Não existe um pedido aberto do tipo "analise este artigo". Cada etapa tem perguntas fechadas e específicas: liste as falácias neste trecho, identifique que informações de contexto estão faltando, compare a manchete com o corpo do texto.

O modelo nunca sabe se quem está operando concorda ou discorda do artigo, porque o operador não opina em nenhum momento. Sem opinião na pergunta, a sicofancia fica sem ter a quem agradar.

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
Contra a alucinação, toda etapa que usa um modelo leva uma instrução fixa, escrita em maiúsculas pra deixar claro que é sério. Traduzindo:

> *"Só cite endereços, fontes, afirmações, citações e dados que estejam EXPLICITAMENTE no material que você recebeu. Não invente, não chute, não fabrique. Se não dá pra verificar algo a partir do texto fornecido, marque como não verificável; nunca preencha os detalhes."*

A instrução reduz bastante a alucinação, sem eliminar.

### Três empresas na mesma mesa

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
A segunda defesa é não confiar num modelo só. Naquele março, cada afirmação era avaliada por três modelos de três empresas diferentes: o Claude Sonnet 4.6, da Anthropic, o GPT-5.4, da OpenAI, e o Gemini 3.1 Pro, do Google. Quando um deles alucina, os outros dois geralmente discordam.

<!-- src: original -->
Concordância entre os três também não prova nada sozinha, e o programa sabe disso: o voto dos modelos nunca tem a última palavra.

### A fonte primária manda

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
A salvaguarda que eu considero mais importante é o veto da [fonte primária]{.gls key=fonte-primaria}, que é a origem do dado: a estatística oficial, a decisão judicial, o estudo original. Se uma fonte primária contradiz uma afirmação, a afirmação não sai como "sustentada", mesmo que os três modelos digam que sim. A fonte primária manda. Como os votos são contados e quanto o veto pesa está em @sec-aptecnico-investigator.

![Três modelos de três empresas julgam a mesma afirmação; se a fonte primária a contradiz, ela não sai como sustentada, mesmo com os três dizendo que sim.](assets/figures/ch04-juizes-simples.png){#fig-ch04-juizes-simples fig-alt="Uma caixa com a afirmação manda setas pra três caixas, modelo da empresa A, B e C, cada uma marcada sim. As três setas se juntam numa caixa: os três dizem sustentada. Dali, uma seta leva ao resultado em destaque: não sai como sustentada, porque, de cima, um documento marcado fonte primária desce com uma seta vermelha marcada contradiz. Embaixo, a frase: a fonte primária manda."}

Dez jornais repetindo a mesma coisa sem fonte primária continuam valendo zero. Na mesma linha, se cinco matérias "confirmam" uma afirmação mas todas pertencem ao mesmo grupo de comunicação, o sistema sabe que é uma voz só e reduz o peso.

<!-- src: 2020/09/30/akitando-84-entendendo-o-dilema-social-e-como-voce-e-manipulado -->
Em 2020, num vídeo do meu canal, eu reclamava que a gente "confunde quantidade de evidência com a qualidade das evidências" [@akitando084]. O exemplo era um exame médico: um segundo exame só muda a conta se for independente do primeiro, feito por outro laboratório (a conta inteira está em @sec-apmecanica). Três modelos apoiados na mesma fonte ruim são o mesmo exame repetido três vezes.

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
E tem a cadeia circular. Quando dez veículos repetem a mesma afirmação citando uns aos outros, o resultado tem que mostrar que a evidência anda em círculo. Volume de cobertura não é medida de verdade.

> Mil cópias de uma afirmação valem menos que o documento de onde ela deveria ter saído.

### O que fica de fora

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
Construindo e rodando o programa, a lição que mais me surpreendeu foi que o sinal mais forte de manipulação costuma estar no que o texto deixa de dizer. Por isso uma das etapas lista as perguntas que o artigo deveria ter respondido e não respondeu, e sai buscando evidência pra cada uma.

<!-- src: original -->
Um exemplo inventado mostra o mecanismo. Imagine uma cidade fictícia que, em janeiro, aumenta a passagem de ônibus de 5 pra 6 reais. Em março, depois de muita reclamação, baixa pra 5,50.

Uma manchete diz "prefeitura reduz passagem de ônibus". Outra diz "prefeitura recua de parte do aumento". As duas são verdadeiras, e deixam no leitor impressões opostas.

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
Ninguém mentiu, tecnicamente. A escolha do enquadramento já faz o trabalho. Esse tipo de manipulação é o mais difícil de pegar, porque cada frase, isolada, se defende sozinha. Comparar coberturas diferentes do mesmo fato é a forma mais eficaz que encontrei de enxergar o buraco.

### Nenhum veredito

<!-- src: 2026/03/27/ensinando-a-questionar-noticias-frank-investigator -->
A última decisão: o Frank Investigator não diz o que é verdade e o que é mentira. O resultado é um relatório com pontos fortes e fracos, sem selo de "verdadeiro" ou "falso".

Mesmo com todas as salvaguardas, a contra-evidência buscada automaticamente pode não ser a mais relevante. As falácias apontadas podem ser falsos positivos. A análise de quantos veículos repetem a mesma coisa depende do que a busca na web devolveu naquele momento.

Use os relatórios como ponto de partida pra formar a sua própria opinião. E isso vale pra qualquer coisa que um chatbot te diga. Ele pode ajudar a fazer as perguntas certas, achar o documento certo, entender um termo difícil. A conclusão é sua.

