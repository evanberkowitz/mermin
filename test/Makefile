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
	@# A changed typeset phrase must make LaTeX ask for another run.
	@cp rerun.tex rerun-edit.tex
	@$(ENGINE) -interaction=nonstopmode -halt-on-error rerun-edit >/dev/null; $(ENGINE) -interaction=nonstopmode -halt-on-error rerun-edit >/dev/null
	@sed -i.bak 's/old phrase/new phrase/' rerun-edit.tex && rm -f rerun-edit.tex.bak
	@$(ENGINE) -interaction=nonstopmode -halt-on-error rerun-edit >/dev/null
	@grep -q 'Label(s) may have changed' rerun-edit.log || { echo "rerun: no rerun request after a phrase changed"; exit 1; }
	@$(ENGINE) -interaction=nonstopmode -halt-on-error rerun-edit >/dev/null
	@pdftotext rerun-edit.pdf - | grep -q 'new phrase (1)' || { echo "rerun: the new phrase was not printed"; exit 1; }
	@printf '%s\n' 'rerun checks pass'
	@# xr and xr-hyper import phrases and equation keys from another document.
	@for i in 1 2; do $(ENGINE) -interaction=nonstopmode -halt-on-error xr-supp >/dev/null; done
	@for c in xr-before xr-after; do \
	  for i in 1 2; do $(ENGINE) -interaction=nonstopmode -halt-on-error $$c >/dev/null || { echo "$$c: LaTeX error"; exit 1; }; done; \
	  python3 -c "import subprocess,sys,unicodedata; t=unicodedata.normalize('NFC',' '.join(subprocess.run(['pdftotext','$$c.pdf','-'],capture_output=True,text=True).stdout.split())); sys.exit(0 if 'XR: the Γ act (1) holds' in t else 1)" || { echo "$$c: phrase not imported"; exit 1; }; \
	  ! grep -q 'mermin Warning\|undefined' $$c.log || { echo "$$c: warnings"; exit 1; }; \
	done
	@printf '%s\n' 'xr checks pass'
	@# breqn's displays are equations: no warnings, right numbers.
	@for i in 1 2; do $(ENGINE) -interaction=nonstopmode -halt-on-error breqn >/dev/null || { echo "breqn: LaTeX error"; exit 1; }; done
	@! grep -q 'mermin Warning\|undefined\|multiply' breqn.log || { echo "breqn: warnings"; exit 1; }
	@pdftotext breqn.pdf - | tr '\n' ' ' | grep -q 'BREQN: A (1) A two (1) D (2) G (3a) G two (3a)\.' || { echo "breqn: wrong citations"; exit 1; }
	@printf '%s\n' 'breqn checks pass'

clean:
	rm -f $(foreach c,$(CONFIGS) $(EQ_CONFIGS) $(WARN_CONFIGS) showonlyrefs rerun-edit xr-supp xr-before xr-after breqn,$c.aux $c.log $c.out $c.pdf $c.toc) rerun-edit.tex
