# cafe — YT filter + léxico BR

- `yt-filter.js` — userscript Tampermonkey (YouTube AI/AUTO/CLICK scores, DOM-only).
- `scripts/mine_br_lexicon.py` — minera léxico clickbait PT-BR das seeds e exporta
  `data/br_clickbait_lexicon.parquet` (tabela completa) + `data/br_clickbait_lexicon.json` (compacto p/ HTTP).
- `data/seeds/` — corpus curado: `clickbait_br.txt` vs `neutral_br.txt` (estenda aqui e rode de novo).

## Mineracao

```bash
uv sync
uv run scripts/mine_br_lexicon.py --top-n 250 --min-df 2
```

## Léxico via HTTP (git)

1. Suba o repo p/ o GitHub com `data/br_clickbait_lexicon.json` commitado.
2. No painel do script (botão `AI ⚙` no YouTube), cole em **URL do JSON**:
   `https://raw.githubusercontent.com/<user>/<repo>/main/data/br_clickbait_lexicon.json`
3. Clique **Recarregar léxico**. O JSON fica em cache (`localStorage`) p/ uso offline;
   sem URL, o script usa só o léxico embutido. `raw.githubusercontent.com` libera CORS (`*`),
   então `fetch()` direto funciona sem `@grant` extra.
