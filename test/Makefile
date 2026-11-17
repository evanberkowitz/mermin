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
	@for i in 1 2; do $(ENGINE) -interaction=nonstopmode -halt-on-error rerun-edit >/dev/null || { echo "rerun: LaTeX error"; exit 1; }; done
	@sed -i.bak 's/old phrase/new phrase/' rerun-edit.tex && rm -f rerun-edit.tex.bak
	@$(ENGINE) -interaction=nonstopmode -halt-on-error rerun-edit >/dev/null || { echo "rerun: LaTeX error after the edit"; exit 1; }
	@grep -q 'Label(s) may have changed' rerun-edit.log || { echo "rerun: no rerun request after a phrase changed"; exit 1; }
	@$(ENGINE) -interaction=nonstopmode -halt-on-error rerun-edit >/dev/null || { echo "rerun: LaTeX error"; exit 1; }
	@pdftotext rerun-edit.pdf - | grep -q 'new phrase (1)' || { echo "rerun: the new phrase was not printed"; exit 1; }
	@# Removing a typeset phrase must also make LaTeX ask for another run.
	@sed -i.bak 's/\\aka\[new phrase\]{K}/\\label{K}/' rerun-edit.tex && rm -f rerun-edit.tex.bak
	@$(ENGINE) -interaction=nonstopmode -halt-on-error rerun-edit >/dev/null || { echo "rerun: LaTeX error after removing the phrase"; exit 1; }
	@grep -q 'Label(s) may have changed' rerun-edit.log || { echo "rerun: no rerun request after a phrase was removed"; exit 1; }
	@$(ENGINE) -interaction=nonstopmode -halt-on-error rerun-edit >/dev/null || { echo "rerun: LaTeX error"; exit 1; }
	@pdftotext rerun-edit.pdf - | grep -q 'K (1)' || { echo "rerun: the removed phrase was still printed"; exit 1; }
	@printf '%s\n' 'rerun checks pass'
	@# xr and xr-hyper import phrases and equation keys from another document.
	@for i in 1 2; do $(ENGINE) -interaction=nonstopmode -halt-on-error xr-supp >/dev/null || { echo "xr-supp: LaTeX error"; exit 1; }; done
	@for c in xr-before xr-after; do \
	  for i in 1 2; do $(ENGINE) -interaction=nonstopmode -halt-on-error $$c >/dev/null || { echo "$$c: LaTeX error"; exit 1; }; done; \
	  python3 -c "import subprocess,sys,unicodedata; t=unicodedata.normalize('NFC',' '.join(subprocess.run(['pdftotext','$$c.pdf','-'],capture_output=True,text=True).stdout.split())); sys.exit(0 if 'XR: the Γ act (1) holds and plain (2).' in t and 'XRQ: the sum rule (3).' in t else 1)" || { echo "$$c: phrase not imported"; exit 1; }; \
	  ! grep -q 'mermin Warning\|undefined' $$c.log || { echo "$$c: warnings"; exit 1; }; \
	done
	@printf '%s\n' 'xr checks pass'
	@# breqn's displays are equations: no warnings, right numbers.
	@for i in 1 2; do $(ENGINE) -interaction=nonstopmode -halt-on-error breqn >/dev/null || { echo "breqn: LaTeX error"; exit 1; }; done
	@! grep -q 'mermin Warning\|undefined\|multiply' breqn.log || { echo "breqn: warnings"; exit 1; }
	@pdftotext breqn.pdf - | tr '\n' ' ' | grep -q 'BREQN: A (1) A two (1) D (2) G (3a) G two (3a)\.' || { echo "breqn: wrong citations"; exit 1; }
	@printf '%s\n' 'breqn checks pass'
	@# A key that is not text, cited before its phrase is known, must not
	@# stop the first run.
	@rm -f firstrun.aux
	@for i in 1 2; do $(ENGINE) -interaction=nonstopmode -halt-on-error firstrun >/dev/null || { echo "firstrun: LaTeX error on run $$i"; exit 1; }; done
	@pdftotext firstrun.pdf - | tr '\n' ' ' | grep -qF 'See the E field (1).' || { echo "firstrun: wrong citation"; exit 1; }
	@pdftotext firstrun.pdf - | tr '\n' ' ' | grep -qF 'The H_0 (2) holds.' || { echo "firstrun: unprintable key not printed verbatim"; exit 1; }
	@grep -q "mermin Warning: .H_0' has no typeset phrase" firstrun.log || { echo "firstrun: no warning for an unprintable key"; exit 1; }
	@# A paper that adopts mermin has an .aux without equation marks: no
	@# warnings until mermin has written one.
	@printf '%s\n' '\relax' '\newlabel{anomaly}{{1}{1}}' '\newlabel{fig:x}{{1}{1}}' > adopt.aux
	@$(ENGINE) -interaction=nonstopmode -halt-on-error adopt >/dev/null || { echo "adopt: LaTeX error"; exit 1; }
	@! grep -q 'mermin Warning' adopt.log || { echo "adopt: warnings from an .aux mermin did not write"; exit 1; }
	@# beamer: \aka<overlay> in a display drops the overlay.
	@for i in 1 2; do $(ENGINE) -interaction=nonstopmode -halt-on-error beamer >/dev/null || { echo "beamer: LaTeX error"; exit 1; }; done
	@pdftotext beamer.pdf - | grep -qF 'BEAMER: first phrase (1); two (2).' || { echo "beamer: wrong citations"; exit 1; }
	@printf '%s\n' 'first-run checks pass'
	@# Moving arguments, bookmarks, keys with & and macros, \eq in math, and
	@# equations of cases, IEEEtrantools, and eqnarray.
	@for c in edge-plain edge-cleveref; do \
	  rm -f $$c.aux; \
	  for i in 1 2 3; do $(ENGINE) -interaction=nonstopmode -halt-on-error $$c >/dev/null || { echo "$$c: LaTeX error"; exit 1; }; done; \
	  ! grep -q 'mermin Warning\|undefined\|multiply\|may have changed\|Token not allowed' $$c.log || { echo "$$c: warnings"; exit 1; }; \
	  ! grep -q 'aka' $$c.toc $$c.lof || { echo "$$c: \\aka written to the contents"; exit 1; }; \
	  pdftotext $$c.pdf - | tr '\n' ' ' | grep -qF 'EDGE: Maxwell & Faraday (2); mass phrase (3); sec2:energy (3); numcases line (4); IEEE line (6); eqnarray line (7); 1; 1.' || { echo "$$c: wrong citations"; exit 1; }; \
	  pdftotext $$c.pdf - | grep -qF 'MIXED: mixed phrase (9).' || { echo "$$c: a key given twice on one line"; exit 1; }; \
	  pdftotext $$c.pdf - | grep -qF 'ORDER: order phrase (10).' || { echo "$$c: \\aka before \\label of the same key"; exit 1; }; \
	  pdftotext $$c.pdf - | grep -qF 'cf. anomaly condition (1) and' || { echo "$$c: \\eq in math mode"; exit 1; }; \
	done
	@sed 's/\\000//g' edge-cleveref.out | grep -qF 'On\040the\040anomaly\040condition\040\0501\051' || { echo "edge-cleveref: bookmark lacks the phrase and number"; exit 1; }
	@printf '%s\n' 'edge-case checks pass'
	@# A document that drops mermin must still read an excluded file's .aux.
	@rm -f inc-ch1.aux inc-ch2.aux
	@$(ENGINE) -interaction=nonstopmode -halt-on-error inc-with >/dev/null || { echo "inc-with: LaTeX error"; exit 1; }
	@$(ENGINE) -interaction=nonstopmode -halt-on-error inc-without >/dev/null || { echo "inc-without: cannot read inc-ch1.aux without mermin"; exit 1; }
	@printf '%s\n' 'include checks pass'
	@# unicode-math (LuaLaTeX and XeLaTeX only): a Greek phrase must settle.
	@if [ "$(ENGINE)" != pdflatex ]; then \
	  rm -f unicode-math.aux; \
	  for i in 1 2 3; do $(ENGINE) -interaction=nonstopmode -halt-on-error unicode-math >/dev/null || { echo "unicode-math: LaTeX error"; exit 1; }; done; \
	  ! grep -q 'may have changed' unicode-math.log || { echo "unicode-math: rerun requested forever"; exit 1; }; \
	  printf '%s\n' 'unicode-math checks pass'; \
	fi

clean:
	rm -f $(foreach c,$(CONFIGS) $(EQ_CONFIGS) $(WARN_CONFIGS) showonlyrefs rerun-edit xr-supp xr-before xr-after breqn firstrun adopt beamer edge-plain edge-cleveref inc-with inc-without unicode-math,$c.aux $c.log $c.out $c.pdf $c.toc $c.lof $c.nav $c.snm) inc-ch1.aux inc-ch2.aux rerun-edit.tex
