<!--
PARKED (author decision, 2026-10-13; ledger: book/integration.yml, Genesys PI entry).
Origin: book/pt/ch12.md, section "## O mistério brasileiro", which sat between
"### O tamanho do que eu provei" (end of the Kimi case) and "## O que dá pra saber de fora".
The block below is verbatim, with its provenance markers and figure.
Restore: paste it back at that spot; re-add posts
2026/09/23/llm-benchmark-v4-genesys-pi-novo-competidor-brasileiro and
2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro
to ch12's front-matter sources (and remove them from `excluded` in book/outline.yml);
restore "como no Kimi e no Genesys PI" in the closing section.
Also restore the ch12 refs_projects entries lua-forensics/FINDINGS.md and
model-forensics/FINDINGS.md, the @fig-ch12-impressao-digital credit, and the apA entries.
-->

## O mistério brasileiro

<!-- src: 2026/09/23/llm-benchmark-v4-genesys-pi-novo-competidor-brasileiro -->
Duas semanas depois, a mesma pergunta me alcançou de um lado inesperado. Em setembro de 2026, gente da LUA Vision, uma empresa de São Paulo fundada no fim de 2025, me procurou pelo LinkedIn oferecendo acesso de teste ao Genesys PI, o modelo deles, lançado em abril [@luavision2026empresa]. O argumento era que eles treinavam um modelo próprio pra realidade brasileira, com direito trabalhista, CLT versus PJ e estrutura fiscal local, em vez de revender modelo estrangeiro com uma camada de português por cima.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Antes de qualquer número, o que eu registrei nos dois textos que escrevi sobre o caso. Não tenho relação comercial nenhuma com a LUA Vision. Não sou sócio nem investidor, não assinei contrato nem acordo de confidencialidade, e não recebi nada além de uma chave de avaliação gratuita. Nada do que publiquei passou por eles antes.

<!-- src: original -->
E um aviso de prudência, porque o caso continua em aberto: não há informação suficiente pra uma conclusão sobre o Genesys PI nem sobre a LUA Vision. O que vem a seguir é o registro dos testes que eu fiz, e não deve ser lido como recomendação nem como aval de produto, empresa ou investimento.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Nunca vi dado interno nenhum; tudo a seguir é teste de caixa-preta em cima da API, mais informação pública.

### O que o modelo fez

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Na primeira rodada, em 23 de setembro, rodei os dois níveis do modelo, chamados House e Enterprise, na versão do meu benchmark com armadilhas de segurança plantadas ao longo do projeto, que o @sec-ch11 explica. O House fez 83,5, empatado com o Grok 4.7, no meio do pelotão. O Enterprise ficou um degrau abaixo.

<!-- src: 2026/09/23/llm-benchmark-v4-genesys-pi-novo-competidor-brasileiro -->
Naquele dia eu escrevi, empolgado, que sempre tinha achado inviável treinar um [modelo de fronteira]{.gls key=modelo-de-fronteira} do zero no Brasil, e que a LUA tinha me provado errado. Uma semana depois, com mais testes na mão, eu já separava com bem mais cuidado o que tinha medido do que a empresa dizia.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
A empresa corrigiu um defeito na API e eu rodei de novo. O House subiu pra 95,5, empatado com alguns dos melhores da tabela. Mas o Enterprise ficou praticamente igual, e na mesma semana o GPT-5.5 caiu de 100 pra 91 numa repetição idêntica, sem mudar nada. Uma rodada só não separa melhoria de ruído (o assunto é de @sec-ch11), então mantive a primeira rodada como entrada oficial da tabela, justamente pra não premiar uma execução isolada.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Também pedi pra ele auditar a segurança do meu sandbox de código aberto, o de @sec-ch15, em paralelo com outro modelo. Numa comparação pequena, de um projeto e uma rodada, o relatório do Genesys PI foi o mais forte dos dois, e eu fui consertar a lista dele.

O modelo existe, funciona e é bom no que eu medi. A pergunta que todo mundo me mandou foi outra.

### "Isso não é um Qwen com adesivo?"

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Eu também fiz essa pergunta. O consenso da indústria é que treinar modelo de fronteira custa dezenas ou centenas de milhões de dólares, e uma empresa pequena, sem rodada bilionária de investimento, não deveria chegar perto. A hipótese mais barata é existir outro modelo por baixo.

Chegaram até mim três versões da suspeita:

