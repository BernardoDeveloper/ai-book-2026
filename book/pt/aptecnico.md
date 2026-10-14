---
id: aptecnico
chapter: "Para quem programa: os bastidores"
sources:
  - {post: 2026/03/31/codigo-fonte-do-claude-code-vazou-o-que-achamos-dentro, sha256: "82777df93da3ba3bf92807e76d3326dc878e81b79d78d456926828131b3274eb"}
  - {post: 2026/04/06/rag-esta-morto-contexto-longo, sha256: "7ff16e0b5895ccd7909d0d16cb0d78b8a11dc80629766f7820198555ea8fe711"}
  - {post: 2026/08/16/entendendo-ia-watermark-da-anthropic, sha256: "1d322e2603b8a56d275962144f684c2416294a2db0a1726eb4b8f23f5e63f854"}
  - {post: 2026/04/23/driveclub-shadps4-e-ia-como-aprender, sha256: "40d4966f8b6a7bbd114f67a9991f35d3a0ba9bd2e065920ff089bfb8fb32b57e"}
  - {post: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395, sha256: "5503548667e5a04feb629e98214f329605f7ca537c7095d3afe20c72e9ad2cd1"}
  - {post: 2026/04/05/testando-llms-open-source-e-comerciais-quem-consegue-bater-o-claude-opus, sha256: "6e03e1fcf81b0ab75eb74031ce2c338f5112558afc3475e637f746160a8e59ff"}
  - {post: 2026/06/14/llm-benchmark-kimi-v2-7-code-glm-5-2-minimax-m3-local, sha256: "ea56a609622cfd6ea2f3df72fe53f008ee722fccd6b4df9c81d69eca44c8ebb9"}
  - {post: 2026/10/10/qual-modelo-de-decisao-classificador-de-ia-tipo-jev-e-melhor, sha256: "90819aaee0a700994dc5dbcc83018b026811a12e9ea657a31c3e2d53c6270c0b"}
  - {post: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito, sha256: "4efebd6893539875cd7d62c121b0b6df51ba8610890a2232d996241e4f56d914"}
  - {post: 2026/02/09/ai-agents-qual-seria-a-melhor-linguagem-de-programacao-para-llms, sha256: "82c513848860f28bd296284a54db0565badf72f473d02175271c2afd961f6ba5"}
  - {post: 2026/09/19/nova-linguagem-voltada-pra-ia-bend-2, sha256: "8a98f0d0f644b402a2ad9d95709c6dc204d92c04e390388b3bc148418223e7b1"}
  - {post: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms, sha256: "d0ad6a79b80f5d9dd74bf39c0782d291889f9de32b964c6ea06c580f02bb4079"}
refs_projects:
  - "jev-docs/README.md"
  - "jev-docs/benchmark/reports/next-wave-comparison-v1/support-ticket-case-study.md"
  - "private-notes/benchmarks/BENCHMARK_REPORT.md"
  - "private-notes/benchmarks/FINDINGS.md"
blog_commit: "cc8b467dd4d6d3b5c57fad6bb6fae70ec5839a01"
---

# Para quem programa: os bastidores {#sec-aptecnico}

<!-- src: original -->
Este apêndice guarda o que eu tirei dos capítulos pra não cansar quem não programa: o passo a passo de uma depuração, as contas de memória de um modelo rodando em casa, os detalhes de um teste de linguagens. Cada seção começa dizendo de qual capítulo saiu e se lê sozinha. Se você programa, ou só gosta de ver a engrenagem, é aqui.

## O sonho do Claude Code: como o autoDream consolidaria a memória {#sec-aptecnico-autodream}

<!-- src: 2026/03/31/codigo-fonte-do-claude-code-vazou-o-que-achamos-dentro -->
No @sec-ch02, o código vazado do Claude Code mostrou que a memória do agente eram arquivos de texto em três camadas: um índice curto sempre na mesa, arquivos de tópico buscados quando preciso e transcrições antigas só pesquisadas por palavra. O código trazia também um processo chamado autoDream, ainda desligado na versão pública de março de 2026, que rodaria em segundo plano enquanto você não está usando a ferramenta, pra consolidar essa memória [@deeplearningai2026kairos].

Pra um sonho acontecer, três portas tinham que abrir ao mesmo tempo: pelo menos 24 horas desde o último sonho, pelo menos cinco sessões de trabalho desde então, e uma trava garantindo que não houvesse dois sonhos rodando juntos. Aí o processo relia o índice, procurava sinais novos nas conversas recentes, reescrevia os arquivos de tópico, trocava datas relativas, do tipo "na terça passada", por datas absolutas e apagava fatos que tinham sido contraditos depois. No fim, podava o índice pra ele continuar curto.

O sonhador podia ler o projeto inteiro, mas não podia mudar nada nele. Só mexia nas próprias anotações.

## RAG, embeddings e a volta da busca por palavra {#sec-aptecnico-rag}

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
O @sec-ch02 conta que, entre 2023 e 2025, quem queria um chatbot que respondesse sobre os próprios documentos ouvia que precisava de [RAG]{.gls key=rag} e de um [banco vetorial]{.gls key=banco-vetorial}, e que o Claude Code de 2026 não usava nenhum dos dois. Esta seção guarda a parte técnica dessa história.

O jeito clássico de fazer a busca do RAG dava trabalho:

