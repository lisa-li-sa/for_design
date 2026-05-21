#!/usr/bin/env python3
"""
Reformat kernel_out words with custom grouping order.

Rules implemented:
1. One output line contains 128 bytes = 32 words.
2. kernel_out has 4096 words, split into 16 major groups.
3. Each major group is split into 8 sub-groups, each sub-group has 32 words.
4. For each major group, print sub-group 8 in reverse order (word 32 -> word 1).
5. Then print sub-group 7/6/5/4/3/2/1 with the same reverse rule, each on a new line.
6. Repeat for all 16 major groups.

Input format:
- Supports common hex dump style with optional address header like "@40000000".
- Supports multiple words per line.

Output format:
- Each line has exactly 64 words separated by one space.
"""

from __future__ import annotations

import argparse
from pathlib import Path


TOTAL_WORDS = 4096
MAJOR_GROUPS = 16
WORDS_PER_MAJOR_GROUP = 256
SUB_GROUPS = 8
WORDS_PER_SUB_GROUP = 32


def load_words(path: Path) -> list[str]:
    words: list[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("@"):
                continue
            for tok in s.split():
                t = tok.strip().lower()
                if not t:
                    continue
                if len(t) > 8:
                    raise ValueError(f"Invalid word token '{tok}' in {path}")
                words.append(t.zfill(8))
    return words


def transform(words: list[str]) -> list[list[str]]:
    if len(words) != TOTAL_WORDS:
        raise ValueError(f"Expected {TOTAL_WORDS} words, got {len(words)}")

    out_lines: list[list[str]] = []

    for major_idx in range(MAJOR_GROUPS):
        major_base = major_idx * WORDS_PER_MAJOR_GROUP

        # sub-group order: 4 -> 3 -> 2 -> 1
        for sub_rev_idx in range(SUB_GROUPS - 1, -1, -1):
            sub_base = major_base + sub_rev_idx * WORDS_PER_SUB_GROUP
            block = words[sub_base : sub_base + WORDS_PER_SUB_GROUP]
            block.reverse()  # last word to first word in this sub-group
            out_lines.append(block)

    return out_lines


def write_lines(path: Path, lines: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for line_words in lines:
            if len(line_words) != WORDS_PER_SUB_GROUP:
                raise RuntimeError("Internal error: output line is not 32 words")
            f.write("data = " + "".join(line_words) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reorder kernel_out words by reversed sub-groups")
    parser.add_argument("--input", required=True, help="Input kernel_out hex file")
    parser.add_argument("--output", required=True, help="Output reordered hex file")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    words = load_words(in_path)
    out_lines = transform(words)
    write_lines(out_path, out_lines)

    print(f"input_words={len(words)}")
    print(f"output_lines={len(out_lines)}")
    print(f"words_per_line={WORDS_PER_SUB_GROUP}")
    print(f"wrote={out_path}")


if __name__ == "__main__":
    main()
