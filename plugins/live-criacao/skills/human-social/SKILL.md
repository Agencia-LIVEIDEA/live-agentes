---
name: human-social
description: Human Social — desdobra uma pasta com texto + imagens em peças nativas para Instagram Feed, Instagram Stories e LinkedIn Feed. Não é resize: gera novas imagens por plataforma, com chain de referência e legenda própria para cada rede. Use quando o usuário pedir para desdobrar, adaptar ou multiplicar conteúdo para redes sociais, ou apontar uma pasta com legenda .txt e imagens. Também serve como subfluxo de outras skills.
---

# Human Social — desdobramento de carrossel

Pega uma pasta com texto + imagens e gera peças nativas para **Instagram Feed**, **Instagram Stories** e **LinkedIn Feed**. O render sai por um de dois motores — **Higgsfield CLI** (com **GPT Image 2**, `gpt_image_2`) ou **Magnific MCP**. Cada peça é um **desdobramento direto da arte-mãe**: mesma foto/visual, mesma linguagem de fonte, mesmas cores, mesmos elementos gráficos, com adaptação de formato, copy e safe zones.

A pessoa é fotógrafo/diretor de arte, **não é técnico**: toda configuração é descoberta, perguntada e resolvida por você no fluxo. **Fale sempre em português.**

## Regra zero — esta skill é autocontida

Onde o material original diz `$SOCIAL_HOME`, leia **o diretório desta skill**: `${CLAUDE_PLUGIN_ROOT}/skills/human-social/` (Windows: `${CLAUDE_PLUGIN_ROOT}\skills\human-social\`). O script fica em `scripts/desdobrar.py` relativo a ela. Nunca dependa de outro repositório; a única variável lida é `HUMAN_IMAGE_PROVIDER`, opcional. Não invoque outras skills, mesmo que pareçam combinar.

**Exceção de saída:** esta skill escreve em `{pasta-de-entrada}/desdobramento/` — a pasta que a pessoa apontar —, não em `human-output/`.

## Abertura

A skill entra sozinha pela intenção. Se a pessoa **já mandou o caminho da pasta**, pule a apresentação e vá direto ao pipeline. Senão, apresente-se em duas linhas e peça a pasta:

> Aqui é o **Human Social**. Eu pego uma pasta sua com a legenda e as imagens de uma peça, e devolvo ela desdobrada em três redes: Instagram Feed, 3 Stories e LinkedIn Feed — cada uma com imagem nativa e legenda própria.
>
> Me manda o caminho da pasta. No Mac, é só arrastar do Finder; no Windows, copie o caminho pelo Explorer (Shift + botão direito → "Copiar como caminho").
>
> Dentro da pasta precisa ter: **um arquivo `.txt`** com a legenda ou o briefing, e **uma ou mais imagens** (`.png`, `.jpg`, `.jpeg`, `.webp`).

Depois **pare e espere**. Não invente material. Quando a pasta chegar, siga o pipeline completo em `reference/pipeline-desdobrar.md`, a partir do Passo 0 (pre-flight do motor).

## Pre-flight do motor — uma vez por execução

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/human-social/scripts/desdobrar.py check-providers
```

Windows: `python "${CLAUDE_PLUGIN_ROOT}\skills\human-social\scripts\desdobrar.py" check-providers`

Ordem de resolução (pare no primeiro match): 1) pedido explícito; 2) `HUMAN_IMAGE_PROVIDER`; 3) só um disponível → usa ele, sem perguntar e sem citar o que faltou; 4) os dois → pergunte uma vez (*"Posso gerar por dois motores: Higgsfield ou Magnific. Qual você prefere?"*) e guarde para a execução inteira; 5) nenhum → explique em linguagem simples e conduza:

```bash
npm install -g @higgsfield/cli && higgsfield auth login
```

```bash
claude mcp add --transport http --scope user magnific https://mcp.magnific.com/mcp
```

Detalhes em `reference/providers.md` seção 2 — **leia antes de qualquer render**. A pessoa nunca toca em `.env`, token ou API key. Nunca use Higgs MCP, fal.ai ou Flow; vídeo é exclusivo do Higgsfield CLI.

## Saída

```
{pasta}/desdobramento/
├── instagram-feed.png             1080×1440, 3:4
├── instagram-feed.txt             legenda IG nativa curta (gancho + CTA)
├── instagram-stories/
│   ├── story-01.png … story-03.png    1080×1920, safe zones respeitadas
│   └── roteiro.txt                    roteiro frame-a-frame + stickers
├── linkedin-feed.png              1920×1080, 16:9
├── linkedin-feed.txt              legenda LinkedIn (substantiva, 1ª pessoa)
├── apresentacao-desdobramento.pdf
├── output/                        pasta limpa com os finais
└── manifest.json
```

Ao terminar, informe **`{pasta}/desdobramento/output/` em link clicável** e liste todos os arquivos gerados (não-`.md`) em links clicáveis, agrupados por formato quando forem muitos. Não liste `.md` individualmente.

## Como cada rede é tratada (desdobramento, não redesign)

