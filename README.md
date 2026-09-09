# cafe — YT filter + léxico BR

- `yt-filter.user.js` — userscript Tampermonkey (YouTube AI/AUTO/CLICK scores, DOM-only).
- `scripts/mine_br_lexicon.py` — minera léxicos PT-BR das seeds e exporta
  `data/<kind>_br.parquet` (tabela completa) + `data/<kind>_br.json` (compacto p/ HTTP),
  com `kind` em `clickbait|ai|automation`.
- `data/seeds/` — corpus curado: `clickbait_br.txt`, `ai_br.txt`, `automation_br.txt`
  vs `neutral_br.txt` (estenda aqui e rode de novo).

## Instalação (Tampermonkey, 1 clique)

> Vale após o push deste repo para `darocaecobr/lexico-filter` no GitHub.

1. Instale o Tampermonkey
   ([Chrome](https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo) ·
   [Firefox](https://addons.mozilla.org/firefox/addon/tampermonkey/) ·
   Edge: busque "Tampermonkey" na loja de complementos).
2. Clique para instalar:
   **[yt-filter.user.js](https://raw.githubusercontent.com/darocaecobr/lexico-filter/refs/heads/main/yt-filter.user.js)**
   → **Instalar** na tela do Tampermonkey.
   (A extensão `.user.js` é o que faz o navegador oferecer a instalação direta.)
3. Abra <https://www.youtube.com> → botão **YTAI ⚙** no canto inferior direito
   abre o painel.

## Configuração (padrões já vêm prontos)

- **Tolerância**: 3 sliders em % (IA, Automação, Clickbait). Oculta vídeos cuja
  probabilidade **passa** do valor; 100% = desligado. Abaixo, o contador
  `X ocultos de Y avaliados` mostra o efeito ao vivo.
- **Visibilidade**: mostra/oculta os selos IA, automação e BAIT nos cards.
- **Léxicos remotos**: as 3 URLs já apontam para este repo (raw do GitHub);
  **Atualizar léxicos ao iniciar** vem ligado; **Recarregar léxicos** força o
  download. Sem internet, vale o cache local; sem URL, vale o léxico embutido.
- **Resetar padrões** restaura tudo.

Quem instalou as versões locais antigas (`local.example`): reinstale uma vez
pelo link acima (a identidade do script mudou para o repo).

## Mineracao

```bash
uv sync
uv run scripts/mine_br_lexicon.py --kind clickbait
uv run scripts/mine_br_lexicon.py --kind ai
uv run scripts/mine_br_lexicon.py --kind automation
```

Fontes das seeds: clickbait (YTClickbait21K/BaitBuster/MVD/BollyBAIT),
IA (teses deepfake UNICAMP/UTFPR/UFPR + ferramentas T2V dos papers
VID-AID/GenVideo/GenBuster + disclosure YouTube/C2PA),
automação (Alliance4Europe "Infinite Slop Machine", purga YouTube 2026,
Agarwal/SEPS, CollATe).

## Léxico via HTTP (git)

1. Suba o repo p/ o GitHub com `data/*_br.json` commitados
   (o padrão já aponta para `darocaecobr/lexico-filter`).
2. No painel do script (botão `AI ⚙` no YouTube), confira cada URL:
   `https://raw.githubusercontent.com/darocaecobr/lexico-filter/refs/heads/main/data/<kind>_br.json`
   (troque pelo seu fork, se for o caso).
3. Clique **Recarregar léxicos**. O JSON fica em cache (`localStorage`) p/ uso offline;
   sem URL, o script usa só o léxico embutido. `raw.githubusercontent.com` libera CORS (`*`),
   então `fetch()` direto funciona sem `@grant` extra.

## Updates

- **Script**: `yt-filter.user.js` declara `@updateURL`/`@downloadURL` para
  `darocaecobr/lexico-filter` — o Tampermonkey verifica e oferece a nova versão
  sozinho (basta subir o arquivo com `@version` maior). Reinstale a partir da URL
  raw uma vez para o TM registrar a origem de update.
- **Léxicos**: com **Atualizar léxicos ao iniciar** ligado (padrão), o script baixa
  os 3 JSONs a cada abertura do YouTube; desligado, usa o cache e só atualiza no
  botão **Recarregar léxicos**.

## Créditos das pesquisas

### Clickbait (léxico `clickbait_br`)

- **YTClickbait21K** — Islam et al., 2026. 21.238 vídeos de 40 canais em 29 países,
  anotação tripla (κ≈0.65), metadados + thumbnails. Base da taxonomia multimodal
  título/thumbnail/conteúdo. <https://arxiv.org/abs/2606.14780>
- **BaitBuster-Bangla** — Imran et al., 2024. 253.070 vídeos (58 canais bengalis),
  18 features (metadados, engajamento, labels auto/humano/IA).
  Paper: <https://doi.org/10.1016/j.dib.2024.110239> ·
  HF: <https://huggingface.co/datasets/abdalimran/BaitBuster-Bangla> (MIT) ·
  Código: <https://github.com/abdalimran/BaitBuster-Bangla>
- **MVD (Misleading Video Dataset)** — Varshney & Vishwakarma, 2021. 987 vídeos
  anotados; similaridade título–áudio + consenso humano.
  <https://doi.org/10.1007/s10489-020-02057-9>
- **BollyBAIT + CPDM** — Mowar et al., 2021. 1.000 vídeos em 5 tipos
  (Misleading, Spam, Exaggerated, False Promises, Curiosity Gap); ensemble 92,89%
  (BollyBAIT) / 95,38% (MVD). <https://doi.org/10.48550/arxiv.2112.08611> ·
  Dataset: <https://doi.org/10.5281/zenodo.6559147>
- **Multilingual_Clickbait_Dataset** — `christinacdl`, HF, ~303k títulos EN,
  Apache-2.0. Principal fonte do padrão listicle/curiosity-gap em inglês.
  <https://huggingface.co/datasets/christinacdl/Multilingual_Clickbait_Dataset>

### IA sintética (léxico `ai_br`)

- **Moura (UNICAMP, diss. 2021)** — detecção de deepfakes com visão computacional;
  base própria + FaceForensics++/DFDC. <https://hdl.handle.net/20.500.12733/1640964>
- **Rosa (UTFPR, diss. 2026)** — pistas fisiológicas (PPG) + descritores manuais;
  Celeb-DF v1/v2, FaceForensics++.
  <https://repositoriocopia.utfpr.edu.br/jspui/handle/1/40449>
- **UFPR (TCC 2024)** — comparativo CNN/ViT em DFDC + FaceForensics++.
  <https://www.inf.ufpr.br/bcc/tcc/2024/2024%20A%20COMPARATIVE%20STUDY%20OF%20DEEPFAKE%20DETECTION%20TECHNIQUES.pdf>
- **Batista, 2025** — GenConViT; WildDeepfake, DeepSpeak (93,82%).
  <https://doi.org/10.48550/arxiv.2504.02900>
- **Pinto et al., 2025** — benchmark no Celeb-DF v2 (LSTM 97,32%).
  <https://doi.org/10.17013/risti.59.21-35>
- **Datasets de referência**: FaceForensics++ (1.000 vídeos)
  <https://github.com/ondyari/FaceForensics>, DFDC (~128k clipes;
  paper preview: <https://arxiv.org/abs/1910.08854>), Celeb-DF v2
  (5.639 fake + 890 reais) <https://github.com/yuezunli/celeb-deepfakeforensics>.
- **Geração T2V (vocabulário de ferramentas)**: VID-AID
  <https://doi.org/10.48550/arxiv.2507.13224>, GenVideo/DeMamba
  <https://doi.org/10.1007/s11432-024-4894-0>, GenBuster-200K/BusterX
  <https://doi.org/10.48550/arxiv.2505.12620>, GVF/DeCoF
  <https://arxiv.org/abs/2402.02085>, PS-FNVD/FakeSV <https://arxiv.org/abs/2608.06732>
- **Transparência**: rótulos de IA do YouTube ("conteúdo alterado/sintético")
  <https://support.google.com/youtube/answer/14328491> e padrão de proveniência
  **C2PA** <https://c2pa.org/>

### Automação / content farms (léxico `automation_br`)

- **Alliance4Europe, 2026** — "The Infinite Slop Machine": 29+ contas, 7.300 vídeos
  via InVideo (narração IA, thumbnails sintéticas, padrões `Hub/Updates`, 2–3 vídeos/dia).
  <https://alliance4europe.eu/wp-content/uploads/2026/05/The-Infinite-Slop-Machine.pdf>
- **Kirdemir et al., 2022** — comportamentos coordenados inautênticos no YouTube
  (39 canais, séries temporais + co-comentaristas). <https://ceur-ws.org/Vol-3138/paper6_jot.pdf>
- **Amure & Agarwal, 2025 (SEPS)** — canais anômalos via redes de co-comentaristas
  (97 canais, 702k vídeos). <https://doi.org/10.1007/s13278-025-01493-0>
- **Shajari & Agarwal, 2025** — escore de anomalia por comentaristas + engajamento
  (71 canais). <https://doi.org/10.1007/s13278-025-01470-7>
- **Dutta et al., 2021 (CollATe)** — entidades colusivas via blackmarkets
  (YouLikeHits). <https://doi.org/10.1145/3477300>
- **CSUSB, tese** — detecção de spam em comentários do YouTube (dataset Kaggle,
  CNN 92%+).
  <https://scholarworks.lib.csusb.edu/cgi/viewcontent.cgi?article=3181&context=etd>
- **Kapwing, 2026** — relatório "AI slop" (~21% dos Shorts de contas novas;
  cobertura: <https://www.xataka.com.br/diversos/novo-estudo-comprova-youtube-virou-um-deposito-videos-toscos-inteligencia-artificial>)
- **YouTube, purga 2026** — remoção de 16 canais-fazenda (4,7 bi views):
  sinais oficiais de repetição, narração sintética e volume industrial.
  <https://olhartecdigital.com/youtube-derruba-canais-automatizados-47-bilhoes-visualizacoes/>

> Este projeto usa apenas sinais textuais DOM + léxicos minerados dessas fontes;
> detecção por pixels/áudio/comentários das teses acima é referência, não código.
