# Book build pipeline

Builds *AI-Assisted Coding with Claude* as an A4, 11 pt PDF with a
book-style front and back cover.

```bash
make -C book MANUSCRIPT=/path/to/manuscript.md
# -> book/build/AI-Assisted-Coding-with-Claude.pdf
```

The manuscript is **not** in this repository. Export the book's working
copy as Markdown and pass its path.

| File | Role |
| --- | --- |
| `prep.py` | Turns the exported Markdown into book structure: parts, chapters, appendices, figures |
| `template.tex`, `header.tex` | Pandoc template and styling: fonts, headings, running heads, code boxes, tables |
| `titlepages.tex` | Title page and copyright page |
| `codeblocks.lua` | Pandoc filter: code blocks in shaded, breakable boxes |
| `tablewidths.lua` | Pandoc filter: sizes table columns by their content |
| `figures/*.tex` | TikZ figures: the agent loop, the core loop and the security gates |
| `covers.tex` | Front and back covers |
| `assemble.py` | Joins covers and interior, adds blank inside covers and keeps bookmarks |

Requirements: pandoc 3, XeLaTeX (TeX Live with fontspec, titlesec,
tcolorbox, fvextra, tocloft and TikZ), the fonts TeX Gyre Pagella, Inter and
DejaVu Sans Mono, and Python with `pypdf`.