- é um Qwen ou um DeepSeek, modelos abertos chineses, com outro nome;
- é o gpt-oss, o modelo aberto da OpenAI, com outra roupa;
- a API é só um intermediário que repassa os pedidos pro Claude ou pro GPT.

Numa caixa-preta, sem acesso aos pesos, é impossível afirmar com certeza de onde um modelo veio. O que dá pra fazer é excluir hipóteses, uma de cada vez.

### A impressão digital

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Antes de processar qualquer texto, todo modelo quebra o texto em pedaços, os [tokens]{.gls key=token} de @sec-ch01. Quem faz essa quebra é o [tokenizador]{.gls}, um vocabulário com regras próprias, e cada família de modelo tem o seu. A mesma frase em chinês, a mesma sequência de dígitos, o mesmo emoji composto viram quantidades diferentes de tokens em famílias diferentes.

E o ponto decisivo: quem ajusta ou continua treinando um modelo herda o tokenizador dele. Trocar o vocabulário exige treinar de novo do zero. Por isso o tokenizador funciona como uma impressão digital de linhagem.

<!-- src: ref:llm-coding-benchmark/lua-forensics/FINDINGS.md -->
Medi quantos tokens a API da LUA cobrava por uma bateria de textos: chinês, português acentuado, inglês, sequências de dígitos, emojis compostos. Descontei o prompt de sistema que eles injetam e comparei com os tokenizadores das principais famílias, rodando na minha máquina. Uma sequência de dígitos que o Qwen e o DeepSeek contam como 200 tokens, a LUA contava como 67. Somando as diferenças de todos os textos, o tokenizador público da OpenAI, chamado o200k, ficou a 2 tokens de distância.

O mais próximo depois dele, o do Llama 3, ficou a 68. O do Qwen, a quase 200.