- cortar todos os documentos em pedaços pequenos, de umas poucas centenas de palavras;
- transformar cada pedaço num [embedding]{.gls}, uma lista de números que representa o "sentido" do texto;
- guardar esses números num banco vetorial, um tipo de banco de dados feito pra achar listas de números parecidas;
- na hora da pergunta, transformar a pergunta em números também, buscar os cinco pedaços mais parecidos e rezar pra que fossem os certos.

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
Virou indústria. Pinecone, Weaviate, Qdrant, Chroma, LangChain, LlamaIndex: produto e biblioteca pra cada etapa do encanamento, tutorial em todo canto, consultorias inteiras vivendo de "construa seu chatbot com seus PDFs".

### O que o Claude Code usava no lugar

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
A memória do Claude Code era um índice em texto, arquivos de tópico e transcrições pesquisadas por palavra-chave, com a ferramenta mais velha e mais burra que existe pra isso: procurar onde a palavra aparece, letra por letra. Nenhum embedding, nenhum banco vetorial. A navegação pelo código dos projetos funcionava do mesmo jeito: listar arquivos, procurar palavras, abrir o arquivo inteiro.

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
A minha leitura é que a equação mudou de lado. Quando a janela era minúscula, o leitor (o modelo) era caro e limitado, então o buscador tinha que ser esperto e seletivo. Quando a janela passou a caber um romance inteiro, o leitor virou a peça mais inteligente do sistema, e o buscador pôde voltar a ser burro: ele só precisa trazer bastante coisa possivelmente relevante, e quem separa o que importa é o modelo.

### Os defeitos que os tutoriais não mostravam

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
O banco vetorial confunde parecido com relevante. Você pergunta como o sistema trata erro de autenticação e ele devolve todo pedaço que fala de autenticação. O pedaço que de fato responde pode estar em décimo lugar, ou nem aparecer, porque quem escreveu o manual usou "login".

O corte em pedaços destrói o que está na fronteira. A tabela importante foi partida no meio, a definição ficou num pedaço e o exemplo no outro, e quase sempre a fronteira cai exatamente onde a resposta morava.

E quando ele erra, erra sem deixar pista. Se a busca por palavra não acha nada, você sabe por quê: a palavra não está no documento. Se o banco vetorial devolve um trecho plausível e errado, não há nenhum sinal de onde o processo falhou. Além disso, cada vez que um documento muda, os números precisam ser recalculados, e sempre há uma janela em que o índice e o documento discordam.

### A conta do custo

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
O argumento clássico a favor do RAG era o custo: mandar o documento inteiro pro modelo sairia caro demais. Em abril de 2026 eu fiz a conta. Uma pergunta com 200 mil tokens na mesa, um romance grande inteiro, custava uns 60 centavos de dólar no Claude Sonnet 4.6, menos ainda nas perguntas seguintes sobre os mesmos documentos, graças a descontos por repetição.

Montar e manter um encanamento de busca vetorial, por outro lado, consome semanas de trabalho de engenheiro, e engenheiro é caro. Esses preços são de abril de 2026 e mudam a cada lançamento, quase sempre pra baixo. O raciocínio fica: token virou a parte barata da conta.

### Onde o RAG ainda ganha

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
Nada disso quer dizer que o RAG morreu. Ele ainda ganha em casos bem definidos:

- acervos gigantescos, centenas de gigabytes de texto, onde nem a busca por palavra dá conta sem um índice prévio;
- vocabulário muito diferente entre quem pergunta e quem escreveu, como o cliente que diz "tô sem net" e o manual que diz "perda de conectividade";
- imagens e áudio, onde não existe palavra pra procurar;
- respostas que precisam sair em frações de segundo, sem espaço pra mesa grande;
- auditoria, quando é preciso provar exatamente qual trecho foi consultado.

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
A pesquisa acadêmica conta a mesma história, sem bala de prata. Um estudo do Google DeepMind de 2024 concluiu que, quando há recursos, a janela grande costuma ganhar em qualidade, enquanto o RAG continua bem mais barato em tokens [@li2024rag]. Avaliações de busca mostram há anos que a velha busca por palavra-chave segue difícil de bater fora do domínio em que os embeddings foram treinados [@thakur2021beir].

A própria Anthropic publicou em 2024 que juntar a cada pedaço uma frase de contexto e combinar busca por palavra com busca vetorial derrubava as falhas de busca quase pela metade, e que um passo extra de reordenação dos resultados reduzia ainda mais [@anthropic2024contextual]. A combinação robusta é híbrida. Quem só puder escolher uma, escolhe a busca por palavra e ainda chega longe.

## A marca d'água estatística do Claude, por dentro {#sec-aptecnico-watermark}

<!-- src: 2026/08/16/entendendo-ia-watermark-da-anthropic -->
O @sec-ch04 conta que, desde 2 de agosto de 2026, a Anthropic marca de forma invisível o texto dos modelos Claude, pra cumprir o Artigo 50 do AI Act europeu, e explica o que essa marca prova e o que não prova. Esta seção mostra como a marca é feita e por que ela sai com tanta facilidade.

