"""Mineracao de lexico clickbait PT-BR.

Le os corpus de seeds (clickbait vs neutro), calcula n-gramas
discriminativos via log-odds suavizado e exporta:
  - data/br_clickbait_lexicon.parquet (tabela completa p/ analise)
  - data/br_clickbait_lexicon.json   (compacto p/ o userscript via HTTP)

Uso:
    uv run scripts/mine_br_lexicon.py
    uv run scripts/mine_br_lexicon.py --top-n 300 --min-df 2
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEEDS = DATA / "seeds"

TOKEN = re.compile(r"[\w]+", re.UNICODE)

STOPWORDS = {
    "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas",
    "para", "com", "que", "como", "por", "ao", "aos", "uma", "uns",
    "umas", "se", "sua", "seu", "suas", "seus", "este", "esta",
    "esse", "essa", "isso", "isto", "foi", "são", "ser", "tem",
    "mais", "mas", "sem", "sobre", "entre", "até", "após", "dos",
    "das", "e", "o", "a", "os", "as", "um", "é", "à",
}


def load_titles(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


def ngrams(tokens: list[str], n: int) -> list[str]:
    if len(tokens) < n:
        return []
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def doc_terms(title: str, max_n: int = 3) -> set[str]:
    tokens = tokenize(title)
    terms: set[str] = set()
    for n in range(1, max_n + 1):
        for gram in ngrams(tokens, n):
            words = gram.split()
            # Unigrama puro de stopword nao carrega sinal.
            if n == 1 and words[0] in STOPWORDS:
                continue
            # N-grama valido se tem ao menos 1 palavra fora da stoplist.
            if any(w not in STOPWORDS for w in words):
                terms.add(gram)
    return terms


def mine(
    cb_titles: list[str],
    nb_titles: list[str],
    min_df: int = 2,
    min_log_odds: float = 0.5,
) -> list[dict]:
    df_cb: Counter[str] = Counter()
    df_nb: Counter[str] = Counter()
    for title in cb_titles:
        df_cb.update(doc_terms(title))
    for title in nb_titles:
        df_nb.update(doc_terms(title))

    n_cb, n_nb = len(cb_titles), len(nb_titles)
    rows: list[dict] = []
    for term, c in df_cb.items():
        if c < min_df:
            continue
        o = df_nb.get(term, 0)
        p_cb = (c + 1) / (n_cb + 2)
        p_nb = (o + 1) / (n_nb + 2)
        log_odds = math.log(p_cb / p_nb)
        if log_odds < min_log_odds:
            continue
        # Normaliza: ~4 nats = sinal fortissimo -> score 1.0
        score = round(min(1.0, log_odds / 4.0), 3)
        rows.append(
            {
                "term": term,
                "n": len(term.split()),
                "df_cb": c,
                "df_nb": o,
                "log_odds": round(log_odds, 3),
                "score": score,
            }
        )
    rows.sort(key=lambda r: (-r["log_odds"], -r["df_cb"], r["term"]))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Minera lexico clickbait PT-BR")
    parser.add_argument("--clickbait", default=str(SEEDS / "clickbait_br.txt"))
    parser.add_argument("--neutral", default=str(SEEDS / "neutral_br.txt"))
    parser.add_argument("--out-parquet", default=str(DATA / "br_clickbait_lexicon.parquet"))
    parser.add_argument("--out-json", default=str(DATA / "br_clickbait_lexicon.json"))
    parser.add_argument("--top-n", type=int, default=250)
    parser.add_argument("--min-df", type=int, default=2)
    parser.add_argument("--min-log-odds", type=float, default=0.5)
    parser.add_argument("--version", default="1")
    args = parser.parse_args()

    cb_titles = load_titles(Path(args.clickbait))
    nb_titles = load_titles(Path(args.neutral))
    if not cb_titles or not nb_titles:
        raise SystemExit("corpus vazio: verifique os arquivos de seeds")

    rows = mine(cb_titles, nb_titles, args.min_df, args.min_log_odds)

    import pandas as pd

    df = pd.DataFrame(rows, columns=["term", "n", "df_cb", "df_nb", "log_odds", "score"])
    df["lang"] = "pt-BR"
    df["lexicon_version"] = f"br-v{args.version}"
    out_parquet = Path(args.out_parquet)
    out_parquet.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_parquet, index=False)

    top = rows[: args.top_n]
    payload = {
        "version": f"br-v{args.version}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "lang": "pt-BR",
        "source": "seeds BR locais (clickbait vs neutro)",
        "count": len(top),
        "phrases": [{"t": r["term"], "s": r["score"]} for r in top],
    }
    out_json = Path(args.out_json)
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"titles: cb={len(cb_titles)} nb={len(nb_titles)}")
    print(f"termos: {len(rows)} (top-{len(top)} no JSON)")
    print(f"parquet: {out_parquet} ({out_parquet.stat().st_size} bytes)")
    print(f"json: {out_json} ({out_json.stat().st_size} bytes)")
    print("top-20:")
    for r in top[:20]:
        print(f"  {r['term']!r} s={r['score']} cb={r['df_cb']} nb={r['df_nb']}")


if __name__ == "__main__":
    main()