![A mesma frase vira quantidades diferentes de tokens em cada família de modelo; a contagem funciona como impressão digital.](assets/figures/ch12-impressao-digital.png){#fig-ch12-impressao-digital fig-alt="Tabela com quantos tokens o mesmo trecho em chinês, a mesma sequência de dígitos e o mesmo emoji composto viram em cada tokenizador. A API testada conta 42, 67 e 168. O o200k, da OpenAI, conta 42, 67 e 169, e fica a 2 tokens de distância somando todos os textos. Na distância somada de todos os textos, Llama 3 fica a 68, cl100k a 134, Qwen a 193, DeepSeek a 255 e Mistral a 289. Embaixo, a nota: mesma contagem não quer dizer mesmos pesos."}

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Em setembro, isso derrubou a primeira suspeita. Nenhum Qwen, DeepSeek, Llama ou Mistral usa esse vocabulário, e nenhum ajuste em cima deles conseguiria adquiri-lo.

A segunda também enfraqueceu. O gpt-oss usa uma variante do mesmo vocabulário com marcadores especiais próprios, e na API da LUA cada um desses marcadores custava uns 4 tokens, como texto comum. Além disso, o gpt-oss nem conseguiu terminar o meu benchmark, no mesmo programa em que o Genesys PI passou pelas sete etapas. Um adesivo leve em cima do gpt-oss não faz isso.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
A terceira suspeita, a do intermediário, foi testada pelo comportamento da API. Ela recusa uma série de parâmetros de configuração que a API da OpenAI aceita, e outros que qualquer servidor comum de modelo aberto aceitaria. Um [proxy]{.gls} transparente, que só repassa o pedido, aceitaria esses parâmetros e deixaria rastro.

E tem o argumento do desempenho. O GPT-5.5 e o GPT-6 Luna pegavam sem aviso duas armadilhas muito bem disfarçadas do meu teste. O Genesys PI deixava passar as mesmas duas, de forma estável, em todas as rodadas. Um repasse não fica consistentemente mais fraco que o modelo por trás dele, num ponto específico.

### Três direções diferentes

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
O resultado que mais me interessou foi outro. Comparei a assinatura de erros do Genesys PI com a de todos os modelos da tabela.

A cauda de erros parecia a do Qwen, mas isso era efeito da faixa de nota: todo modelo na casa dos 80 pontos erra aquelas duas armadilhas, de qualquer família. Uma correção rara parecia a do GPT-6 Luna. O tokenizador parecia OpenAI.

Um clone ou um repasse se parece com um único modelo em todos os eixos ao mesmo tempo. O Genesys PI não se parecia com nenhum modelo da tabela em todos os eixos.

> Um teste de caixa-preta exclui hipóteses. Ele não prova a origem de nada.

### O que nenhum teste de API atravessa

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Aqui está o limite. Um modelo novo, com pesos próprios e o vocabulário público da OpenAI, pode ter sido treinado do zero com dados próprios. Ou pode ter sido treinado do zero imitando respostas do Claude e do GPT, a destilação. As duas histórias produzem exatamente as mesmas observações que eu fiz.

Uma grade de 20 perguntas comparando o estilo das respostas com o de vários "professores" possíveis deu resultado nulo, compatível com as duas histórias.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Outro limite é o tamanho da lista: "não encontrei parentesco" significa "não encontrei entre os modelos que testei", e existem dezenas que eu não testei.

Registrei também uma inconsistência, a primeira pergunta que eu faria à empresa.

A pesquisa publicada da LUA trata do "imposto do token", o custo extra que um vocabulário otimizado pro inglês cobra do português. Só que a API que eu medi quebra português exatamente como esse vocabulário da OpenAI. Adotá-lo é a escolha barata e profissional que qualquer laboratório pequeno faria, e nada diz sobre linhagem; mas pesquisa e produto contam histórias diferentes nesse ponto.

<!-- src: ref:llm-coding-benchmark/model-forensics/FINDINGS.md -->
Em outubro, rodei uma bateria mais rigorosa, com centenas de textos que eu não tinha usado antes e modelos de controle conhecidos, e ela me deixou mais cauteloso. A contagem de tokens da API bateu com a do vocabulário da OpenAI em todos os 768 textos novos.

Mas isso descreve só como a API conta tokens. Quais pesos estão por trás dela é outra pergunta, e o mesmo vocabulário aparece em outros modelos abertos que eu nem tinha na lista, inclusive de outras empresas.

As respostas do Genesys PI ficaram bem longe das versões do GPT-4o que testei, um indício contra um simples repasse daquelas versões, mas os controles positivos e negativos se sobrepuseram e o protocolo não permitiu classificar nada formalmente. Nenhuma origem ficou provada, nenhuma ficou excluída de forma conclusiva, e eu não consigo atribuir um número de probabilidade a hipótese de origem nenhuma.

### Checado, alegado, em aberto

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
A ferramenta mais útil que saiu desse caso é um hábito: separar o que eu medi do que me disseram. Ele serve pra qualquer anúncio de IA, de empresa grande ou pequena.

Checado por mim:

- o Genesys PI existe, responde e completa um benchmark difícil na faixa dos tiers A e B da minha tabela;
- a contagem de tokens da API bate com o vocabulário público da OpenAI e diverge da de Qwen, DeepSeek, Llama e Mistral;
- a API não se comporta como um repasse transparente, e o modelo tem fraquezas próprias e estáveis;
- o gpt-oss de fábrica não explica o resultado.

Não checado, só a palavra da empresa:

- que o modelo foi treinado do zero, e não destilado;
- que a arquitetura é nova, de uma geração posterior ao [transformer]{.gls};
- que o treino aconteceu em hardware comum, AMD e ARM, sem as placas da NVIDIA, em poucos meses;
- que existe um modelo melhor a caminho.

<!-- src: 2026/09/23/llm-benchmark-v4-genesys-pi-novo-competidor-brasileiro -->
O mesmo critério vale pro material público: os artigos da LUA estão num repositório de pré-publicações, sem revisão por pares, e a nota de LiveBench que aparece no material dela foi autodeclarada, num pedido de inclusão no ranking que, até setembro, nenhum mantenedor tinha confirmado [@livebench2026issue370].

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Se as afirmações mais fortes forem verdadeiras, o domínio da NVIDIA no treino de modelos leva um golpe sério. Afirmação desse tamanho exige evidência desse tamanho, e eu não tenho. O que resolveria é documento: o arquivo do tokenizador, a receita de treino, a curva de aprendizado, um teste inédito que eu mesmo rode.

Do outro lado da balança, enganar essa análise daria um trabalho enorme: adotar o vocabulário da OpenAI, mascarar a identidade do modelo, montar uma API que rejeita exatamente os parâmetros certos, manter fraquezas estáveis por várias rodadas e ainda completar um benchmark difícil em nível alto. A partir de certo ponto, uma falsificação convincente de um modelo é indistinguível de ter um modelo.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Minha posição, quando fecho este capítulo, é a mesma de 30 de setembro: um modelo que se comporta como independente, em cima de um vocabulário público, com uma origem que ninguém de fora consegue certificar. Mais do que eu esperava de uma empresa desse tamanho, menos do que o site deles vende.
