# Link check da bibliografia

Verificação de 292 URLs de `book/back/references.yaml` em 2026-10-13: GET com user agent `ai-book-2026/1.0 (https://www.akitaonrails.com/)`, seguindo redirecionamentos, no máximo 2 requisições por segundo, com espera e nova tentativa em respostas 429. Nenhuma citação foi removida por causa do resultado; links mortos ganharam um `note` "Arquivado em: ..." apontando para a cópia no Wayback Machine, sem remover a URL original.

Resumo: 264 respondem 2xx; 2 mortos (404/410/DNS); 26 bloqueados ou com paywall (401/403/429); 1 com outros erros.

## Links mortos (404, 410, DNS)

| Chave | URL | Status | Capítulos | Arquivo (Wayback) |
|---|---|---|---|---|
| `koi2026clawhavoc` | <https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting> | HTTP 200, redireciona para página não relacionada (Palo Alto Networks) | apA, ch16 | <https://web.archive.org/web/20260210212946/https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting> |
| `openai2025codexprompt` | <https://github.com/openai/codex/blob/main/codex-rs/core/prompt.md> | HTTP 404 | ch03 | <https://web.archive.org/web/20260201125545/https://github.com/openai/codex/blob/main/codex-rs/core/prompt.md> |

## Bloqueados ou com paywall (401, 403, 429)

Em geral são proteções anti-robô (Cloudflare, Akamai) ou paywall; a página existe para um navegador comum. Mantidos como estão.

| Chave | URL | Status | Capítulos |
|---|---|---|---|
| `adobe2026genai` | <https://helpx.adobe.com/photoshop/kb/troubleshoot-generative-ai-features.html> | HTTP 403 | ch19 |
| `alammar2024handson` | <https://www.oreilly.com/library/view/hands-on-large-language/9781098150952/> | HTTP 403 | antes |
| `axios2026sora` | <https://www.axios.com/2026/03/24/openai-discontinue-sora-video-app> | HTTP 403 | apA, ch17 |
| `bender2021dangers` | <https://doi.org/10.1145/3442188.3445922> | HTTP 403 | apmecanica |
| `franzen2026claude` | <https://venturebeat.com/technology/claude-codes-source-code-appears-to-have-leaked-heres-what-we-know/> | HTTP 429 | ch02 |
| `gartner2025agentic` | <https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027> | HTTP 403 | ch14 |
| `kelleher2019deep` | <https://mitpress.mit.edu/9780262537551/deep-learning/> | HTTP 403 | antes |
| `krietzberg2026mythos` | <https://puck.news/is-anthropics-mythos-model-as-dangerous-as-everyone-says/> | HTTP 403 | ch14 |
| `lefkowitz2019perceptron` | <https://news.cornell.edu/stories/2019/09/professors-perceptron-paved-way-ai-60-years-too-soon> | HTTP 403 | apA, ch01 |
| `martin2008clean` | <https://www.oreilly.com/library/view/clean-code-a/9780136083238/> | HTTP 403 | ch09 |
| `mediaite2026pace` | <https://www.mediaite.com/media/elon-musk-and-sam-altman-agree-with-anthropic-boss-ai-must-slow-down-to-avoid-catastrophic-damage/> | HTTP 403 | ch14 |
| `openai2019gpt2` | <https://openai.com/index/gpt-2-1-5b-release/> | HTTP 403 | apA, ch01 |
| `openai2022chatgpt` | <https://openai.com/index/chatgpt/> | HTTP 403 | apA, ch01, ch18 |
| `openai2023classifier` | <https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/> | HTTP 403 | ch04 |
| `openai2023custominstructions` | <https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions> | HTTP 403 | ch09 |
| `openai2023function` | <https://openai.com/index/function-calling-and-other-api-updates/> | HTTP 403 | apA, ch03, ch20 |
| `openai2024caching` | <https://openai.com/index/api-prompt-caching/> | HTTP 403 | apA, ch20 |
| `openai2024o1` | <https://openai.com/index/learning-to-reason-with-llms/> | HTTP 403 | apA, ch03, ch20 |
| `openai2026navierstokes` | <https://openai.com/index/navier-stokes-solution/> | HTTP 403 | apA, ch14 |
| `openai2026sweverified` | <https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/> | HTTP 403 | apA, ch11 |
| `axios2026astra` | <https://www.axios.com/2026/09/03/openai-astra-gpt-6-agi-brockman> | HTTP 403 | apA, ch14 |
| `piratewires2026coxon` | <https://www.piratewires.com/p/jacob-coxon-worked-with-ai-doomer-firm> | HTTP 429 | ch14 |
| `radford2019better` | <https://openai.com/index/better-language-models/> | HTTP 403 | apA, ch01, ch20 |
| `reuters2024limitations` | <https://www.reuters.com/technology/artificial-intelligence/openai-rivals-seek-new-path-smarter-ai-current-methods-hit-limitations-2024-11-11/> | HTTP 401 | apA, ch01, ch20 |
| `rozen2026senate` | <https://www.reuters.com/legal/litigation/us-senate-negotiators-consider-requiring-ai-firms-mitigate-known-major-risks-2026-09-11/> | HTTP 401 | ch14 |
| `weizenbaum1966eliza` | <https://doi.org/10.1145/365153.365168> | HTTP 403 | apA, ch01 |

## Outros erros

| Chave | URL | Status | Capítulos | Observação |
|---|---|---|---|---|
| `amd2025ryzenaimax` | <https://www.amd.com/en/products/processors/laptop/ryzen/ai-300-series/amd-ryzen-ai-max-plus-395.html> | erro de rede (curl 92: HTTP/2 stream 1 reset by server (error 0x2 INTERNAL_ERROR)) | ch13 | servidor derruba a conexão HTTP/2 e não responde em HTTP/1.1 para clientes não-navegador; provável bloqueio anti-robô, mantido |
