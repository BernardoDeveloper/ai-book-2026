---
id: apestudar
chapter: "Como estudar com a IA do lado"
sources:
  - {post: 2019/10/23/akitando-65-a-dor-de-aprender-que-cursos-livros, sha256: "2b05e6d3d26f3a619e53e6350dcbcd6a3f36c3ea7a77961ce845ddbe9561b322"}
  - {post: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r, sha256: "4c8343cf9487f3e389341a2e5654a423cb2ff2cced3ecbbddb5aed5385b544c1"}
  - {post: 2021/01/06/akitando-90-o-que-os-cursos-nao-te-ensinam-sobre-mercados, sha256: "5a6b08a8fdebc6eac5511e470883960e1f763187351f8df54e684349eee446c1"}
refs_projects: ["microgpt/README.md"]
blog_commit: "b54f14bf348a68cd8529004a4743d35dbbc5590d"
---

# Como estudar com a IA do lado {#sec-apestudar}

<!-- src: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r -->
Em abril de 2020, no começo da pandemia, eu gravei um episódio chamado "Aprendendo a aprender". Nele eu resumi o jeito certo de aprender em três frases [@akitando076]:

> 1) dando problemas pra serem resolvidos 2) não ter nenhum material oficial, e sim forçar as pessoas a saber encontrar os materiais que precisam 3) não ter nenhum supervisor ou chefe que dá mastigado, forçando a criar senso de autonomia e responsabilidade.

<!-- src: original -->
Na época, o inimigo era o curso de passo a passo. Em 2026 apareceu um adversário bem mais simpático: uma máquina que responde qualquer pergunta na hora, com paciência infinita e sem cobrar por aula. As três regras continuam valendo, e cada uma ficou mais difícil de cumprir, porque o agente faz de graça exatamente o que elas proíbem.

## Um problema seu

<!-- src: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r -->
A primeira regra pede um problema de verdade, sem roteiro. O tutorial te leva pela mão até um resultado que alguém já conhecia; o problema real te deixa sozinho com algo que ninguém resolveu do seu jeito.

Com IA, o tutorial ficou ainda mais confortável, porque agora ele se adapta a você e até digita os passos. Por isso o problema precisa ser seu: uma planilha que te irrita no trabalho, um programinha que você quer usar, uma dúvida que nenhum vídeo responde. Foi assim que eu passei quatro dias caçando um defeito num emulador (@sec-ch08), e é isso que transforma a resposta da máquina em aprendizado.

<!-- src: ref:microgpt/README.md -->
Se o problema que te coça é a própria IA, existe um bom pra começar. A primeira lição do meu microgpt lab treina um modelo de menos de um milhão de parâmetros num processador comum, em menos de um minuto, e mostra o ciclo inteiro do @sec-ch13b em código que dá pra ler [@akita2026microgpt]. Rode, quebre de propósito, mude o tamanho e veja o que acontece antes de pedir explicação a qualquer agente.

## O material, você que acha

<!-- src: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r -->
A segunda regra parece a mais velha. Eu aprendi a programar antes da internet, pegando ônibus pra tirar xerox de material emprestado, e hoje material sobra. Mas o exercício nunca foi juntar papel: foi escolher, comparar e descobrir qual fonte presta.

O agente pula essa etapa por você e entrega o resumo pronto. Use o resumo como mapa e vá ler o lugar de onde ele veio: a documentação, o código, o artigo original. Você já viu no @sec-ch04 o que acontece com quem confia na fonte que o modelo cita sem abrir.

## Ninguém mastigando

<!-- src: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r -->
A terceira regra é a que a IA mais ameaça. O chefe que dá tudo mastigado agora mora no seu bolso, e nunca se cansa de mastigar.

<!-- src: original -->
O hábito que eu recomendo é simples de dizer e chato de seguir: tente sozinho antes de perguntar à máquina. Dê um tempo a si mesmo, meia hora, uma tarde, e só então pergunte. Quando perguntar, peça uma pista em vez da solução, e depois compare a resposta dela com a sua tentativa. É na diferença entre as duas que o aprendizado acontece.

<!-- src: 2019/10/23/akitando-65-a-dor-de-aprender-que-cursos-livros -->
Vai doer, e é pra doer. Em 2019 eu escrevi que "aprendizado, no seu núcleo, é uma briga de você contra você mesmo" [@akitando065]. Se a máquina tira toda a dor, leva o aprendizado junto.

## O como e o porquê

<!-- src: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r -->
No mesmo episódio de 2020 eu reclamava de quem trocava de linguagem e se perdia:

> Como elas aprenderam só "como" usar a ferramenta mas nunca "por que" a ferramenta existe, toda nova ferramenta confunde elas.

<!-- src: original -->
Com o agente, o "como" ficou de graça: ele escreve o código, a fórmula, o parágrafo. O "por que" continua inteiro com você. Pra cada coisa que ele fizer, pergunte por que é assim, e confira se você saberia explicar sem ele (@sec-ch18). Se não saberia, você ainda não aprendeu, só recebeu.

## O que não envelhece

<!-- src: 2021/01/06/akitando-90-o-que-os-cursos-nao-te-ensinam-sobre-mercados -->
Ferramenta muda a cada década, às vezes a cada ano. O que eu vi atravessar todas as trocas, do dBase ao agente, foi uma base pequena:

- algoritmos e estruturas de dados, a matéria que, na minha opinião, separa o amador de quem vai fazer carreira [@akitando065];
- como o computador funciona por baixo: memória, processos, rede, o que acontece quando um programa roda [@akitando076];
- matemática básica, estatística e probabilidade, que nenhum curso de ferramenta ensina [@akitando090] e que são a matéria-prima de um modelo de linguagem (@sec-apmecanica).

<!-- src: 2019/10/23/akitando-65-a-dor-de-aprender-que-cursos-livros -->
Com essa base, linguagem nova vira questão de semanas. Em 2019 eu contei que aprendi Elixir, Crystal e Rust em uns 30 dias cada, a ponto de ficar produtivo, porque já tinha programado em muitas outras [@akitando065], contra os meses que as minhas primeiras linguagens me custaram sem base nenhuma (@sec-ch08).

<!-- src: original -->
Quem não programa pode trocar a lista pela base do próprio ofício: a contabilidade por trás da planilha, a gramática por trás do texto, a lei por trás do contrato. A regra é a mesma. A máquina acelera muito quem já tem o mapa, e quem não tem só chega mais rápido ao lugar errado.

<!-- src: original -->
A conta do epílogo, o 1% que o curso dá e os 99% que você caça sozinho (@sec-epilogo), continua de pé com a máquina do lado. Ela pode encurtar muito a caçada, desde que quem segure a lanterna continue sendo você.
