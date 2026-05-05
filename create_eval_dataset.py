import os
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
MD_FILE = ROOT / 'labs_open_ended.md'
OUT_FILE = ROOT / 'test_dataset.json'


def split_sentences(text):
    # naive sentence splitter: split on ., ? or ! followed by whitespace/newline
    parts = re.split(r'(?<=[\.\?\!])\s+', text)
    # clean and remove short fragments
    sentences = [p.strip() for p in parts if len(p.strip()) > 30]
    return sentences


def build_dataset_from_md(md_path, n=20):
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")
    text = md_path.read_text(encoding='utf-8')
    sents = split_sentences(text)
    items = []
    for i, s in enumerate(sents[:n]):
        # create a conservative question that asks to quote/recall the sentence
        excerpt = ' '.join(s.split()[:8])
        question = f"According to the document, what is stated about: '{excerpt}...'?"
        items.append({"question": question, "ground_truth": s})
    return items


def main():
    dataset = build_dataset_from_md(MD_FILE, n=20)
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(dataset)} examples to {OUT_FILE}")


if __name__ == '__main__':
    main()
