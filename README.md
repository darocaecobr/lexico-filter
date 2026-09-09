# cafe — YT filter + léxico BR

- `yt-filter.js` — userscript Tampermonkey (YouTube AI/AUTO/CLICK scores, DOM-only).
- `scripts/mine_br_lexicon.py` — minera léxicos PT-BR das seeds e exporta
  `data/<kind>_br.parquet` (tabela completa) + `data/<kind>_br.json` (compacto p/ HTTP),
  com `kind` em `clickbait|ai|automation`.
- `data/seeds/` — corpus curado: `clickbait_br.txt`, `ai_br.txt`, `automation_br.txt`
  vs `neutral_br.txt` (estenda aqui e rode de novo).

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

1. Suba o repo p/ o GitHub com `data/*_br.json` commitados.
2. No painel do script (botão `AI ⚙` no YouTube), cole em cada URL:
   `https://raw.githubusercontent.com/<user>/<repo>/main/data/<kind>_br.json`
3. Clique **Recarregar léxicos**. O JSON fica em cache (`localStorage`) p/ uso offline;
   sem URL, o script usa só o léxico embutido. `raw.githubusercontent.com` libera CORS (`*`),
   então `fetch()` direto funciona sem `@grant` extra.

## Créditos das pesquisas

### Clickbait (léxico `clickbait_br`)

- **YTClickbait21K** — Islam et al., 2026. 21.238 vídeos de 40 canais em 29 países,
  anotação tripla (κ≈0.65), metadados + thumbnails. Base da taxonomia multimodal
  título/thumbnail/conteúdo. `arXiv:2606.14780`.
- **BaitBuster-Bangla** — Imran et al., 2024. 253.070 vídeos (58 canais bengalis),
  18 features (metadados, engajamento, labels auto/humano/IA).
  `doi:10.1016/j.dib.2024.110239` · `arXiv:2310.11465` · HF `abdalimran/BaitBuster-Bangla` (MIT).
- **MVD (Misleading Video Dataset)** — Varshney & Vishwakarma, 2021. 987 vídeos
  anotados; similaridade título–áudio + consenso humano.
  `doi:10.1007/s10489-020-02057-9`.
- **BollyBAIT + CPDM** — Mowar et al., 2021. 1.000 vídeos em 5 tipos
  (Misleading, Spam, Exaggerated, False Promises, Curiosity Gap); ensemble 92,89%
  (BollyBAIT) / 95,38% (MVD). `arXiv:2112.08611` · Zenodo `doi:10.5281/zenodo.6559147`.
- **Multilingual_Clickbait_Dataset** — `christinacdl`, HF, ~303k títulos EN,
  Apache-2.0. Principal fonte do padrão listicle/curiosity-gap em inglês.

### IA sintética (léxico `ai_br`)

- **Moura (UNICAMP, diss. 2021)** — detecção de deepfakes com visão computacional;
  base própria + FaceForensics++/DFDC. `hdl.handle.net/20.500.12733/1640964`.
- **Rosa (UTFPR, diss. 2026)** — pistas fisiológicas (PPG) + descritores manuais;
  Celeb-DF v1/v2, FaceForensics++.
- **UFPR (TCC 2024)** — comparativo CNN/ViT em DFDC + FaceForensics++.
- **Batista, 2025** — GenConViT; WildDeepfake, DeepSpeak (93,82%).
  `arXiv:2504.02900`.
- **Pinto et al., 2025** — benchmark no Celeb-DF v2 (LSTM 97,32%).
  `doi:10.17013/risti.59.21-35`.
- **Datasets de referência**: FaceForensics++ (1.000 vídeos), DFDC (~128k clipes),
  Celeb-DF v2 (5.639 fake + 890 reais).
- **Geração T2V (vocabulário de ferramentas)**: VID-AID `arXiv:2507.13224`,
  GenVideo/DeMamba, GenBuster-200K/BusterX `arXiv:2505.12620`,
  GVF/DeCoF `arXiv:2402.02085`, PS-FNVD/FakeSV `arXiv:2608.06732`.
- **Transparência**: rótulos de IA do YouTube ("conteúdo alterado/sintético") e
  padrão de proveniência **C2PA**.

### Automação / content farms (léxico `automation_br`)

- **Alliance4Europe, 2026** — "The Infinite Slop Machine": 29+ contas, 7.300 vídeos
  via InVideo (narração IA, thumbnails sintéticas, padrões `Hub/Updates`, 2–3 vídeos/dia).
- **Kirdemir et al., 2022** — comportamentos coordenados inautênticos no YouTube
  (39 canais, séries temporais + co-comentaristas). CEUR-WS Vol-3138.
- **Amure & Agarwal, 2025 (SEPS)** — canais anômalos via redes de co-comentaristas
  (97 canais, 702k vídeos). `doi:10.1007/s13278-025-01493-0`.
- **Shajari & Agarwal, 2025** — escore de anomalia por comentaristas + engajamento
  (71 canais). `doi:10.1007/s13278-025-01470-7`.
- **Dutta et al., 2021 (CollATe)** — entidades colusivas via blackmarkets
  (YouLikeHits). `doi:10.1145/3477300`.
- **CSUSB, tese** — detecção de spam em comentários do YouTube (dataset Kaggle,
  CNN 92%+).
- **Kapwing, 2026** — relatório "AI slop" (~21% dos Shorts de contas novas).
- **YouTube, purga 2026** — remoção de 16 canais-fazenda (4,7 bi views):
  sinais oficiais de repetição, narração sintética e volume industrial.

> Este projeto usa apenas sinais textuais DOM + léxicos minerados dessas fontes;
> detecção por pixels/áudio/comentários das teses acima é referência, não código.
