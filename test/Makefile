# make -C test : build every configuration twice and check the results.
CONFIGS    = test-plain test-hyperref test-cleveref test-mermin-first
EQ_CONFIGS = eq-plain eq-cleveref
WARN_CONFIGS = warn-plain warn-cleveref
export TEXINPUTS := ..:

check:
	@for c in $(CONFIGS) $(EQ_CONFIGS) $(WARN_CONFIGS); do \
	  pdflatex -interaction=nonstopmode -halt-on-error $$c >/dev/null && \
	  pdflatex -interaction=nonstopmode -halt-on-error $$c >/dev/null || { echo "$$c: LaTeX error, see $$c.log"; exit 1; }; \
	  ! grep -q 'multiply defined\|undefined' $$c.log || { echo "$$c: label warnings"; exit 1; }; \
	done
	@python3 check.py $(addsuffix .aux,$(CONFIGS)) | grep -v ' ok$$' ; \
	python3 check.py $(addsuffix .aux,$(CONFIGS)) >/dev/null && printf "%s\n" "\\alsolabel checks pass"
	@python3 check_eq.py $(addsuffix .pdf,$(EQ_CONFIGS))
	@python3 check_warn.py $(addsuffix .log,$(WARN_CONFIGS))

clean:
	rm -f $(foreach c,$(CONFIGS) $(EQ_CONFIGS) $(WARN_CONFIGS),$c.aux $c.log $c.out $c.pdf)
