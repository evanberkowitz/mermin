# make -C test : build every configuration twice and check the .aux files.
CONFIGS = plain hyperref cleveref mermin-first
export TEXINPUTS := ..:
check:
	@for c in $(CONFIGS); do \
	  pdflatex -interaction=nonstopmode -halt-on-error test-$$c >/dev/null && \
	  pdflatex -interaction=nonstopmode -halt-on-error test-$$c >/dev/null || { echo "$$c: LaTeX error, see test-$$c.log"; exit 1; }; \
	  ! grep -q 'multiply defined\|undefined' test-$$c.log || { echo "$$c: label warnings"; exit 1; }; \
	done
	@python3 check.py $(addsuffix .aux,$(addprefix test-,$(CONFIGS))) | grep -v ' ok$$' ; \
	python3 check.py $(addsuffix .aux,$(addprefix test-,$(CONFIGS))) >/dev/null && echo "all configurations pass"
clean:
	rm -f test-*.aux test-*.log test-*.out test-*.pdf
