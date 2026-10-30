# Build the book PDF: A4, 11 pt, with front and back covers.
#
#   make MANUSCRIPT=/path/to/manuscript.md
#
# The manuscript itself is not in this repository. Export it from the book's
# working copy as Markdown. Requires pandoc, XeLaTeX (TeX Live with
# fontspec, titlesec, tcolorbox, fvextra, tocloft, tikz), the fonts TeX Gyre
# Pagella, Inter and DejaVu Sans Mono, and Python with pypdf.

MANUSCRIPT ?= manuscript.md
BUILD      := build
OUT        := $(BUILD)/AI-Assisted-Coding-with-Claude.pdf
TEX        := TEXINPUTS=..:../figures: xelatex -interaction=nonstopmode -halt-on-error

all: $(OUT)

$(BUILD)/body.md: $(MANUSCRIPT) prep.py
	mkdir -p $(BUILD)
	python3 prep.py $(MANUSCRIPT) $@

$(BUILD)/book.tex: $(BUILD)/body.md template.tex codeblocks.lua tablewidths.lua
	pandoc $< -f markdown+task_lists-auto_identifiers --template=template.tex \
	  --lua-filter=codeblocks.lua --lua-filter=tablewidths.lua --top-level-division=part -o $@

$(BUILD)/book.pdf: $(BUILD)/book.tex header.tex titlepages.tex $(wildcard figures/*.tex)
	cp -r figures $(BUILD)/
	cd $(BUILD) && $(TEX) book.tex >/dev/null && $(TEX) book.tex >/dev/null

$(BUILD)/covers.pdf: covers.tex
	mkdir -p $(BUILD)
	cd $(BUILD) && $(TEX) ../covers.tex >/dev/null && $(TEX) ../covers.tex >/dev/null

$(OUT): $(BUILD)/covers.pdf $(BUILD)/book.pdf assemble.py
	python3 assemble.py $(BUILD)/covers.pdf $(BUILD)/book.pdf $@

clean:
	rm -rf $(BUILD)

.PHONY: all clean