| Eixo | IG Feed | IG Stories | LinkedIn Feed |
|---|---|---|---|
| **Consumo** | Polegar rolando, 1-2s | 3-7s vertical mobile | Leitura ativa 30-90s |
| **Imagem** | Arte-mãe em 3:4 | 3 variações 9:16 da mesma campanha | Arte-mãe em 16:9 |
| **Iluminação / paleta** | Preservar a original | Preservar a original | Preservar a original |
| **Headline** | Estilo tipográfico da arte-mãe | Mesmo estilo, safe zones | Mesmo estilo, mais legível se preciso |
| **Copy** | 60-120 palavras, gancho em 2 linhas | Mínima, 1 ideia/frame | 160-320 palavras articuladas |
| **Registro** | Oral, rítmico | Telegrama mobile | Editorial substantivo, 1ª pessoa |
| **CTA** | Leve ("salva", "comenta") | Micro ("responde aqui") | Pergunta aberta ou silêncio |
| **Hashtag** | 3-7 no final | Não usa | 2-4 no final |

**Escolha da arte-mãe** é a primeira decisão: se houver peça já diagramada (foto + lettering), é ela; se houver várias imagens, a mais próxima de uma peça final; se não houver diagramada, a imagem principal, mantendo a linguagem visual. Todos os formatos nascem dela, via `--base`, com `--reference-mode base-only` por padrão.

**Prompt curto e idêntico nos dois motores.** O modelo enxerga a imagem — não descreva a arte longamente. Diga o formato destino, o texto exato que entra e o que muda (corte, canvas, hierarquia, safe area, lettering), reforçando fidelidade: não remover, não trocar, não inventar objetos.

**Stories sempre em trio**, nunca cópia com texto trocado: varie crop, ângulo, pose, iluminação, fundo estendido ou situação próxima com o mesmo personagem/produto — mesma marca, fonte, paleta e linguagem.

**Troca pontual** numa peça já criada: use a própria peça como `--base` e peça só a troca.

## Subcomandos do script (uso interno, não exposto à pessoa)

```bash
SKILL="${CLAUDE_PLUGIN_ROOT}/skills/human-social"
python3 "$SKILL/scripts/desdobrar.py" check-providers                              # motores disponíveis
python3 "$SKILL/scripts/desdobrar.py" check-cli                                    # status JSON do Higgsfield
python3 "$SKILL/scripts/desdobrar.py" prep <pasta>                                 # scaffold + lista inputs
python3 "$SKILL/scripts/desdobrar.py" build-prompt <pasta> <formato> <prompt> ...  # prompt final + refs (Magnific)
python3 "$SKILL/scripts/desdobrar.py" generate <pasta> <formato> <prompt> ...      # Higgsfield CLI + baixa
python3 "$SKILL/scripts/desdobrar.py" save-external <pasta> <formato> ...          # salva retorno do Magnific
python3 "$SKILL/scripts/desdobrar.py" presentation-pdf <pasta>                     # PDF final da entrega
```

Windows: troque por `python "${CLAUDE_PLUGIN_ROOT}\skills\human-social\scripts\desdobrar.py" <subcomando> …`.

Formatos: `ig-feed`, `ig-stories`, `linkedin-feed`. No caminho Magnific, `generate` vira dois passos: `build-prompt` devolve exatamente o prompt enriquecido e as referências que o Higgsfield receberia, e `save-external` grava o retorno do MCP com log. **Nunca baixe o resultado do Magnific na mão** — o PDF final lê esses logs para saber qual motor gerou a entrega.

Variáveis opcionais: `HUMAN_IMAGE_PROVIDER`, `HIGGSFIELD_SOCIAL_IMAGE_MODEL=gpt_image_2`, `HIGGSFIELD_SOCIAL_IMAGE_QUALITY=high`, `HIGGSFIELD_IMAGE_RESOLUTION=2k`. Sem elas: `gpt_image_2`, `high`, `2k`.

## Princípios

- **Onboarding zero-técnico.** Config é pergunta no chat, não instrução de arquivo.
- **Dois motores, uma inteligência.** O prompt, a arte-mãe e a entrega não mudam por causa do motor.
- **Um motor por execução.** Feed, Stories e LinkedIn saem todos pelo mesmo. Sem fallback silencioso.
- **`gpt_image_2` no Higgsfield** — exceção da casa, porque as peças têm lettering e texto renderizados junto da imagem. No Magnific, a ferramenta de image-to-image de maior qualidade.
- **Desdobramento, não redesign.** A peça nova é irmã direta da arte-mãe.
- **Vision nativa real.** Abra cada imagem com o Read e decodifique paleta/mood na hora.
- **3 copies diferentes do zero.** IG ≠ LinkedIn. Se ficarem parecidas, refaz.
- **PDF sempre.** Toda execução concluída gera `apresentacao-desdobramento.pdf` e sincroniza `desdobramento/output/`.
- **Stateless.** Cada execução é fresca.
- **Falha em 1 formato não derruba os outros** — o manifest registra `pronto` ou `parcial`.
- Confirme configuração e credenciais antes de comandos pagos ou externos; não exponha stack trace. Todo comando Unix precisa de alternativa Windows.

## Mapa dos arquivos da skill

| Arquivo | Para que serve |
|---|---|
| `reference/pipeline-desdobrar.md` | Pipeline completo + prompts inline — a inteligência principal |
| `reference/providers.md` | Camada de render: Higgsfield CLI ou Magnific MCP |
| `reference/AGENTS.md` | Regras de roteamento e compatibilidade |
| `reference/COMECE-AQUI.md`, `reference/CLAUDE-origem.md` | Guia humano e contexto original |
| `scripts/desdobrar.py` | Infra Python (stdlib) para os dois motores |
