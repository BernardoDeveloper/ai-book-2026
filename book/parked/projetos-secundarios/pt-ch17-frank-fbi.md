<!-- Parked 2026-10-14: the Frank FBI subsections as they stood before the trim (book/pt/ch17.md). -->

### Frank FBI

<!-- src: 2026/03/09/atacando-fraudes-via-email-frank-fbi -->
Assim nasceu o Frank FBI, de Fraud Bureau of Investigation [@akita2026frankfbi]. A ideia é simples: recebeu um e-mail suspeito, encaminha pra um endereço dedicado. Em poucos minutos, a resposta volta na mesma conversa, com um relatório de risco.

Por trás, o e-mail passa por seis camadas de análise, cada uma com um peso na nota final:

- a autenticação do remetente, que confere se o e-mail veio mesmo do servidor de quem diz ter mandado;
- a reputação do remetente, incluindo a idade do domínio (domínio registrado poucos dias antes já é um sinal) e listas públicas de endereços problemáticos;
- o conteúdo, procurando urgência artificial ("sua conta será bloqueada em 24 horas"), pedidos de dados pessoais e links cujo texto aponta pra um lugar e o endereço real pra outro;
- bases públicas de links maliciosos já conhecidos;
- uma investigação em fontes abertas pra ver se a empresa ou pessoa que assina existe e é quem diz ser;
- e, por fim, a análise por LLM.

<!-- src: 2026/03/09/atacando-fraudes-via-email-frank-fbi -->
A camada de IA é a que tem mais peso sozinha, 30% da nota. As outras cinco somam 70%, e a própria camada não depende de um modelo só.

Três modelos de empresas diferentes (naquele março, um Claude, um GPT e um Grok) leem o e-mail de forma independente, e um sistema de votação pondera as respostas pela confiança de cada um. Se os três concordam que é fraude, a confiança é alta. Se divergem, o sistema pesa. Se todos falham, a camada cai pra uma nota neutra de 50 em vez de chutar.

![O e-mail suspeito passa por seis camadas; o LLM é uma voz entre várias, e suas afirmações são conferidas contra os dados das outras.](assets/figures/ch17-camadas-frank-fbi.png){#fig-ch17-camadas-frank-fbi fig-alt="Um envelope rotulado e-mail suspeito entra por cima e passa por seis faixas horizontais empilhadas, cada uma com seu peso: autenticação do remetente 15%, reputação do remetente 15%, conteúdo 15%, links maliciosos conhecidos 15%, identidade de quem assina 10% e análise por LLM 30%. Na faixa do LLM, três pequenas caixas alimentam uma votação. Setas pontilhadas de conferência, à esquerda, ligam a faixa do LLM às outras cinco. À direita, as seis faixas convergem num medidor de risco de 0 a 100."}

<!-- src: 2026/03/09/atacando-fraudes-via-email-frank-fbi -->
Teve um cuidado a mais, porque LLM inventa coisa (@sec-ch04). Se um modelo escreve no relatório que "este domínio foi registrado há um dia" sem nenhuma evidência nos dados, o relatório fica comprometido. Então as afirmações dos modelos são conferidas contra os dados concretos das camadas que não usam IA, como a consulta de quando o domínio foi registrado. Se o modelo contradiz os fatos, a afirmação é descartada ou sinalizada.

Também apareceu um defeito que eu gosto de lembrar. Quando uma camada falhava, ela devolvia nota zero, e esse zero puxava a média pra baixo, fazendo e-mails fraudulentos parecerem mais seguros do que eram. Uma camada quebrada estava, na prática, absolvendo golpistas. A correção passou a descartar a camada que falhou em vez de deixá-la votar.

> Um LLM é uma boa camada de um detector de golpe. Nunca deveria ser o juiz.

### Pensar como o atacante

<!-- src: 2026/03/09/atacando-fraudes-via-email-frank-fbi -->
O Frank FBI saiu em umas 17 horas de trabalho, com muito código escrito pela IA. Mas nenhum dos reforços de segurança importantes veio do modelo sugerindo "ei, vamos proteger isso aqui".

Fui eu que parei e perguntei: e se alguém falsificar o endereço de um dos usuários autorizados pra usar o serviço? A ferramenta passou a conferir a autenticação de quem encaminha antes de aceitar qualquer coisa.

<!-- src: 2026/03/09/atacando-fraudes-via-email-frank-fbi -->
A outra pergunta foi mais traiçoeira. O Frank FBI pode, se você quiser, denunciar golpes confirmados a bases comunitárias, que filtros de e-mail e firewalls do mundo inteiro consultam pra bloquear ameaças. E se um atacante percebe isso e manda e-mails de propósito, montados pra fazer o sistema denunciar o domínio de uma empresa inocente?

Isso tem nome, envenenamento, e é um ataque real contra esse tipo de base. A defesa veio em camadas: uma lista de uns 40 domínios conhecidos que nunca são denunciados, exclusão de domínios com varredura limpa, filtro de endereços de grandes provedores de nuvem.

<!-- src: 2026/03/09/atacando-fraudes-via-email-frank-fbi -->
O modelo implementou tudo isso quando eu pedi. Perceber o buraco foi trabalho meu. É o mesmo recado de @sec-ch16, visto de outro ângulo: a IA acelera quem já sabe onde o perigo mora.

### Por que eu não ofereço isso como serviço

<!-- src: 2026/03/09/atacando-fraudes-via-email-frank-fbi -->
Quem olha pro Frank FBI pode ter a ideia de transformá-lo em serviço pro público. Eu desaconselho com todas as letras. Quem opera um serviço desses tem acesso a todos os e-mails encaminhados pelos usuários: dados pessoais, correspondência de empresa, conversas sensíveis de gente que já está numa situação vulnerável.

Um servidor central vira um alvo valiosíssimo, e ninguém garante que o próprio operador não vá ler o que passa por ali.

<!-- src: 2026/03/09/atacando-fraudes-via-email-frank-fbi -->
Por isso o projeto foi feito pra rodar no seu servidor, ou na infraestrutura da sua empresa, com os dados ficando com você. A licença escolhida obriga quem oferecer o código como serviço de rede a abrir todas as mudanças que fizer, justamente pra dificultar que alguém pegue o projeto, acrescente rastreamento e ofereça como "verificação gratuita de e-mail" enquanto coleta dados por baixo dos panos.

<!-- src: original -->
Repare no padrão. O detector de golpe "grátis" que lê todos os seus e-mails é o mesmo negócio do aplicativo "grátis" que monta o seu fingerprint. Quando o serviço é de graça e você não sabe quem está do outro lado, a desconfiança começa pela própria ferramenta.

