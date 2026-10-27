PYTHON ?= python3
all: main.pdf
figures:
	$(PYTHON) figures/make_all.py
main.pdf: main.tex references.bib $(wildcard sections/*.tex)
	$(PYTHON) figures/make_all.py
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
clean:
	latexmk -C
	rm -f figures/generated/*.pdf figures/generated/*.png
.PHONY: all figures clean