<!-- src: 2026/08/16/entendendo-ia-watermark-da-anthropic -->
A marca, um [watermark]{.gls} (marca d'água), não usa caractere escondido, espaço invisível nem fonte alterada. Ela é estatística. O modelo monta o texto escolhendo a próxima palavra numa lista de candidatas prováveis (@sec-ch01). Quando duas ou três servem igualmente bem, um número aleatório decide; com a marca, esse número passa a sair de uma chave secreta combinada com as palavras anteriores.

![Em cada encruzilhada de sinônimos, a chave inclina a escolha; num texto longo, as inclinações formam uma assinatura.](assets/figures/ch04-marca-dagua.png){#fig-ch04-marca-dagua fig-alt="Uma frase com bifurcações em dois pontos: 'nublado' ou 'cinzento', 'vazia' ou 'deserta'. Em cada bifurcação, uma pequena chave empurra a escolha pra um dos lados. Embaixo, uma grade com centenas de escolhas, a maioria marcada, forma um padrão chamado assinatura. Ao lado, a mesma grade depois de o texto ser reescrito por outro modelo, com as marcas espalhadas ao acaso: o sinal some."}

"O céu estava nublado" e "o céu estava cinzento" dizem a mesma coisa. Nesses encontros de sinônimos, a chave inclina o Claude pra um lado com mais frequência do que o puro acaso inclinaria. Cada escolha isolada passa despercebida, mas um texto longo repete esse ponto de decisão centenas de vezes, e o conjunto vira uma assinatura que só quem tem a chave consegue medir.

O método vem do SynthID-Text, que o Google DeepMind publicou em 2024 [@dathathri2024synthid].

### Por que ela sai com facilidade

<!-- src: 2026/08/16/entendendo-ia-watermark-da-anthropic -->
Como a assinatura mora nas escolhas de palavra, ela depende de existir escolha. Em trecho curto ou muito factual, onde quase não há sinônimo possível, o sinal enfraquece. E quando outro modelo reescreve o texto por inteiro, as escolhas passam a ser dele, e o padrão some. A própria Anthropic reconhece que retoque leve provavelmente deixa parte da marca, e que uma reescrita completa a elimina.

<!-- src: 2026/08/16/entendendo-ia-watermark-da-anthropic -->
Testes acadêmicos com o SynthID-Text apontam na mesma direção: a detecção cai bastante depois de uma paráfrase que preserva o sentido [@han2025synthid]. E reescrever um parágrafo mantendo o sentido não exige o modelo mais esperto do mercado. Um modelo aberto pequeno, rodando no seu computador, faz o serviço.

<!-- src: original -->
A conferência também é fechada. A marca só pode ser medida por um detector que tenha a chave da Anthropic, e cada fabricante que adotar a sua vai ter a sua própria chave e o seu próprio método.

## A tela preta do Driveclub, passo a passo {#sec-aptecnico-driveclub}

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
Em @sec-ch08 eu conto, em versão curta, os quatro dias de abril de 2026 em que cacei um defeito do Driveclub, um jogo de corrida de PlayStation 4, rodando no shadPS4, um [emulador]{.gls key=emulador} de código aberto ainda sem versão estável [@shadps4]. Nas corridas noturnas, a tela escurecia logo depois da largada até ficar preta, e só voltava perto de um minuto e meio depois. Foram 31 fases de investigação, 44 commits na minha cópia do emulador e mais de 15 mil linhas de código de diagnóstico, e a solução foi trocar um número inteiro num arquivo de configuração. Aqui vai o caminho por dentro.

### A informação que existe e não ajuda

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
A primeira coisa que qualquer um faz é procurar na internet. O que aparece:

- guias de 2025 dizendo pra sempre ligar uma certa opção de sincronização;
- guias de alguns meses depois dizendo pra desligar a mesma opção, porque ela mata o desempenho;
- vídeos com versões modificadas do emulador que ninguém documentou;
- uma discussão no fórum do projeto com três explicações pro escurecimento, incompatíveis entre si;
- as minhas próprias anotações, escritas poucos dias antes, recomendando o oposto do que eu descobri depois.

A informação existe, mas está espalhada, datada e contraditória.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
Um agente de IA, perguntado direto, devolve exatamente esse material, organizado e confiante: sugere uma modificação que faz o jogo rodar em câmera lenta, sugere mexer no brilho e na correção de cores, o que trata o sintoma e esconde a causa. A fonte dele são os mesmos fóruns, e os fóruns estavam errados.

### O que estava acontecendo

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
O Driveclub ajusta o brilho da cena como o olho humano se adapta ao escuro. A placa de vídeo mede quão clara está a imagem, e o processador principal lê essa medida no quadro seguinte pra decidir a exposição, como um fotógrafo abrindo ou fechando o diafragma.

O emulador, na configuração padrão, não sincronizava essa leitura. O processador lia uma medida velha, zerada, e concluía que a cena estava escura. Abria o diafragma, e mais, e mais, até a imagem saturar de um jeito que tudo virava preto.

Existe um modo de sincronização mais rigoroso que resolve. Ele fica escondido entre as opções avançadas porque custa caro e, em algumas placas de vídeo, derruba o desempenho. Ninguém tinha ligado publicamente esse modo ao escurecimento do Driveclub.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
Nada disso era conhecimento que eu tinha no domingo à noite. Eu não sabia que o jogo fazia esse ciclo de medir e corrigir, nem que a opção tinha três modos, nem por que o modo do meio não bastava. Se tivesse simplesmente "ligado a opção" que os fóruns mencionavam, teria escolhido o modo errado e desistido achando que não funcionava.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
O que destravou foi uma lista de sete suspeitos que a investigação tinha levantado. Um deles me incomodava porque era o único ligado a *quando* a informação era lida, enquanto os outros tratavam de *se* ela era escrita certo. Troquei o modo de sincronização, rodei a corrida noturna no Canadá, e a noite caiu naturalmente.

### O rodízio entre dois agentes

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
Usei o Claude Code e o Codex, e nenhum dos dois sabia mais do que eu sobre o problema. O que eles faziam bem era agregar: liam o código do emulador em paralelo comigo, cruzavam referências, compilavam, rodavam testes e analisavam registros de dezenas de megabytes muito mais rápido do que eu conseguiria sozinho.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
Nenhum dos dois, sozinho, fechou o problema. Várias vezes o Claude Code entrou em círculo, repetindo as mesmas hipóteses sem trazer nada novo. Quando isso acontecia, eu passava algumas horas no Codex pra arejar, com outras ideias e outro ângulo de leitura do código, e depois voltava. A solução final saiu no Claude Code, mas a jornada trocou de modelo várias vezes.

Teve também uma coisa que eu nunca tinha visto em nenhum agente: o Codex começou a repetir a mesma "solução" que tinha acabado de tentar, de novo e de novo, sem perceber o que estava fazendo. Tive que matar a sessão e começar outra do zero.

Isso diz muito sobre sessões longas. Quanto mais a conversa cresce, mais a [janela de contexto]{.gls key=janela-de-contexto} fica entulhada de tentativas anteriores (@sec-ch02). A complexidade e a duração daquela investigação derrubaram os dois modelos, cada um do seu jeito.

### A técnica da espingarda

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
Na maior parte das 31 fases, sem saber que estava fazendo isso, eu usei uma técnica que tem nome: espingarda.

Durante a corrida, o jogo usava mais de mil texturas, as imagens que cobrem os objetos da cena. Se a suspeita era "o escurecimento vem de alguma textura" e cada uma levasse vinte minutos pra examinar, eu passaria dias num galho só da árvore. E talvez a resposta nem estivesse nela.

Em vez disso, você atira em todas ao mesmo tempo. Altera todas as texturas de uma vez, roda o jogo e, em trinta segundos, sabe se alguma delas mexe no escurecimento. Se nenhuma mexeu, você acabou de descartar a categoria inteira, e passa pra próxima.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
Criei 32 desses mecanismos de teste ao longo da investigação, e um só foi efetivamente usado pra encontrar o bug. Ainda assim, cada rodada descartou uma família inteira de hipóteses. E, enquanto isso, eu aprendia o sistema: cada teste que travava o jogo me dizia onde morava algo crítico, cada cor estranha na tela me dizia qual peça alimentava qual.

Quando você não conhece o sistema, os tiros de espingarda são um mapa. Você não usa eles pra achar a resposta. Usa pra conhecer o terreno.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
Tudo isso dependia de uma preparação. Antes da primeira fase, eu garanti que o defeito aparecia em 100% das tentativas, sempre no mesmo padrão de tempo. Se você não consegue reproduzir o problema quando quer, está caçando fantasma, porque cada experimento precisa de um antes e um depois que dê pra medir.

### Um inteiro e sete mil linhas de anotações

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
A conta final me diverte: mais de 50 documentos de anotações, quase 7 mil linhas de texto descrevendo hipóteses e descartes, contra um número inteiro na configuração. Quase nada das 15 mil linhas de código serve pra contribuir com o emulador, porque é instrumentação feita pro Driveclub naquelas condições. A solução, aliás, estava no código do emulador havia sete meses.

## IA em casa: a conta da memória {#sec-aptecnico-memoria-local}

<!-- src: original -->
O @sec-ch13 compara duas máquinas de casa: um computador de mesa com a RTX 5090, placa de vídeo de 32 GB, e um mini-PC com o chip AMD Ryzen AI Max+ 395, apelidado de Strix Halo. O capítulo resume tudo numa imagem, a do escritor que vai até a estante consultar a enciclopédia inteira a cada palavra: o tamanho da estante (a memória) decide o que cabe, e a largura do corredor (a largura de banda) decide a velocidade. Esta seção guarda as contas por trás da imagem.

### Quanto ocupa um modelo

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
A conta é de padeiro. Cada parâmetro, guardado com a precisão normal de 16 bits, ocupa 2 bytes. O GLM 4.7 Flash, da chinesa Z.ai, tem uns 30 bilhões de parâmetros [@zai2026glm47flash], e nessa precisão os pesos dele ocupam uns 60 GB, quase o dobro da RTX 5090.

Na placa, não cabe. No mini-PC, coube inteiro, sem cortar precisão nenhuma, e rodou a uns 18 tokens por segundo.

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
A [quantização]{.gls key=quantizacao} encolhe essa conta. Um modelo de 70 bilhões de parâmetros que ocuparia uns 140 GB em 16 bits cabe em uns 40 GB em 4 bits, com uma perda de qualidade pequena o bastante pra uso prático.

<!-- src: 2026/04/05/testando-llms-open-source-e-comerciais-quem-consegue-bater-o-claude-opus -->
Em 8 bits a perda é quase imperceptível; em 4 já dá pra medir; abaixo de 3 o modelo começa a falar besteira de verdade. Pra programação e raciocínio de vários passos, a regra que eu sigo é não descer de 4.

### O caderno de anotações

<!-- src: 2026/04/05/testando-llms-open-source-e-comerciais-quem-consegue-bater-o-claude-opus -->
O peso do modelo é metade da conta. Pra não reler o [contexto]{.gls} inteiro a cada palavra que escreve, o modelo mantém um caderno de anotações sobre cada pedaço que já leu. Esse caderno tem nome técnico, [KV cache]{.gls key=kv-cache}, e ele também mora na VRAM.

O caderno cresce na mesma proporção da conversa. Num modelo de 70 bilhões de parâmetros em precisão normal, cada token lido acrescenta uns 0,3 MB de anotações. Parece nada, até você fazer a conta de uma conversa de 128 mil tokens: uns 40 GB só de caderno, por cima dos pesos.

<!-- src: 2026/04/05/testando-llms-open-source-e-comerciais-quem-consegue-bater-o-claude-opus -->
E um agente de programação enche o caderno depressa. Ele lista arquivos, lê código, compila, recebe a saída de cada comando, e tudo isso entra no contexto. Nos meus testes de abril, uma sessão de agente consumia de uns 40 mil a mais de 150 mil tokens. Com menos de uns 100 mil de espaço, projeto de verdade não anda.

<!-- src: 2026/04/05/testando-llms-open-source-e-comerciais-quem-consegue-bater-o-claude-opus -->
Na RTX 5090, a conta não fecha sem sacrifício. Pra caber um modelo de 27 bilhões de parâmetros e um caderno de 128 mil tokens nos 32 GB da placa, tive que arredondar os pesos pra 3 bits, abaixo da minha própria regra.

### O corredor em números

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
Até março de 2026, meu servidor de casa era um mini-PC antigo, sem placa de vídeo, e qualquer IA ali rodava no processador e ficava inutilizável. O chip novo tem um bloco só de 128 GB de memória unificada, dividido entre processador e vídeo como você quiser [@amd2025ryzenaimax]. No review de março, eu separei 96 GB pra parte de vídeo.

<!-- src: ref:private-notes/server-notes.md -->
Essa divisão não durou. Em 8 de abril baixei a parte de vídeo pra 64 GB, porque o resto do servidor, com dezenas de serviços rodando, precisava de memória pra respirar. Tudo que o @sec-ch13 conta depois de abril, do benchmark de setembro aos classificadores de outubro, rodou com 64 GB de VRAM. A fronteira é uma configuração, e dá pra mover.

<!-- src: ref:private-notes/benchmarks/BENCHMARK_REPORT.md -->
A memória da RTX 5090 entrega uns 1.792 GB por segundo [@pcgamesn2025rtx5090]. A do Strix Halo entrega uns 256 GB por segundo, e ainda divide esse corredor com o processador e o sistema operacional. A razão entre as duas é quase exatamente sete, e a diferença de velocidade que eu medi foi de 6,7 vezes. Um modelo pequeno que a RTX escrevia a 155 tokens por segundo, o mini-PC escrevia a 23.

A placa de vídeo tem cálculo sobrando. O que falta é corredor.

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
Também não adianta enfiar só um pedaço do modelo na placa e deixar o resto na memória do computador. Esse vaivém atravessa um canal ainda mais estreito, de uns 32 GB por segundo, e a velocidade despenca de 150 tokens por segundo pra algo entre 2 e 8.

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
O Mac Studio de 2025, com o chip M3 Ultra, juntava as duas coisas: ia até 512 GB de memória unificada com mais de 800 GB por segundo de banda [@apple2025m3ultra]. Pela minha estimativa de março, com impostos de importação, a configuração máxima passava de 110 mil reais no Brasil.

### Muitos especialistas, poucos acordados

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
Tinha um mistério nos meus números. Um modelo de 35 bilhões de parâmetros rodava a 43 tokens por segundo no mini-PC. Um de 72 bilhões, o dobro do tamanho, rodava a 4,5, quase dez vezes mais lento.

<!-- src: ref:private-notes/benchmarks/FINDINGS.md -->
Os dois são construídos de jeitos diferentes. O de 72 bilhões é um modelo denso: a cada token, ele consulta todos os seus pesos, a enciclopédia inteira. O de 35 bilhões é um [MoE]{.gls key=moe}, uma mistura de especialistas.

Um MoE divide boa parte do modelo em blocos, os tais especialistas, e tem um pequeno roteador que escolhe, pra cada token, quais poucos blocos vão trabalhar. No modelo de 35 bilhões, só uns 3 bilhões ficam ativos por token. O escritor consulta só alguns volumes da enciclopédia, e o corredor deixa de ser o gargalo.

<!-- src: original -->
O nome engana um pouco. Ninguém treinou um especialista em medicina e outro em direito. Quando os pesquisadores da Mistral foram olhar como o roteador do Mixtral distribuía o trabalho, não acharam divisão por assunto: o que aparecia era mais parecido com tipos de palavra e de pontuação [@jiang2024mixtral]. "Especialista" aqui quer dizer só "bloco que o roteador acordou desta vez".

![Num modelo denso, o modelo inteiro trabalha em cada token; num MoE, um roteador acorda só alguns blocos, mas todos precisam estar na memória.](assets/figures/ch13-especialistas.png){#fig-ch13-especialistas fig-alt="Dois painéis. No primeiro, modelo denso: uma grade de blocos todos acesos, com a legenda todos os pesos lidos a cada token. No segundo, MoE: a mesma grade com apenas dois blocos acesos e um pequeno roteador apontando pra eles, e a legenda só alguns blocos trabalham, mas todos ocupam memória."}

<!-- src: 2026/06/14/llm-benchmark-kimi-v2-7-code-glm-5-2-minimax-m3-local -->
Tem uma pegadinha, e ela me pegou em junho. Os especialistas que dormem continuam ocupando memória. Pra rodar um MoE, você precisa caber o modelo inteiro, e só ganha velocidade porque lê uma parte dele.

Quando a MiniMax publicou os pesos do M3, um MoE de uns 428 bilhões de parâmetros com uns 23 bilhões ativos, fiz a conta pra rodar em casa. Nem a versão mais esmagada, a chamada "de 1 bit", que já seria inútil pra programar, caberia. Ela sozinha ocuparia uns 128 GB, a memória unificada inteira do mini-PC e o dobro dos 64 GB reservados pra vídeo, sem deixar espaço pro caderno de anotações nem pro sistema. O nome engana, aliás: essas versões guardam as partes mais sensíveis do modelo com mais precisão, e a média fica perto de 2,4 bits por parâmetro.

## O teste dos classificadores, por dentro {#sec-aptecnico-classificadores}

<!-- src: original -->
O @sec-ch13 conta o teste que eu montei em outubro de 2026 pra modelos de decisão da família do Jev, os [classificadores]{.gls key=classificador} que recebem um texto, umas regras e uma lista de opções e escolhem uma. O capítulo fica com a lição: um modelo pequeno e especializado empata com serviços pagos numa decisão fechada, e a regra que dá pra escrever fica no código. Aqui estão os resultados em detalhe.

<!-- src: ref:jev-docs/README.md -->
Os casos eram de suporte, reembolso, moderação e roteamento, metade escritos em inglês e metade em português, cada um com a resposta certa congelada antes de qualquer modelo rodar. Foram vinte e três configurações: cinco serviços pagos na nuvem e dezoito modelos abertos rodando no mini-PC.

O resultado, em 12 de outubro de 2026, foi este:

- no topo, dois modelos abertos de 27 bilhões de parâmetros, o Perplexity Decider e o Decision 3.0, ambos com 99,4% de acerto nos casos compactos e 100% em português; os dois deram exatamente as mesmas respostas em todas as 1.024 classificações;
- logo atrás, empatados em 97,6%, o próprio Jev e o Microsoft Decision-1, este o serviço pago mais barato que eu medi, uns 6 centavos de dólar a cada 10 mil decisões;
- os melhores modelos abertos de 4 bilhões de parâmetros, como o Jebadiah, ficaram entre 87% e 90%, respondendo em uns 200 milissegundos.

<!-- src: 2026/10/10/qual-modelo-de-decisao-classificador-de-ia-tipo-jev-e-melhor -->
Um modelo de 4 bilhões de parâmetros, que cabe numa placa de vídeo comum, empatou com o serviço de decisões da OpenAI, que estreou com 90,5%. E o melhor resultado da tabela inteira veio de dois modelos que qualquer um pode baixar e rodar em casa.

<!-- src: ref:private-notes/decision-models.md -->
O Decision 3.0 ocupou uns 49 GB de memória de vídeo, e no pico o total encostou em 63,5 dos 64 GB do mini-PC. Os dois campeões tinham que rodar sozinhos, com todo o resto desligado, e cada decisão levava perto de um segundo e meio. Os serviços na nuvem respondiam, quase todos, em menos de meio segundo.

### A moeda

<!-- src: ref:jev-docs/README.md -->
As tarefas tinham três ou quatro opções, então chutar ao acaso acertaria uns 31%. O Julia-1, o menor modelo da lista, com 144 milhões de parâmetros, acertou 31,5%. Respondia em 12 milissegundos, o mais rápido de todos, e acertava como uma moeda.

<!-- src: 2026/10/10/qual-modelo-de-decisao-classificador-de-ia-tipo-jev-e-melhor -->
Dos 71 palpites que ele deu com mais de 90% de confiança, 48 estavam errados. Esses modelos minúsculos foram feitos pra ser ajustados com os dados de quem vai usar; de fábrica, aplicando regras que nunca viram, não servem.

### O ticket crítico

<!-- src: ref:jev-docs/benchmark/reports/next-wave-comparison-v1/support-ticket-case-study.md -->
Um caso não aparece em média nenhuma. A regra de severidade dizia: perda contínua de dados em produção é crítica, não importa quantos clientes afeta. O ticket descrevia perda permanente de dados, confirmada pelos engenheiros, de um cliente só.

A resposta certa é "crítico". O Clef completo, da Cloudflare, um modelo de 27 bilhões de parâmetros, respondeu "degradado", junto com vários modelos de 4 a 9 bilhões. O Jev acertou, e alguns modelos bem menores também.

É um caso só, sintético. Mas é exatamente o erro que mais custa, e a porcentagem de acerto não mostra. É também o melhor argumento pra regra de severidade morar no código, como o capítulo defende.

## A reescrita do Bun e a resposta do Zig {#sec-aptecnico-bun}

<!-- src: original -->
Em @sec-ch16 eu conto como Jarred Sumner reescreveu o Bun, o ambiente de JavaScript que a Anthropic comprou e sobre o qual o Claude Code roda, de Zig pra Rust com agentes, em julho de 2026. O capítulo fica com o método. Aqui vai a briga que veio depois, entre o criador do Zig e o time do Bun, e o que eu tirei dela.

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
No dia seguinte ao relato do Sumner, Andrew Kelley, o criador do Zig, publicou a resposta dele [@kelley2026bun]. Eu queria ler o melhor argumento técnico possível em defesa do Zig. Ele traz alguns, e eles merecem ser ouvidos:

- parte do ganho de desempenho que o Bun atribuiu à reescrita veio de uma otimização na montagem final do programa que o Zig sempre ofereceu, e que o Bun não tinha ligado;
- o trabalho de reduzir o tamanho do executável não dependia da linguagem e podia ter sido feito no código antigo;
- se a bateria de testes basta pra dar confiança ao código novo em Rust, que pelas contas dele passava de um milhão de linhas sem revisão humana linha a linha, por que não bastava pro código Zig?

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
A terceira pergunta é boa e cai em cheio no tema de código que ninguém leu. Uma parte grande do texto dele, porém, sai do campo técnico e entra em queixas sobre a gestão do Bun, a relação entre os dois projetos e acusações pessoais que ele mesmo diz não poder detalhar. Não tenho como verificar nada disso, e isso tampouco ajuda a entender a decisão técnica. Fiquei decepcionado.

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
Então fiz o exercício que eu esperava ter lido. Pedi a dois [modelos de fronteira]{.gls key=modelo-de-fronteira}, os mais fortes do mercado naquele julho, que fizessem papel de árbitro técnico e escrevessem a resposta que o Zig merecia, com o código do Bun aberto na frente deles. O resultado foi mais equilibrado do que a briga na internet.

O Zig não estava indefeso. Ele tem mecanismos explícitos pra limpar recursos quando algo dá errado e ferramentas de teste que acusam vazamentos e memória devolvida duas vezes, embora só nos caminhos que os testes exercitam.

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
E num ponto o Zig tinha vantagem clara. Uma rotina do Bun que colore mensagens no terminal se apoiava num recurso do Zig que roda código durante a compilação. A primeira tradução pra Rust perdeu essa garantia e causou uma regressão na versão de testes, que depois foi corrigida com outro mecanismo [@bun2026issue30693]. Ponto pro Zig.

Os ganhos de tamanho e velocidade que o Bun mostrou, uns 20% a menos no executável e de 2% a 5% a mais nos testes de desempenho, têm causas misturadas: linguagem, ferramentas de compilação, configuração, limpeza acumulada. Dá pra acreditar nos números sem atribuir tudo ao Rust.

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
Há ainda um conflito de interesse: a Anthropic é dona do Bun e vende o Claude Code. O time do Bun tinha todo o incentivo pra transformar a reescrita numa vitrine do produto do novo empregador. Isso não prova má-fé nem invalida o resultado técnico, mas pesa na forma como o caso foi contado. Ignorar isso seria tão ingênuo quanto ignorar a mágoa do Kelley.

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
A minha leitura, em julho, ficou assim. Rust foi uma escolha defensável pro Bun naquele momento: trocou uma parte da disciplina humana por verificação do compilador, e isso pesa quando parte do código está sendo escrita por agentes, que avançam batendo em erros de compilação.

Mas a evidência não prova que o Zig era inviável. Uma reestruturação agressiva dentro do próprio Zig talvez resolvesse muito. Não temos o contrafactual.

O que dá pra afirmar é que o método pesou tanto quanto a linguagem. Linguagem não substitui arquitetura. Ela só muda quais erros ficam baratos de detectar.

## Uma linguagem feita pra IA: do PACT ao Bend 2 {#sec-aptecnico-bend}

<!-- src: original -->
Em @sec-ch18 eu conto como a pergunta sobre que linguagem aprender atravessou o meu ano, de um palpite em fevereiro a uma medição em outubro. O capítulo fica com a resposta. Aqui vão os dois experimentos com linguagens desenhadas pra IA que vieram no meio do caminho.

<!-- src: 2026/02/09/ai-agents-qual-seria-a-melhor-linguagem-de-programacao-para-llms -->
Em 9 de fevereiro de 2026 eu fiz um exercício bem bobo. Perguntei ao Claude e ao GPT Codex como seria uma linguagem de programação feita pra ser editada por LLMs, sem nenhuma preocupação em ser amigável pra humanos. Linguagens são desenhadas em volta dos limites humanos: nomes legíveis, indentação, atalhos que deixam o código bonito. Python e Ruby levam isso longe, e o preço costuma ser eficiência pra máquina.

<!-- src: 2026/02/09/ai-agents-qual-seria-a-melhor-linguagem-de-programacao-para-llms -->
Os dois modelos chegaram mais ou menos à mesma conclusão. Descreveram algo parecido com a estrutura em árvore que o compilador monta por dentro do programa, só que carregada de anotações: contratos dizendo o que cada função promete, a lista de tudo que ela pode afetar fora de si, a origem de cada linha. O humano escreveria só a especificação da intenção; a máquina cuidaria do resto. A frase que resumia o raciocínio deles era esta: a linguagem ideal pra IA é a que os humanos continuam rejeitando.

<!-- src: 2026/02/09/ai-agents-qual-seria-a-melhor-linguagem-de-programacao-para-llms -->
Eu deixei claro na hora que aquilo era achismo. É o que o modelo consegue deduzir das próprias probabilidades, e perguntar ao modelo não é evidência de nada. Ainda assim, pedi ao Claude um protótipo de compilador pra linguagem que ele mesmo descreveu. Ele escolheu escrever em Rust, batizou a linguagem de PACT, e eu publiquei o projeto sem nem testar [@akita2026pact].

Ficava no ar uma ideia que eu achava inevitável a longo prazo. Se gerar código ficar trivial, talvez valha voltar a escrever especificações detalhadas, coisa que a indústria abandonou por ser improdutiva demais. Era uma hipótese, e eu ainda não tinha como testá-la.

<!-- src: 2026/09/19/nova-linguagem-voltada-pra-ia-bend-2 -->
Em 17 de setembro de 2026, o pesquisador brasileiro Victor Taelin lançou o Bend 2, vendido como uma linguagem rápida que bloqueia os erros da IA por meio de prova [@taelin2026bend2]. Era quase a minha hipótese de fevereiro em carne e osso. O humano escreve as leis do sistema num arquivo, e a IA escreve as provas de que o código cumpre essas leis. Um verificador, que roda em um décimo de segundo, barra qualquer mudança cuja prova não fecha.

No dia do lançamento eu apontei meus agentes pra dois programas meus escritos em Rust e mandei portar pra Bend 2. O que segue é uma revisão de segundo dia de vida da linguagem, datada, e muita coisa pode ter mudado depois.

<!-- src: 2026/09/19/nova-linguagem-voltada-pra-ia-bend-2 -->
A parte boa foi muito boa. Eu injetei de propósito um erro de "um a mais" numa rotina que distribuía um limite de itens entre repositórios. As três saídas de exemplo continuaram idênticas, então uma bateria de testes daquele tamanho teria aprovado. O verificador de provas recusou, apontando o termo exato que deixou de bater.

<!-- src: 2026/09/19/nova-linguagem-voltada-pra-ia-bend-2 -->
O resto ainda era de brinquedo:

- foram 93 linhas de leis e provas pra garantir dois fatos simples sobre uma rotina de umas 30 linhas;
- a parte do programa que dava pra provar ficou em poucos por cento do código; leitura de dados, ordenação, tela e rede ficaram de fora;
- a biblioteca padrão não tinha conexão segura pra internet nem leitura de teclado no terminal, e precisei de oito funções escritas à mão em C pra preencher os buracos;
- a linguagem teve nove versões em dez horas no dia seguinte ao lançamento.

<!-- src: 2026/09/19/nova-linguagem-voltada-pra-ia-bend-2 -->
Teve crítica pesada de especialistas. Um dia depois do lançamento, um programador refez o joguinho de demonstração do Bend em SPARK, uma ferramenta madura de [verificação formal]{.gls key=verificacao-formal} da família Ada, e provou as mesmas propriedades automaticamente, sem as centenas de linhas de prova manual [@powell2026bend]. A minha conclusão foi que o nicho natural do Bend é o de núcleos pequenos e críticos, escritos por IA e provados por máquina. E que eu escolho linguagem pelo tamanho do ecossistema em volta dela: eu uso muito Rust, odeio a sintaxe e tolero, porque quem escreve é o LLM.

## O benchmark de sete linguagens {#sec-aptecnico-linguagens}

<!-- src: original -->
Em @sec-ch18 eu resumo numa frase o teste que fiz em outubro de 2026 pra saber se alguma linguagem de programação rende mais com agentes: testes ajudaram mais do que a escolha da linguagem. Aqui vão a discussão que motivou o teste, o desenho e os números.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
No começo de outubro de 2026, o DHH, criador do Ruby on Rails, converteu o aplicativo de chat dele pra várias linguagens usando agentes e foi publicando os resultados de desempenho no X [@dhh2026campfire]. Rust saiu na frente de Elixir e Ruby, e a discussão pegou fogo. Logo apareceu quem notasse que a versão em Rust tinha passado por bem mais rodadas de agente que as outras. Um programador pegou a versão em Elixir e, com otimizações óbvias que nenhuma primeira conversão faz, deixou a página principal dez vezes mais rápida [@kurtome2026elixir].

Uma conversão única feita por agente mede o quanto o modelo conhece cada linguagem e quantas voltas ele deu em cada uma.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
Aquilo ressuscitou duas crenças que circulam desde que LLM virou ferramenta de trabalho:

- linguagem enxuta, de script, seria melhor pra IA porque gastaria menos [tokens]{.gls key=token};
- linguagem de tipagem forte seria melhor pra IA porque o compilador pegaria os erros, e o agente precisaria consertar menos.

A segunda é prima direta da minha hipótese de fevereiro (@sec-aptecnico-bend). Em vez de discutir no X, eu fui medir.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
Montei um benchmark reproduzível e publiquei tudo [@akita2026vibebench]. A tarefa era uma só, de propósito difícil: levar um livro-razão contábil que atende várias empresas ao mesmo tempo de uma versão a outra mais exigente, com regras que atravessam várias operações. A correção era julgada por 43 cenários de teste, 16 deles escondidos do agente.

Cruzei sete linguagens, de Rust e Haskell a Python e Ruby, com quatro configurações de modelo: Kimi K3, GLM 5.3, Claude Opus 5.5 e o GPT-6 Sol pelo Codex. Cada combinação rodou com e sem uma bateria de testes pública em mãos, duas vezes. Deu 112 tentativas.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
Os resultados, naquele outubro:

- os dois modelos de fronteira, Opus e Sol, acertaram 53 de 53 tentativas válidas, em todas as linguagens (as outras três caíram por falha de infraestrutura, não do código); a tarefa foi fácil demais pra separar os modelos, e muito menos as linguagens, então não sobrou ranking nenhum pra publicar;
- nos modelos mais fracos, o que mudou o resultado foi a presença de testes: 24 entregas corretas com a bateria em mãos, contra 16 sem ela;
- Ruby, a linguagem mais enxuta em linhas, gastou praticamente os mesmos tokens que Rust no Sol, e no Opus foi a mais cara de todas, mais que o dobro do C#;
- nas tentativas do Opus que auditei, em Ruby, Rust e Haskell, não houve nenhum ciclo de conserto de erro de compilação: o código compilou de primeira.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
Onde os modelos erraram, erraram regra de negócio: uma propriedade do livro-razão que precisava valer entre uma operação e outra. Compilador nenhum pega esse tipo de erro, em linguagem tipada ou dinâmica.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
Os freios fazem parte do resultado. Foi uma tarefa só, com duas repetições por combinação, e mede o piso que cada linguagem entrega sob o mesmo esforço curto, sem mostrar o máximo que um engenheiro paciente extrairia dela. Um empate no teto também não diz qual linguagem iria mais longe numa tarefa mais difícil, só que nenhuma atrapalhou nesta. Se a sua tarefa não se parece com um livro-razão, os números não se transferem.

E se você discordar, a atitude correta é a que eu tive: rode o seu próprio teste.
