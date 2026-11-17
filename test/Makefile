# make -C test [ENGINE=pdflatex|lualatex|xelatex] : build every configuration
# twice with ENGINE and check the results.
ENGINE     ?= pdflatex
CONFIGS    = test-plain test-hyperref test-cleveref test-mermin-first
EQ_CONFIGS = eq-plain eq-cleveref eq-nccmath
WARN_CONFIGS = warn-plain warn-cleveref
export TEXINPUTS := ..:

check:
	@for c in $(CONFIGS) $(EQ_CONFIGS) $(WARN_CONFIGS); do \
	  $(ENGINE) -interaction=nonstopmode -halt-on-error $$c >/dev/null && \
	  $(ENGINE) -interaction=nonstopmode -halt-on-error $$c >/dev/null || { echo "$$c: LaTeX error, see $$c.log"; exit 1; }; \
	  ! grep -q 'multiply defined\|undefined' $$c.log || { echo "$$c: label warnings"; exit 1; }; \
	done
	@python3 check.py $(addsuffix .aux,$(CONFIGS)) | grep -v ' ok$$' ; \
	python3 check.py $(addsuffix .aux,$(CONFIGS)) >/dev/null && printf "%s\n" "\\alsolabel checks pass"
	@python3 check_eq.py $(addsuffix .pdf,$(EQ_CONFIGS))
	@# nccmath defines \eq and eq-nccmath defines \aka: mermin must leave both
	@# alone and say so, and only there.
	@for n in eq aka; do \
	  grep -qF "\\$$n was already defined" eq-nccmath.log || { printf '%s\n' "eq-nccmath: no \\$$n-taken warning"; exit 1; }; \
	  ! grep -lF "\\$$n was already defined" $(filter-out eq-nccmath.log,$(addsuffix .log,$(CONFIGS) $(EQ_CONFIGS) $(WARN_CONFIGS))) || { printf '%s\n' "spurious \\$$n-taken warning"; exit 1; }; \
	done
	@printf '%s\n' '\eqcite and \alsolabel fallback checks pass'
	@python3 check_warn.py $(addsuffix .log,$(WARN_CONFIGS))
	@# mathtools' showonlyrefs needs a third run to settle.
	@for i in 1 2 3; do $(ENGINE) -interaction=nonstopmode -halt-on-error showonlyrefs >/dev/null || { echo "showonlyrefs: LaTeX error"; exit 1; }; done
	@pdftotext showonlyrefs.pdf - | tr '\n' ' ' | grep -q 'See (1), (2), (3)\.' || { echo "showonlyrefs: aliases did not number their lines"; exit 1; }
	@! pdftotext showonlyrefs.pdf - | grep -q '(4)' || { echo "showonlyrefs: an uncited line was numbered"; exit 1; }
	@printf '%s\n' 'showonlyrefs checks pass'

clean:
	rm -f $(foreach c,$(CONFIGS) $(EQ_CONFIGS) $(WARN_CONFIGS) showonlyrefs,$c.aux $c.log $c.out $c.pdf $c.toc)
