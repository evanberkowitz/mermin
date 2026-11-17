# make        generate mermin.sty and typeset the manual mermin.pdf
# make test   check \alsolabel in every supported configuration
# make clean  remove generated and auxiliary files

all: mermin.sty mermin.pdf

mermin.sty: mermin.ins mermin.dtx
	tex -interaction=nonstopmode mermin.ins >/dev/null

mermin.pdf: mermin.dtx mermin.sty
	pdflatex -interaction=nonstopmode -halt-on-error mermin.dtx >/dev/null
	makeindex -q -s gind.ist mermin.idx
	makeindex -q -s gglo.ist -o mermin.gls mermin.glo
	pdflatex -interaction=nonstopmode -halt-on-error mermin.dtx >/dev/null
	pdflatex -interaction=nonstopmode -halt-on-error mermin.dtx >/dev/null

test: mermin.sty
	$(MAKE) -C test

clean:
	rm -f mermin.sty mermin.pdf mermin.aux mermin.log mermin.out mermin.toc \
	      mermin.idx mermin.ind mermin.ilg mermin.glo mermin.gls mermin.hd
	$(MAKE) -C test clean

.PHONY: all test clean
